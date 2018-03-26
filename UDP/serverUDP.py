import sys
import os
import socket
import pickle
import tempfile
from pathlib import Path
from datetime import datetime
UDP_PORT=5000
if sys.argv[1]:
  UDP_PORT=sys.argv[1]
  
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

def reemplazar(arch, tiempoAct,objLeido):
  f= open(arch, 'r')
  linea=f.readline()
  recibidos=linea.split(':')[1]
  linea=f.readline()
  faltantes=linea.split(':')[1]
  linea=f.readline()
  promedio=linea.split(':')[1]
  tiempoTemp=(float(promedio)*int(recibidos)+float(tiempoAct))/(int(recibidos)+1)
  recibidos=int(recibidos)+1
  abs_path='t'+arch
  fh= open(abs_path,'a')
  fh.write('Numero de objetos recibidos:'+str(recibidos)+'\n')
  fh.write('Numero de objetos faltantes:'+str(int(faltantes)-1)+'\n')
  fh.write('Tiempo promedio de envio:'+str(tiempoTemp)+'\n')
  linea=f.readline().strip()
  while linea:
    fh.write(linea+'\n')
    linea=f.readline().strip()
  f.close()
  fh.close()
  os.remove(arch)
  os.rename(abs_path, arch)

sock = socket.socket(socket.AF_INET, # Internet
	  socket.SOCK_DGRAM) # UDP
sock.bind(('', int(UDP_PORT)))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes.
    print(addr)
    tRecibido= datetime.now()
    objLeido =pickle.loads(data)
    nombreArch=str(objLeido.nombre)+'.txt'
    my_file = Path(nombreArch)

    if my_file.is_file():
      reemplazar(nombreArch, (tRecibido-objLeido.marcaTiempo).microseconds/1000,objLeido)
    else:
      f=open(nombreArch, 'w')
      f.write('Numero de objetos recibidos:1\n')
      f.write('Numero de objetos faltantes:'+str(int(objLeido.total)-1)+'\n')
      f.write('Tiempo promedio de envio:'+str((tRecibido-objLeido.marcaTiempo).microseconds/1000)+'\n')
      f.close()
      
    f=open(nombreArch, 'a')
    f.write(str(objLeido.numeroSecuencia)+': '+str((tRecibido-objLeido.marcaTiempo).microseconds/1000)+' ms\n')
    f.close()        
    
sock.close()
