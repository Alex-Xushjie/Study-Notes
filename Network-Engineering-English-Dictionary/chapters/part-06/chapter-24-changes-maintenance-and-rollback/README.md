# Chapter 24 · Changes, Maintenance & Rollback

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-23-incidents-and-escalation/README.md) · [Next chapter](../../part-07/chapter-25-requirements-and-constraints/README.md)

## Chapter topics

1. [Planning a Network Change](01-change.md)
2. [Validation and Rollback](02-rollback.md)

## Say it at work

> The approved change is limited to one branch router.

> We will begin after the prerequisites and baseline checks are complete.

> We will roll back if the agreed connectivity checks fail.

> The change is complete; the post-change validation passed.

## Quick review

1. Does an access window authorize a network change?
2. Does a saved configuration include all system state?
3. What makes rollback criteria useful?
4. Does deployment alone mean the change is complete?

**Answers**

1. No; the required change authorization and prerequisites are separate.
2. Not necessarily; verify what the backup covers.
3. Observable conditions, a decision owner, and appropriate timing.
4. No; required validation, records, and communication must also be completed.

## All chapter entries (24)

- [baseline check](entries/baseline-check.md)
- [change approval](entries/change-approval.md)
- [change closure](entries/change-closure.md)
- [change deployment](entries/deployment.md)
- [change freeze](entries/change-freeze.md)
- [change log](entries/change-log.md)
- [change owner](entries/change-owner.md)
- [change plan](entries/change-plan.md)
- [change prerequisite](entries/prerequisite.md)
- [change request](entries/change-request.md)
- [change scope](entries/change-scope.md)
- [configuration backup](entries/configuration-backup.md)
- [implementation plan](entries/implementation-plan.md)
- [maintenance window](entries/maintenance-window.md)
- [network change](entries/change.md)
- [planned service impact](entries/maintenance-impact.md)
- [post-change validation](entries/post-change-validation.md)
- [post-implementation review](entries/post-implementation-review.md)
- [pre-change check](entries/pre-change-check.md)
- [restore a configuration](entries/restore-configuration.md)
- [rollback criteria](entries/rollback-criteria.md)
- [rollback decision](entries/rollback-decision.md)
- [rollback plan](entries/rollback-plan.md)
- [We will roll back if …](entries/rollback-expression.md)

## Sources

- [NIST SP 800-128: Security-Focused Configuration Management](https://csrc.nist.gov/pubs/sp/800/128/upd1/final)
- [Google SRE: Release Engineering](https://sre.google/sre-book/release-engineering/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
