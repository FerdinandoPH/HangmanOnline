try:
    import socket,threading,sys,pynput,time
except:
    import os,sys
    os.system("pip install pynput")
    print("Se han instalado las dependencias")
    sys.exit()
global stopRecv
stopRecv=False
def FinalizaJuego():
    teclado=pynput.keyboard.Controller()
    for i in range(6):
        teclado.press("0")
        teclado.release("0")
    teclado.press("1")
    teclado.release("1")
    teclado.press(pynput.keyboard.Key.enter)
    teclado.release(pynput.keyboard.Key.enter)
def Juego(client,pal):
    stopCode="0000001"
    global gameStatus
    print("Bienvenido al juego")
    print("La palabra es "+pal)
    print("Por ahora no hay mucho que hacer, escribe 1 para ganar o 0 para perder")
    stopGame=False
    while stopGame==False:
        result=input("Introduce tu entrada: ")
        if stopCode in result:
            print("stop")
            stopGame=True
        else:
            if result=="1":
                gameStatus=result
                client.send(("RESULT"+result).encode(FORMAT))
            elif result=="0":
                gameStatus=result
                client.send(("RESULT"+result).encode(FORMAT))
            else:
                print("No has introducido un valor valido")

def recv_server(cliente):
    global idpartida
    global mode
    global pal
    global gameStatus
    global stopRecv
    while stopRecv==False:
        try:
            msg=cliente.recv(2048).decode(FORMAT)
            if msg:
                #print(msg)
                if msg=="ADIOS":
                    stopRecv=True
                elif msg=="Nohay":
                    print("Esa partida no existe o ya está llena")
                    stopRecv=True
                elif msg[:7]=="Partida":
                    idpartida=msg[7:]
                    print("Partida: "+idpartida)
                    print("Esperando a que el otro jugador se conecte")
                elif msg[:2]=="Ok":
                    pal=msg[2:]
                    if mode=="J1":
                        print("Conectado! La palabra es: "+pal)
                        gameThread=threading.Thread(target=Juego, args=(cliente,pal,))
                        gameThread.start()
                    else:
                        print("Te has unido! La palabra es: "+pal)
                        gameThread=threading.Thread(target=Juego, args=(cliente,pal,))
                        gameThread.start()
                elif msg=="Cerrada":
                    if gameThread.is_alive():
                        FinalizaJuego()
                    print("La partida se ha cerrado")
                    stopRecv=True
                elif msg[:6]=="RESULT":
                    resultado=msg[6:]
                    if resultado=="1":
                        FinalizaJuego()
                        print("Ganaste!")
                    else:
                        FinalizaJuego()
                        print("Perdiste!")
                    stopRecv=True
        except:
            print("Se ha cerrado la conexión")
            stopRecv=True
            break
    try:
        cliente.send(TERMINATED.encode(FORMAT))
    except:
        print("Se ha intentado cerrar la conexión de forma limpia")
    cliente.close()
    InicioOnline()    
global idpartida
global mode
global pal
global gameStatus
gameStatus="2"
PORT=44444
SERVER="80.29.24.47"
ADDR=(SERVER, PORT)
FORMAT="utf-8"
TERMINATED="ADIOS"
def Inicio():
    print("Bienvenido al ahorcado")
    print("1. Jugar online")
    print("2. Jugar offline")
    print("3. Salir")
    opcion=""
    while opcion not in ["1","2","3"]:
        opcion=input("Introduce una opción: ")
        if opcion=="1":
            print("Iniciando conexión...")
            InicioOnline()
        elif opcion=="2":
            print("Por ahora no hay modo offline")
            Inicio()
        elif opcion=="3":
            print("Adiós")
            sys.exit()
        else:
            print("No has introducido una opción válida")

def InicioOnline():
    global stopRecv
    global mode
    stopRecv=False
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
    except:
        print("Parece que el servidor no funciona. Inténtalo más tarde")
        Inicio()
    thread=threading.Thread(target=recv_server, args=(client,))
    thread.start()
    print("Se ha establecido la conexión al servidor")
    print("Quieres conectarte a una partida o crear una nueva?")
    print("1. Conectarte a una partida")
    print("2. Crear una nueva partida")
    print("3. Salir")
    opcion=input("Opcion: ")
    if opcion=="1":
        mode="J2"
        print("Ingresa el codigo de la partida (o nada para salir)")
        validez=False
        while validez==False:
            codigo=input("Codigo: ")
            if codigo=="":
                client.send(("SEPPUKU").encode(FORMAT))
            try:
                codigo2=int(codigo)
                if codigo2 >999 and codigo2<10000:
                    validez=True
                else:
                    print("Codigo invalido")
            except:
                if codigo!="":
                    print("Codigo invalido")
                else:
                    client.send(("SEPPUKU").encode(FORMAT))
                    break
        if validez==True:
            client.send(("CLIENT"+codigo).encode(FORMAT))
    elif opcion=="2":
        mode="J1"
        print("Elige la dificultad (o nada para salir)")
        print("1.Facil (hasta 5 letras)")
        print("2.Medio (hasta 9 letras)")
        print("3.Dificil (sin límite)")
        dificultad=""
        while dificultad!="1" and dificultad!="2" and dificultad!="3":
            dificultad=input("Dificultad: ")
            if dificultad=="":
                client.send(("SEPPUKU").encode(FORMAT))
                break
        if dificultad!="":
            client.send(("SERVER"+dificultad).encode(FORMAT))
    elif opcion=="3":
        print("Saliendo...")
        sys.exit()
    else:
        print("Opcion invalida")
        client.send(("SEPPUKU").encode(FORMAT))
Inicio()