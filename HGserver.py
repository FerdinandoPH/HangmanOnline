#!/usr/bin/env python3
try:
    import socket,threading,random,os,sys,unidecode
    #import pynput
except:
    import os,sys
    os.system("pip install unidecode")
    print("Unidecode instalado. Reinicia el programa")
    '''
    os.system("pip install pynput")
    print("Keyboard instalado. Reinicia el programa")
    '''
    a=input("Pulsa enter para cerrar el programa")
    sys.exit()
currdir=os.path.dirname(os.path.abspath(__file__))
wlist=[]
def CargaPalabras():
    with open (currdir+"\\diccionario.txt", "r",encoding="utf-8") as f:
        for line in f:
            if "," in line:
                line=line[:line.find(",")]
            if line.isalpha() and len(line)>1:
                wlist.append(unidecode.unidecode(line.strip()))
        f.close()
CargaPalabras()
PORT=1234
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, PORT)
FORMAT="utf-8"
TERMINATED="ADIOS"
REMOTE_TERMINATED="SEPPUKU"
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
conectados=[]
conectadosaddr=[]
partidas={}
class Partida():
    def __init__(self,id,difficulty,j1):
        self.id=id
        self.difficulty=difficulty
        self.j1=j1
        self.j2=None
        self.palabra=""
def BorraTrazas(conn):
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
def start():
    server.listen()
    while True:
        conn,addr=server.accept()
        conectados.append(conn)
        conectadosaddr.append(addr)
        thread=threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Conexiones activas: {len(conectados)}")
def handle_client(conn, addr):
    print(f"Nueva conexion de {addr}")
    conectado=True
    mode="Undef"
    gameId=""
    while conectado:
        try: 
            msg=conn.recv(2048).decode(FORMAT)
            if msg:
                print("{} : {}".format(addr,msg))
                if msg==TERMINATED:
                    conectado=False
                elif msg==REMOTE_TERMINATED:
                    conn.send(("ADIOS").encode(FORMAT))
                    conectado=False
                elif msg[:6]=="SERVER":
                    mode="Server"
                    darid=str(random.randint(1000,9999))
                    while darid in partidas.keys():
                        darid=random.randint(1000,9999)
                    partidas.update({darid:Partida(darid,int(msg[6:]),conn)})
                    gameId=darid
                    conn.send(("Partida"+str(darid)).encode(FORMAT))
 
                elif msg[:6]=="CLIENT":
                    mode="Client"
                    idrequest=msg[6:]
                    if idrequest not in partidas.keys() or partidas[idrequest].j2!=None:
                        conn.send(("Nohay").encode(FORMAT))
                        conectado=False
                    else:
                        partidas[idrequest].j2=conn
                        dificultad=partidas[idrequest].difficulty
                        if dificultad==1:
                            palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                            while len(palabraAadivinar)>5:
                                palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                        elif dificultad==2:
                            palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                            while len(palabraAadivinar)>9:
                                palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                        else:
                            palabraAadivinar=wlist[random.randint(0,len(wlist)-1)]
                        print("Palabra a adivinar: ",palabraAadivinar)
                        gameId=idrequest
                        partidas[idrequest].palabra=palabraAadivinar
                        conn.send(("Ok"+partidas[idrequest].palabra).encode(FORMAT))
                        partidas[idrequest].j1.send(("Ok"+partidas[idrequest].palabra).encode(FORMAT))
                elif msg[:6]=="RESULT":
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

        except Exception as e:
            print("ERROR: ",e)
            conectado=False
    print(f"{addr} se ha desconectado")
    BorraTrazas(conn)
    conn.close()
    conectadosaddr.remove(addr)
    conectados.remove(conn)
    print(f"Conexiones activas: {len(conectados)}")
print("Servidor escuchando en:", SERVER, ":", PORT)
def on_press(key):
    try:
        if key.char=='q':
            print("Partidas: ",partidas)
            print("Conectados: ",conectadosaddr)
    except:
        pass
'''
thread2=threading.Thread(target=Stats)
thread2.start()
'''
start()