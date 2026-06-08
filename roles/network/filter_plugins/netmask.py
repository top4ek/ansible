class FilterModule(object):
    def filters(self):
        return {
            "netmask_prefix": netmask_prefix,
            "dns_nameservers": dns_nameservers,
        }


def netmask_prefix(netmask):
    """Convert a dotted-decimal netmask to a CIDR prefix length."""
    parts = str(netmask).split(".")
    if len(parts) != 4:
        raise ValueError(f"Invalid netmask: {netmask}")

    try:
        octets = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError(f"Invalid netmask: {netmask}") from exc

    if any(octet < 0 or octet > 255 for octet in octets):
        raise ValueError(f"Invalid netmask: {netmask}")

    binary = "".join(f"{octet:08b}" for octet in octets)
    if "01" in binary:
        raise ValueError(f"Invalid netmask: {netmask}")

    return binary.count("1")


def dns_nameservers(nameservers, separator=" "):
    if isinstance(nameservers, list):
        return separator.join(str(ns) for ns in nameservers)
    return str(nameservers).replace(" ", separator).replace(",", separator)
