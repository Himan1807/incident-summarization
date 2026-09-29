#!/usr/bin/env python3
"""Pull additional per-host facts not in aggregate.py: MAC address for a given
IP (from Ethernet source of packets it sent) and a quick DHCP hostname lookup.
Usage: python3 extra_facts.py <pcap> <target_ip>
"""
import sys, struct
sys.path.insert(0, '/home/claude/dataset_work/scripts')
from pcap_parser import read_pcap, parse_ethernet, parse_ipv4

def mac_str(b):
    return ':'.join(f'{x:02x}' for x in b)

def find_mac(pcap_path, target_ip):
    macs = set()
    for ts, pkt in read_pcap(pcap_path):
        if len(pkt) < 14:
            continue
        eth_type, offset = parse_ethernet(pkt)
        if eth_type != 0x0800:
            continue
        ip = parse_ipv4(pkt, offset)
        if ip and ip['src'] == target_ip:
            src_mac = pkt[6:12]
            macs.add(mac_str(src_mac))
    return sorted(macs)

if __name__ == '__main__':
    pcap_path, target_ip = sys.argv[1], sys.argv[2]
    print(target_ip, find_mac(pcap_path, target_ip))
