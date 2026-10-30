---
id: "NEED-TEC-address-aggregation"
headword: "address aggregation"
type: "technical"
chapter: "07"
aliases: []
tags: ["addressing"]
status: "draft"
updated: "2026-10-30"
---

# address aggregation

**Network engineering term** · Chapter 07

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

The representation of multiple address prefixes by a shorter covering prefix.

## Usage and distinctions

An aggregate covers all addresses within its prefix; advertise it only when the routing design handles covered destinations appropriately.

## Examples

> The two /25 networks can be represented by one /24 aggregate.

> Check reachability before advertising the aggregate.

## Sources and review

See the [Chapter 07 references](../README.md#sources). Original learning entry; technical and language review are pending.
