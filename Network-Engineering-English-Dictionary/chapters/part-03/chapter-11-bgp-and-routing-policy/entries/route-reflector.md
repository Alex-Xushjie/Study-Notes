---
id: "NEED-TEC-route-reflector"
headword: "BGP route reflector"
type: "technical"
chapter: "11"
aliases: []
tags: ["BGP routing policy"]
status: "draft"
updated: "2026-10-30"
---

# BGP route reflector

**Network engineering term** · Chapter 11

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

An iBGP speaker that can re-advertise routes between designated iBGP clients and other peers.

## Usage and distinctions

A route reflector reduces the need for a full iBGP mesh but introduces design considerations for path visibility and loop prevention.

## Examples

> The route reflector distributes the route to its clients.

> Check the reflector’s client relationships and policy.

## Sources and review

See the [chapter references](../README.md#sources). Original learning entry; technical and language review are pending.
