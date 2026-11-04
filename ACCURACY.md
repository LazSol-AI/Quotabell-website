# Accuracy and asset provenance

Checked against the Quotabell app worktree on 2026-11-03. App source paths below refer to that separate repository; they are historical references and are not included in this website repository. No live provider requests, sign-ins or app launches were made. No credential files, Keychain entries or tokens were read.

## Source map

The requested starting documents were read: `CLAUDE.md`, `Docs/HANDOFF.md`, `Docs/STATUS.md`, `Docs/APP_PRIVACY_INVENTORY.md`, `Docs/APP_STORE_METADATA.md`, `Docs/THIRD_PARTY_NOTICES.md` and the phone-only research (including its superseding OAuth addendum). Current code takes precedence over older draft copy.

| Website claim | Checked sources |
| --- | --- |
| Claude, ChatGPT / Codex session/weekly windows; Grok weekly pool | `Packages/QuotabellCore/Sources/QuotabellCore/Parsing/`, `QuotaModels.swift`, `Display/QuotaFormatting.swift`; live-read shape evidence recorded in `Docs/STATUS.md` (no new live calls) |
| Small, medium, large, circular, rectangular, inline widgets | `Apps/Widgets/QuotabellWidgets.swift` supported families; `QuotabellUI/Widgets/` |
| Multiple accounts, nicknames, per-account data source, Mac config folders | `Accounts/QuotaAccount.swift`, `AccountDirectory.swift`, `Apps/iOS/Phone/PhoneAccounts.swift`, `Apps/Mac/AppModel.swift`, Mac account settings |
| Alerts at 20%/5% left, local, opt-in, reset conditions | `Display/QuotaPolicy.swift`, `Alerts/AlertPlanner.swift`, `AlertEngine.swift`, `AlertModels.swift`, `SystemAlertDelivery.swift` |
| Wake, disabled by default, CLI message, plan usage, no Grok | `Wake/WakeDisclosure.swift`, `WakeModels.swift`, `WakeCommand.swift`, `WakePlanner.swift`, `WakeStore.swift`, `Apps/Mac/WakeController.swift`, `Views/WakeView.swift` |
| Token-free Mac helper and Claude.app history fallback | `Readers/ClaudeReader.swift`, Codex/Grok readers, `ReaderSupport.swift`; fixed protocol allowlists |
| CloudKit private DB payload and cache | `Sync/SyncedQuotaState.swift`, `CloudKitQuotaStore.swift`, `SharedStateCache.swift`, `Apps/Mac/CloudSync.swift`, `Apps/iOS/PhoneModel.swift` |
| Phone Keychain, sync opt-in and sign-out | `Phone/SecretStore.swift`, `PhoneSource.swift`, `Apps/iOS/Phone/PhoneAccounts.swift` |
| Official CLI identities, host restrictions, risks and fallback | `Phone/PhoneOAuth.swift`, `PhoneDisclosure.swift`, `PhoneHTTP.swift`, `PhoneUsageReader.swift`, `PhoneLogin.swift`, `Apps/iOS/Phone/WebPagePhoneTransport.swift`; `Docs/research/phone-only-2026-11-01.md` addendum 2 |
| Local history, pruning and deletion limits | `Store/SnapshotStore.swift`, `Wake/WakeStore.swift`, `Apps/iOS/PhoneModel.swift: deleteSyncedData`, `PhoneAccounts.swift: signOut` |
| iOS/macOS minimums, planned distribution | `project.yml`, `CLAUDE.md`, `Packaging/homebrew/quotabell.rb`, `Docs/HANDOFF.md` release blockers |

## Differences from stale drafts / important limits

- The original privacy inventory table says Quotabell never holds provider tokens and the metadata says a Mac is required, there is no sign-in and there are no provider network calls. These statements predate phone-only OAuth. The website explicitly distinguishes the two modes and describes phone tokens, identity metadata and direct requests. Neither app code nor these source documents was changed.
- “Only quota numbers sync” is shorthand. The actual private CloudKit payload also contains account IDs/nicknames, order/source metadata, plan/window labels, timestamps, read status, sanitized Mac name, random Mac ID and Wake summary. The privacy page lists these; no promise of numeric-only payloads is made.
- **Wake’s three-per-day policy is three scheduled times per Mac account.** `WakeSettings` truncates configured times to `WakePolicy.maxTimesPerDay == 3`. `WakeController.wakeNow` calls `run(requireIdle: false)` separately; it does not enforce a daily run total or the scheduler’s paused-day guard. Therefore the site says “up to three scheduled times per day per Mac account” and that manual runs are additional. A strict three-run daily cap, including manual runs, is not established by the current code. Adjusting that would require app changes outside this task.
- Scheduled Wake skips active windows and stops scheduling for the day after an error. Manual Wake has separate behavior. It does not increase quota or promise a start. No unverified plan-specific guarantee is repeated from the draft disclosure.
- Alerts use the displayed integer percent left (floor rounding), rather than an exact raw floating-point 80.000%/95.000% crossing. The website gives 20%/5% left as the primary thresholds. Reset alerts are for previously warned 5-hour windows and need a new usable reading; weekly reset alerts are off. iPhone and Mac notification ledgers are independent.
- The phone’s default sign-in is OAuth as each provider’s CLI, not a Quotabell-approved public API. Website-cookie fallback remains; Grok’s fallback is a different, foreground-only chat limit. Provider-policy risks are described as the app’s disclosure, without asserting independent new legal clearance.
- Mac successful quota history is pruned at launch to 30 days. Wake’s history reader filters to 60 days but does not prune its file; privacy copy avoids promising deletion at 60 days.
- Cloud deletion does not delete the Mac’s local files or phone-only tokens. A running Mac may republish. Sign Out attempts provider revocation only where supported; Claude tokens can remain valid at the provider until expiry.
- App Store and Mac release availability is not asserted. Developer ID/notarized ZIP and Homebrew are the distribution plan; their URLs/tap are unresolved placeholders. Production CloudKit, notarization, real-device refresh/alerts and provider access remain app release concerns in the handoff.
- The website requires a real support channel, chosen domain and reviewed legal text before publication/App Store use. Host connection processing is disclosed separately from the absence of developer app-data collection. No invented company registration number, address, launch date, testimonials, ratings or user statistics are included.

## Assets

All imagery comes from this repository; no external assets or third-party website resources were fetched. Assets were copied/cropped/resized with macOS `sips`, then JPEG-encoded at quality 82 (dashboard) or 85 (widgets). No UI values were changed.

| Output in `public/assets/` | Source | Treatment |
| --- | --- | --- |
| `icon-1024.png` | `Apps/iOS/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png` | Exact copy of current teal icon |
| `icon-256.png`, `favicon.png` | Same icon | Resize to 256 and 32 square |
| `dashboard-{light,dark}.jpg` | `Website/_source-shots/header-top-{light,dark}.png` | 720 × 1565, full screenshot |
| `widget-medium-{light,dark}.jpg` | `Website/_source-shots/widgets-3acc-{light,dark}.png` | Crop 1014 × 478 at x=48, y=424; no resize |
| `widget-large-{light,dark}.jpg` | `Website/_source-shots/widgets-large-6acc-{light,dark}.png` | Crop 1014 × 1060 at x=48, y=424; resize to 861 × 900 |
| `widgets-lock-{light,dark}.jpg` | `Website/_source-shots/widgets-lock-6acc-{light,dark}.png` | Crop 1030 × 830 at x=64, y=1030; resize to 900 × 725 |

`Website/_source-shots/` was supplied as an untracked staging folder, then deleted as requested after producing the public assets. No original screenshots are committed in that folder. The gallery contains sample data. Website captions explicitly distinguish in-app simulator widget previews from a live Home/Lock Screen. Press downloads retain that disclosure in surrounding copy.

The brand token `#30848C` was sampled from the actual PNG ring at x=512, y=875 via AppKit in sRGB. Other ring samples: x=512,y=150 `#469EA5`; x=850,y=512 `#3B9198`. Darker teal `#216970` provides normal-text AA contrast for buttons. No red/orange site palette colours are used. The unmodified dashboard screenshots contain the app’s small official Claude mark in its original clay colour; no provider mark is recreated, enlarged or used as separate hero art.

## 2026-11-04 redesign and Antigravity CLI

- Visual redesign only for the layout; claims are carried over from the sections above. Screenshots were
  recaptured on the iPhone 17 Pro Max simulator from the current main working tree with `-demoHealthy` /
  `-demoMultiAccount` sample data. The Lock Screen crop no longer cuts off the gallery.
- Antigravity CLI copy follows `Docs/STATUS.md` (2026-11-04 entry), `Docs/HANDOFF.md` and
  `Docs/research/antigravity-2026-11-04.md` in the app repo. **Status at writing: implemented in the main
  working tree but not yet committed.** Validation there: 264 package tests pass, Mac live refresh returned
  four quota windows, builds installed on the Mac and iPhone. Real Antigravity Google sign-in on the
  iPhone, its callback and credentialed phone quota reads are **unverified**. Do not publish the Antigravity
  claims until that work lands on main and the phone sign-in has been verified.
- Claims used: Mac helper runs version-gated `agy -p /usage --output-format json` (agy 1.1.11 or later), no
  agent turn, current `agy` sign-in only, no config folder, no Wake. Phone-only uses Antigravity CLI's
  Google OAuth client with PKCE loopback; scopes (cloud-platform, userinfo.email) are broader than quota
  access and the app says so; no website fallback; hosts accounts.google.com, oauth2.googleapis.com,
  cloudcode-pa.googleapis.com, daily-cloudcode-pa.googleapis.com; best-effort revocation at
  oauth2.googleapis.com/revoke. Quotas: measured 5-hour and weekly buckets per reported group; the Gemini
  group drives the main tiles; weekly-only accounts get no invented 5-hour window.
- Trademark line now names Google, Gemini and Antigravity; Terms say independent of Google too.
- The support page and Terms no longer name an individual; the company is the contact.
