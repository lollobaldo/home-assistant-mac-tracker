from scapy.all import ARP, Ether, srp

def ping_mac(mac: str, timeout: int = 2) -> bool:
    """
    Sends a broadcast ARP request for the given MAC.
    Returns True if any device with the MAC responds.
    """
    broadcast = "ff:ff:ff:ff:ff:ff"
    arp_request = ARP(hwsrc=broadcast, hwdst=mac, pdst="255.255.255.255")
    ether = Ether(dst=broadcast) / arp_request

    answered, _ = srp(ether, timeout=timeout, verbose=False)

    return len(answered) > 0
