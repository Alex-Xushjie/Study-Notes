---
id: "NEED-TEC-longest-prefix-match"
headword: "longest prefix match"
type: "technical"
chapter: "09"
aliases: []
tags: ["routing"]
status: "draft"
updated: "2026-10-30"
---

# longest prefix match

**Network engineering term** · Chapter 09

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

The selection of the matching route with the greatest prefix length for a destination.

## Usage and distinctions

Longest prefix match is applied to matching destination prefixes; it is distinct from choosing between otherwise competing routes to the same prefix.

## Examples

> A /24 route is selected over a matching /16 route.

> Check for a more specific prefix before blaming the default route.

## Sources and review

See the [Chapter 09 references](../README.md#sources). Original learning entry; technical and language review are pending.
