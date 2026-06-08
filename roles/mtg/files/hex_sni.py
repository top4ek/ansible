#!/usr/bin/env python3
import argparse
import binascii
import sys

def extract_domain_from_hex(hex_str: str) -> str:
    raw = binascii.unhexlify(hex_str.strip().lower())
    start = len(raw)
    while start > 0 and 0x20 <= raw[start - 1] < 0x7F:
        start -= 1
    return raw[start:].decode("ascii")


def main() -> int:
    p = argparse.ArgumentParser(description="Extract SNI domain from hex-encoded secret.")
    p.add_argument("hex", help="hex string (e.g. eed0...636f6d)")
    args = p.parse_args()

    try:
        domain = extract_domain_from_hex(args.hex)
    except (binascii.Error, ValueError) as e:
        print(f"invalid hex: {e}", file=sys.stderr)
        return 2

    if not domain:
        print("no domain found", file=sys.stderr)
        return 3

    print(domain)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
