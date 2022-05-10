from signal import valid_signals


try:
    import socket,threading,sys,time
    from tkinter import *
except:
    import os,sys
    os.system("pip install pynput")
    print("Se han instalado las dependencias")
    sys.exit()
#Para parar la conexión
global stopRecv
stopRecv=False
PORT=1234
SERVER="10.227.31.235"
ADDR=(SERVER, PORT)
FORMAT="utf-8"
TERMINATED="ADIOS"
global vidas
vidas=6
def Asterisca(pal,letrasdadas):
    nuevapal=""
    for i in range (0,len(pal)):
        if pal[i] not in letrasdadas:
            nuevapal+="_"
        else:
            nuevapal+=pal[i]
    return nuevapal
def TkinterClear(root):
    #Limpia la ventana de todos los objetos colocados con pack, place o grid
    activos=root.pack_slaves()
    activos+=(root.place_slaves())
    activos+=(root.grid_slaves())
    #print(activos)
    for widget in activos:
        widget.destroy()
def Inicio():
    root.title("HGclientGUI")
    root.geometry("300x200")
    #Haz un titulo que diga: Ahorcado, céntralo y ponlo grande
    titulo=Label(root,text="Ahorcado",font=("Times New Roman",30))
    titulo.pack(pady=10)
    #Haz un boton que diga: Iniciar partida online
    botonOnline=Button(root,text="Iniciar partida online",command=ConectaAlServer)
    botonOnline.pack(pady=5)
    #Haz un boton que diga: Iniciar partida offline a la derecha del boton anterior
    botonOffline=Button(root,text="Iniciar partida offline",command=InicioOffline)
    botonOffline.pack(pady=5)
    #Haz un boton que diga: Salir
    botonSalir=Button(root,text="Salir",command=lambda:root.destroy())
    botonSalir.pack(pady=10)
def ConectaAlServer():
    global stopRecv
    stopRecv=False
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        recvThread=threading.Thread(target=recv_server, args=(client,))
        recvThread.daemon=True
        recvThread.start()
        print("Se ha establecido la conexión al servidor")
        InicioOnline(client)
    except:
        print("Parece que el servidor no funciona. Inténtalo más tarde")
def InicioOnline(cliente):
        TkinterClear(root)
        root.geometry("300x200")
        #Haz un titulo que diga: Modo online, céntralo y ponlo grande
        tituloOnline=Label(root,text="Modo online",font=("Times New Roman",30))
        tituloOnline.pack(pady=10)
        #Crea un botón para crear una partida y a la derecha un botón para unirse a una partida
        botonCrear=Button(root,text="Crear partida",command=lambda:CrearPartida(cliente))
        botonCrear.pack(pady=5)
        botonUnirse=Button(root,text="Unirse a partida",command=lambda:UnirsePartida(cliente))
        botonUnirse.pack(pady=5)

def CancelaPartida(cliente,id):
    cliente.send(("CANCEL"+str(id)).encode(FORMAT))
    print("Partida cancelada")
    InicioOnline(cliente)
def recv_server(cliente):
    '''
    global idpartida
    global mode
    global pal
    global gameStatus
    '''
    global stopRecv
    while stopRecv==False:
        try:
            msg=cliente.recv(2048).decode(FORMAT)
            if msg:
                #print(msg)
                
                if msg=="ADIOS":
                    stopRecv=True
                elif msg=="Nohay":
                    for widget in root.pack_slaves():
                        if widget.winfo_class()=="Label" and widget.cget("text")=="No existe esa partida o ya está en curso":
                            widget.destroy()
                    nohayLabel=Label(root,text="No existe esa partida o ya está en curso")
                    #Pon el texto en rojo
                    nohayLabel.config(fg="red")
                    nohayLabel.pack(pady=10)
                elif msg[:7]=="Partida":
                    idpartida=msg[7:]
                    TkinterClear(root)
                    root.geometry("300x200")
                    #Haz un titulo que diga: Esperando a J2, céntralo y ponlo grande
                    tituloEspera=Label(root,text="Esperando a J2",font=("Times New Roman",30))
                    tituloEspera.pack(pady=10)
                    PartidaLabel=Label(root,text="Partida: "+idpartida)
                    PartidaLabel.pack(pady=5)
                    #Haz un boton que diga: Salir
                    botonSalir=Button(root,text="Cancelar",command=lambda:CancelaPartida(cliente,idpartida))
                    botonSalir.pack(pady=10)

                
                elif msg[:2]=="Ok":
                    pal=msg[2:]
                    Ahorcado(pal,cliente)
                    '''
                    if mode=="J1":
                        print("Conectado! La palabra es: "+pal)
                        gameThread=threading.Thread(target=Juego, args=(cliente,pal,))
                        gameThread.start()
                    else:
                        print("Te has unido! La palabra es: "+pal)
                        gameThread=threading.Thread(target=Juego, args=(cliente,pal,))
                        gameThread.start()
                    '''
                '''
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
                    '''
        except Exception as e:
            print("Se ha cerrado la conexión")
            print("El error ha sido: ",e)
            stopRecv=True
            break
    try:
        cliente.send(TERMINATED.encode(FORMAT))
    except:
        print("Se ha intentado cerrar la conexión de forma limpia")
    cliente.close()    
def CrearPartida(cliente):
    TkinterClear(root)
    root.geometry("400x300")
    #Haz un titulo que diga: Elige dificultad, céntralo y ponlo grande
    tituloDificultad=Label(root,text="Elige dificultad",font=("Times New Roman",30))
    tituloDificultad.pack(pady=10)
    #Haz tres botones: uno para facil (maximo 5 letras), otro para medio (maximo 9 letras) y uno para dificil (sin limite de letras). Debajo de los botones, introduce una etiquetaque explique cada dificultad. Debajo de la etiqueta, pon un botón para volver al menú anterior
    botonFacil=Button(root,text="Facil",command=lambda:cliente.send("SERVER1".encode(FORMAT)))
    botonFacil.pack(pady=5)
    botonMedio=Button(root,text="Medio",command=lambda:cliente.send("SERVER2".encode(FORMAT)))
    botonMedio.pack(pady=5)
    botonDificil=Button(root,text="Dificil",command=lambda:cliente.send("SERVER3".encode(FORMAT)))
    botonDificil.pack(pady=5)
    explicacion=Label(root,text="Fácil: 5 letras.\nMedio: 9 letras.\nDificil: Sin limite de letras")
    explicacion.pack(pady=5)
    botonVolver=Button(root,text="Volver",command=lambda:InicioOnline(cliente))
    botonVolver.pack(pady=10)


def UnirsePartida(cliente):
    TkinterClear(root)
    root.geometry("400x300")
    #Haz un titulo que diga: Unirse a una partida, céntralo y ponlo grande
    tituloUnirse=Label(root,text="Unirse a una partida",font=("Times New Roman",30))
    tituloUnirse.pack(pady=10)
    promptEntrada=Label(root,text="Introduce el id de la partida")
    promptEntrada.pack(pady=5)
    #Haz una caja de texto para introducir el id de la partida
    idPartidaEntrada=Entry(root)
    idPartidaEntrada.pack(pady=5)
    #Haz un boton para unirte a la partida
    botonUnirse=Button(root,text="Unirse",command=lambda:[cliente.send(("CLIENT"+idPartidaEntrada.get()).encode(FORMAT)),idPartidaEntrada.delete(0,END)])
    #Haz que también se envíe el id si se pulsa enter
    idPartidaEntrada.bind("<Return>",lambda event:[cliente.send(("CLIENT"+idPartidaEntrada.get()).encode(FORMAT)),idPartidaEntrada.delete(0,END)])
    botonUnirse.pack(pady=10)
def InicioOffline():
    pass
def Ahorcado(pal,cliente=None):
    letrasdadas=[]
    adivinaTitulo=Label(root,text="Adivina la palabra",font=("Times New Roman",30))
    adivinaTitulo.pack(pady=10)
    palabraLabel=Label(root,text=Asterisca(pal,letrasdadas))
    palabraLabel.pack(pady=5)
    #Haz una caja de texto para introducir la letra
    letraEntrada=Entry(root)
    letraEntrada.pack(pady=5)
    #Haz un boton para introducir la letra
    botonLetra=Button(root,text="Enviar",command=lambda:[letrasdadas.append(letraEntrada.get().lower()),palabraLabel.config(text=Asterisca(pal,letrasdadas)),letraEntrada.delete(0,END),EsCorrecto(pal,letraEntrada.get().lower(),letrasdadas,cliente)])
    botonLetra.pack(pady=10)
    botonLetra.bind("<Return>",lambda event:[letrasdadas.append(letraEntrada.get().lower()),palabraLabel.config(text=Asterisca(pal,letrasdadas)),letraEntrada.delete(0,END),EsCorrecto(pal,letraEntrada.get().lower(),letrasdadas,cliente)])
def EsCorrecto(pal,letra,letrasdadas,cliente=None):
    global vidas
    if letra not in pal:
        vidas-=1
        if vidas==0:
            if cliente!=None:
                cliente.send("RESULT0".encode(FORMAT))
        elif vidas==1:
            Pista()
    else:
        if Asterisca(pal,letrasdadas)==pal:
            if cliente!=None:
                cliente.send("RESULT1".encode(FORMAT))
def Pista():
    pass

root=Tk()
Inicio()
root.mainloop()