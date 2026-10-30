# Chapter 07 · IP Addressing & Subnetting

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-06-ethernet-and-switching/README.md) · [Next chapter](../chapter-08-transport-and-application-services/README.md)

## Visual pages

1. [IPv4 address and prefix](01-ipv4.md): octets, prefixes, host addresses and masks.
2. [IPv6 address and prefix](02-ipv6.md): prefix notation, address scope and examples.

## Say it at work

> Which subnet and prefix length should we use for the management interface?

> Please confirm that the address is not already assigned.

> The host can reach the default gateway, but not the remote subnet.

> Update the IPAM record after the allocation is approved.

## Quick review

1. How many bits are in IPv4 and IPv6 addresses?
2. Is a VLAN the same thing as a subnet?
3. Does IPv6 use broadcast addresses?
4. Does a globally scoped address guarantee Internet reachability?

**Answers:** 1. IPv4 has 32 bits; IPv6 has 128 bits. 2. No; VLANs are Layer 2 segments and subnets are IP addressing constructs. 3. No. 4. No; routing and policy also matter.

## All chapter entries (24)

- [address aggregation](entries/address-aggregation.md)
- [address allocation](entries/address-allocation.md)
- [Classless Inter-Domain Routing](entries/cidr.md)
- [default gateway](entries/default-gateway.md)
- [host address](entries/host-address.md)
- [IP address](entries/ip-address.md)
- [IP address conflict](entries/address-conflict.md)
- [IP address management](entries/ip-address-management.md)
- [IPv4 address](entries/ipv4-address.md)
- [IPv4 directed broadcast address](entries/broadcast-address.md)
- [IPv4 network address](entries/network-address.md)
- [IPv6 address](entries/ipv6-address.md)
- [IPv6 global unicast address](entries/ipv6-global-unicast.md)
- [IPv6 unique local address](entries/ipv6-unique-local.md)
- [link-local address](entries/link-local-address.md)
- [loopback address](entries/loopback-address.md)
- [network prefix](entries/network-prefix.md)
- [octet](entries/octet.md)
- [prefix length](entries/prefix-length.md)
- [private IPv4 address](entries/private-ipv4-address.md)
- [public IP address](entries/public-ip-address.md)
- [subnet](entries/subnet.md)
- [subnet mask](entries/subnet-mask.md)
- [subnetting](entries/subnetting.md)

## Sources

- [RFC 791: Internet Protocol](https://www.rfc-editor.org/info/rfc791/)
- [RFC 1918: Address Allocation for Private Internets](https://www.rfc-editor.org/info/rfc1918/)
- [RFC 4291: IP Version 6 Addressing Architecture](https://www.rfc-editor.org/info/rfc4291/)
- [RFC 4193: Unique Local IPv6 Unicast Addresses](https://www.rfc-editor.org/info/rfc4193/)
- [RFC 5737: IPv4 Address Blocks Reserved for Documentation](https://www.rfc-editor.org/info/rfc5737/)

Original text and conceptual diagrams; independent technical and language review remain pending. RFCs may have subsequent updates.
