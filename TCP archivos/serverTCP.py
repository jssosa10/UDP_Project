import sys
import os
import socket
import hashlib
from datetime import datetime
TCP_PORT=5000
if sys.argv[1]:
  TCP_PORT=sys.argv[1]
print("Ingrese tamano del buffer")
tamBuffer= int(input())

sock = socket.socket(socket.AF_INET, # Internet
	  socket.SOCK_STREAM) # TCP
sock.bind(('', int(TCP_PORT)))
sock.listen(1)
while True:
    s, addr = sock.accept() # buffer size is 1024 bytes.
    leido =s.recv(1024)
    nombreArch= "video.mp4"
    s.sendall(nombreArch.encode())
    nombreArch= "enviar/"+nombreArch    
    s.recv(1024)
    f = open(nombreArch,'rb')
    l = f.read(tamBuffer)
    hash_md5 = hashlib.md5()
    tiempoAct= datetime.now()
    while (l):    
      hash_md5.update(l)
      s.sendall(l)
      l = f.read(tamBuffer)
    s.sendall(b'termine')
    f.close()    
    s.recv(1024)
    hashCalculado= hash_md5.hexdigest()
    s.sendall(hashCalculado.encode())
    s.recv(1024)
    s.sendall(str(tiempoAct).encode())
sock.close()
