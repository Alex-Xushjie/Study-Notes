# Chapter 26 · Architecture & Trade-offs

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-25-requirements-and-constraints/README.md) · [Next chapter](../chapter-27-documentation-diagrams-and-handover/README.md)

## Chapter topics

1. [Architecture and Alternatives](01-architecture.md)
2. [Resilience and Capacity](02-risk.md)

## Say it at work

> What requirements does each option satisfy, and what does each cost?

> The two paths appear redundant but share a power dependency.

> This option is simpler to operate, but it has less capacity headroom.

> We recommend a pilot with clear success and rollback criteria.

## Quick review

1. Does redundant hardware alone prove resilience?
2. Does a successful proof of concept prove production readiness?
3. What is residual risk?
4. Why record design rationale?

**Answers**

1. No; shared dependencies and operational recovery also matter.
2. No; it validates only its defined scope and conditions.
3. Risk that remains after mitigation.
4. So future reviewers can understand the context and trade-offs.

## All chapter entries (24)

- [capacity headroom](entries/headroom.md)
- [capacity planning](entries/capacity-planning.md)
- [dependency mapping](entries/dependency-mapping.md)
- [design alternative](entries/design-alternative.md)
- [design complexity](entries/complexity.md)
- [design criterion](entries/design-criterion.md)
- [design decision](entries/design-decision.md)
- [design failure domain](entries/failure-domain-design.md)
- [design option](entries/design-option.md)
- [design principle](entries/design-principle.md)
- [design rationale](entries/design-rationale.md)
- [design review](entries/design-review.md)
- [design trade-off](entries/trade-off.md)
- [design validation](entries/design-validation.md)
- [fault isolation](entries/fault-isolation.md)
- [network architecture](entries/network-architecture.md)
- [network resilience](entries/resilience.md)
- [operational simplicity](entries/simplicity.md)
- [pilot deployment](entries/pilot.md)
- [proof of concept](entries/proof-of-concept.md)
- [reference architecture](entries/reference-architecture.md)
- [residual risk](entries/residual-risk.md)
- [risk mitigation](entries/risk-mitigation.md)
- [scalability](entries/scalability.md)

## Sources

- [NIST: System Security Engineering](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final)
- [Google SRE: The Evolution of Automation](https://sre.google/sre-book/evolving-automation/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
