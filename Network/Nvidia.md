本文主要用于记录配置信息，拓扑参考Nvidia官方仿真平台实验《CL5.14.0 - EVPN Symmetric Routing Best Practices》

=========Leaf_01===========
---------基本配置------------
nv set system hostname Leaf01
nv set interface lo ip address 10.10.10.1/32
nv set interface swp1-3,9-10,11-14 link state up
nv set bridge domain br_default
nv set bridge domain br_default vlan 10,20,30

---------M-LAG配置------------
nv set interface peerlink bond member swp9-10
nv set interface peerlink bridge domain br_default
nv set mlag peer-ip linklocal
nv set mlag init-delay 10
nv set mlag mac-address 44:38:39:BE:EF:BB
nv set mlag backup 10.10.10.2
nv set interface bond1 bond member swp1
nv set interface bond1 bridge domain br_default access 10
nv set interface bond1 bond mlag id 1
nv set interface bond1 lacp-bypass on
nv set interface bond1 link mtu 9216
nv set interface bond2 bond member swp2
nv set interface bond2 bridge domain br_default access 20
nv set interface bond2 bond mlag id 2
nv set interface bond2 lacp-bypass on
nv set interface bond2 link mtu 9216
nv set interface bond3 bond member swp3
nv set interface bond3 bridge domain br_default access 10
nv set interface bond3 bond mlag id 3
nv set interface bond3 lacp-bypass on
nv set interface bond3 link mtu 9216

