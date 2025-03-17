import sys
from scapy.all import rdpcap, Dot11

def analyze_pcap(pcap_file):
    packets = rdpcap(pcap_file)  # Load the pcap file
    wifi_detected = False
    
    for packet in packets:
        if packet.haslayer(Dot11):  # Check for 802.11 (WiFi) packets
            wifi_detected = True
            break  # No need to continue once WiFi is detected
    
    if wifi_detected:
        print("WiFi packets detected in the pcap file.")
    else:
        print("No WiFi packets found in the pcap file.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Need input file path")
        exit()
    pcap_file = sys.argv[1]  # Change this to your actual pcap file
    analyze_pcap(pcap_file)
