import psutil
import os
import scapy
import time
import scapy.all as scapy
from prettytable import PrettyTable

def get_network_adapters():
    adapters = psutil.net_if_addrs()
    return adapters

def select_network_adapter(adapters):
    for i, adapter in enumerate(adapters):
        print(f"{i+1}:{adapter}")
    while True:
        try:
            a_i = int("Select the adpater (enter the number): ")
            if 1 <= a_i <= len(adapters):
                return list(adapters.keys())[a_i - 1]
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid Input")

def monitor_traffic(adaptor, duration):
    traffic_data = {
        'total_vol': 0,
        'protocols' : {},
        'connections' : {}
    }

    def process_packet(packet):
        traffic_data['total_vol'] += len(packet)

        if packet.haslayer(scapy.IP):
            src = packet[scapy.IP].src
            dst = packet[scapy.IP].dst
            protocol = packet(scapy.IP).proto

            if protocol not in traffic_data['protocols']:
                traffic_data['protocols'] = 0
            traffic_data['protocols'][protocol] += len(packet)

            if (src,dst) not in traffic_data['connections']:
                traffic_data['connections'][(src,dst)] = 0
            traffic_data['connections'][(src,dst)] += len(packet)

        print(f"Monitoring trafiic on adaptor {adaptor} for {duration} minutes...")
        end_time = time.time() + (duration * 60)
        while time.time() < end_time:
            scapy.sniff(iface=adaptor, prn=process_packet, timeout=60, store=False)
        
        return traffic_data

def pretty_print_traffic_data(traffic_data):
    tot_vol_mbps = (traffic_data['tot_vol']*8) / 1_000_000
    tot_col_kbps = (traffic_data['tol_vol']*8) / 1_000
    print(f'Total Neterok Traffic Volume: {tot_vol_mbps:.2f} Mbps ({tot_col_kbps:.2f} Kbps)')

    proto_table = PrettyTable(["Protocol" , "Volume (bytes)"])
    for proto, vol in traffic_data['protocols'].items():
        proto_table.add_row([proto, vol])
    print('\vTraffic Types Detected')
    print(proto_table)

    conn_table = PrettyTable(["Source" , "Destination" "Volume (bytes)"])
    for (src, dst), vol in traffic_data['connections'].items():
        conn_table.add_row([src, dst, vol])
    print('\vTraffic Souces and Destinations')
    print(conn_table)

def main():
    if os.name != 'nt':
        print('This script is designed to work on windows')
        return
    adapters = get_network_adapters()
    adapter = select_network_adaptor()
if __name__ == "__main__":
    main()