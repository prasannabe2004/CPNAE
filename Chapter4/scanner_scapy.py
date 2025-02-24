from scapy.all import IP, TCP, sr1
from ipaddress import IPv4Network

subnet="10.211.55.0/24"

port_range=range(1,101)

for ip in IPv4Network(subnet):
    print(f"Scanning {ip}:")
    for port in port_range:
        packet=IP(dst=str(ip))/TCP(dport=port, flags="S")
        response=sr1(packet, timeout=1, verbose=0)
        if response is None:
            print(f"port {port}: No response")
        elif response.haslayer(TCP):
            if response.getlayer(TCP).flags == 0x12:
                print(f" Port {port}: Open")
                sr1(IP(dst=str(ip))/TCP(dport=port, flags="R"), timeout=1, verbose=0)
            elif response.getlayer(TCP).flags == 0x14:
                print(f" Port {port}: Closed")
        else:
            print(f" Port {port}: No response")

