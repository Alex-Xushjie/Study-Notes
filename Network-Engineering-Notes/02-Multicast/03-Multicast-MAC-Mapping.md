---
status: en-draft
title: IPv4 Multicast to Ethernet MAC Mapping
chapter: 03
tags:
  - Multicast
  - Ethernet
  - MAC Address
  - IPv4
  - Address Planning
---

# 03 - IPv4 Multicast to Ethernet MAC Mapping

## 1. Chapter Objectives

This chapter focuses exclusively on **how IPv4 multicast addresses map to Ethernet multicast MAC addresses**, including:

- Why an IPv4 multicast packet needs a Layer 2 multicast destination address;
- The purpose of the `01:00:5E` prefix;
- How the lower 23 bits of an IPv4 group map to a MAC address;
- Why `32:1` address overlap occurs;
- The possible Layer 2 forwarding impact of MAC address overlap;
- How to identify and avoid unnecessary overlap during address planning;
- How to verify mapping results with packet captures and scripts.

The complete IGMP Snooping forwarding-table process, platform hardware-entry structures, and multicast routing are covered in later chapters.

---

## 2. Why Multicast IP Addresses Must Map to Multicast MAC Addresses

In an Ethernet network, switches perform Layer 2 forwarding according to the Ethernet frame's destination MAC address.

At Layer 3, an IPv4 multicast packet uses a group address such as:

```text
239.1.1.1
```

When transmitted over Ethernet, the packet must also be encapsulated with a corresponding Layer 2 destination address:

```text
Destination IP:  239.1.1.1
Destination MAC: 01:00:5e:01:01:01
```

This is not the unicast MAC address of any receiver, nor is it dynamically resolved through ARP.

It is calculated directly from the IPv4 multicast group:

> IPv4 multicast addresses are deterministically mapped to Ethernet multicast MAC addresses.

The source therefore does not need to know each receiver's unicast MAC address.

---

## 3. Ethernet Multicast MAC Address

### 3.1 Individual/Group Bit

The least significant bit of the first octet of an Ethernet MAC address is called the:

```text
I/G Bit
```

Where:

```text
0 = Individual Address
1 = Group Address
```

For example:

```text
00:50:56:aa:bb:cc
```

The first octet is `00`, so the I/G bit is 0 and this is a unicast MAC address.

In contrast:

```text
01:00:5e:01:01:01
```

The first octet is `01`, so the I/G bit is 1 and this is a multicast MAC address.

---

### 3.2 Fixed MAC Prefix Used by IPv4 Multicast

IPv4 multicast over Ethernet uses the fixed prefix:

```text
01:00:5E
```

The complete mapping range is:

```text
01:00:5E:00:00:00
-
01:00:5E:7F:FF:FF
```

The most significant bit of the fourth octet is fixed at 0:

```text
01:00:5E:0xxxxxxx:xxxxxxxx:xxxxxxxx
```

Only the final 23 bits are therefore available to carry IPv4 group information.

---

## 4. Bit Structure of an IPv4 Multicast Address

IPv4 multicast uses:

```text
224.0.0.0/4
```

The four most significant bits are fixed at:

```text
1110
```

The remaining 28 bits represent different multicast groups:

```text
┌──────────┬────────────────────────────┐
│   1110   │       Group ID: 28 bits    │
└──────────┴────────────────────────────┘
  4 bits             28 bits
```

However, the Ethernet mapping space can retain only 23 bits:

```text
IPv4 Group ID: 28 bits
Ethernet Mapping: 23 bits
```

Five bits of information cannot be retained during mapping.

---

## 5. IPv4-to-MAC Mapping Rules

### 5.1 Bit-Level Mapping

The lower 23 bits of an IPv4 multicast address are copied into the lower 23 bits of the Ethernet multicast MAC address.

```text
IPv4 Multicast Address:

┌──────────┬─────────────┬────────────────────────┐
│   1110   │ 5 bits lost │   Lowest 23 bits kept  │
└──────────┴─────────────┴────────────────────────┘
  4 bits       5 bits              23 bits


Ethernet Multicast MAC:

┌────────────────────────┬───┬────────────────────────┐
│       01:00:5E          │ 0 │   Lowest 23 IP bits    │
└────────────────────────┴───┴────────────────────────┘
         24 bits          1 bit         23 bits
```

The five discarded bits are:

- The lower four bits of the first IPv4 octet, excluding the fixed `1110` prefix;
- The most significant bit of the second IPv4 octet.

The retained bits are:

- The lower seven bits of the second IPv4 octet;
- All eight bits of the third octet;
- All eight bits of the fourth octet.

---

### 5.2 Quick Calculation Formula

Assume the IPv4 group is:

```text
A.B.C.D
```

The corresponding multicast MAC is:

```text
01:00:5E:(B & 0x7F):C:D
```

Where:

```text
B & 0x7F
```

means retaining only the lower seven bits of the second octet.

---

### 5.3 Mental Decimal Calculation

Calculation procedure:

1. Fix the first three MAC octets:

   ```text
   01:00:5E
   ```

2. Process the second octet of the group IP:

   - If it is less than 128, leave it unchanged;
   - If it is greater than or equal to 128, subtract 128.

3. Convert the processed second octet and the original third and fourth octets to hexadecimal.

---

## 6. Mapping Examples

### 6.1 `239.1.1.1`

Second octet:

```text
1 & 127 = 1
```

Convert to hexadecimal:

```text
1  = 01
1  = 01
1  = 01
```

Final result:

```text
239.1.1.1
→ 01:00:5E:01:01:01
```

---

### 6.2 `232.100.1.10`

Second octet:

```text
100 & 127 = 100
```

Convert to hexadecimal:

```text
100 = 64
1   = 01
10  = 0A
```

Final result:

```text
232.100.1.10
→ 01:00:5E:64:01:0A
```

---

### 6.3 `239.192.10.20`

Second octet:

```text
192 - 128 = 64
```

Convert to hexadecimal:

```text
64 = 40
10 = 0A
20 = 14
```

Final result:

```text
239.192.10.20
→ 01:00:5E:40:0A:14
```

---

### 6.4 `224.129.1.1`

Second octet:

```text
129 - 128 = 1
```

Final result:

```text
224.129.1.1
→ 01:00:5E:01:01:01
```

This is the same result as for `239.1.1.1`.

---

## 7. Why 32:1 Address Overlap Occurs

### 7.1 Mathematical Reason

An IPv4 multicast group has 28 variable bits, while Ethernet mapping retains only 23:

```text
28 - 23 = 5
```

Losing five bits means:

```text
2^5 = 32
```

different IPv4 multicast groups can map to the same Ethernet multicast MAC address. This is called:

```text
32:1 Multicast MAC Address Overlap
```

---

### 7.2 Overlap Condition

Two IPv4 multicast groups map to the same MAC address if and only if their lower 23 bits are identical:

```text
IP1 & 0x7FFFFF == IP2 & 0x7FFFFF
```

In dotted-decimal terms, all of the following must be true:

1. The lower seven bits of the second octet are identical;
2. The third octets are identical;
3. The fourth octets are identical.

Changes to the first IPv4 octet do not affect the mapping. If second octets differ by 128, their lower seven bits are also identical.

---

### 7.3 Typical Overlap Example

The following addresses all map to:

```text
01:00:5E:01:01:01
```

Examples include:

```text
224.1.1.1
224.129.1.1
225.1.1.1
225.129.1.1
232.1.1.1
232.129.1.1
239.1.1.1
239.129.1.1
```

The complete set of combinations includes:

- 16 possible first-octet values, from `224` through `239`;
- Two possible values for the most significant bit of the second octet, 0 or 1;
- Identical third and fourth octets.

Therefore:

```text
16 × 2 = 32
```

---

## 8. What Does MAC Overlap Mean?

### 8.1 It Does Not Mean That Two Groups Are Identical at Layer 3

For example:

```text
232.1.1.1
239.1.1.1
```

These are completely different IPv4 multicast groups. Applications and operating systems can still distinguish them by destination IP.

MAC overlap does not cause:

- The IPv4 group address to change;
- The UDP port to change;
- Two IP groups to become one application-layer channel;
- Packet contents to be merged.

---

### 8.2 It Can Cause Layer 2 Over-Forwarding

If a switch platform and forwarding implementation use only:

```text
VLAN + Destination Multicast MAC
```

as the Layer 2 multicast forwarding key, IP groups that map to the same MAC may share the same outgoing ports.

For example:

```text
Receiver A joins 232.1.1.1
Receiver B joins 239.1.1.1
```

Both map to:

```text
01:00:5E:01:01:01
```

With MAC-only forwarding, the switch may create:

```text
VLAN 10
01:00:5E:01:01:01
→ Port A, Port B
```

As a result:

- Traffic for `232.1.1.1` may reach both Port A and Port B;
- Traffic for `239.1.1.1` may also reach both Port A and Port B.

This is called:

```text
Layer 2 Multicast Over-Forwarding
```

---

### 8.3 A Host Can Still Drop Unrelated Traffic at Layer 3

Even if an unrelated multicast frame reaches a host NIC, the operating system still checks:

- Destination IP;
- Group membership;
- UDP port;
- Socket binding.

If the application did not join the corresponding group, the packet is normally not delivered to it.

However, over-forwarding can still consume:

- Interface bandwidth;
- NIC processing resources;
- Host receive queues;
- Kernel packet processing;
- Packet-capture and monitoring resources.

In high-throughput, low-latency environments, these additional packets can still have an impact.

---

## 9. Forwarding Implementations on Different Platforms

Switches do not all forward multicast traffic in exactly the same way.

Possible forwarding keys include:

```text
VLAN + Multicast MAC
```

or:

```text
VLAN + Group IP
```

or the more precise:

```text
VLAN + Source IP + Group IP
```

The practical effect of the same MAC overlap can therefore vary by platform.

### Incorrect Conclusion to Avoid

The fact that this command displays a group IP:

```text
show ip igmp snooping groups
```

does not prove that the ASIC uses IP-based forwarding.

The CLI may display group information maintained by the control plane while the actual hardware table uses a different key.

Base the determination on:

- The specific device model;
- ASIC architecture;
- Software version;
- Vendor documentation;
- Hardware forwarding-table inspection;
- Actual packet-capture testing.

For this chapter, remember:

> Multicast MAC overlap is inherent in the IPv4-to-Ethernet mapping. Its forwarding impact depends on the switch implementation.

---

## 10. Address-Planning Principles

### 10.1 Core Validation Rule

When planning multiple multicast groups in the same VLAN or bridge domain, check whether they have identical lower 23 bits.

The equivalent test is to compare all three of these components:

```text
Second octet & 0x7F
Third octet
Fourth octet
```

---

### 10.2 Changing the First Octet Cannot Prevent a Collision

These addresses:

```text
232.1.1.1
239.1.1.1
```

have different first octets but map to the same result:

```text
01:00:5E:01:01:01
```

Therefore:

> Changing only the first octet never changes the mapped Ethernet multicast MAC.

---

### 10.3 Second Octets That Differ by 128 Collide

For example:

```text
239.1.1.1
239.129.1.1
```

Because:

```text
1 & 0x7F   = 1
129 & 0x7F = 1
```

the mapping results are identical.

There is no universal rule requiring a fixed planning increment for the second octet. The only reliable principle is:

> Compare the complete lowest 23 bits.

---

### 10.4 Fix the First Two Octets and Vary the Final Two

Within a local planning range, one of the simplest approaches is to fix the first two octets and assign unique values in the third and fourth octets.

For example:

```text
239.192.1.1
239.192.1.2
239.192.2.1
239.192.2.2
```

The corresponding MAC addresses are:

```text
01:00:5E:40:01:01
01:00:5E:40:01:02
01:00:5E:40:02:01
01:00:5E:40:02:02
```

They do not overlap.

---

### 10.5 Recheck When Planning Across Address Ranges

These groups may belong to different address blocks:

```text
232.100.1.1
239.100.1.1
```

but they map to the same MAC:

```text
01:00:5E:64:01:01
```

Do not plan SSM, ASM, or departmental addresses separately without performing a global lower-23-bit check.

---

### 10.6 Must All Overlap Be Completely Avoided?

Not every network must eliminate all MAC overlap globally.

Whether proactive avoidance is necessary depends on:

- Whether groups share the same VLAN or bridge domain;
- Whether the switch forwards based on MAC addresses;
- Traffic volume;
- Receiver sensitivity to additional traffic;
- Whether resource exhaustion causes platform degradation or flooding;
- The presence of mixed-vendor devices;
- Whether low-latency services strictly minimize unrelated packets.

Overlap may have no noticeable effect in an ordinary low-volume environment.

In high-bandwidth or low-latency environments, avoid unnecessary overlap within the same Layer 2 domain whenever possible.

---

## 11. Python Mapping Tool

The following Python 3 script converts an IPv4 multicast group into an Ethernet multicast MAC address:

```python
#!/usr/bin/env python3

import ipaddress


def multicast_ip_to_mac(group_ip: str) -> str:
    ip = ipaddress.IPv4Address(group_ip)

    if not ip.is_multicast:
        raise ValueError(f"{group_ip} is not an IPv4 multicast address")

    low_23_bits = int(ip) & 0x7FFFFF
    mac_value = 0x01005E000000 | low_23_bits

    mac_hex = f"{mac_value:012x}"

    return ":".join(
        mac_hex[index:index + 2]
        for index in range(0, 12, 2)
    )


if __name__ == "__main__":
    groups = [
        "232.1.1.1",
        "239.1.1.1",
        "239.129.1.1",
        "239.192.10.20",
    ]

    for group in groups:
        print(f"{group:15} -> {multicast_ip_to_mac(group)}")
```

Expected output:

```text
232.1.1.1       -> 01:00:5e:01:01:01
239.1.1.1       -> 01:00:5e:01:01:01
239.129.1.1     -> 01:00:5e:01:01:01
239.192.10.20   -> 01:00:5e:40:0a:14
```

---

## 12. MAC Overlap Audit Script

The following script checks multiple groups for MAC overlap:

```python
#!/usr/bin/env python3

import ipaddress
import re
from collections import defaultdict
from typing import Dict, List


def multicast_ip_to_mac(group_ip: str) -> str:
    """
    Convert an IPv4 multicast address to its Ethernet multicast MAC.
    """

    ip = ipaddress.IPv4Address(group_ip)

    if not ip.is_multicast:
        raise ValueError(
            "{} is not an IPv4 multicast address".format(group_ip)
        )

    low_23_bits = int(ip) & 0x7FFFFF
    mac_value = 0x01005E000000 | low_23_bits
    mac_hex = "{:012x}".format(mac_value)

    return ":".join(
        mac_hex[index:index + 2]
        for index in range(0, 12, 2)
    )


def find_collisions(groups: List[str]) -> Dict[str, List[str]]:
    """
    Find multicast IP addresses that map to the same Ethernet MAC.
    """

    mapping = defaultdict(list)

    for group in groups:
        mac = multicast_ip_to_mac(group)
        mapping[mac].append(group)

    return {
        mac: addresses
        for mac, addresses in mapping.items()
        if len(addresses) > 1
    }


def collect_multicast_groups() -> List[str]:
    """
    Collect multicast addresses interactively.

    Users may enter one or multiple addresses per line.
    Spaces and commas are both accepted as separators.
    Submit an empty line to start the audit.
    """

    groups = []

    print("IPv4 Multicast MAC Collision Audit")
    print("----------------------------------")
    print("Enter one or more multicast IP addresses.")
    print("Separate multiple addresses with spaces or commas.")
    print("Press Enter on an empty line to start the audit.\n")

    while True:
        try:
            user_input = input("Multicast IP: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            break

        addresses = re.split(r"[\s,]+", user_input)

        for address in addresses:
            if not address:
                continue

            try:
                ip = ipaddress.IPv4Address(address)

                if not ip.is_multicast:
                    print(
                        "  Skipped: {} is not an IPv4 multicast address.".format(
                            address
                        )
                    )
                    continue

                normalized_address = str(ip)

                if normalized_address in groups:
                    print(
                        "  Skipped: {} has already been entered.".format(
                            normalized_address
                        )
                    )
                    continue

                groups.append(normalized_address)

            except ipaddress.AddressValueError:
                print(
                    "  Skipped: {} is not a valid IPv4 address.".format(
                        address
                    )
                )

    return groups


def print_audit_report(groups: List[str]) -> None:
    """
    Print all mappings and detected MAC collisions.
    """

    if not groups:
        print("\nNo valid multicast addresses were entered.")
        return

    print("\nMulticast IP to MAC Mapping")
    print("-" * 45)
    print("{:<18} {}".format("Multicast IP", "Ethernet MAC"))
    print("{:<18} {}".format("-" * 15, "-" * 17))

    for group in groups:
        print(
            "{:<18} {}".format(
                group,
                multicast_ip_to_mac(group)
            )
        )

    collisions = find_collisions(groups)

    if not collisions:
        print("\nAudit result: No multicast MAC collisions were found.")
        return

    print("\nAudit result: Multicast MAC collisions were found.")

    for mac, addresses in collisions.items():
        print("\n{}".format(mac))

        for address in addresses:
            print("  - {}".format(address))


def main() -> None:
    groups = collect_multicast_groups()
    print_audit_report(groups)


if __name__ == "__main__":
    main()
```

This script is suitable for auditing addresses before deploying a new group.

---

## 13. Packet-Capture Verification

### 13.1 Wireshark

Assume the group is:

```text
239.1.1.1
```

Use this display filter:

```text
ip.dst == 239.1.1.1
```

Verify the Ethernet destination with:

```text
eth.dst == 01:00:5e:01:01:01
```

Check both fields simultaneously:

```text
ip.dst == 239.1.1.1 and eth.dst == 01:00:5e:01:01:01
```

---

### 13.2 Checking Other Groups Under the Same MAC Address

To check whether a MAC address carries another destination IP:

```text
eth.dst == 01:00:5e:01:01:01 and ip.dst != 239.1.1.1
```

This filter shows only that other multicast packets mapped to the same MAC appeared at the capture point.

By itself, it does not prove the switch's hardware forwarding key or IGMP Snooping implementation.

---

### 13.3 tcpdump

Display the Ethernet header:

```bash
tcpdump -i eth0 -e -nn ether dst 01:00:5e:01:01:01
```

Capture only a specific destination IP:

```bash
tcpdump -i eth0 -e -nn dst host 239.1.1.1
```

Check for packets under the same MAC that do not belong to the expected group:

```bash
tcpdump -i eth0 -e -nn \
  'ether dst 01:00:5e:01:01:01 and not dst host 239.1.1.1'
```

---

## 14. Common Misconceptions

### 14.1 “One Multicast IP Corresponds to One Unique MAC Address”

Incorrect.

The IPv4 multicast-to-Ethernet MAC mapping ratio is:

```text
32 IPv4 Groups : 1 Ethernet Multicast MAC
```

---

### 14.2 “The Same MAC Means That Two Groups Are the Same”

Incorrect.

The same MAC means only that their lower 23 bits are identical. Their destination IP addresses remain different.

---

### 14.3 “Changing the Group's First Octet Prevents a Collision”

Incorrect.

The first IPv4 octet is not part of the lower-23-bit mapping.

---

### 14.4 “The Second Octet Must Use a Planning Increment Greater Than 128”

Incorrect.

Only the most significant bit of the second octet is discarded, so values that differ by 128 actually collide.

There is no fixed-increment rule; compare the complete lower 23 bits.

---

### 14.5 “If the Snooping Table Displays an IP, Hardware Must Use IP-Based Forwarding”

Incorrect.

The control-plane CLI display format does not directly prove the ASIC's actual forwarding key.

---

### 14.6 “MAC Overlap Always Causes an Application to Receive Incorrect Data”

Not necessarily.

Even when a packet reaches a host interface, the operating system and application still check group membership, destination IP, and UDP port.

The actual effect depends on switch forwarding behavior, host processing, and traffic volume.

---

## 15. Chapter Summary

1. IPv4 multicast packets require a multicast destination MAC on Ethernet networks.
2. IPv4 multicast over Ethernet uses the fixed `01:00:5E` prefix.
3. The most significant bit of the mapped MAC's fourth octet is fixed at 0.
4. The Ethernet mapping space retains only the lower 23 bits of an IPv4 group.
5. An IPv4 multicast address has a 28-bit group ID, so five bits are lost during mapping.
6. Because `2^5 = 32`, up to 32 different groups map to the same MAC address.
7. The quick calculation formula is `01:00:5E:(B & 0x7F):C:D`.
8. Changing the first IPv4 octet does not change the mapped MAC address.
9. MAC overlap occurs when second octets differ by 128 and the final two octets are identical.
10. MAC overlap does not make two IPv4 groups the same group at Layer 3.
11. On a MAC-based Layer 2 multicast-forwarding platform, overlap may cause over-forwarding.
12. A host can still drop unrelated traffic based on destination IP and membership.
13. Different switches may use the MAC address, group IP, or `(S,G)` as the forwarding key.
14. A CLI displaying a group IP does not directly prove that the ASIC uses IP-based forwarding.
15. Address planning should compare the complete lower 23 bits rather than rely on a fixed increment.
16. Avoid unnecessary MAC overlap in high-bandwidth or low-latency Layer 2 domains.
17. Python scripts can automate mapping calculations and address-conflict audits.
18. A later chapter covers specific IGMP Snooping state and forwarding mechanisms.

---

## 16. References

- RFC 1112 — Host Extensions for IP Multicasting
- RFC 4541 — Considerations for Internet Group Management Protocol Snooping Switches
- IANA — Ethernet Numbers
- IANA — IPv4 Multicast Address Space
