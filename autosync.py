import socket
import os
import hashlib
import time
ENDSTRING = 'oUtAnDoVeRHello'
s = socket.socket()
host = ""
port = input("Enter port for client: ")
s.connect((host, port))
folder = raw_input("Path of folder: ")
os.chdir(folder)
# s.send("Hello server!")

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def receiveFunc(com):
    s.send(com)
    data = s.recv(1024)
    s.send('received')
    retstr = ''
    while data != ENDSTRING:
        # print data+'\n'
        retstr += data
        data = s.recv(1024)
        s.send('received')
    # print retstr
    return retstr

def indexFunc( com ):
    com1 = com.split()
    text = receiveFunc(com)
    # s.recv(1024)
    # print text
    return text

def downloadFunc(com):
    s.send(com)
    com = com.split()
    if com[1] == 'TCP':
        f = open(com[2],'wb')
        data = s.recv(1024)
        s.send('received')
        while data!= ENDSTRING:
            f.write(data)
            data = s.recv(1024)
            s.send('received')
        f.close()
    elif com[1] == 'UDP':
        port2 = int(s.recv(1024))
        soc2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr2 = (host,port2)
        soc2.sendto('received',addr2)
        f = open(com[2],'wb')
        while True:
            text,addr2 = soc2.recvfrom(1024)
            # print "Text received: ",text
            if  text == ENDSTRING:
                break
            f.write(text)
            soc2.sendto('received',addr2)
        f.close()
        soc2.close()
        # s.recv(1024)
FLAG = True
initime = time.time()
TIMEPERIOD = raw_input("Enter timeperiod: ")
while FLAG==True:
    currtime = time.time()
    if currtime - initime >= TIMEPERIOD :
        all =  indexFunc('index longlist')
        all = all.split()
        i=0
        for a  in all[1::11]:
            if os.path.isfile(a):
                loc5 = md5(a)
                rem5 = indexFunc('hash verify '+a).split()[0]
                stas = os.stat(a)
                loctime = stas.st_mtime
                remtime = indexFunc('index longlist').split()[11*i+6]
                # print "Local: ",loctime," Remote: ",remtime
                if loc5 != rem5 and loctime <= remtime:
                    downloadFunc('download TCP '+a)
                    print "File ",a," updated"
                else:
                    print "File ",a," up-to-date"
            else:
                downloadFunc('download TCP '+a)
                print "New File ",a," made"
            i+=1
        initime = currtime
s.close()

print('connection closed')