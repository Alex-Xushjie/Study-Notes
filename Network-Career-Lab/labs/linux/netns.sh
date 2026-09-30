#!/usr/bin/env bash
# Dedicated Linux lab VM only. Run from project root with sudo bash.
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
command -v ip >/dev/null
names=(ncl-c ncl-r ncl-s)
exists() { ip netns list | awk '{print $1}' | grep -Fxq "$1"; }
case "${1:-}" in
  up)
    for n in "${names[@]}"; do
      if exists "$n"; then echo "$n already exists; inspect before cleanup." >&2; exit 1; fi
    done
    for n in "${names[@]}"; do ip netns add "$n"; ip -n "$n" link set lo up; done
    ip -n ncl-c link add c0 type veth peer name r0 netns ncl-r
    ip -n ncl-r link add r1 type veth peer name s0 netns ncl-s
    ip -n ncl-c addr add 10.10.0.2/24 dev c0
    ip -n ncl-r addr add 10.10.0.1/24 dev r0
    ip -n ncl-r addr add 10.20.0.1/24 dev r1
    ip -n ncl-s addr add 10.20.0.2/24 dev s0
    ip -n ncl-c link set c0 up
    ip -n ncl-r link set r0 up
    ip -n ncl-r link set r1 up
    ip -n ncl-s link set s0 up
    ip netns exec ncl-r sysctl -qw net.ipv4.ip_forward=1
    ip -n ncl-c route add default via 10.10.0.1
    ip -n ncl-s route add default via 10.20.0.1
    echo 'Created ncl-c <-> ncl-r <-> ncl-s. Test: sudo ip netns exec ncl-c ping -c 3 10.20.0.2'
    ;;
  down)
    for n in "${names[@]}"; do
      if exists "$n" && [[ -n "$(ip netns pids "$n")" ]]; then
        echo "Stop lab processes in $n before cleanup." >&2; exit 1
      fi
    done
    for n in "${names[@]}"; do if exists "$n"; then ip netns del "$n"; fi; done
    ;;
  *) echo 'Usage: sudo bash netns.sh up|down' >&2; exit 2 ;;
esac
