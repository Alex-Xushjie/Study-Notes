# Chapter 17 · Firewalls, ACLs & Segmentation

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../../part-04/chapter-16-cloud-and-hybrid-connectivity/README.md) · [Next chapter](../chapter-18-identity-aaa-and-secure-access/README.md)

## Chapter topics

1. [Traffic Through a Firewall](01-firewall.md)
2. [Policy and Segmentation](02-segmentation.md)

## Say it at work

> Please confirm the original and translated source and destination addresses.

> Which security rule matches the connection, and what action does it take?

> The rule permits the session, but the application still times out.

> Check the return path and firewall session state.

## Quick review

1. Does a permit rule guarantee application reachability?
2. Does NAT replace firewall policy?
3. Are source and destination NAT the same?
4. Do all firewalls use the same implicit default?

**Answers**

1. No; routing, endpoint availability, and authentication also matter.
2. No; translation and access control are different functions.
3. No; they modify different address fields.
4. No; verify the platform and configuration.

## All chapter entries (24)

- [access control entry](entries/acl-entry.md)
- [access control list](entries/access-control-list.md)
- [application control](entries/application-control.md)
- [deny traffic](entries/deny.md)
- [destination address](entries/destination-address.md)
- [destination network address translation](entries/destination-nat.md)
- [firewall](entries/firewall.md)
- [firewall log](entries/firewall-log.md)
- [firewall network object](entries/network-object.md)
- [firewall policy](entries/firewall-policy.md)
- [firewall rule](entries/firewall-rule.md)
- [firewall service object](entries/service-object.md)
- [firewall session](entries/firewall-session.md)
- [implicit deny](entries/implicit-deny.md)
- [least privilege](entries/least-privilege.md)
- [microsegmentation](entries/microsegmentation.md)
- [network address translation](entries/network-address-translation.md)
- [permit traffic](entries/permit.md)
- [security policy hit](entries/security-policy-hit.md)
- [security segmentation](entries/security-segmentation.md)
- [security zone](entries/security-zone.md)
- [source address](entries/source-address.md)
- [source network address translation](entries/source-nat.md)
- [stateful inspection](entries/stateful-inspection.md)

## Sources

- [NIST: Guidelines on Firewalls and Firewall Policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
- [RFC 3022: Traditional IP Network Address Translator](https://www.rfc-editor.org/info/rfc3022/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
