#!/usr/bin/env python3

import socket,threading,random,os,sys,time, datetime
#import pynput

currdir=os.path.dirname(os.path.abspath(__file__))
wlist=[]
def CargaPalabras(): #Trata de cargar las palabras del archivo "diccionario.txt" 
    try:
        with open (currdir+"/Assets/diccionario.txt", "r",encoding="utf-8") as f:
            for line in f:
                if "," in line:
                    line=line[:line.find(",")]
                if line.isalpha() and len(line)>1:
                    line=line.replace('á','a')
                    line=line.replace('é','e')
                    line=line.replace('í','i')
                    line=line.replace('ó','o')
                    line=line.replace('ú','u')
                    line=line.replace('ü','u')
                    wlist.append(line.strip())
            f.close()
    except:
        print("No se ha podido cargar la lista de palabras. Comprueba que el archivo diccionario.txt esté en la carpeta del programa")
PORT=20224
SERVER="192.168.1.118"
ADDR=(SERVER, PORT)
FORMAT="utf-8"
TERMINATED="ADIOS"
REMOTE_TERMINATED="SEPPUKU"
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
conectados=[]
conectadosaddr=[]
partidas={}
CargaPalabras()
class Partida(): #Atributos que tiene cada partida que se genera
    def __init__(self,id,difficulty,j1):
        self.id=id
        self.difficulty=difficulty
        self.j1=j1
        self.j2=None
        self.palabra=""
def BorraTrazas(conn): #Cuando se cierra una conexion de forma abrupta, esta función se encarga de avisar al otro jugador y de borrar la partida
    for Partida in list(partidas.keys()):
        if partidas[Partida].j1==conn:
            if partidas[Partida].j2!=None:
                partidas[Partida].j2.send(("Cerrada").encode(FORMAT))
            del partidas[partidas[Partida].id]
            
        elif partidas[Partida].j2==conn:
            if partidas[Partida].j1!=None:
                partidas[Partida].j1.send(("Cerrada").encode(FORMAT))
            del partidas[partidas[Partida].id]
'''
def Stats():
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()
'''
def ahora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def start(): #Función que se encarga de iniciar el servidor y escuchar nuevas conexiones
    server.listen()
    while True:
        conn,addr=server.accept()
        conectados.append(conn)
        conectadosaddr.append(addr)
        thread=threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon=True
        thread.start()
        print(f"{ahora()}: Conexiones activas: {len(conectados)}")
def handle_client(conn, addr): #Hilo que se genera para cada conexión
    print(f"{ahora()}: Nueva conexion de {addr}")
    conn.settimeout(60)
    conectado=True
    mode="Undef" #Advertencia: aunque la variable mode inidca si es el J1 o el J2, debido a mi pasada experiencia con el appinventor los llamé "server" al J1 y "client" al J2. Sé que es un poco confuso -_-
    gameId=""
    while conectado:
        try: 
            msg=conn.recv(2048).decode(FORMAT)
            if msg:
                print("{} : {}".format(addr,msg))
                if msg==TERMINATED: #Se cierra la conexión
                    conectado=False
                elif msg==REMOTE_TERMINATED: #El cliente ha solicitado cerrar la conexión 
                    conn.send(("ADIOS").encode(FORMAT))
                    conectado=False
                elif msg == "VIVO":
                    pass
                elif msg[:6]=="SERVER": #Se ha solicitado que se genere una partida (el último caracter es la dificultad)
                    mode="Server"
                    darid=str(random.randint(1000,9999))
                    while darid in partidas.keys():
                        darid=random.randint(1000,9999)
                    partidas.update({darid:Partida(darid,int(msg[6:]),conn)})
                    gameId=darid
                    conn.send(("Partida"+str(darid)).encode(FORMAT))
                elif msg[:6]=="CANCEL": #Se ha solicitado cancelar una partida en espera al J2
                    if msg[6:] in partidas.keys():
                        del partidas[msg[6:]]
                        print(f"Partida {msg[6:]} cancelada")
                elif msg[:6]=="CLIENT": #Se ha solicitado unirse a una partida (se responde en función de si esa partida existe y no está en curso)
                    mode="Client"
                    idrequest=msg[6:]
                    if idrequest not in partidas.keys() or partidas[idrequest].j2!=None:
                        conn.send(("Nohay").encode(FORMAT))
                    else:
                        partidas[idrequest].j2=conn
                        dificultad=partidas[idrequest].difficulty
                        if dificultad==1:
                            palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                            while len(palabraAadivinar)>5:
                                palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                        elif dificultad==2:
                            palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                            while len(palabraAadivinar)>9 or len(palabraAadivinar)<6:
                                palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                        else:
                            palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                            while len(palabraAadivinar)<9:
                                palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                        print("Palabra a adivinar: ",palabraAadivinar)
                        gameId=idrequest
                        partidas[gameId].palabra=palabraAadivinar
                        conn.send(("Ok"+partidas[gameId].palabra).encode(FORMAT))
                        partidas[gameId].j1.send(("Ok"+partidas[gameId].palabra).encode(FORMAT))
                elif msg[:4]=="PROG": #El servidor envía cuántas letras le quedan al otro jugador
                    progreso=msg[4:]
                    if mode=="Server":
                        partidas[gameId].j2.send(("PROG"+progreso).encode(FORMAT))
                    elif mode=="Client":
                        partidas[gameId].j1.send(("PROG"+progreso).encode(FORMAT))
                elif msg[:6]=="RESULT": #Uno de los jugadores ha ganado o se ha quedado sin vidas. Se avisa al otro jugador
                    resultado=msg[6:]
                    if resultado=="1":
                        if mode=="Server":
                            partidas[gameId].j2.send(("RESULT0").encode(FORMAT))
                            partidas[gameId].j1.send(("RESULT1").encode(FORMAT))
                        else:
                            partidas[gameId].j1.send(("RESULT0").encode(FORMAT))
                            partidas[gameId].j2.send(("RESULT1").encode(FORMAT))
                    elif resultado=="0":
                        if mode=="Server":
                            partidas[gameId].j2.send(("RESULT1").encode(FORMAT))
                            partidas[gameId].j1.send(("RESULT0").encode(FORMAT))
                        else:
                            partidas[gameId].j1.send(("RESULT1").encode(FORMAT))
                            partidas[gameId].j2.send(("RESULT0").encode(FORMAT))
                    time.sleep(0.1)
                    del partidas[gameId]
                else:
                    raise ValueError("Mensaje no reconocido")
        except Exception as e: #Ha ocurrido un error (normalmente es porque el cliente ha cerrado el programa con la X). Se procede a cerrar la conexión
            print(f"{ahora()}ERROR: ",e)
            try:
                conn.send(("ADIOS").encode(FORMAT))
            except:
                pass
            conectado=False
    print(f"{ahora()}: {addr} se ha desconectado")
    BorraTrazas(conn)
    conn.close()
    conectadosaddr.remove(addr)
    conectados.remove(conn)
    print(f"{ahora()}: Conexiones activas: {len(conectados)}")
print(f"{ahora()}: Servidor escuchando en:", SERVER, ":", PORT)
'''
def on_press(key):
    try:
        if key.char=='q':
            print("Partidas: ",partidas)
            print("Conectados: ",conectadosaddr)
    except:
        pass
    '''
'''
thread2=threading.Thread(target=Stats)
thread2.start()
'''
start()
