---
id: "NEED-TEC-igmp-querier"
headword: "IGMP querier"
type: "technical"
chapter: "06"
aliases: []
tags: ["network-engineering"]
status: "draft"
updated: "2026-10-30"
---

# IGMP querier

**Network engineering term** · Chapter 06

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

A device that sends IGMP queries on a network segment to solicit group membership information.

## Usage and distinctions

The elected IGMP querier is normally a multicast router. Some switches offer an IGMP snooping querier for a VLAN; its behavior is platform-specific and does not by itself provide multicast routing.

## Examples

> The IGMP querier sends a general query.

> Verify that the receiver subnet has an operational querier.

## Sources and review

See [RFC 9776](https://www.rfc-editor.org/rfc/rfc9776.html) and [Cisco IGMP snooping guidance](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3750x_3560x/software/release/15-2_3_e/multicast/configuration_guide/b_mc_1523e_3750x_3560x_cg/b_ipmc_3750x_3560x_chapter_0110.html). Original teaching text; independent review remains pending.
