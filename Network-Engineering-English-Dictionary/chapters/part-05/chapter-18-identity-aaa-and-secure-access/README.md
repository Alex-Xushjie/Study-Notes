# Chapter 18 · Identity, AAA & Secure Access

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-17-firewalls-acls-and-segmentation/README.md) · [Next chapter](../chapter-19-high-availability-and-failover/README.md)

## Chapter topics

1. [Authentication and Authorization](01-aaa.md)
2. [Controlling Access](02-access.md)

## Say it at work

> Does the authentication fail, or does authorization deny the requested action?

> Please provide the timestamp and device name, without sharing credentials.

> Check the RADIUS or TACACS+ server status and relevant logs.

> Verify that the out-of-band path is reachable independently.

## Quick review

1. Does successful authentication imply unrestricted authorization?
2. Is a management port automatically an independent out-of-band path?
3. What is the difference between a supplicant and an authenticator?
4. Is an SSH host key the same as a user authentication key?

**Answers**

1. No; authorization is a separate policy decision.
2. No; the full path and dependencies must be checked.
3. The supplicant requests access; the authenticator controls the access port.
4. No; they serve different identity roles.

## All chapter entries (26)

- [802.1X authenticator](entries/authenticator.md)
- [802.1X supplicant](entries/supplicant.md)
- [AAA accounting](entries/accounting.md)
- [AAA server](entries/aaa-server.md)
- [authentication](entries/authentication.md)
- [authentication authorization and accounting](entries/aaa.md)
- [authentication fallback](entries/fallback-authentication.md)
- [authorization](entries/authorization.md)
- [certificate authority](entries/certificate-authority.md)
- [credentials](entries/credentials.md)
- [digital certificate](entries/certificate.md)
- [identity provider](entries/identity-provider.md)
- [IEEE 802.1X](entries/8021x.md)
- [management plane](entries/management-plane.md)
- [multi-factor authentication](entries/multifactor-authentication.md)
- [network device administration](entries/device-administration.md)
- [out-of-band management](entries/out-of-band-management.md)
- [password](entries/password.md)
- [privileged access](entries/privileged-access.md)
- [public key infrastructure](entries/public-key-infrastructure.md)
- [read-only access](entries/read-only-access.md)
- [Remote Authentication Dial-In User Service](entries/radius.md)
- [role-based access control](entries/role-based-access-control.md)
- [Secure Shell](entries/ssh.md)
- [SSH host key](entries/ssh-host-key.md)
- [TACACS+](entries/tacacs-plus.md)

## Sources

- [RFC 2865: RADIUS](https://www.rfc-editor.org/info/rfc2865/)
- [RFC 8907: TACACS+](https://www.rfc-editor.org/info/rfc8907/)
- [IEEE 802.1X Port-Based Network Access Control](https://1.ieee802.org/security/802-1x/)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
