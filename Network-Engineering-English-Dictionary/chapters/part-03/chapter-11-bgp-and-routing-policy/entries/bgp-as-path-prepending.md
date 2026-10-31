---
id: "NEED-TEC-bgp-as-path-prepending"
headword: "BGP AS-path prepending"
type: "technical"
chapter: "11"
aliases: []
tags: ["network-engineering"]
status: "draft"
updated: "2026-10-30"
---

# BGP AS-path prepending

**Network engineering term** · Chapter 11

[Chapter](../README.md) · [English index](../../../../indexes/ENGLISH-INDEX.md)

## Definition

The practice of adding occurrences of an autonomous system number to an advertised AS path to influence remote route preference.

## Usage and distinctions

Remote policy can override the intended effect, so prepending does not guarantee inbound traffic selection.

## Examples

> Apply BGP AS-path prepending on the less-preferred provider link.

> Check the path seen by the remote network after prepending.

## Sources and review

Original teaching text. Technical and English-language review is pending; confirm platform-specific details in current equipment or standards documentation.
