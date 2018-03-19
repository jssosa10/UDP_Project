import socket
import hashlib
import sys
import select
from datetime import datetime
print("Ingrese dir IP deseada")
TCP_IP = input()
print("Ingrese puerto deseado")
TCP_PORT = input()
print("Ingrese tamaño del buffer")
tamBuffer= int(input())

sock = socket.socket(socket.AF_INET, # Internet
	  socket.SOCK_STREAM) # TCP
sock.connect((TCP_IP, int(TCP_PORT)))
sock.sendall('Holiwi'.encode())
nombreArch= sock.recv(1024).decode()
nombreArch= "recibir/"+nombreArch
print('archivo a recibir: ',nombreArch)
f = open(nombreArch,'wb')
sockUDP= socket.socket(socket.AF_INET, # Internet
	  socket.SOCK_DGRAM) # UDP
sockUDP.sendto(b'ready', (TCP_IP, int(TCP_PORT)-1))
hash_md5 = hashlib.md5()
l, addr = sockUDP.recvfrom(tamBuffer)
try:
    while (l):
        tiempoAct= datetime.now()
        hash_md5.update(l)
        f.write(l)
        sockUDP.settimeout(2)
        l, addr=sockUDP.recvfrom(tamBuffer)
except socket.timeout:
    a=1
f.close()
sockUDP.close()
sock.sendall(b'done')
hashServer=sock.recv(1024).decode()
hashCliente=hash_md5.hexdigest()
print('Hash del server ',hashServer)
print('Hash cliente ',hashCliente)
print('Archivo correcto (hash iguales): ',hashCliente==hashServer)
sock.sendall(b'tiempos')
tiempoServer=datetime.strptime(sock.recv(1024).decode(),'%Y-%m-%d %H:%M:%S.%f')
tiempito= (tiempoAct-tiempoServer).total_seconds()
print('Tiempo de envío: ',tiempito,' segundos')

