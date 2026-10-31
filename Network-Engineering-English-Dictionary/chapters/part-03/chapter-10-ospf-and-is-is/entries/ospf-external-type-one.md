---
id: "NEED-TEC-ospf-external-type-one"
headword: "OSPF external type 1 route"
type: "technical"
chapter: "10"
aliases: []
tags: ["network-engineering"]
status: "draft"
updated: "2026-10-30"
---

# OSPF external type 1 route

**Network engineering term** · Chapter 10

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

An OSPF external route whose type 1 metric includes the internal cost to the ASBR or the forwarding address, plus the advertised external metric.

## Usage and distinctions

Often written E1. In OSPFv2, a nonzero forwarding address changes the internal endpoint used in the calculation; additional route-selection rules apply.

## Examples

> The team selected an OSPF external type 1 route for the design.

> Compare the total internal and external costs.

## Sources and review

See [RFC 2328, section 16.4](https://www.rfc-editor.org/rfc/rfc2328.html#section-16.4). Original teaching text; independent technical and language review remains pending.
