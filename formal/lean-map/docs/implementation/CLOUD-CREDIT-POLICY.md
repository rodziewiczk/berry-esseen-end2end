# Credit-only Google Cloud activation gate

Read-only research checkpoint, 25 October 2026. No account identifiers,
payment details, resource activation or billing/API changes are included.
This note does not assert that the configured account is currently a trial.

Read-only UI follow-up: opening Billing in the in-app browser redirected to
Google's account chooser. No account was selected and no login/2FA was
automated. Billing Overview and Credits were therefore not visible. The
actual account mode, balance, expiry and eligible scope remain unverified;
the browser tab was left for the user to authenticate manually.

## Current authorization

The user's latest instruction replaces the earlier 75 + 550 PLN model:

* Maximum authorized consumption of existing promotional credits: **1000 PLN**
  (100000 grosz), including setup, compute, retries, ancillary services,
  cleanup and funded retention.
* Authorized cash/card expenditure: **0 PLN**. The reported roughly 1100 PLN
  balance and roughly 100 PLN reserve are not independently verified balances
  or an additional spending allowance.
* No upgrade to paid billing, purchase, payment-method change or cloud resource
  creation is authorized by this research task.

The previous cloud example policy is historical planning, not an authorization
to deploy. The implemented local pilot does not activate Google Cloud.

## The decisive distinction

Google's signup FAQ says a non-upgraded Free Trial does not automatically
become paid when its credit/time ends. Manually upgrading changes that rule:
remaining Welcome credit can still be used, but usage beyond it and free-tier
allowances can be billed. Thus **having promotional credit does not prove
that an account cannot charge its payment method**. [Official signup FAQ](https://cloud.google.com/signup-faqs).

The documented way to distinguish modes is Cloud Billing **Overview**, which
labels the account `Free trial account` or `Paid account`. The Welcome trial
is normally 300 USD for 90 days; its unused credit keeps the original expiry
after upgrade. Other promotions require their own grant terms. Nonbillable
trial restrictions include no GPU VMs, quota increases, Marketplace or
Windows Server VM images. Do not upgrade merely to bypass a restriction.
[Free program and account-mode check](https://docs.cloud.google.com/free/docs/free-cloud-features).

Existing sanitized preflight only established `billing_enabled=true` and
quotas. Neither establishes trial status, current credit balance or credit
eligibility. The documented BillingAccount v1 resource exposes account
open/currency/identity information, not a trial-status or remaining-credit
field. Do not invent such a field in a `gcloud` check.
[BillingAccount API](https://docs.cloud.google.com/billing/docs/reference/rest/v1/billingAccounts).

**Activation decision:** for a verified, non-upgraded, nonbillable Free Trial,
Google's documented no-billing rule supplies the relevant provider-side
protection, subject to that program's coverage and restrictions. For a Paid
account with promotional credit, a trial-like zero-cash guarantee is not
established. With the account type still unknown, cloud activation remains
blocked. A software estimate/watchdog cannot replace this missing protection.

## Read-only evidence required before any cloud activation

1. In the correct linked billing account, inspect Overview and record its
   mode, observation time and billing currency privately. Confirm no upgrade
   is being proposed or performed. A credit banner alone is insufficient.
2. Inspect Billing **Credits**. For each usable grant, record exact remaining
   amount/currency, available status, start/end dates and service/SKU scope.
   Do not confuse promotional credit with discounts or the month's total
   savings. [Official credit inventory instructions](https://docs.cloud.google.com/billing/docs/how-to/resolve-issues).
3. Resolve every intended cost line against those grant scopes: VM CPU/RAM,
   disks, network, GCS data/operations, Batch's underlying resources,
   Firestore, Cloud Run, registry/build, Scheduler and observability. Mark
   each line eligible, independently free, or unsupported. Unknown or uncovered
   lines block activation while cash authorization is zero.
4. Bound already incurred but unreported costs, other projects sharing the
   billing account, and residual disks/storage from stopped resources. The
   earlier preflight did not audit those residual charges. Do not spend the
   same balance in two independent schedulers.
5. Freeze a conservative eligible-credit allocation, current SKU/currency
   quote and absolute shutdown policy. Credit expiry must cover admitted
   lifetimes and retention; export evidence before trial closure could stop
   access or remove resources. All setup costs consume this same 1000 PLN cap.

Only redacted verification results should enter the repository. Account,
grant and payment identifiers remain private. No evidence above was obtained
from the actual Billing Overview/Credits pages during this research step.

## Why the nominal reserve and alerts are not a hard cap

Usage/payment reporting is delayed; official guidance says cost details can
take over 24 hours to appear, and charges can precede reports. Therefore a
displayed remaining balance is not a synchronous reservation API, and a
nominal 100 PLN margin cannot prove the absence of outstanding liabilities.
[Billing/reporting latency](https://docs.cloud.google.com/billing/docs/how-to/view-history).

Current service spend caps are not a general Compute Engine/Batch guard.
Their documented eligible list covers selected API services, uses gross
estimated costs rather than promotional-credit depletion, and warns of
enforcement delay and billable overages. Alerts-only budgets are also not
an enforceable credit wallet. [Spend-cap scope and limitations](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps),
[budget credit filtering](https://docs.cloud.google.com/billing/docs/reference/budget/rest/v1/billingAccounts.budgets).

An operational admission check must conservatively reserve all eligible cost
liabilities before submission, retain unknown create/cancel liabilities, and
stop admission well before the credit/time boundary. It may spend at most
the lesser of 1000 PLN and the conservatively available eligible allocation
after other liabilities and the required reserve. It must not automatically
increase this limit, transfer a previous budget, upgrade billing or fall back
to a paid service when credits are insufficient.

These controls reduce credit consumption risk; on a Paid account they do not
prove a zero invoice under delayed charges, exclusions or provider-control
outages. Removing/limiting a card is not evidence that usage cannot create a
payable liability. If provider-side nonbillable status or equivalent verified
protection cannot be established, continue locally and keep cloud activation
disabled under the user's 0 PLN cash instruction.
