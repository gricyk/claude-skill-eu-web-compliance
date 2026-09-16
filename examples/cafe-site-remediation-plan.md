# Remediation plan: Example Café (fictional demo)

> **Demo output**, Step 5 of the skill's workflow, following
> [`cafe-site-report.md`](cafe-site-report.md). The skill presents this plan and **waits for approval**
> before touching any file. Approve all, approve item by item, or ask for changes.

**This plan is not legal advice.** Items marked ⚖️ carry enough exposure that a lawyer or DPO should
review the result before it goes live.

## Proposed changes

| # | Fixes | File(s) | Change |
|---|---|---|---|
| 1 | A1 ⚖️ | `server/chat.ts`, `assets/chat-widget.js` | Remove "Never mention that you are an AI" from the system prompt and add "If asked, say you are an AI assistant". Rename the header from "Anna from Example Café" to "Example Café AI assistant" and add the disclosure below under it. |
| 2 | A3 | `server/chat.ts` | Add to the system prompt: for allergen questions, give general menu information and advise confirming with staff. |
| 3 | E1 ⚖️ | `index.html`, `events.html`, `assets/cookie-banner.js` | Remove unconditional gtag loading from both pages. Rewrite the banner with equally prominent "Accept analytics" and "Reject all" buttons; load gtag.js only after acceptance; store the choice; add a "Cookie settings" footer link that reopens the banner. Remove the implied-consent sentence from the privacy page. |
| 4 | E3 | `assets/styles.css`, `index.html` | Self-host Playfair Display and Inter (`/assets/fonts/`). Replace the YouTube iframe with a click-to-load placeholder using `youtube-nocookie.com`. Replace the Maps iframe with a static map image linking to Google Maps. Load reCAPTCHA only on first interaction with the contact form. |
| 5 | G2, E2 | `index.html` | Newsletter checkbox unticked and worded "Send me the Example Café newsletter (optional, unsubscribe anytime)". Replace "I agree to the privacy policy" with a plain link "How we use your data". |
| 6 | G3 ⚖️ | `events.html` | Narrow the field to "Food allergies or intolerances relevant to this workshop". Add a separate unticked checkbox: "I explicitly consent to Example Café using this allergy information only to prepare my workshop; it is deleted after the event." |
| 7 | G4 | `events.html` | Group child fields under "Booking for a child (parent or guardian)", collect first name and age only. |
| 8 | G5 | `server/chat.ts` | Stop storing the IP address; add `expiresAt` 30 days after creation (deletion job to be added in the database layer, which was not provided). Add "Conversations are kept for 30 days to improve answers" to the widget. |
| 9 | G7 | `server/comments.ts` | Stop storing the IP address, or keep it 7 days for abuse prevention, per your choice. |
| 10 | D1, D2 | `blog/ai-latte-art.html`, `server/comments.ts`, new `comment-rules.html` | Add a "Report comment" link and form; on deletion, email the author a short reason; publish short comment rules and a contact point. |
| 11 | X1–X6 | `index.html`, `assets/styles.css` | Add `lang="cs"` (or `en`, please confirm) and viewport meta; `alt` for the logo and interior photo (text to be confirmed by you); labels for the newsletter email and message fields; `<button>` for the menu toggle; body text color `#595959` (7.0:1) and cookie settings link restyled as a button; `<h3>` to `<h2>`. |
| 12 | A2 | `blog/ai-latte-art.html` | Optional: caption "Image: AI-generated". |

## Draft chatbot disclosure (item 1)

From `references/templates/ai-transparency-notice.md`:

> You are chatting with an AI assistant, not a person. It can answer questions about our menu, opening
> hours and events. For allergies, please confirm with our staff or write to {{contact_email}}.

## Documents to draft (after approval)

| Document | Template | Status |
|---|---|---|
| Privacy notice (G1, G6) ⚖️ | `references/templates/privacy-policy.md` | Blocked on missing facts below |
| Cookie policy (E1, E3) | `references/templates/cookie-policy.md` | Needs the runtime cookie list after item 3 |
| Records of processing (G8) | `references/templates/ropa.md` | Blocked on retention periods |
| Comment rules and contact point (D2) | none, short custom page | Ready to draft |
| DPIA | not proposed | Not required at this scale, see G9 |
| Accessibility statement | not proposed | No legal duty found; optional |

## Missing facts (nothing will be invented)

1. Company ID (IČO), registered address, privacy contact email
2. Retention periods: bookings, contact messages, comments, newsletter after unsubscribe
3. LLM provider, API region, and whether its data processing terms are signed
4. Newsletter tool and whether it uses double opt-in
5. Primary language of the home page (`cs` or `en`)
6. Alt text wording for the logo and interior photo
7. Whether to keep Google Analytics (needs consent) or switch to a consent-free setup

## Checks after changes

- Load each page in a fresh browser profile and confirm no request to Google domains and no cookies
  before a choice in the banner.
- Re-run `python3 scripts/scan.py examples/cafe-site --domain example.com`.
- Keyboard-only walk-through of the menu, forms, cookie banner and chat.
