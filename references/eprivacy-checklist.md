# ePrivacy checklist (Directive 2002/58/EC, as amended by 2009/136/EC)

As of this writing the ePrivacy Directive, not a Regulation, still governs cookies and similar
technologies alongside the GDPR. The European Commission withdrew its long-stalled ePrivacy Regulation
proposal, and a "Digital Omnibus" package would fold cookie rules into a new GDPR Art. 88a instead.
As last checked (16 September 2026) that package was still in the legislative procedure and not adopted
law, `VERIFY` its status before relying on anything beyond what is below. Until it is adopted and
applicable, the rule is still the national transposition of the Directive plus the GDPR. Do not confuse
it with the separate "Digital Omnibus on AI", which amended the AI Act and was adopted in 2026.

## 1. Consent for storage and access (Art. 5(3))

Any cookie, local storage, or similar technology that is not "strictly necessary" for a service the
user explicitly requested needs prior, informed, freely given consent before it is set or read. This
covers analytics cookies (including "privacy-friendly" analytics, in most regulator guidance these are
still not automatically exempt, `VERIFY` for the specific tool), advertising and retargeting pixels,
third-party embeds that set cookies (YouTube, Google Maps, social share/follow buttons, font or CDN
scripts that track), and A/B testing or personalization scripts.

Strictly necessary, generally exempt: session cookies needed for login state, a shopping cart, load
balancing, or the cookie-consent tool's own memory of the user's choice.

## 2. What "valid consent" means for cookies in practice

- No pre-ticked boxes or pre-loaded acceptance.
- A genuine reject option, equally easy and equally prominent as accept, not hidden behind extra
  clicks or a confusing "manage preferences" maze while "accept all" is one click.
- No non-essential cookie actually fires before the user makes a choice. Test this, not just read the
  banner code, many implementations set analytics/ad cookies on page load regardless of the banner.
- Granular choice by purpose/category where more than one non-essential purpose exists, not just a
  single accept-everything toggle if there are, for example, both analytics and advertising cookies.
- Consent must be re-obtainable, i.e. there is a way to withdraw or change the choice later (a
  persistent "cookie settings" link/footer item).
- No "cookie wall" that blocks all access to content unless the user accepts non-essential cookies,
  most national regulators treat this as invalid consent (Art. 7(4) GDPR, freely given).

## 3. Direct electronic marketing (Art. 13)

Sending marketing emails, SMS, or similar to individuals generally requires prior opt-in consent, with
a narrow "soft opt-in" exception in some member states for existing customers being marketed similar
products, `VERIFY` the exact national transposition. Every marketing message needs a clear, working
unsubscribe/opt-out mechanism. Check any newsletter signup: is it single or double opt-in, is consent
for marketing bundled with an unrelated action (e.g. auto-subscribing on account creation) which is not
valid.

## 4. Third-party embeds, a common trap

Embedding YouTube, Google Maps, Google Fonts loaded from Google's CDN, Facebook/Instagram widgets, or
similar third-party content typically triggers a request to that third party's servers, which can set
cookies or share the visitor's IP address before any consent choice. Options worth flagging in the
report: load the embed only after consent, use a privacy-enhanced/no-cookie mode if the provider offers
one, self-host static assets like fonts instead of calling an external CDN, or replace the embed with a
click-to-load placeholder.
