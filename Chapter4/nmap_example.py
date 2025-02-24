import nmap

nm = nmap.PortScanner()

subnet = "23.216.155.42/30"
ports="1-10"

nm.scan(hosts=subnet,arguments=f'p {ports}')
print("Hello")
for host in nm.all_hosts():
    print(f'Scanning {host}')
    for proto in nm[host].all_protocols():
        print(f'Protocol: {proto}')
        ports = nm[host][proto].keys()
        for port in ports:
            state = nm[host][proto][port]['state']
            print(f'Port {port}: {state}')