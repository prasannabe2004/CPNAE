import psutil
import os
import scapy
import time
from scapy.all import sniff, IP, TCP, UDP
from prettytable import PrettyTable
from collections import defaultdict

def get_network_adapters():
    adapters = psutil.net_if_addrs()
    return adapters

def select_network_adapter(adapters):
    for i, adapter in enumerate(adapters):
        print(f"{i+1}:{adapter}")
    while True:
        try:
            a_i = int(input("Select the adapter (enter the number): "))
            if 1 <= a_i <= len(adapters):
                return list(adapters.keys())[a_i - 1]
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid Input")

def monitor_traffic(adaptor, duration):
    traffic_data = {
        'total_vol': 0,
        'protocols' : defaultdict(int),
        'connections' : defaultdict(int)
    }

    def process_packet(packet):
        traffic_data['total_vol'] += len(packet)
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
            if TCP in packet:
                traffic_data['protocols']['TCP'] += 1
            elif UDP in packet:
                traffic_data['protocols']['UDP'] += 1
            else:
                traffic_data['protocols']['Other'] += 1

            if (src,dst) not in traffic_data['connections']:
                traffic_data['connections'][(src,dst)] = 0
            traffic_data['connections'][(src,dst)] += len(packet)

    print(f"Monitoring traffic on adapter {adaptor} for {duration} minutes...")
    end_time = time.time() + (duration * 60)
    while time.time() < end_time:
        sniff(iface=adaptor, prn=process_packet, timeout=60, store=False)
        
    return traffic_data

def pretty_print_traffic_data(traffic_data):
    tot_vol_mbps = (traffic_data['total_vol']*8) / 1_000_000
    tot_col_kbps = (traffic_data['total_vol']*8) / 1_000
    print(f'Total Neterok Traffic Volume: {tot_vol_mbps:.2f} Mbps ({tot_col_kbps:.2f} Kbps)')

    proto_table = PrettyTable(["Protocol" , "Volume (bytes)"])
    for proto, vol in traffic_data['protocols'].items():
        proto_table.add_row([proto, vol])
    print('\vTraffic Types Detected')
    print(proto_table)

    conn_table = PrettyTable(["Source" , "Destination", "Volume (bytes)"])
    for (src, dst), vol in traffic_data['connections'].items():
        conn_table.add_row([src, dst, vol])
    print('\vTraffic Souces and Destinations')
    print(conn_table)

def main():
    print(f'OS is {os.name}')
    adapters = get_network_adapters()
    adapter = select_network_adapter(adapters)
    duration_min = int(input("Enter the duration to monitor the traffic in mins: "))
    traffic_data = monitor_traffic(adapter, duration_min)
    pretty_print_traffic_data(traffic_data)
if __name__ == "__main__":
    main()