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
        <SSID>HomeNetwork</SSID>
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

def scan_networks(policies):
    print("Starting scan for wireless networks...")
    ssid=''
    network_type=''
    auth_type=''
    bssid=''
    result = subprocess.run(['sudo', 'iwlist', 'wlp0s20f3', 'scan'], capture_output=True, text=True)
    networks= result.stdout
    ssids = list(filter(None,re.findall(r'ESSID:"(.*?)"', networks)))

    print(ssids)
    print(policies)
    for ssid in ssids:
        # Check SSID Validity
        if ssid not in policies['valid_ssids']:
            print(f'Voilation: SSID {ssid} is not allowed. Detected BSSID {bssid}')
        else:
            print(f'Voilation: SSID {ssid} is ALLOWED. Detected BSSID {bssid}')

def main():
    policies = read_security_policies("security_policies.xml")
    scan_networks(policies)

if __name__ == "__main__":
    main()