from scapy.all import IP, TCP, sr1
from ipaddress import IPv4Network

# Scan www.example.com IP. 80 will be open
ip_addresses=["23.216.155.42"]

port_range=range(1,101)

for ip in ip_addresses:
    print(f"Scanning {ip}:")
    for port in port_range:
        packet=IP(dst=ip) / TCP(dport=port, flags="S")
        response=sr1(packet, timeout=1, verbose=0)
        if response is None:
            print(f"Port {port}: No response")
        elif response.haslayer(TCP):
            if response.getlayer(TCP).flags == 0x12:
                print(f" Port {port}: Open")
                sr1(IP(dst=ip)/TCP(dport=port, flags="R"), timeout=1, verbose=0)
            elif response.getlayer(TCP).flags == 0x14:
                print(f" Port {port}: Closed")
        else:
            print(f" Port {port}: No response")

