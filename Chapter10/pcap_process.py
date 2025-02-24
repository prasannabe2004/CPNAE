from scapy.all import *


def find_packets_to_ip(pacp_file, target_ip):
    packets = rndcap(pacp_file)
    packet_count = 0
    for packet in packets:
        if IP in packet and packet[IP].dst == target_ip:
            #print  (packet.summary())
            packet_count += 1
    print(f"Packets destined to {target_ip} is {packet_count}")


pcap_file = "pcatired_traffic.pcap"

find_packets_to_ip(pcap_file, "8.8.8.8")

