# Chapter 05 · Models, Frames & Packets

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../../part-01/chapter-04-site-surveys-and-installation/README.md) · [Next chapter](../chapter-06-ethernet-and-switching/README.md)

## Visual pages

1. [The OSI reference model](01-layers.md): seven layers and their functions.
2. [Frames, packets, and encapsulation](02-encapsulation.md): headers, payloads, and protocol units.

## Say it at work

> The physical link is up, but the application request is failing.

> Please capture the packet and check the source and destination addresses.

> Does the path MTU allow the packet to be transmitted without fragmentation?

## Quick review

1. Is encapsulation the same as encryption?
2. Is an Ethernet frame the same object as the IP packet it carries?
3. What is a payload relative to?
4. Do IPv6 routers fragment packets in transit?

**Answers:** 1. No. 2. No; the frame can carry an IP packet. 3. A particular protocol layer. 4. No.

## All chapter entries (24)

- [application layer](entries/application-layer.md)
- [data link layer](entries/data-link-layer.md)
- [datagram](entries/datagram.md)
- [decapsulation](entries/decapsulation.md)
- [encapsulation](entries/encapsulation.md)
- [frame](entries/frame.md)
- [IP fragmentation](entries/fragmentation.md)
- [IP reassembly](entries/reassembly.md)
- [maximum transmission unit](entries/maximum-transmission-unit.md)
- [network layer](entries/network-layer.md)
- [network protocol](entries/protocol.md)
- [OSI model](entries/osi-model.md)
- [packet](entries/packet.md)
- [payload](entries/payload.md)
- [physical layer](entries/physical-layer.md)
- [presentation layer](entries/presentation-layer.md)
- [protocol data unit](entries/protocol-data-unit.md)
- [protocol header](entries/header.md)
- [protocol stack](entries/protocol-stack.md)
- [protocol trailer](entries/trailer.md)
- [session layer](entries/session-layer.md)
- [TCP segment](entries/segment.md)
- [TCP/IP model](entries/tcp-ip-model.md)
- [transport layer](entries/transport-layer.md)

## Sources

- [RFC 791: Internet Protocol](https://www.rfc-editor.org/info/rfc791/)
- [RFC 8200: Internet Protocol, Version 6](https://www.rfc-editor.org/info/rfc8200/)
- [RFC 9293: Transmission Control Protocol](https://www.rfc-editor.org/info/rfc9293/)
- [RFC 768: User Datagram Protocol](https://www.rfc-editor.org/info/rfc768/)

Original text and conceptual diagrams; independent technical and language review remain pending. RFCs may have subsequent updates.
