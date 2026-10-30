# Chapter 16 · Cloud & Hybrid Connectivity

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-15-data-center-networks/README.md) · [Next chapter](../../part-05/chapter-17-firewalls-acls-and-segmentation/README.md)

## Chapter topics

1. [Hybrid Connectivity](01-hybrid.md)
2. [Cloud Workload Connectivity](02-workload.md)

## Say it at work

> Which virtual network, subnet and region contain the affected workload?

> The tunnel is up; please check the propagated routes and security rules.

> Does the load balancer health check reach the expected port?

> Private connectivity does not by itself establish that the traffic is encrypted.

## Quick review

1. Are VPC and VNet guaranteed to have identical behavior?
2. Does an active cloud VPN guarantee application reachability?
3. Does private cloud connectivity automatically imply encryption?
4. Does a successful health check validate every application function?

**Answers**

1. No; terminology and capabilities vary by provider.
2. No; routes, policies and endpoints also matter.
3. No; encryption must be checked separately.
4. No; it validates the configured probe.

## All chapter entries (25)

- [availability zone](entries/availability-zone.md)
- [cloud DNS](entries/cloud-dns.md)
- [cloud egress traffic](entries/cloud-egress.md)
- [cloud load balancer](entries/cloud-load-balancer.md)
- [cloud network](entries/cloud-network.md)
- [cloud network ACL](entries/network-acl-cloud.md)
- [cloud network address translation](entries/cloud-nat.md)
- [cloud network interface](entries/cloud-network-interface.md)
- [cloud private endpoint](entries/private-endpoint.md)
- [cloud region](entries/cloud-region.md)
- [cloud route propagation](entries/cloud-route-propagation.md)
- [cloud route table](entries/cloud-route-table.md)
- [cloud security group](entries/cloud-security-group.md)
- [cloud subnet](entries/cloud-subnet.md)
- [cloud transit gateway](entries/transit-gateway.md)
- [cloud virtual machine](entries/cloud-virtual-machine.md)
- [cloud VPN](entries/cloud-vpn.md)
- [hybrid cloud](entries/hybrid-cloud.md)
- [load balancer health check](entries/health-check.md)
- [on-premises network](entries/on-premises-network.md)
- [private cloud connectivity](entries/private-cloud-connectivity.md)
- [transit attachment](entries/cloud-attachment.md)
- [virtual network](entries/virtual-network.md)
- [virtual network peering](entries/cloud-peering.md)
- [virtual private cloud](entries/virtual-private-cloud.md)

## Sources

- [AWS: VPC networking concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Microsoft Azure Virtual Network overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
- [Google Cloud VPC overview](https://cloud.google.com/vpc/docs/vpc)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
