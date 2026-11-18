# Audit checklist

The one-stop list this skill audits against. Every check has a stable ID, the insight(s) it came from, and how to verify it. New insights add or sharpen checks here; never renumber an existing ID.

Format rule (the summary script counts these): each check is one line starting with `- **AREA-N**`.

## Data ownership (DATA)

- **DATA-1** Every record that matters lives in a server database you own. Browser storage (localStorage, sessionStorage, IndexedDB, cookies) is only a cache or a draft. Verify: list every browser-storage key and confirm that each one is either disposable UI state or a copy of a server record. _From R004, R005._
- **DATA-2** No business logic reads a browser-only value that the server doesn't also hold. Old cache keys that nothing writes anymore are the classic trap: results then differ by device. Verify: for each storage key, find its writers; a key that's read but never written is a bug. _From R004, R005._
- **DATA-3** Automatic backups exist, and a restore has actually been done and dated. Verify: name the last restore drill and its result. _From R004, R006._

## Server-side authorization (AUTHZ)

- **AUTHZ-1** Every API route checks who is calling on the server (token, session, signed URL), on every request. Verify: list every route with its auth check; public routes are listed on purpose with what they expose. _From R004, R005._
- **AUTHZ-2** Every route checks what the caller may do: role, plus ownership of the specific record (account, customer, event). Changing an ID in the request must never reach someone else's data (IDOR). _From R004, R005._
- **AUTHZ-3** Hiding a button is not access control. Any action the UI hides must also be refused by the server. _From R004, R005._
- **AUTHZ-4** Tests call each route directly as the wrong user (no token, other customer, lower role) and expect a refusal. Verify: such a test exists per protected route and fails on code without the check. _From R004._

## Secrets (SEC)

- **SEC-1** No secret key ships in front-end code or browser bundles. Know which keys are public by design (for example Firebase web API keys, publishable payment keys) and make sure server rules protect the data behind them. _From R004, R005._
- **SEC-2** Scan the code and its full git history for keys; rotate every key that was ever exposed, even once. _From R004._
- **SEC-3** Secrets live in server environment variables or a secrets manager; third-party calls (payments, email, AI providers) go through your server. _From R004, R005._

## Agent harness (HAR)

- **HAR-1** Your standards for AI agents are written down in files you own and version: rules, project knowledge, allowed tools. They must work no matter which model is plugged in. _From R001._
- **HAR-2** What each agent may touch is explicit (permissions, protected paths, no-go actions), and enforced rather than just requested. _From R001._
- **HAR-3** Work is proven by checks (tests, builds, contract checks) before anything ships; agents report what they did not verify. _From R001._
- **HAR-4** Swapping a model or tool is a config change, not a rebuild. If a new tool forces a rebuild, the standards weren't in the harness. _From R001._

## Vendors and AI agencies (VEN)

- **VEN-1** Ask every AI vendor what they did before. Look for a track record of deploying software into companies: onboarding, training, change management, multi-year support. _From R002._
- **VEN-2** Talk to a customer who has worked with them for more than a year before signing. _From R002._
- **VEN-3** Know who patches, monitors and supports the agent in year two and during an outage, and give vendors least-privilege access with their own credentials. _From R002._

## Evidence and recoverability (EVI)

- **EVI-1** Keep a dated register of every AI system and automation: what it does, the data it touches, who built it, who owns it now, and the last independent review with its reviewer. _From R006._
- **EVI-2** Access is provable: 2FA on every account, no shared passwords, agents on their own service credentials. Export the list and flag gaps. _From R006._
- **EVI-3** Logging and retention are confirmed per system, and a one-page incident and recovery summary records the date and result of the last drill. _From R006._

## User communication and trust (COM)

- **COM-1** The product delivers its core value up front; it doesn't hide it behind engagement tricks (forced follows, "reply with a keyword", fake urgency or other dark patterns). Verify: walk the onboarding, sharing and upgrade flows and list every step that gates value on engagement. _From R003._
- **COM-2** Conversations with users stay real: AI or automated replies are labelled as automated and can hand off to a person. Verify: find every support, chat, email and DM automation and check that it's disclosed and has a handoff path. _From R003._
- **COM-3** Abuse is handled without feeding it: users can block and report, and admins can hide or remove bad-faith content quickly. Verify: find the block, report and remove paths and who can use them. _From R003._
