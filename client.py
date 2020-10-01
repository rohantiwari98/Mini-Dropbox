import socket
import os
import hashlib
ENDSTRING = 'oUtAnDoVeRHello'
s = socket.socket()
host = ""
port = input("Enter port for client: ")
s.connect((host, port))
folder = raw_input("Path of folder: ")
os.chdir(folder)

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
        retstr += data
        data = s.recv(1024)
        s.send('received')
    return retstr

def indexFunc( com ):
    com1 = com.split()
    text = receiveFunc(com)
    print text
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
            if  text == ENDSTRING:
                break
            f.write(text)
            soc2.sendto('received',addr2)
        f.close()
        soc2.close()

FLAG = True
while FLAG==True:
    com = raw_input("prompt> ")
    com1 = com.split()
    if len(com1) >= 2 :
        if(com1[0]=='index'):
            indexFunc(com)
        elif(com1[0]=='hash'):
            indexFunc(com)
        elif(com1[0]=='download'):
            hash5 = indexFunc('hash verify '+com1[2]).split()[0]
            downloadFunc(com)
            if com1[1] == 'UDP':
                loc5 = md5(com1[2])
                print "Hash of file in remote: ",hash5
                print "Hash of file in local: ",loc5
                if loc5 == hash5:
                    print "Both the files are same!!!!"
                else:
                    print "UDP messed up, files are not the same"
        elif(com1[0]=='exit'):
            FLAG=False
        else:
            print "Not a correct command\n"
    else:
        print "Not a correct command\n"
s.close()

print('connection closed'