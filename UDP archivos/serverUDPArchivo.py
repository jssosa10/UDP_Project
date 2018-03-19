import sys
import os
import socket
import hashlib
from datetime import datetime
TCP_PORT=5000
if sys.argv[1]:
  TCP_PORT=sys.argv[1]
print("Ingrese tamaño del buffer")
tamBuffer= int(input())

sock = socket.socket(socket.AF_INET, # Internet
	  socket.SOCK_STREAM) # TCP
sock.bind(('127.0.0.1', int(TCP_PORT)))
sock.listen(1)
while True:
    s, addr = sock.accept() # buffer size is 1024 bytes.
    leido =s.recv(1024)
    nombreArch2= "musica.mp4"
    nombreArch= "enviar/"+nombreArch2
    f = open(nombreArch,'rb')
    l = f.read(tamBuffer)
    hash_md5 = hashlib.md5()
    s.sendall(nombreArch2.encode())
    sockUDP= socket.socket(socket.AF_INET, # Internet
	  socket.SOCK_DGRAM) # UDP
    sockUDP.bind(('127.0.0.1', int(TCP_PORT)-1))    
    data2, addr2= sockUDP.recvfrom(1024)    
    tiempoAct= datetime.now()
    while (l):    
      hash_md5.update(l)
      sockUDP.sendto(l,addr2)
      l = f.read(tamBuffer)
    f.close()
    sockUDP.close()
    s.recv(1024)
    hashCalculado= hash_md5.hexdigest()
    s.sendall(hashCalculado.encode())
    s.recv(1024)
    s.sendall(str(tiempoAct).encode())
sock.close()
