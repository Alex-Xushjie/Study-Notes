"""Offline teaching example: explicit PASS / FAIL / UNKNOWN for BGP."""
import argparse
import csv
import json
from pathlib import Path


def evaluate(data):
    if not isinstance(data, dict) or not isinstance(data.get("devices"), list):
        raise ValueError("Input must contain a devices list")
    if not data["devices"]:
        raise ValueError("devices must not be empty")
    results = []
    seen = set()
    for device in data["devices"]:
        if not isinstance(device, dict):
            raise ValueError("Each device must be an object")
        name = device.get("name")
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError("Device names must be unique nonempty strings")
        seen.add(name)
        if device.get("error"):
            status, detail = "UNKNOWN", "Collection failed: " + str(device["error"])
        else:
            peers = device.get("bgp")
            if not isinstance(peers, list) or not peers:
                status, detail = "UNKNOWN", "Missing or empty BGP data"
            else:
                failed, invalid, peer_ids = [], False, set()
                for peer in peers:
                    if not isinstance(peer, dict):
                        invalid = True
                        continue
                    address, state = peer.get("peer"), peer.get("state")
                    if (not isinstance(address, str) or not address.strip()
                            or address in peer_ids or not isinstance(state, str)
                            or not state.strip()):
                        invalid = True
                        continue
                    peer_ids.add(address)
                    if state != "Established":
                        failed.append(address + ":" + state)
                if failed:
                    status, detail = "FAIL", "; ".join(failed)
                    if invalid:
                        detail += "; also contains incomplete/duplicate records"
                elif invalid:
                    status, detail = "UNKNOWN", "Incomplete or duplicate peer records"
                else:
                    status, detail = "PASS", "All observed BGP peers Established"
        results.append({"device": name, "check": "bgp", "status": status, "detail": detail})
    return results


def exit_code(results):
    statuses = {r["status"] for r in results}
    return 1 if "FAIL" in statuses else 2 if "UNKNOWN" in statuses else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    csv_path = args.output.with_suffix(".csv")
    if args.output.suffix.lower() != ".json":
        parser.error("--output must end with .json")
    if args.input.resolve() in {args.output.resolve(), csv_path.resolve()}:
        parser.error("Report must not overwrite input")
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        results = evaluate(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        with csv_path.open("w", newline="", encoding="utf-8") as out:
            writer = csv.DictWriter(out, fieldnames=["device", "check", "status", "detail"])
            writer.writeheader()
            writer.writerows(results)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Input/report error: {error}\n")
    for result in results:
        print(f'{result["device"]}: {result["status"]} - {result["detail"]}')
    return exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main())
