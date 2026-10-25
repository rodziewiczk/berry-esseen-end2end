param(
    [string]$MathlibWorkspace = $env:BEMAP_MATHLIB_WORKSPACE,
    [string]$LeanExe = $env:BEMAP_LEAN_EXE,
    [ValidateSet('All', 'Core')][string]$Scope = 'All',
    [switch]$ReuseVerified
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
# Inspect Git metadata read-only: the dependency cache need not be writable.
$taskMathlibGit = Join-Path $taskMathlib '.git'
if (-not (Test-Path -LiteralPath $taskMathlibGit -PathType Container)) {
    $taskGitPointer = (Get-Content -LiteralPath $taskMathlibGit -Raw).Trim()
    if ($taskGitPointer -notmatch '^gitdir:\s*(.+)$') { throw 'Invalid mathlib Git metadata' }
    $taskMathlibGit = [System.IO.Path]::GetFullPath((Join-Path $taskMathlib $Matches[1]))
}
$taskMathlibRev = (Get-Content -LiteralPath (Join-Path $taskMathlibGit 'HEAD') -Raw).Trim()
if ($taskMathlibRev -match '^ref:\s*(.+)$') {
    $taskMathlibRef = $Matches[1]
    $taskLooseRef = Join-Path $taskMathlibGit $taskMathlibRef
    if (Test-Path -LiteralPath $taskLooseRef) {
        $taskMathlibRev = (Get-Content -LiteralPath $taskLooseRef -Raw).Trim()
    } else {
        $taskPacked = @(Get-Content -LiteralPath (Join-Path $taskMathlibGit 'packed-refs') |
            Where-Object { $_ -match ('^[0-9a-f]{40} ' + [regex]::Escape($taskMathlibRef) + '$') })
        if ($taskPacked.Count -ne 1) { throw 'Cannot resolve mathlib HEAD' }
        $taskMathlibRev = $taskPacked[0].Substring(0, 40)
    }
}
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
$taskCoreModules = @('BEMap/Finite', 'BEMap/Cover25', 'BEMap/Tail')
$taskSourceFiles = @((Get-ChildItem -LiteralPath (Join-Path $taskRoot 'BEMap') -Recurse -File -Filter '*.lean')) +
    @((Get-ChildItem -LiteralPath $taskRoot -File -Filter '*.lean'))
$taskSources = @{}
$taskImports = @{}
foreach ($taskFile in $taskSourceFiles) {
    $taskModuleName = $taskFile.FullName.Substring($taskRoot.Length + 1).Replace('\', '/') -replace '\.lean$', ''
    $taskSources[$taskModuleName] = $taskFile.FullName
}
foreach ($taskName in $taskSources.Keys) {
    $taskText = Get-Content -LiteralPath $taskSources[$taskName] -Raw
    $taskImports[$taskName] = @([regex]::Matches($taskText, '(?m)^\s*import\s+([A-Za-z0-9_.]+)') |
        ForEach-Object { $_.Groups[1].Value.Replace('.', '/') } |
        Where-Object { $taskSources.ContainsKey($_) })
}
$taskVisitState = @{}
$taskOrdered = [System.Collections.Generic.List[string]]::new()
function Visit-BEMapModule([string]$taskName) {
    if ($taskVisitState[$taskName] -eq 2) { return }
    if ($taskVisitState[$taskName] -eq 1) { throw "Cyclic project imports at $taskName" }
    if (-not $taskSources.ContainsKey($taskName)) { throw "Project source missing: $taskName" }
    $taskVisitState[$taskName] = 1
    foreach ($taskDependency in $taskImports[$taskName]) { Visit-BEMapModule $taskDependency }
    $taskVisitState[$taskName] = 2
    $taskOrdered.Add($taskName)
}
foreach ($taskName in $taskCoreModules) { Visit-BEMapModule $taskName }
if ($Scope -eq 'All') {
    foreach ($taskName in ($taskSources.Keys | Sort-Object)) { Visit-BEMapModule $taskName }
}
$taskModules = $taskOrdered.ToArray()
$taskCachePath = Join-Path $taskRoot '.lake\verified-check.json'
$taskCached = @{}
if ($ReuseVerified) {
    if (-not (Test-Path -LiteralPath $taskCachePath)) {
        throw 'No verified project cache. Run once without -ReuseVerified.'
    }
    $taskCache = Get-Content -LiteralPath $taskCachePath -Raw | ConvertFrom-Json
    if (-not $taskCache.passed -or $taskCache.lean -ne $taskVersion -or
        $taskCache.mathlib_revision -ne $taskMathlibRev -or
        $taskCache.compiler_options -ne 'autoImplicit=false;relaxedAutoImplicit=false') {
        throw 'Verified cache configuration mismatch. Run without -ReuseVerified.'
    }
    foreach ($taskRow in $taskCache.modules) { $taskCached[$taskRow.module] = $taskRow }
}
$taskRebuilt = @{}
$taskInitialHashes = @{}
foreach ($taskName in $taskModules) {
    $taskInitialHashes[$taskName] = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskSources[$taskName]).Hash.ToLowerInvariant()
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
        New-Item -ItemType Directory -Force (Split-Path $taskOutput -Parent) | Out-Null
        $taskPrior = $taskCached[$taskModule]
        $taskCanReuse = $ReuseVerified -and $null -ne $taskPrior -and
            $taskPrior.source_sha256 -eq $taskInitialHashes[$taskModule] -and
            (Test-Path -LiteralPath $taskOutput)
        if ($taskCanReuse) {
            $taskCanReuse = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskOutput).Hash.ToLowerInvariant() -eq
                $taskPrior.artifact_sha256
            foreach ($taskDependency in $taskImports[$taskModule]) {
                if ($taskRebuilt[$taskDependency]) { $taskCanReuse = $false }
            }
        }
        if ($taskCanReuse) {
            $taskRows += [ordered]@{
                module = $taskModule
                seconds = 0
                exit_code = 0
                source_sha256 = $taskPrior.source_sha256
                artifact_sha256 = $taskPrior.artifact_sha256
                reused_artifact = $true
                verified_at = $taskPrior.verified_at
                last_compile_seconds = $taskPrior.last_compile_seconds
                compiler_output = @($taskPrior.compiler_output)
            }
            $taskRebuilt[$taskModule] = $false
            $taskAllLog += @("--- $taskModule ---", "Verified unchanged source, compiled artifact and project dependencies; compiler check at $($taskPrior.verified_at).")
            $taskAllLog += @($taskPrior.compiler_output | ForEach-Object { "$_" })
            Write-Output "$taskModule : verified unchanged compiler artifact"
            continue
        }
        $taskWatch = [System.Diagnostics.Stopwatch]::StartNew()
        $taskLog = @(& $LeanExe -DautoImplicit=false -DrelaxedAutoImplicit=false -o $taskOutput $taskSource 2>&1)
        $taskExit = $LASTEXITCODE
        $taskWatch.Stop()
        $taskRows += [ordered]@{
            module = $taskModule
            seconds = [math]::Round($taskWatch.Elapsed.TotalSeconds, 3)
            exit_code = $taskExit
            source_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskSource).Hash.ToLowerInvariant()
            artifact_sha256 = if ($taskExit -eq 0) { (Get-FileHash -Algorithm SHA256 -LiteralPath $taskOutput).Hash.ToLowerInvariant() } else { $null }
            reused_artifact = $false
            verified_at = (Get-Date).ToString('o')
            last_compile_seconds = [math]::Round($taskWatch.Elapsed.TotalSeconds, 3)
            compiler_output = @($taskLog | ForEach-Object { "$_" })
        }
        $taskRebuilt[$taskModule] = $true
        if ($taskRows[-1].source_sha256 -ne $taskInitialHashes[$taskModule]) {
            throw "Source changed during compilation: $taskModule"
        }
        $taskAllLog += @("--- $taskModule ---") + @($taskLog | ForEach-Object { "$_" })
        Write-Output "$taskModule : $($taskWatch.Elapsed.TotalSeconds.ToString('F2')) seconds; exit $taskExit"
        $taskLog | ForEach-Object { Write-Output "$_" }
        if ($taskExit -ne 0) { throw "Lean rejected $taskModule" }
    }
    foreach ($taskName in $taskModules) {
        $taskFinalHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskSources[$taskName]).Hash.ToLowerInvariant()
        if ($taskFinalHash -ne $taskInitialHashes[$taskName]) { throw "Source changed during full check: $taskName" }
    }
    if ($Scope -eq 'All') {
        $taskFinalSources = @((Get-ChildItem -LiteralPath (Join-Path $taskRoot 'BEMap') -Recurse -File -Filter '*.lean')) +
            @((Get-ChildItem -LiteralPath $taskRoot -File -Filter '*.lean'))
        if ($taskFinalSources.Count -ne $taskSourceFiles.Count) { throw 'Project source inventory changed during check' }
        foreach ($taskFinalSource in $taskFinalSources) {
            $taskFinalName = $taskFinalSource.FullName.Substring($taskRoot.Length + 1).Replace('\', '/') -replace '\.lean$', ''
            if (-not $taskSources.ContainsKey($taskFinalName)) { throw "New project module during check: $taskFinalName" }
        }
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
        method = if ($ReuseVerified) { 'Incremental direct Lean check; unchanged project source/artifact/dependencies verified against prior compiler record' } else { 'Direct Lean compiler; existing compiled mathlib dependencies; every selected project module recompiled' }
        compiler_options = 'autoImplicit=false;relaxedAutoImplicit=false'
        reused_modules = @($taskRows | Where-Object { $_.reused_artifact }).Count
        recompiled_modules = @($taskRows | Where-Object { -not $_.reused_artifact }).Count
        total_seconds = [math]::Round($taskTimer.Elapsed.TotalSeconds, 3)
        modules = $taskRows
        remaining_assumptions = 'Exact analytic and checker-soundness parameters: see theorem signatures and docs/contracts/README.md. No heavy numerical kernels run.'
    }
    $taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskRoot "check-$Scope.json") -Encoding utf8
    $taskAllLog | Set-Content -LiteralPath (Join-Path $taskRoot "check-$Scope.log") -Encoding utf8
    if ($taskPassed -and $Scope -eq 'All') {
        $taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskCachePath -Encoding utf8
    }
}
