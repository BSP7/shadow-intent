from scapy.all import Ether, IP

# Simple dictionary mapping MAC to IP addresses for local identification
_mac_to_ip = {}

# Mock OUI database
KNOWN_OUIS = {
    "b8:27:eb": {"vendor": "Raspberry Pi Foundation", "type": "IoT Device"},
    "00:1a:11": {"vendor": "Google", "type": "IoT Device"}, 
    "28:c6:3f": {"vendor": "Amazon", "type": "IoT Device"},
    "cc:50:e3": {"vendor": "Tuya Smart", "type": "IoT Device"},
    "a4:83:e7": {"vendor": "Apple", "type": "Mobile"},
    "00:50:56": {"vendor": "VMware", "type": "Laptop/PC"},
    "dc:a6:32": {"vendor": "Dell", "type": "Laptop/PC"}
}

def get_device_id(packet):
    """Identify IoT devices using MAC address instead of only IP."""
    if packet.haslayer(Ether) and packet.haslayer(IP):
        mac = packet[Ether].src
        ip = packet[IP].src
        _mac_to_ip[mac] = ip
        return mac
    return None

def identify_device(mac: str):
    """
    Lookup vendor and type from MAC address prefix.
    """
    if not mac:
        return {"vendor": "Unknown Vendor", "type": "Unknown"}

    prefix = mac[:8].lower()
    return KNOWN_OUIS.get(prefix, {"vendor": "Unknown Vendor", "type": "Unknown"})

def track_device_activity(packet):
    """Tracks network activity based on MAC address identity."""
    mac = get_device_id(packet)
    if mac:
        identity = identify_device(mac)
        return {
            "device_id": mac, 
            "ip": _mac_to_ip.get(mac), 
            "vendor": identity["vendor"],
            "type": identity["type"]
        }  
    return None
