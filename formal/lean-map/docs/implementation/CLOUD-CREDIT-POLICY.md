# Credit-only Google Cloud activation gate

Read-only research checkpoint, 25 October 2026. No account identifiers,
payment details, resource activation or billing/API changes are included.
This note does not assert that the configured account is currently a trial.

Funding update: on 25 October 2026 the user explicitly attested that about
1000 PLN of promotional credit remains, valid until January 2027, and
authorized autonomous CLI configuration and ordinary compute activation
within those credits. This attestation is the funding source; it is not a
claim that a CLI or browser read independently established the balance.
Further login/screenshots are not a prerequisite. Account mode and exact
grant/SKU terms have not been independently read from Billing Overview.

## Current authorization

The user's latest instruction replaces the earlier 75 + 550 PLN model:

* Maximum authorized consumption of existing promotional credits: **1000 PLN**
  (100000 grosz), including setup, compute, retries, ancillary services,
  cleanup and funded retention.
* Authorized cash/card expenditure: **0 PLN**. The latest declared balance is
  approximately 1000 PLN, not the earlier rough 1100 PLN estimate.
* The overnight allocation is **300 PLN planned**, with a separate conservative
  **350 PLN ceiling including setup, run, retries, cleanup and funded retention**.
  Reserve outstanding charges and enforce this smaller allocation before
  dispatch; the remaining declared credit is a substantial safety margin, not
  an instruction to spend it automatically.
* Ordinary qualified VM CPU/RAM, disks and networking already used by this
  project may be configured/activated through the CLI after runtime and stop
  readiness. No billing upgrade, new payment commitment or cash fallback is
  authorized. The current supervisor development itself activates no cloud VM.

The previous 75/550 PLN cloud example policy is historical planning and must
not silently replace this credit-only allocation. The implemented local pilot
does not activate Google Cloud.

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

**Activation decision:** a verified, non-upgraded, nonbillable Free Trial has
Google's documented no-billing protection, subject to its coverage and
restrictions. A Paid account can still use eligible promotional credits, but
does not inherit that trial protection. The user's credit-only authorization
therefore uses the user's explicit funding attestation, ordinary already used
eligible service classes, a conservative allocation covering outstanding and
maximum admitted liabilities, and an independent shutdown mechanism. It does
not authorize cash fallback. Unknown credit scope for a new service blocks
that service, not all previously authorized ordinary compute. An absolute
invoice guarantee during a provider outage is not an implementable preflight
test. Runtime/source qualification and tested shutdown remain concrete gates.

## Funding provenance and practical activation checks

1. Record the 25 October user attestation and approximate January 2027 expiry.
   Use real CLI usage/cost fields where available, without inventing a remaining
   credit API field or repeatedly requiring UI authentication. No upgrade is
   proposed or performed. Billing mode remains independently unknown.
2. If accessible, read Billing **Credits** to refine remaining amount/currency,
   status, expiry and service/SKU scope. This is useful additional evidence,
   not a new login requirement overriding the user's attestation. Never confuse
   promotional credit with discounts or the month's total savings.
   [Official credit inventory instructions](https://docs.cloud.google.com/billing/docs/how-to/resolve-issues).
3. Resolve every intended cost line against those grant scopes: VM CPU/RAM,
   disks, network, GCS data/operations, Batch's underlying resources,
   Firestore, Cloud Run, registry/build, Scheduler and observability. Mark
   each line covered by the declared ordinary-service allocation, independently
   free, or unsupported. A new unknown/uncovered service is not admitted.
   The initial bounded pilot need not activate every service in this list.
4. Bound already incurred but unreported costs, other projects sharing the
   billing account, and residual disks/storage from stopped resources. The
   earlier preflight did not audit those residual charges. Do not spend the
   same balance in two independent schedulers.
5. Freeze the conservative 350 PLN overnight allocation, current SKU/currency
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
after other liabilities and the required reserve, and at most the separately
admitted 350 PLN overnight ceiling. It must not automatically
increase this limit, transfer a previous budget, upgrade billing or fall back
to a paid service when credits are insufficient.

These controls reduce credit consumption risk; on a Paid account they do not
prove a zero invoice under delayed charges, exclusions or provider-control
outages. Removing/limiting a card is not evidence that usage cannot create a
payable liability. Do not replace the concrete credit and liability checks with
an impossible demand for a provider-outage guarantee. Fail closed when the
declared eligible allocation cannot cover conservative liabilities plus the
reserved margin, when a line is uncovered, or when the declared funding expires
before the admitted liability horizon. Do not treat missing independent UI
balance verification as rejection of the user's funding attestation. Continue
locally for unsupported work. The authorized cash amount remains
0 PLN even if an operational estimate later proves inaccurate.
