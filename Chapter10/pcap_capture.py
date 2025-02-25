from scapy.all import *
import time

def packet_callback(packet):
    print(packet.summary())
    return packet

def capture_pcap(iface, dur, file):
    print(f'Starting packet capture on interface {iface} for {dur} seconds....')
    packets = sniff(iface=iface, prn=packet_callback, timeout=dur)
    wrpcap(file, packets)
    print(f'Packet capture completed. Saved to {file}')


if __name__ == "__main__":
    interface = "cscotun0"
    duration = 60
    output_file = "captured_traffic.pcap"
    capture_pcap(interface, duration, output_file)
