from scapy.all import IP, TCP, UDP, DNS, DNSQR, send
import time
import random

# Abstract code examples for testing cybersecurity detection logic.
# These functions send small burst counts of local traffic for monitoring simulations.

def simulate_port_scan(target_ip="192.168.1.100", src_ip="192.168.1.50"):
    print(f"Simulating Port Scan logic toward {target_ip}...")
    # Send a few SYN packets to simulate scanning behavior
    for port in [22, 80, 443, 8080, 8443]:
        packet = IP(src=src_ip, dst=target_ip)/TCP(dport=port, flags="S")
        send(packet, verbose=0)
    print("Port Scan simulation complete.")

def simulate_syn_flood(target_ip="192.168.1.100", target_port=80):
    print(f"Simulating abstract SYN Flood behavior toward {target_ip}:{target_port}...")
    # Send a small batch of SYN packets from random IPs
    for _ in range(10):  # Limited for educational and testing simulation
        src_port = random.randint(1024, 65535)
        fake_ip = f"192.168.1.{random.randint(2, 254)}"
        packet = IP(src=fake_ip, dst=target_ip)/TCP(sport=src_port, dport=target_port, flags="S")
        send(packet, verbose=0)
    print("SYN Flood simulation complete.")

def simulate_dns_anomaly(target_dns="8.8.8.8", src_ip="192.168.1.50"):
    print(f"Simulating DNS Anomaly from {src_ip}...")
    # Generating anomalous DNS queries
    for i in range(5):
        domain = f"anomalous-test-domain-{i}.com"
        packet = IP(src=src_ip, dst=target_dns)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
        send(packet, verbose=0)
    print("DNS Anomaly simulation complete.")

def simulate_packet_burst(target_ip="192.168.1.100", src_ip="192.168.1.50"):
    print(f"Simulating Packet Burst from {src_ip} to {target_ip}...")
    payload = b"TEST_PAYLOAD" * 64
    for _ in range(20):  # Limited simulating traffic burst
        rand_dport = random.randint(1024, 65535)
        packet = IP(src=src_ip, dst=target_ip)/UDP(dport=rand_dport)/payload
        send(packet, verbose=0)
    print("Packet Burst simulation complete.")

if __name__ == "__main__":
    # Simulate an integration testing scenario
    simulate_port_scan()
    simulate_dns_anomaly()
