import xml.etree.ElementTree as ET
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt

security_policies_xml = """
<SecurityPolicies>
    <Authentication>
        <AllowedTypes>
            <Type>WPA-Personal</Type>
            <Type>WPA3</Type>
        </AllowedTypes>
    </Authentication>
    <IBSSNetworks>
        <Allowed>False</Allowed>
    </IBSSNetworks>
    <ValidSSIDs>
        <SSID>Mobile</SSID>
        <SSID>Guest</SSID>
    </ValidSSIDs>
</SecurityPolicies>
"""

with open("security_policies.xml", "w") as file:
    file.write(security_policies_xml)

def read_security_policies(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    policies = {
        "authentication": [auth.text for auth in root.find(".//Authentication/AllowedTypes")],
        "ibss_allowed": root.find(".//IBSSNetworks/Allowed").text.lower() == 'true',
        "valid_ssids" : [ssid.text for ssid in root.find(".//ValidSSIDs")]
    }
    return policies

def get_authentication_type(akm_suite_selector):
    akm_mapping = {
        b'\x00\x0f\xac\x02': 'WPA2-Personal',
        b'\x00\x0f\xac\x01': 'WPA2-Enterprise',
        b'\x00\x0f\xac\x08': 'WPA3-SAE',
        b'\x00\x0f\xac\x09': 'WPA3-Enterprise'
    }
    return akm_mapping.get(akm_suite_selector, 'Unknown')

def get_encryption_type(packet):
    crypto = set()
    cap = packet[Dot11Beacon].cap
    privacy = cap.privacy
    rsn = None
    wpa = None

    for element in packet[Dot11Elt]:
        if element.ID == 48:  # RSN (Robust Security Network)
            rsn = element.info
        elif element.ID == 221 and element.info.startswith(b'\x00P\xf2\x01\x01\x00'):
            wpa = element.info

    if not privacy:
        return "Open"
    
    if rsn:
        # Parse RSN element
        rsn_info = int.from_bytes(rsn[2:4], byteorder='little')
        
        # Check for CCMP (AES) cipher
        if rsn_info & 0x04:
            crypto.add("CCMP")
        
        # Parse AKM suites
        akm_count = int.from_bytes(rsn[8:10], byteorder='little')
        akm_suites = rsn[10:10+akm_count*4]
        
        if b'\x00\x0f\xac\x02' in akm_suites:
            crypto.add("PSK")
        if b'\x00\x0f\xac\x01' in akm_suites:
            crypto.add("802.1X")
        if b'\x00\x0f\xac\x08' in akm_suites:
            crypto.add("SAE")  # WPA3

        if "SAE" in crypto:
            return "WPA3-Personal"
        elif "CCMP" in crypto and "PSK" in crypto:
            return "WPA2-Personal"
        elif "CCMP" in crypto and "802.1X" in crypto:
            return "WPA2-Enterprise"
    
    if wpa:
        # Check if it's WPA-Personal (PSK)
        if b'\x00P\xf2\x02' in wpa:
            return "WPA-Personal"
    
    if privacy:
        return "WEP"
    
    return "Unknown"

def scan_networks(policies):
    def packet_handler(packet):
        if packet.haslayer(Dot11):
            if packet.type == 0 and packet.subtype == 8:
                ssid = packet.info.decode()
                bssid = packet.addr2
                #capabilities = packet.sprintf("%Dot11Beacon.cap%")
                channel = None
                for element in packet[Dot11Elt]:
                    if element.ID == 3:  # Channel information element
                        if len(element.info) == 1:
                            channel = ord(element.info)
                        else:
                            channel = int.from_bytes(element.info, byteorder='little')
                        break
                if channel is None:
                    channel = "N/A"
                akm_suite = None
                print("CHANNEL=", channel)
                print("AUTH=" + get_encryption_type(packet))
                rsn = packet.getlayer(Dot11Elt, ID=48)
                if rsn:
                    akm_count = int.from_bytes(rsn.info[6:8], 'little')
                    akm_start = 8
                    for i in range(akm_count):
                        akm_suite_selector = rsn.info[akm_start:akm_start+4]
                        akm_suite = get_authentication_type(akm_suite_selector)
                        akm_start += 4
                        break
                if ssid:
                    print(f'SSID={ssid} BBSID={bssid} AUTH={akm_suite}')

    print('Starting scan for wireless networks....')
    sniff(iface="mon0", prn=packet_handler, store=0)


def main():
    policies = read_security_policies("security_policies.xml")
    scan_networks(policies)

if __name__ == "__main__":
    main()