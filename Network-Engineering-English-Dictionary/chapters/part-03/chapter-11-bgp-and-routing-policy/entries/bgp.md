---
id: "NEED-TEC-bgp"
headword: "Border Gateway Protocol"
type: "technical"
chapter: "11"
aliases: ["BGP"]
tags: ["networking", "technical"]
status: "draft"
updated: "2026-10-30"
---

# Border Gateway Protocol

**Proper noun; abbreviation: BGP.** · Chapter 11 · `technical`

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

A routing protocol that exchanges network reachability information between BGP speakers.

## Usage and distinctions

An established BGP session alone does not guarantee reachability. Verify routes, policies, next-hop reachability, and forwarding.

## Common combinations

BGP session; advertise a prefix; withdraw a route; routing policy

## Examples

> The BGP session is established, but the expected prefix is not being advertised.

> Check the export policy before changing the peer configuration.

## Related entries

[Domain Name System](../../../part-02/chapter-08-transport-and-application-services/entries/dns.md) · [maintenance window](../../../part-06/chapter-24-changes-maintenance-and-rollback/entries/maintenance-window.md)

## Sources and review

[S5](../../../../SOURCES.md#s5) Original learning text; draft awaiting independent technical and language review.
