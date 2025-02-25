import xml.etree.ElementTree as ET
import subprocess
import re

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
        <SSID>HomeNetwrok</SSID>
        <SSID>OfficeNetwork</SSID>
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
        "valid_ssids" : [ssid.text for ssid in root.find(".//ValidSSIDs/SSID")]
    }
    return policies

def scan_networks(policies):
    print("Starting scan for wireless networks...")
    result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], capture_output=True, text=True)
    networks= result.stdout.split("\n\n")

    for n in networks:
        ssid_match = re.search(r"SSID \d+ : (.+)", n)
        if ssid_match:
            ssid = ssid_match.group(1).strip()
            bssid_match = re.search(r"BSSID \d+ : (.+)", n)
            bssid = bssid_match.group(1).strip() if bssid_match else "Unknown"
            auth_match = re.search(r"Authenication : (.+)", n)
            auth_type = auth_match.group(1).strip() if auth_match else "Unknown"
            network_type_match = re.search(r"network type : (.+)", n)
            network_type = network_type_match.group().strip() if network_type_match else "Unknown"

        # Check SSID Validity
        if ssid not in policies['valid_ssids']:
            print("Voilation")
        if network_type == "Ad hoc" and not policies['ibss_allowed']:
            print("Voilation")
        if auth_type not in policies['authentication']:
            print("Voilation")

def main():
    policies = read_security_policies("security_policies.xml")
    scan_networks(policies)

if __name__ == "__main__":
    main()