# Sources

[Home](README.md)

Definitions and examples are original teaching text. These references are starting points for technical review; they do not establish that every entry has been independently reviewed. Project-specific drawings are examples, not universal design requirements.

<a id="s1"></a>
## S1 · Telecommunications room and racks

[Maine Office of Information Technology: Wiring Specifications](https://www.maine.gov/oit/sites/maine.gov.oit/files/inline-files/WiringSpecs.pdf) shows an example MDF/IDF layout and relevant equipment terminology.

<a id="s2"></a>
## S2 · Rack units

One rack unit is 1.75 inches, equivalent to 44.45 mm. An accessible primary source for the mounting specification remains to be added before publication.

<a id="s3"></a>
## S3 · Fiber patch panels

[Cisco: High-Density Fiber Patch Panel and Cable Portfolio](https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/high-density-fiber-patch-mpo-ds.html) provides examples of fiber patch-panel products and terminology.

<a id="s4"></a>
## S4 · DNS

[RFC 1034: Domain Names — Concepts and Facilities](https://www.rfc-editor.org/info/rfc1034/) describes foundational DNS concepts. Check subsequent updates when reviewing the entry.

<a id="s5"></a>
## S5 · BGP

[RFC 4271: A Border Gateway Protocol 4](https://www.rfc-editor.org/info/rfc4271/) describes foundational BGP behavior. Check subsequent updates when reviewing the entry.

## Illustration

`assets/network-room.png` is an original AI-generated illustration created for this draft. Prompt: a clean, text-free isometric telecommunications room with an open rack, enclosed cabinet, patch panels, switches, cable management, rack power distribution unit, UPS, and overhead cable tray. The illustration is conceptual and equipment details should be verified against actual products and site drawings.

The labeled scene and six detail cards are original vector overlays and crops made from the generated illustration for this project. Labels identify recognizable components, and all views are illustrative.


## Chapter 01: facility and airflow references

[Cisco Nexus N93180YC-FX3: Airflow requirements](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180yc-fx3/cisco-n93180yc-fx3-hardware-installation-guide/site-prep/airflow-requirements.html) illustrates model-specific airflow directions; do not assume these match other equipment.

[Maine Office of Information Technology: Wiring Specifications](https://www.maine.gov/oit/sites/maine.gov.oit/files/inline-files/WiringSpecs.pdf) contains sample telecommunications room and rack terminology; it is a project reference rather than a universal requirement.

The room, rack, and power-equipment pictures are AI-generated illustrative renderings. The cooling diagram is an original editable SVG illustration created for this chapter. All illustrations simplify real environments and are not installation plans.


## Visual revision: wireless and leaf-spine

The Chapter 14 wireless picture is an original AI-generated illustrative scene made with the built-in image generator. Prompt: a laptop client, visible radio waves, a wireless access point, and a cabled Ethernet switch on a clear light background. It is not a product photograph or installation instruction.

The Chapter 15 leaf-spine picture is an original vector topology diagram: each of the three leaves connects to each of two spines, and one server connects to a leaf. It shows logical physical-link relationships, not an exact wiring plan.


## Chapter 01: realistic cooling scene

The cold-aisle scene is an AI-generated, photorealistic illustration, not a photograph of a real facility. The numbered leaders and blue airflow arrows were added for teaching. It illustrates one possible raised-floor arrangement; the rear of the cabinet, hot aisle and raised-floor plenum are not visible. Equipment appearance is illustrative and model-specific details require verification.

[Cisco UCS Site Preparation Guide](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/hw/site-prep-guide/ucs_siteprep_chapter_010.html) describes front-to-back airflow for its equipment and cold-aisle alignment. [Cisco Nexus airflow requirements](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180yc-fx3/cisco-n93180yc-fx3-hardware-installation-guide/site-prep/airflow-requirements.html) illustrates how airflow direction depends on the particular equipment configuration.


## Chapter 05: OSI and encapsulation example

The send-side diagram is an original conceptual illustration. HTTP over TCP, IPv4, and Ethernet is used as one example, and OSI layers 5 and 6 are shown as functional concepts rather than mandatory independent protocol headers.

[RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html) describes HTTP/1.1 message syntax. [RFC 9293: TCP](https://www.rfc-editor.org/rfc/rfc9293.html) specifies TCP headers and its byte-stream service. [RFC 791: Internet Protocol](https://www.rfc-editor.org/rfc/rfc791.html) specifies IPv4. [RFC 894: IP over Ethernet](https://www.rfc-editor.org/rfc/rfc894.html) describes IPv4 encapsulation and Ethernet padding. [Cisco OSI Reference Model](https://www.cisco.com/c/en/us/td/docs/ios/sw_upgrades/interlink/r2_0/api_con/acoview.pdf) describes the conceptual layers. The diagram is a teaching simplification and is pending independent review.


The Chapter 05 frame illustration is an original, not-to-scale diagram of one Ethernet II / IPv4 / TCP example. It uses the same protocol references listed above; Ethernet padding and VLAN tags are intentionally omitted. The Ethernet FCS is outside the IP packet.


## Chapter 06: access and trunk example

The VLAN illustration is an original logical diagram: two VLANs cross one trunk between two switches. [Cisco access and trunk interface documentation](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/infra/interface-characteristics/interface-characteristics-configuration-guide.html) describes access ports, 802.1Q trunks and native VLAN behavior. Exact tagging and forwarding depend on platform and configuration.


The Chapter 06 Ethernet frame diagram is an original teaching illustration of an untagged Ethernet II frame. [RFC 894](https://www.rfc-editor.org/rfc/rfc894.html) specifies IPv4 over Ethernet and padding; [Cisco frame-format documentation](https://www.cisco.com/c/en/us/support/docs/lan-switching/8021q/17056-741-4.html) describes the FCS and VLAN tag placement.


## Chapter 07: address diagrams

The IPv4 and IPv6 diagrams use documentation address ranges described in [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737.html) and [RFC 3849](https://www.rfc-editor.org/rfc/rfc3849.html). IPv6 notation is described in [RFC 4291](https://www.rfc-editor.org/rfc/rfc4291.html) and canonical text recommendations in [RFC 5952](https://www.rfc-editor.org/rfc/rfc5952.html). Prefix splits are examples, not universal fixed boundaries.


## Chapter 08: TCP and DNS diagrams

Original teaching diagrams; the handshake example follows [RFC 9293 section 3.5](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.5). The DNS example follows concepts in [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.html) and [RFC 9499](https://www.rfc-editor.org/rfc/rfc9499.html).


## Chapter 09: forwarding and prefix selection

These original IPv4 forwarding diagrams use [RFC 1812](https://www.rfc-editor.org/rfc/rfc1812.html) for longest matching prefix, TTL and outgoing-link encapsulation. Examples assume an ordinary unicast forwarding context; policy routing, tunnels, NAT and alternate forwarding contexts require additional consideration.


## Chapter 10: OSPF neighbors and SPF

The original OSPFv2 teaching diagrams illustrate a point-to-point adjacency and an intra-area SPF example. [RFC 2328](https://www.rfc-editor.org/rfc/rfc2328.html) describes neighbor discovery, synchronization, LSAs and shortest-path calculation. Neighbor adjacency behavior differs by network type.


## Work-scenario pilot: interface flapping

The diagram, times, dialogue and counter values are invented for language practice. [Cisco: Troubleshoot Port Flaps on Catalyst 9000 Switches](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9500-series-switches/218397-troubleshoot-port-flaps-on-catalyst-9000.html) illustrates correlation of link-state logs and interface counters on specific platforms. An error counter increase does not by itself identify the cause of a flap. Independent technical and language review is pending.
