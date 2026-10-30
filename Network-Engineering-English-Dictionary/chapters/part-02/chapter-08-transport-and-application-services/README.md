# Chapter 08 · Transport & Application Services

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-07-ip-addressing-and-subnetting/README.md) · [Next chapter](../../part-03/chapter-09-routing-fundamentals-and-static-routes/README.md)

## Visual pages

1. [A TCP connection](01-tcp.md): the handshake, ports and retransmission.
2. [A DNS query](02-dns.md): clients, resolvers, authoritative servers and records.

## Say it at work

> Is the service listening on TCP or UDP, and which destination port does it use?

> The TCP handshake completes, but the application request times out.

> Which DNS resolver did the client use for this query?

> Check the DHCP lease and relay configuration for the affected subnet.

## Quick review

1. Does an established TCP connection prove that the application works?
2. What is the difference between a recursive resolver and an authoritative server?
3. Which DNS record types carry IPv4 and IPv6 addresses?
4. What is a DHCP relay used for?

**Answers:** 1. No. 2. A recursive resolver obtains answers for a client; an authoritative server supplies zone data. 3. A and AAAA, respectively. 4. To forward DHCP messages between clients and servers across networks.

## All chapter entries (28)

- [authoritative name server](entries/authoritative-name-server.md)
- [destination port](entries/destination-port.md)
- [DHCP lease](entries/dhcp-lease.md)
- [DHCP relay](entries/dhcp-relay.md)
- [DHCP server](entries/dhcp-server.md)
- [DNS A record](entries/dns-a-record.md)
- [DNS AAAA record](entries/dns-aaaa-record.md)
- [DNS client](entries/dns-client.md)
- [DNS query](entries/dns-query.md)
- [DNS resource record](entries/dns-record.md)
- [DNS time to live](entries/dns-ttl.md)
- [Dynamic Host Configuration Protocol](entries/dhcp.md)
- [ephemeral port](entries/ephemeral-port.md)
- [HTTPS](entries/https.md)
- [Hypertext Transfer Protocol](entries/http.md)
- [Network Time Protocol](entries/ntp.md)
- [recursive resolver](entries/recursive-resolver.md)
- [source port](entries/source-port.md)
- [TCP acknowledgment](entries/acknowledgment.md)
- [TCP connection](entries/tcp-connection.md)
- [TCP retransmission](entries/retransmission.md)
- [TCP SYN](entries/syn.md)
- [TCP SYN-ACK](entries/syn-ack.md)
- [TCP three-way handshake](entries/three-way-handshake.md)
- [Transmission Control Protocol](entries/tcp.md)
- [transport port number](entries/port-number.md)
- [User Datagram Protocol](entries/udp.md)
- [Domain Name System](entries/dns.md)

## Sources

- [RFC 9293: Transmission Control Protocol](https://www.rfc-editor.org/info/rfc9293/)
- [RFC 768: User Datagram Protocol](https://www.rfc-editor.org/info/rfc768/)
- [RFC 1034: Domain Names — Concepts and Facilities](https://www.rfc-editor.org/info/rfc1034/)
- [RFC 2131: Dynamic Host Configuration Protocol](https://www.rfc-editor.org/info/rfc2131/)
- [RFC 5905: Network Time Protocol Version 4](https://www.rfc-editor.org/info/rfc5905/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. RFCs may have subsequent updates.
