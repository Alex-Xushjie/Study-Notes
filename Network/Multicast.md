# Preface
Multicast is a very important tech for fintech firm and it determines the upper limit of income.\
This article contains my notes from learning "**IP-Multicast-Volume-II**", and I hope it can be helpful to you. Of course, if you have any questions, you can refer to the original book or contact the author directly.

# Introduction
For studying multicast, we need to follow below three steps:
1) Understand "What is multicast for?"
2) Foucs on three key concepts: RPF; (S,G) vs (*,G); RP
3) Studying multicast in real environment

## 1. What is Multicast for?
When we need to send some "message", we usually choice unicast. But if we want to send same mesaage to many recivers at the same time, we'll waste many resource of network.\
As we all know, IP was created as 'best effort' service. There are no guarantees of optimal forwarding—or even that packets will make it to the final destination at all.\
So the answer is that we use multicast to **send message to many recivers at the same time.**

## 2. Three key concepts:
1) RPF - Reverse Path Forwarding
Unicast cares about where you're going but multicast cares about where you came from.\
RPF is a mechanism to check the multicast traffic. Making sure it comes from the right direction.\
It relies on unicast RIB, so that's why IGP/BGP is very important of multicast environment.

## 3. (S,G) vs (*,G)





# Chapter 1 - Interdomain Routing and Internet Multicast
**Three pillars of interdomain multicast :**
1) The control plane for source identification;
2) The control plane for receiver identification;
3) The downstream control plane.

## Introduciton of Interdomain Multicast
Generally, we can't make sure that the source of multicast and the recivers of multicast are in the same domain, so we need to config or run a multicast between different domain(Internet).\

### Multicast domain
PIM is the IETF standard for Any-Source Multicast(ASM) and Source-Specific Multicast(SSM) in IP network. It isn't just a multicast routing protocol because it cares about building loop-free forwarding topologies or trees more rather than route sharing policy.

IGP routers will share RIB with each other, PIM routers also have the similar capability to dynamically share information about multicast trees.

