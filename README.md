# Cash Predict website

Static, buildless website for https://cashpredict.app. The selected design combines
the Light direction’s spacious product story with the Dark direction’s navy contrast.
One responsive layout follows system appearance using `prefers-color-scheme`; no
manual preference, cookie, remote font, analytics, framework or third-party runtime
is added to the website. Editorial is an archived exploration, not the selected site.

## Source and hosting

- Checkout: `/Users/klebermaia/Projects/Web/cashpredict`.
- Repository: `git@github.com:kleber-maia/web.cashpredict.git`.
- GitHub Pages API verified on 2026-10-26: legacy publishing from `master`, `/`,
  custom domain `cashpredict.app`; baseline `78106758f647c1094b6a8456ac1026e43ef8b54c`.
- CNAME and hosting configuration are unchanged. The user approved this design and
  publication on 2026-10-26: “looks nice: publish it”. Publish only the production
  website deliverables to the existing `master` branch; leave local design previews
  and the separate app checkout untouched. No hosting or DNS changes are needed.

## Preview and checks

The detached local server serves this checkout on `http://127.0.0.1:8765/`.
It is bound to loopback, not exposed publicly. To start a stopped server:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

The selected automatic site is `/`. Local review pages are intentionally excluded
from production commits. The noindex review page `/previews/system/`
shows generated Light and Dark review copies of that exact site and stylesheet,
with tokens pinned only in those noindex review files. IAB forces its dark preference
after loading even on an iframe requesting light, so the pinned review copies allow
honest visual verification of both palettes without changing the Mac’s settings.
The product site has no override and uses only the system media query.
The earlier `/previews/dark/`, `/previews/light/` and `/previews/editorial/` are
historical local explorations and are not linked from the selected site.

```sh
python3 scripts/check-site.py
node --check assets/js/site.js
# Optional: also inspect local design explorations, when present.
python3 scripts/check-site.py --include-previews
```

Checks cover links, anchors, schemas, preserved destinations/message, original image
hashes, seven full captures, matching frame models/orientations/openings, license
provenance and Pages CNAME. Responsive and visual rendering still require IAB review.
The site works without JavaScript; JavaScript adds the mobile menu and automatically
opens a linked FAQ. All screenshot detail crops were removed from the selected site.

## Design and preserved content

The two original statements remain: “Micromanaging expenses is ancient thinking.”
and “Cash Predict is all about your present and future.” The logo, future focus,
no-micromanagement philosophy, App Store destination, support and blog are preserved.
Website text is navy/charcoal in light mode and white in dark mode; green remains
only within genuine app UI. The logo and official App Store badge follow the system
appearance too. Design dials: variance 7, motion 2, density 3; native CSS evolves the
existing static site, with a uniform whole-page palette and restrained interaction.

Current app evidence is version 27.0.4, commit
`5fca70cee1a9ae1d90065da37b800a8d41daa78a` in `kleber-maia/cash-predict`:

| Website claim | App source evidence |
| --- | --- |
| Savings goals and debt payoff | `Model/Account.swift`, `AI Tools/GoalsTool.swift`, current Goals screenshot |
| Multi-year Future Outlook and assumptions | `Model/ProjectionSettings.swift`, `Helpers/ProjectionCalculator.swift`, current Outlook screenshot |
| Financial insights | `Helpers/InsightsHelper.swift`, `Views/Cards/GlobalInsightsCard.swift` |
| 3-, 6-, 12-month dashboard chart range | App `README.md`, Settings display configuration |
| iCloud sync | `Helpers/Extensions/SyncEngine+Ext.swift`, `Helpers/SyncHelper.swift` |
| Widgets and Siri Shortcuts | `Widget/`, `Cash Predict/App Intents/`, app development guide |
| User-initiated one-year PDF export for AI | `SwiftUI/AIExportView.swift` |
| Private chat currently disabled | `SwiftUI/AIExperienceView.swift`: `privateChatEnabled = false` |
| iOS/iPadOS 26+, Apple silicon macOS 26+ | App `README.md` and deployment configuration |
| Analytics API calls supply aggregate account balances | `Helpers/AnalyticsHelper.swift`, `Model/Account.swift`, `AppDelegate.swift` |
| Free app advertising, Plus removes ads | `Helpers/AdManager.swift`, `Helpers/StoreHelper.swift` |

Paths in the table are relative to the app's `Cash Predict/` folder unless a
repository-level path is shown. No Apple Watch app exists. Old Watch support
claims and unverified rating/review-count metadata were removed. Absolute
no-transmission or complete-privacy claims were replaced with specific facts
about sign-up, iCloud, analytics, advertising and optional sharing. Existing
privacy-policy and terms PDFs are retained unchanged. A read-only comparison
found that the legacy privacy PDF’s no-transmission-except-iCloud promise and
complete-anonymity wording need review against current analytics API calls and a
persistent user ID. Actual production network transmission was not tested. The
GoogleService-Info.plist IS_ANALYTICS_ENABLED flag is false, but Firebase lists
that as an unread field; it is not a documented collection gate. This website
work does not change app telemetry or rewrite legal policies. The standard EULA
showed no additional material product-feature inconsistency in this comparison.

## Genuine screenshots and Apple artwork

`img/current/provenance.json` is the source of truth for seven original native PNGs,
app baseline/version, device, runtime, fictional $60k dataset and capture method.
Those files have not been retouched, recomposed, cropped or re-encoded in this step.
Every screenshot in the selected site is displayed in full inside an official frame.
Links to original PNGs remain for inspection. The native app’s existing chart-label
clipping is visible faithfully; this website work does not change the app.

Official source: https://developer.apple.com/design/resources/#product-bezels
Guidelines: https://developer.apple.com/app-store/marketing/guidelines/

The user approved the bundled Apple Design Resources license LYL142 (06/21/2023):
“Yes, accept the Apple resource license”. Both official packages were opened read-only.
`img/apple/Apple-Design-Resources-License.txt` preserves the readable bundled terms;
`img/apple/provenance.json` records the exact downloads, hashes, screen geometry and
approval quote. This is licensed Apple artwork for depictions of the Apple-platform
app, not a general-purpose clip-art package or standalone asset redistribution.

| Capture | Official frame | Native canvas | Screen opening |
| --- | --- | --- | --- |
| Six iPhone 18 Pro portrait screens | iPhone 18 Pro, Black, Portrait | 1350×2760 | x72, y69, 1206×2622 |
| iPad (A16) landscape | iPad (A16), Silver, Landscape | 2760×2040 | x200, y200, 2360×1640 |

Apple PNGs are copied byte-for-byte and displayed without added shadows, tilt,
perspective, flipping, animation or crop. Screens scale uniformly to their matching
openings; the iPad capture’s original PNG orientation metadata is retained. Native
corner masking sits beneath the unmodified artwork. Promotional copy stays beside
the devices. The footer credits Apple trademarks and links the artwork license.

Review captures and temporary downloads live under `/tmp/cashpredict-site-review`
and `/tmp/cashpredict-apple-frames`; they are not deployment output. The app checkout,
normal financial store, existing stash and accepted App Store artwork are untouched.
