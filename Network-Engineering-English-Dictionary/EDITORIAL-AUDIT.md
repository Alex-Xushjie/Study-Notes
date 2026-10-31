# Editorial Audit — 30 October 2026

[Home](README.md) · [Vocabulary progress](VOCABULARY-PROGRESS.md) · [Contents](TABLE-OF-CONTENTS.md)

## Scope and result

An automated structural audit covered all 1,019 entry files present at the start of this pass. It checked metadata, normalized headwords and IDs, chapter assignment, required definitions and examples, and internal file links. It was followed by a focused editorial check of duplicate candidates and selected OSPF, BGP, and IGMP entries. This was not an independent expert review of all entries, nor a verification of every technical statement or illustration.

Four duplicated concepts were merged, and their alternative names were kept as searchable aliases. The current count is **1,015 distinct draft entries**, not 1,019. Another 1,985 are needed to reach 3,000. The original files are retained in a local audit backup outside this project.

## Corrections

- Restored the cable-manager entry to English, including its usage, combinations and related-entry links.
- Merged duplicate entries for area border router, autonomous system boundary router, AS_PATH and route distinguisher. Names with a protocol prefix remain aliases.
- Corrected the OSPF type 1 external-route definition to account for a nonzero forwarding address, using [RFC 2328 section 16.4](https://www.rfc-editor.org/rfc/rfc2328.html#section-16.4).
- Clarified that some switches provide an IGMP snooping querier and that this function is not itself multicast routing. See [RFC 9776](https://www.rfc-editor.org/rfc/rfc9776.html) and the cited vendor documentation in the entry.
- Kept T568A and T568B as separate entries: they are different termination schemes even though their earlier short definitions were identical. Their distinctions still need a source-backed editorial pass.

## Outstanding work

- At the start of the pass, 982 of 1,019 entries lacked the dedicated common-combinations and related-entry sections specified by the style guide. These require meaningful individual editing, not automatically inserted filler.
- Review every entry against current primary sources, including protocol version, operational scope and platform-specific claims. Verify examples and workplace expressions for natural usage. All entries remain drafts until independently reviewed.
- Inspect every active illustration and numbered label against the actual object or documented topology. Do not treat an illustration or a passed link check as technical verification. Abstract concepts remain text-first until discussed.
- Continue expanding the dictionary to at least 3,000 useful, distinct headwords and expressions. Do not count aliases or mechanically generated variations as entries.
