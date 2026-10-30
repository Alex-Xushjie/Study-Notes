# Chapter 28 · Automation & APIs

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-27-documentation-diagrams-and-handover/README.md) · [Next chapter](../../part-08/chapter-29-meetings-and-clarification/README.md)

## Chapter topics

1. [Using an API](01-api.md)
2. [Automation Workflow](02-workflow.md)

## Say it at work

> Which environment, endpoint and API version does this request use?

> The dry run shows changes outside the approved scope.

> The task is idempotent when repeated under the tested conditions.

> The commit is merged, but deployment and post-change validation are still pending.

## Quick review

1. Does a Git commit mean the change is deployed?
2. Does idempotent mean the first run cannot change anything?
3. Is JSON a network protocol?
4. Does a dry run predict every runtime effect?

**Answers**

1. No; deployment is a separate action.
2. No; it concerns the effect of repeating the operation.
3. No; it is a data format.
4. Not necessarily; tool behavior and dependencies matter.

## All chapter entries (24)

- [API endpoint](entries/api-endpoint.md)
- [API rate limiting](entries/rate-limiting.md)
- [API request](entries/api-request.md)
- [API response](entries/api-response.md)
- [application programming interface](entries/api.md)
- [automation inventory](entries/inventory.md)
- [automation pipeline](entries/pipeline.md)
- [automation secret](entries/secret.md)
- [automation validation](entries/automation-validation.md)
- [configuration drift](entries/configuration-drift.md)
- [data schema](entries/schema.md)
- [desired state](entries/desired-state.md)
- [dry run](entries/dry-run.md)
- [HTTP method](entries/http-method.md)
- [HTTP status code](entries/http-status-code.md)
- [idempotence](entries/idempotence.md)
- [JavaScript Object Notation](entries/json.md)
- [network automation](entries/network-automation.md)
- [REST API](entries/rest-api.md)
- [source of truth](entries/source-of-truth.md)
- [source repository](entries/repository.md)
- [version control](entries/version-control.md)
- [version-control commit](entries/commit.md)
- [YAML](entries/yaml.md)

## Sources

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/info/rfc9110/)
- [RFC 8259: The JSON Data Interchange Format](https://www.rfc-editor.org/info/rfc8259/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
