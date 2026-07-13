# Overview
As the cornerstone of network engineering, Routing and Switching (R&S) forms the core foundation of all technical knowledge. Although I have repeatedly attempted to relearn and systematically document the entire R&S curriculum, my progress has invariably been disrupted by unforeseen circumstances, a lack of consistency, or insufficient depth that led to overlooking crucial fundamentals. Consequently, I have decided to relaunch this project, striving to make this definitive series my final and most comprehensive set of R&S notes.

As the opening chapter of this entire series, this section sets the baseline tone for what follows. Consequently, I will use this overview note to map out the comprehensive learning framework and methodology that will guide our journey.


At their core, all Routing and Switching protocols serve the identical purpose: controlling and forwarding data traffic. These protocols share a high degree of commonality and are deeply intertwined by their underlying logic. Consequently, every protocol within the R&S domain can be systematically analyzed through the following conceptual model.
```text
+---------------------------------------------------+
|   1. Control Plane                                |
|   (Protocol Packets, State Machines, Neighbor     |
|    Establishment, Algorithms, DB Synchronization) |
+---------------------------------------------------+
 * Context: The Brain / Cognitive Processing
 * Logic: How do they "communicate" and reach a consensus?
                        |
                        v Programmed / Mapped to
+-------------------------------------------------+
|   2. Data / Forwarding Plane                    |
|   (CAM Tables, FIB Prefix Trees, LFIBs,         |
|    Encap / Decapsulation)                       |
+-------------------------------------------------+
 * Context: The Muscle / Hardware Execution
 * Logic: How are packets routed on the hardware ASICs?
                        |
                        v Secured / Bound with
+-------------------------------------------------+
|   3. Infrastructure & Maintenance               |
|   (Sub-second BFD, Non-Stop Forwarding/GR,      |
|    Dot1x/MAB Access Control)                    |
+-------------------------------------------------+
 * Context: The Immune System
 * Logic: How does the network fail-safe against 
          anomalies, flaps, or security threats?
```

Based on this conceptual model, I have compiled a concise overview of the most ubiquitous routing and switching protocols encountered in production environments:
## I. Layer 2 Switching & Topology Control Family
*   **STP / RSTP / MSTP (Spanning Tree Protocol Suite)**
    *   ├─ **Control Plane**: Exchanges BPDUs, elects Root Bridge/Designated Port/Root Port, computes loop-free topology, and transitions port states.
    *   ├─ **Data Plane**: Performs line-rate unicast forwarding, Unknown Unicast/Broadcast flooding, or port blocking based on the CAM Table (MAC Address Table).
    *   └─ **Maintenance**: BPDU Guard, Root Guard, Loop Guard, and TC-BPDU flood protection mechanisms.
*   **LACP / Eth-Trunk (Link Aggregation Control Protocol)**
    *   ├─ **Control Plane**: Exchanges LACPDU messages, negotiates system priority and interface weights, and monitors member link states.
    *   └─ **Data Plane**: Binds multiple physical interfaces into a logical pipe, executing hardware-level load balancing via Hash algorithms (Source-Destination IP/MAC).
*   **VLAN / QinQ (Virtual LAN & Double Tagging)**
    *   ├─ **Control Plane**: Dynamically synchronizes VLAN databases via GVRP/VTP (historical/specific use cases); defines broadcast domain boundaries.
    *   └─ **Data Plane**: Inserts/strips 802.1Q tags (or QinQ outer tags) in the Ethernet frame, achieving Layer 2 logical isolation at the ASIC level.

## II. Layer 3 Unicast Routing Family
*   **OSPF (Open Shortest Path First)**
    *   ├─ **Control Plane**: Hello packets establish adjacency ➔ 8-step state machine transitions ➔ Floods Type 1/2/3/4/5/7 LSAs to sync LSDB ➔ Runs SPF algorithm to calculate the shortest path tree.
    *   ├─ **Data Plane**: Downloads optimal paths to RIB ➔ Converts RIB to FIB (Prefix Tree) for hardware-level Longest Prefix Matching (LPM) forwarding.
    *   └─ **Maintenance**: Millisecond-level triggering with BFD, Graceful Restart (GR) for Non-Stop Forwarding, and Area-based loop prevention rules (Backbone Area dependency).
*   **EIGRP (Enhanced Interior Gateway Routing Protocol)**
    *   ├─ **Control Plane**: Hello packets build neighbors ➔ Exchanges Update packets to sync Topology Table ➔ Computes Metric based on 5 K-values ➔ Runs DUAL algorithm to verify Feasible Condition (FC).
    *   ├─ **Data Plane**: Calculates Successor (Primary) and Feasible Successor (Backup) to populate FIB; supports Equal/Unequal (Variance) Cost Load Balancing.
    *   └─ **Maintenance**: RTP (Reliable Transport Protocol) sequence number/acknowledgment mechanism; SIA (Stuck-In-Active) timers coupled with Query/Reply loop mitigation.
*   **BGP-4 (Border Gateway Protocol)**
    *   ├─ **Control Plane**: Establishes neighbors over TCP 179 ➔ 6-step state machine transitions ➔ Advertises NLRI ➔ Colors routes via Path Attributes (LP, MED, AS_Path, Community) ➔ Runs 13-step best-path selection algorithm.
    *   ├─ **Data Plane**: Installs best paths to FIB; resolves next-hop reachability in multi-tier topologies via Recursive Lookup pointing to actual physical egress.
    *   └─ **Maintenance**: Route Reflector (RR) / Confederation loop prevention, BGP Peer Tracking, BFD triggering, and strict path filtering via Prefix-List/Route-Policy.
*   **Static Route & PBR (Policy-Based Routing)**
    *   ├─ **Control Plane**: Manually injects Next-Hop IP/Egress Interface, or defines hard-coded matching logic via PBR route-maps (Match Clauses / Set Clauses).
    *   └─ **Data Plane**: **PBR completely bypasses the standard FIB routing table**, directly overriding the hardware forwarding plane to force a specific Next-Hop IP, Egress Interface, or Type of Service (ToS/DSCP).

## III. Multicast Family
*   **IGMP v1/v2/v3 & MLD (Internet Group Management Protocol)**
    *   ├─ **Control Plane**: Host-to-Router signaling (Query / Report / Leave) used to dynamically maintain multicast group membership tables on the local segment.
    *   └─ **Data Plane**: Works alongside Layer 2 **IGMP Snooping**, intercepting multicast flooding to precisely forward multicast frames only to ports with active receivers.
*   **PIM-SM / PIM-SSM (Protocol Independent Multicast - Sparse / Source Specific)**
    *   ├─ **Control Plane**: Neighbor discovery ➔ RPF (Reverse Path Forwarding) check for loop prevention ➔ Builds Shared Tree (RPT) and Source Tree (SPT) ➔ RP (Rendezvous Point) election via BSR / Auto-RP.
    *   └─ **Data Plane**: Generates `(*, G)` or `(S, G)` multicast routing entries mapped to the hardware **OIF List (Outgoing Interface List)** to perform efficient wire-speed packet replication.
*   **MSDP (Multicast Source Discovery Protocol)**
    *   ├─ **Control Plane**: Inter-domain PIM communication, utilizing Source Active (SA) messages to share and synchronize multicast source information across different RP domains.
    *   └─ **Data Plane**: Pure control-plane protocol; does not forward actual multicast payload. Solves source visibility issues between distinct administrative domains.

## IV. WAN, VPN & Tunneling Family
*   **MPLS / LDP (Multiprotocol Label Switching / Label Distribution Protocol)**
    *   ├─ **Control Plane**: LDP binds local labels to IGP prefixes derived from the unicast routing table, advertising them to peers to build the LIB (Label Information Base).
    *   └─ **Data Plane**: **Bypasses IP routing completely**; looks up the **LFIB (Label Forwarding Information Base)** to execute hardware-level label operations: Push, Swap, or Pop.
*   **MP-BGP / MPLS VPN (Multi-Protocol BGP VPN)**
    *   ├─ **Control Plane**: Isolates paths via VRFs ➔ Prepends RD to convert overlapping IPv4 addresses into globally unique VPNv4 routes ➔ Controls route leaking via RTs ➔ MP-BGP exchanges routes and assigns **inner VPN/private labels**.
    *   └─ **Data Plane**: PE routers execute **Dual-Layer Label Stacking**: the outer label steers traffic across the public LDP transit network, while the inner label is popped at the egress PE to forward raw data into the target VRF.
*   **VXLAN & BGP EVPN (Virtual Extensible LAN)**
    *   ├─ **Control Plane**: BGP EVPN (Type 2/3/5 routes) distributes Layer 2 MAC reachability, Layer 3 host IP routing, and VTEP peer bindings to dynamically discover tunnel endpoints.
    *   └─ **Data Plane**: Takes raw Layer 2 Ethernet frames at the VTEP ASIC and encapsulates them into an outer **UDP packet (Destination Port 4789)**, tunneling Layer 2 traffic over a Layer 3 IP fabric.
*   **GRE / DMVPN (Dynamic Multipoint VPN)**
    *   ├─ **Control Plane**: Utilizes NHRP (Next Hop Resolution Protocol) to dynamically map dynamic public NBMA IP addresses to fixed private Tunnel IP addresses for Spoke-to-Spoke/Hub-to-Spoke environments.
    *   └─ **Data Plane**: Provides generic point-to-point or point-to-multipoint encapsulation, wrapping original IP packets inside a GRE header and a new public IP header (Protocol 47) for public transit.

## V. Infrastructure, High Availability & Safeguards
*   **BFD (Bidirectional Forwarding Detection)**
    *   ├─ **Control Plane**: A highly lightweight, protocol-independent path monitoring mechanism. Periodically transmits ultra-fast Hello probes (at millisecond intervals).
    *   └─ **Triggering**: Carries no user payload; upon detecting a link loss, it **instantly triggers** the control plane of registered protocols (OSPF, BGP, Static Route, VRRP) to initiate sub-second convergence.
*   **802.1X & MAB (Network Admission Control)**
    *   ├─ **Control Plane**: Drives identity/digital certificate validation via EAPOL state machines and RADIUS/ISE infrastructure. If a client lacks an 802.1X supplicant, it fails over to MAC Authentication Bypass (MAB).
    *   └─ **Triggering**: Prior to successful control-plane validation, hardware ACLs strictly block the port in the data plane (permitting only authentication traffic). Upon success, it dynamically pushes authorized VLANs/ACLs to open the port.