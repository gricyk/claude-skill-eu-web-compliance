# GDPR checklist (Regulation (EU) 2016/679)

Core articles are stable law and safe to cite directly. Anything about fines, guidance, or national
detail should still be checked live, mark `VERIFY` if not confirmed this session.

## 1. Is there personal data at all (Art. 4(1))

Any information relating to an identified or identifiable natural person: name, email, phone, IP
address, cookie/device identifiers, photos of identifiable people, free-text form fields that could
name someone (e.g. a prayer request naming a third person). If the site truly collects nothing beyond
anonymous page views with no identifiers, GDPR exposure is minimal, say so and move on.

## 2. Lawful basis (Art. 6)

For every data flow found (contact form, newsletter signup, account creation, event/membership
registration, analytics), identify the claimed lawful basis: consent (6(1)(a)), contract (6(1)(b)),
legal obligation (6(1)(c)), vital interests (6(1)(d)), public task (6(1)(e)), or legitimate interests
(6(1)(f)). Flag any data flow with no identifiable basis. Legitimate interest requires a genuine
balancing test, do not accept it as a default label without one.

## 3. Consent quality (Art. 7)

If consent is the basis: was it freely given, specific, informed, and unambiguous, given by a clear
affirmative act? Check for pre-ticked boxes (not valid), bundled consent (e.g. one checkbox for
"terms + newsletter + data sharing", not valid), and whether withdrawal is as easy as giving consent.

## 4. Children's data (Art. 8)

If the site is directed at children, or a child could plausibly submit data (registration for
children's or youth groups, events, camps), Art. 8 requires parental consent or authorization for
"information society services" offered directly to a child below the applicable age, the GDPR default
is 16, but member states may set their own threshold between 13 and 16. The applicable age for the
site's target country is always `VERIFY`, do not assume 16. Check: is there any age gate, any
parental consent mechanism, any indication of who is actually filling in the form (parent vs child)?

## 5. Special categories of data (Art. 9)

Religious or philosophical belief, health data, data revealing racial or ethnic origin, and others
listed in Art. 9(1) get extra protection and generally need an Art. 9(2) condition (most often
explicit consent) on top of an Art. 6 basis. Church, ministry, and community-group sites routinely
touch this: membership lists that reveal religious affiliation, prayer request forms, health
information in event registration (allergies, medical needs for a camp), or photos tagged with
religious context. Flag these explicitly, they are a common blind spot.

## 6. Transparency (Art. 12 to 14)

Is there a privacy notice, is it easy to find, written in plain language, and does it actually cover
what Art. 13 (data collected directly, e.g. via a form) or Art. 14 (data collected indirectly) require:
identity and contact of the controller, purposes and legal basis, recipients, retention period or
criteria, data subject rights, right to lodge a complaint with a supervisory authority, and, for
automated decision-making, meaningful information about the logic involved.

## 7. Data subject rights (Art. 15 to 22)

Is there a clear, working way to exercise: access (15), rectification (16), erasure (17), restriction
(18), portability (20), and objection (21)? A dead "contact us for your data" link with no defined
process is a gap, not a fix.

## 8. Security (Art. 32)

Is data in transit encrypted (HTTPS everywhere, no mixed content)? Are form submissions handled by a
reputable, current backend, not an unmaintained plugin with known vulnerabilities? Is access to any
admin panel or data export protected properly?

## 9. Breach notification readiness (Art. 33 to 34)

Not something code alone can confirm, but check whether there is any process referenced (who gets
notified, how) and flag if there is clearly none for a site handling non-trivial personal data.

## 10. DPO (Art. 37 to 39)

Required in specific cases (public authority, large-scale regular/systematic monitoring, large-scale
special-category processing). Most small sites will not need one, note the assessment briefly rather
than skipping it.

## 11. Records of processing (Art. 30)

Formally required mainly above a certain size or where processing is not occasional, or involves
special categories/high risk. Regardless of the legal threshold, a short internal record of what data
is collected, why, and for how long is good practice, and the skill can draft one
(`references/templates/ropa.md`).

## 12. International transfers (Art. 44 to 49)

Check every third-party service the site sends personal data to (analytics, email marketing tool,
form backend, hosting, AI API). Is data going outside the EU/EEA? If so, is there an adequacy decision,
Standard Contractual Clauses, or another Art. 46 mechanism in place, and is this reflected in the
privacy notice? Flag any US-based analytics, forms, or AI service without a stated transfer mechanism.

## 13. Cookies and consent-management tooling

GDPR and the ePrivacy Directive work together here, see `eprivacy-checklist.md` for the cookie-specific
rules. Confirm the consent-management tool itself (if any) actually blocks non-essential
cookies/scripts before consent, a banner that only hides itself while scripts already fired is a
common real-world defect worth specifically testing for.
