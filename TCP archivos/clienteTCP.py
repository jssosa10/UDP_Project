import socket
import hashlib
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
sock.sendall(b'ready')
hash_md5 = hashlib.md5()
l = sock.recv(tamBuffer)
while (l):
    if l.endswith(b'termine'):
        tiempoAct= datetime.now()
        u=l[:-7]
        f.write(u)
        hash_md5.update(u)
        break
    else:
        f.write(l)
        hash_md5.update(l)
        l = sock.recv(tamBuffer)
f.close()
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

