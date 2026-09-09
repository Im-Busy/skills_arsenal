# Search lanes

Load this file after the SKILL.md workflow. Run all four lanes unless the
user narrowed the request. Use at least two query angles per lane.

## Papers

Check the local academic-papers catalog (`CATALOG.jsonl`) first. Prefer arXiv
PDF URLs. Also search PLOS, ACM, IEEE, Springer, Nature, and university
    10|repositories. Register every kept PDF in the catalog with tag
`academic-papers`.

Query angles: the failure mode, the named technique, the measurement.

## Existing projects

Search GitHub repositories and code, then the local `useful_repos/`
reference clone directory and any existing `projects/` tree. Record
owner/repo, stars, license, last push, and what identity-or-location
mechanism the repo actually implements.
    20|
Query angles: tool name, problem phrase, language plus checker or catalog.

Do not clone here. If the user later names URLs and a link root, hand off
to `acquire-and-link-repos`.

## Engineering guidelines

Search standards bodies and long-lived practice notes: W3C, IETF/RFCs,
ISO, NIST, CNCF, docs-as-code writeups, and vendor-neutral engineering
    30|handbooks. Keep a source only when it states a rule or mechanism, not a
product pitch.

Query angles: the durable name of the practice, plus guideline or
best practice.

## Forums

Search more than one Stack Exchange site and at least one other forum
family. Default hosts:
    40|
- stackoverflow.com
- softwareengineering.stackexchange.com
- superuser.com
- serverfault.com
- reddit.com
- news.ycombinator.com
- discourse-hosted project forums
- dev.to
- journal.code4lib.org and similar practitioner venues
    50|
Query angles: the practitioner symptom, then the named technique.
Treat forum answers as practice evidence, not as papers. Record the URL
and the claimed mechanism.
