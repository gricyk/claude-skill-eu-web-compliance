# EU AI Act checklist (Regulation (EU) 2024/1689, as amended)

Only relevant if the site actually uses an AI system: a chatbot, AI-generated text/image/audio/video,
a recommender or personalization engine, automated scoring/screening, or similar. A static informational
site with no AI feature has essentially no AI Act exposure, say so and skip the rest.

**Always web search the current timeline before citing a deadline.** Treat every date below as the
situation when this file was last checked (16 September 2026, from secondary legal commentary), not a
guarantee, and confirm with a search, ideally against EUR-Lex, before using it in a report.

Snapshot as last checked:

- Entered into force 1 August 2024; generally applicable from 2 August 2026.
- Prohibited practices (Art. 5) and AI literacy (Art. 4): applicable since 2 February 2025.
- The "Digital Omnibus on AI", reported as Regulation (EU) 2026/1744 (in force 27 July 2026), amended
  the timeline:
  - Annex III high-risk systems: postponed to 2 December 2027.
  - High-risk AI in products covered by Annex I sectoral legislation: postponed to 2 August 2028.
  - Art. 50 disclosure duties for deployers (chatbots, deepfakes, public-interest text): not postponed,
    apply from 2 August 2026.
  - Art. 50(2) machine-readable marking, for systems already on the market before 2 August 2026:
    reported as 2 December 2026.
  - Reported new prohibition on AI systems used to generate child sexual abuse material or
    non-consensual intimate imagery, and SME relief extended to small mid-caps.
  `VERIFY` the regulation number and each date against the Official Journal text before citing.

## 1. Prohibited practices (Art. 5)

Applicable since 2 February 2025. Relevant to a typical website mainly if it does anything close
to: subliminal or manipulative techniques that materially distort behavior and cause harm, exploiting
vulnerabilities of a specific group (age, disability), social scoring, or untargeted scraping of facial
images to build a recognition database. Most content and marketing sites will not trigger this, but
flag it explicitly if the site uses aggressive dark-pattern-style AI personalization aimed at
vulnerable users, e.g. children.

## 2. AI literacy (Art. 4)

Providers and deployers of AI systems must ensure staff and others dealing with the AI system on their
behalf have sufficient AI literacy. Organizational, not a code check, but worth a one-line note if the
site's operator deploys an AI feature and clearly has no policy or training around it.

## 3. Transparency obligations (Art. 50), the article most likely to matter for a website

- If a person is interacting with an AI system (chatbot, voice assistant) and it is not obvious from
  the circumstances, they must be informed they are interacting with AI, unless it is obvious to a
  reasonably well-informed person.
- AI-generated or manipulated image, audio, or video content ("deepfake"-style) must be disclosed as
  such, with specific exceptions (e.g. clearly artistic/satirical work, with appropriate disclosure of
  the work's fictional nature).
- AI-generated or manipulated text published to inform the public on matters of public interest must be
  disclosed as AI-generated, unless it went through human review/editorial control and a natural or
  legal person holds editorial responsibility.
- Emotion recognition or biometric categorization systems must inform the people exposed to them.
- A machine-readable marking requirement for synthetic content exists for providers (Art. 50(2)), its
  in-force date for systems already on the market was moved by the Digital Omnibus on AI, see the
  snapshot above and `VERIFY`.

For a church, ministry, or small business site: a chatbot needs a "you're chatting with an AI
assistant" style disclosure, AI-generated images or illustrative content used editorially should
generally be labeled as AI-generated, and AI-drafted blog/news content presented as if from the
organization should go through real human editorial review to fall outside the disclosure duty (or be
labeled if it does not).

## 4. Risk classification (Art. 6, Annex III)

Most content, marketing, or community-organization websites do not use "high-risk" AI as defined by
Annex III (biometric ID, critical infrastructure, education/employment scoring, access to essential
services, law enforcement, migration, justice, etc.). Check specifically if the site does anything like
automated screening of job or program applicants, automated eligibility decisions for services, or
biometric identification, if so, flag it clearly as potentially high-risk and recommend dedicated legal
review, this checklist is not sufficient for that case.

## 5. General-purpose AI (GPAI) models

Relevant to the provider of the underlying model (e.g. the company behind the API the site calls), not
usually to the website operator using that API. Note this distinction in the report so the user does
not think they owe GPAI-provider obligations for simply calling a third-party AI API.

## 6. Governance and enforcement

From 2 August 2026 the AI Office and national competent authorities can enforce the Act. Which
authority applies nationally is `VERIFY` per member state, see `national-law-guide.md`.
