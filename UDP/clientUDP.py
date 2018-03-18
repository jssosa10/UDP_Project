import socket
import pickle
from datetime import datetime
print("Ingrese dir IP deseada")
UDP_IP = input()
print("Ingrese puerto deseado")
UDP_PORT = input()
print("Ingrese nombre deseado para su archivo")
inNombre = input()
print("Ingrese numero de objetos deseados")
numObjetos = input()
class Envio:
    numeroSecuencia = 0
    marcaTiempo = ""
    total=0
    nombre=""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, numeroSecuencia, total, nombre):
        self.numeroSecuencia = numeroSecuencia
        self.marcaTiempo= datetime.now()
        self.total=total
        self.nombre=nombre

sock = socket.socket(socket.AF_INET, # Internet
	  socket.SOCK_DGRAM) # UDP

for i in range(int(numObjetos)):
  message=pickle.dumps(Envio(i+1,numObjetos, inNombre))
  sock.sendto(message, (UDP_IP, int(UDP_PORT)))
sock.close()
