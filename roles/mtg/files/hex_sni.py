#!/usr/bin/env python3
import argparse
import binascii
import re
import sys


DOMAIN_RE = re.compile(r"([a-z0-9-]+(?:\.[a-z0-9-]+)+)")


def extract_domain_from_hex(hex_str: str) -> str:
    raw = binascii.unhexlify(hex_str.strip())
    text = raw.decode("utf-8", errors="ignore")
    matches = DOMAIN_RE.findall(text)
    return matches[-1] if matches else ""


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
