---
id: "NEED-TEC-dead-interval"
headword: "OSPF dead interval"
type: "technical"
chapter: "10"
aliases: []
tags: ["link-state routing"]
status: "draft"
updated: "2026-10-30"
---

# OSPF dead interval

**Network engineering term** · Chapter 10

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

The time after which an OSPF neighbor is considered down if expected hellos are not received.

## Usage and distinctions

The dead interval is a protocol setting; faster failure detection may use additional mechanisms such as BFD.

## Examples

> The neighbor is declared down after the dead interval expires.

> Check the dead interval when troubleshooting adjacency formation.

## Sources and review

See the [chapter references](../README.md#sources). Original learning entry; technical and language review are pending.
