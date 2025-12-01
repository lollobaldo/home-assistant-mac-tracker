import logging
import re
import subprocess

_LOGGER = logging.getLogger(__name__)

def scan_network(options="-l -g -t1 -q"):
    """Run arp-scan and return list of (mac, ip)."""
    try:
        scandata = subprocess.getoutput(f"arp-scan {options}")
    except Exception as e:
        _LOGGER.error("Failed to run arp-scan: %s", e)
        return []

    results = []
    for line in scandata.splitlines():
        match = re.findall(r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+([0-9a-fA-F:]{17})", line)
        if match:
            ip, mac = match[0]
            results.append((mac.lower(), ip))
    return results

def is_mac_online(mac: str, scan_results):
    """Check if the MAC is in scan results."""
    mac = mac.lower()
    for m, ip in scan_results:
        if m == mac:
            return True, ip
    return False, None
