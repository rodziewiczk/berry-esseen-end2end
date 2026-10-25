param(
    [string]$MathlibWorkspace = $env:BEMAP_MATHLIB_WORKSPACE,
    [string]$LeanExe = $env:BEMAP_LEAN_EXE,
    [ValidateSet('All', 'Core')][string]$Scope = 'All'
)

# Verify only this project's source, using existing compiled dependency files.
# Parameters and BEMAP_* environment variables override local autodetection.
# For a portable Lake build, see README.md.
$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
if (-not $MathlibWorkspace) {
    $MathlibWorkspace = Join-Path $env:USERPROFILE 'Desktop\eventual_exactness_proof'
}
if (-not $LeanExe) {
    $taskLeanCommand = Get-Command lean -ErrorAction SilentlyContinue
    if ($taskLeanCommand) {
        $LeanExe = $taskLeanCommand.Source
    } else {
        $LeanExe = Join-Path $env:USERPROFILE '.elan\toolchains\leanprover--lean4---v4.32.0\bin\lean.exe'
    }
}
$taskPackages = Join-Path $MathlibWorkspace '.lake\packages'
if (-not (Test-Path -LiteralPath $LeanExe)) { throw "Lean executable not found: $LeanExe" }
if (-not (Test-Path -LiteralPath $taskPackages)) { throw "Dependency cache not found: $taskPackages" }
$taskVersion = (& $LeanExe --version | Out-String).Trim()
if ($taskVersion -notmatch 'Lean \(version 4\.32\.0,') { throw "Expected Lean 4.32.0; found $taskVersion" }
$taskMathlib = Join-Path $taskPackages 'mathlib'
$taskMathlibRev = (& git -C $taskMathlib rev-parse HEAD | Out-String).Trim()
if ($taskMathlibRev -ne '81a5d257c8e410db227a6665ed08f64fea08e997') {
    throw "Mathlib revision mismatch: $taskMathlibRev"
}
$taskLib = Join-Path $taskRoot '.lake\build\lib\lean'
New-Item -ItemType Directory -Force (Join-Path $taskLib 'BEMap\Foundations') | Out-Null
$taskDependencies = @(Get-ChildItem -LiteralPath $taskPackages -Directory |
    ForEach-Object { Join-Path $_.FullName '.lake\build\lib\lean' } |
    Where-Object { Test-Path -LiteralPath $_ })
$taskOldLeanPath = $env:LEAN_PATH
$env:LEAN_PATH = (@($taskLib) + $taskDependencies) -join ';'
$taskModules = @('BEMap/Finite', 'BEMap/Cover25', 'BEMap/Tail')
if ($Scope -eq 'All') {
    $taskModules += @('BEMap/Foundations/ProbabilityLaw', 'BEMap/Foundations/OptimalConstant',
        'BEMap/Interfaces', 'BEMap', 'Audit')
}
$taskRows = @()
$taskAllLog = @()
$taskTimer = [System.Diagnostics.Stopwatch]::StartNew()
$taskPassed = $false
Push-Location -LiteralPath $taskRoot
try {
    foreach ($taskModule in $taskModules) {
        $taskSource = "$taskModule.lean"
        $taskOutput = Join-Path $taskLib "$taskModule.olean"
        $taskWatch = [System.Diagnostics.Stopwatch]::StartNew()
        $taskLog = @(& $LeanExe -DautoImplicit=false -DrelaxedAutoImplicit=false -o $taskOutput $taskSource 2>&1)
        $taskExit = $LASTEXITCODE
        $taskWatch.Stop()
        $taskRows += [ordered]@{
            module = $taskModule
            seconds = [math]::Round($taskWatch.Elapsed.TotalSeconds, 3)
            exit_code = $taskExit
            source_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskSource).Hash.ToLowerInvariant()
        }
        $taskAllLog += @("--- $taskModule ---") + @($taskLog | ForEach-Object { "$_" })
        Write-Output "$taskModule : $($taskWatch.Elapsed.TotalSeconds.ToString('F2')) seconds; exit $taskExit"
        $taskLog | ForEach-Object { Write-Output "$_" }
        if ($taskExit -ne 0) { throw "Lean rejected $taskModule" }
    }
    $taskPassed = $true
} finally {
    $taskTimer.Stop()
    Pop-Location
    $env:LEAN_PATH = $taskOldLeanPath
    $taskReport = [ordered]@{
        passed = $taskPassed
        scope = $Scope
        checked_at = (Get-Date).ToString('o')
        lean = $taskVersion
        mathlib_revision = $taskMathlibRev
        method = 'Direct Lean compiler; existing compiled mathlib dependencies; project modules rechecked'
        total_seconds = [math]::Round($taskTimer.Elapsed.TotalSeconds, 3)
        modules = $taskRows
        remaining_assumptions = 'See theorem signatures and docs/mathematical-contracts.md; no numerical kernels run'
    }
    $taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskRoot "check-$Scope.json") -Encoding utf8
    $taskAllLog | Set-Content -LiteralPath (Join-Path $taskRoot "check-$Scope.log") -Encoding utf8
}
