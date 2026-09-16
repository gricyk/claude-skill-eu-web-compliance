# Cookie Policy template

Build the cookie table from what `scripts/scan.py` and manual code review actually found, do not
list a generic/example set of cookies that may not match the real site.

---

## Cookie Policy

Last updated: {{date}}

This site uses cookies and similar technologies as described below.

### Strictly necessary (no consent required)

| Name | Provider | Purpose | Duration |
|---|---|---|---|
| {{cookie_name}} | {{provider}} | {{purpose}} | {{duration}} |

### Requires your consent before being set

| Name | Provider | Category | Purpose | Duration |
|---|---|---|---|---|
| {{cookie_name}} | {{provider}} | {{analytics/advertising/personalization}} | {{purpose}} | {{duration}} |

### Managing your choice

You can accept or reject non-essential cookies when you first visit, and change your choice at any
time via {{cookie_settings_link_or_mechanism}}. Rejecting non-essential cookies does not affect your
ability to use the core functionality of this site.

### Third-party content

{{#if third_party_embeds}}
This site embeds content from {{list_of_third_parties}} (e.g. maps, video). Loading this content may
set cookies from that provider even before you interact with our own consent banner
{{loading_behavior_note}}.
{{/if}}
