try:
    import socket,threading,sys,os,random,time,pygame
    from tkinter import *
    from tkinter import messagebox
except:
    import os,sys
    os.system("pip install pygame")
    os.system("pip3 install pygame")
    print("Se han instalado las dependencias")
    fin=input("Presiona enter para salir")
    sys.exit()
#Para parar la conexión
global stopRecv
global colorclock
colorclock=False
global musica
musica=True
global cancionActual
cancionActual=""
stopRecv=False
PORT=44444
SERVER="80.29.24.47"
ADDR=(SERVER, PORT)
FORMAT="utf-8"
TERMINATED="ADIOS"
global vidas
vidas=6
wlist=[]
currdir=os.path.dirname(os.path.abspath(__file__))
root=Tk()
letrasdadas=[]
horca0=PhotoImage(file=currdir+"\\Assets\\Imgs\\horca.gif")
horca1=PhotoImage(file=currdir+"\\Assets\\Imgs\\horca1.gif")
horca2=PhotoImage(file=currdir+"\\Assets\\Imgs\\horca2.gif")
horca3=PhotoImage(file=currdir+"\\Assets\\Imgs\\horca3.gif")
horca4=PhotoImage(file=currdir+"\\Assets\\Imgs\\horca4.gif")
horca5=PhotoImage(file=currdir+"\\Assets\\Imgs\\horca5.gif")
horca6=PhotoImage(file=currdir+"\\Assets\\Imgs\\horca6.gif")
imagenes=[horca0,horca1,horca2,horca3,horca4,horca5,horca6]
pygame.init()
global efectosSonido
pygame.mixer.set_num_channels(8)
efectosSonido=pygame.mixer.Channel(0)

def Asterisca(pal,letrasdadas): #A partir de una palabra y una lista de letras usadas, devuelve la palabra con asteriscos en las posiciones donde se encuentran las letras que no se han usado
    nuevapal=""
    for i in range (0,len(pal)):
        if pal[i] not in letrasdadas:
            nuevapal+="*"
        else:
            nuevapal+=pal[i]
    return nuevapal
def TkinterClear(root,keepmusic=False,exceptosicancion=""): #Limpia todo el contenido de la ventana y para la canción actual a no ser que se indique lo contrario
    global cancionActual
    global efectosSonido
    if keepmusic==False and cancionActual!=exceptosicancion:
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1)
        efectosSonido.stop()
        cancionActual=""
    activos=root.pack_slaves()
    activos+=(root.place_slaves())
    activos+=(root.grid_slaves())
    for widget in activos:
        widget.destroy()
def PausaColor(root,boton=None): #Activa o desactiva el cambio de color de la ventana
    global colorclock
    if colorclock==True:
        colorclock=False
        if boton!=None:
            boton.config(text="Fondo de colores OFF")
    else:
        colorclock=True
        if boton!=None:
            boton.config(text="Fondo de colores ON")
        clockThread=threading.Thread(target=ColorThread, args=(root,))
        clockThread.daemon=True
        clockThread.start()
def ColorThread(raiz): #Hilo que cambia el color de fondo de la ventana cada dos segundos
    global colorclock
    while colorclock:
        time.sleep(2)
        ColorCambio(raiz)
    raiz.configure(background="white")
    for widget in raiz.pack_slaves():
        if widget.winfo_class()=="Label":
            widget.configure(background="white")
def ColorCambio(raiz): #Cambia el color de fondo de la ventana y de las etiquetas a uno aleatorio
    color=random.choice(["#ff323b","#00ff00","#ffff00","#00ffff","#ff00ff"])
    while color==raiz.cget("bg"):
        color=random.choice(["#ff323b","#00ff00","#ffff00","#00ffff","#ff00ff"])
    raiz.configure(background=color)
    for widget in raiz.pack_slaves():
        if widget.winfo_class()=="Label" and "Vidas" not in widget.cget("text"):
            widget.configure(background=color)
def Inicio(): #Carga la pantalla inicial, con el botón de inicio online, offline y salir, además de las opciones para la música y el cambio de color
    global colorclock
    global musica
    root.title("HGclientGUI")
    TkinterClear(root)
    root.geometry("400x300")
    startclock=True
    for hilo in threading.enumerate():
        if "ColorThread" in hilo.name:
            startclock=False
            break
    if startclock and colorclock:
        clockThread=threading.Thread(target=ColorThread, args=(root,))
        clockThread.daemon=True
        clockThread.start()   
    titulo=Label(root,text="Ahorcado",font=("Times New Roman",30))
    titulo.pack(pady=10)
    botonOnline=Button(root,text="Iniciar partida online (2P)",command=ConectaAlServer)
    botonOnline.pack(pady=5)
    botonOffline=Button(root,text="Iniciar partida offline (1P)",command=InicioOffline)
    botonOffline.pack(pady=5)
    if colorclock:
        botonPausa=Button(root,text="Fondo de colores ON",command=lambda:PausaColor(root,botonPausa))
    else:
        botonPausa=Button(root,text="Fondo de colores OFF",command=lambda:PausaColor(root,botonPausa))
    botonPausa.pack(pady=10)
    if musica:
        botonMusica=Button(root,text="Musica ON",command=lambda:CambiaMusica(botonMusica))
    else:
        botonMusica=Button(root,text="Musica OFF",command=lambda:CambiaMusica(botonMusica))
    botonMusica.pack(pady=10)
    botonSalir=Button(root,text="Salir",command=lambda:root.destroy())
    botonSalir.pack(pady=10)
def CambiaMusica(boton=None): #Activa o desactiva la música
    global musica
    global cancionActual
    if musica==True:
        musica=False
        cancionActual=""
        if boton!=None:
            boton.config(text="Musica OFF")
    else:
        musica=True
        if boton!=None:
            boton.config(text="Musica ON")
        
def ConectaAlServer(): #Intenta conectarse al servidor, si no lo consigue, muestra un mensaje de error, si lo consigue, abre el hilo recv_thread (para comunicarse con el servidor) y va a InicioOnline
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
        messagebox.showerror("","Parece que el servidor no funciona. Inténtalo más tarde")
def InicioOnline(cliente): #Carga la pantalla de inicio online, con los botones para crear una partida o unirse a una ya creada y el botón de desconectarse
    global musica
    global cancionActual
    TkinterClear(root,False,"menu")
    if musica and cancionActual!="menu":
        cancionActual="menu"
        pygame.mixer.music.load(currdir+"\\Assets\\Musica\\menuMusic.mp3")
        pygame.mixer.music.play(-1)
    root.geometry("300x200")
    tituloOnline=Label(root,text="Modo online",font=("Times New Roman",30))
    tituloOnline.pack(pady=10)
    botonCrear=Button(root,text="Crear partida",command=lambda:CrearPartida(cliente))
    botonCrear.pack(pady=5)
    botonUnirse=Button(root,text="Unirse a partida",command=lambda:UnirsePartida(cliente))
    botonUnirse.pack(pady=5)
    botonSalir=Button(root,text="Desconectarse",command=lambda:[cliente.send("SEPPUKU".encode(FORMAT)),Inicio()])
    botonSalir.pack(pady=10)
def FormatLetrasUsadas(letrasdadas): #Convierte la lista de letras usadas en una cadena que puede representarse en una etiqueta (más elegante)
    nuevapal="Letras usadas: "
    for i in range (0,len(letrasdadas)):
        nuevapal+=letrasdadas[i]
        if i!=len(letrasdadas)-1:
            nuevapal+=", "
    return nuevapal
def CancelaPartida(cliente,id): #Cancela la espera a otro jugador, y vuelve a la pantalla de inicio online
    cliente.send(("CANCEL"+str(id)).encode(FORMAT))
    print("Partida cancelada")
    InicioOnline(cliente)
def recv_server(cliente): #Hilo que se encarga de recibir mensajes del servidor y procesarlos
    '''
    global idpartida
    global mode
    global pal
    global gameStatus
    '''
    pal=""
    global stopRecv
    while stopRecv==False:
        try:
            msg=cliente.recv(2048).decode(FORMAT)
            if msg:    
                if msg=="ADIOS": #Comienza la desconexión
                    stopRecv=True
                elif msg=="Nohay": #La partida a la que se quiere unir no existe o ya está en curso
                    for widget in root.pack_slaves():
                        if widget.winfo_class()=="Label" and widget.cget("text")=="No existe esa partida o ya está en curso":
                            widget.destroy()
                    nohayLabel=Label(root,text="No existe esa partida o ya está en curso")
                    nohayLabel.config(fg="red")
                    nohayLabel.pack(pady=10)
                elif msg[:7]=="Partida": #La partida se ha creado con éxito, y se da el id para que otro jugador pueda unirse
                    idpartida=msg[7:]
                    TkinterClear(root,True)
                    root.geometry("300x200")
                    #Haz un titulo que diga: Esperando a J2, céntralo y ponlo grande
                    tituloEspera=Label(root,text="Esperando a J2",font=("Times New Roman",30))
                    tituloEspera.pack(pady=10)
                    PartidaLabel=Label(root,text="Partida: "+idpartida)
                    PartidaLabel.pack(pady=5)
                    #Haz un boton que diga: Salir
                    botonSalir=Button(root,text="Cancelar",command=lambda:CancelaPartida(cliente,idpartida))
                    botonSalir.pack(pady=10)
                elif msg[:2]=="Ok": #Ya hay dos jugadores, y se puede comenzar la partida. El servidor envía la palabra y comienza el juego
                    pal=msg[2:]
                    Ahorcado(pal,cliente)     
                elif msg=="Cerrada": #El otro jugador se ha desconectado en medio de la partida
                    messagebox.showerror("Error","El otro jugador ha abandonado la partida")
                    InicioOnline(cliente)
                elif msg[:6]=="RESULT": #Uno de los jugadores ha acertado la palabra o se ha quedado sin vidas
                    resultado=msg[6:]
                    if resultado=="1":
                        Finjuego(True,cliente,pal)
                    else:
                        Finjuego(False,cliente,pal)
        except Exception as e: #Ha ocurrido un error, por lo que el hilo se cierra
            print("Se ha cerrado la conexión")
            print("El error ha sido: ",e)
            stopRecv=True
            break
    try:
        cliente.send(TERMINATED.encode(FORMAT)) #El hilo intenta avisar al servidor antes de cerrarse para que este se desconecte sin lanzar un error
    except:
        print("Se ha intentado cerrar la conexión de forma limpia") #Si no se puede, se ignora
    cliente.close()    
def CrearPartida(cliente): #Pantalla para crear una partida online. Se especifica una dificultad y se manda al servidor para que cree la partida
    TkinterClear(root,True)
    root.geometry("400x300")
    tituloDificultad=Label(root,text="Elige dificultad",font=("Times New Roman",30))
    tituloDificultad.pack(pady=10)
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
def UnirsePartida(cliente): #Pantalla para unirse a una partida online. Se manda el id de la partida al servidor para que este compruebe si se puede unir
    TkinterClear(root,True)
    root.geometry("400x300")
    tituloUnirse=Label(root,text="Unirse a una partida",font=("Times New Roman",30))
    tituloUnirse.pack(pady=10)
    promptEntrada=Label(root,text="Introduce el id de la partida")
    promptEntrada.pack(pady=5)
    promptEntrada.focus_set()
    idPartidaEntrada=Entry(root)
    idPartidaEntrada.pack(pady=5)
    botonUnirse=Button(root,text="Unirse",command=lambda:[cliente.send(("CLIENT"+idPartidaEntrada.get()).encode(FORMAT)),idPartidaEntrada.delete(0,END)])
    idPartidaEntrada.focus_set()
    idPartidaEntrada.bind("<Return>",lambda event:[cliente.send(("CLIENT"+idPartidaEntrada.get()).encode(FORMAT)),idPartidaEntrada.delete(0,END)])
    botonUnirse.pack(pady=10)
    botonVolver=Button(root,text="Volver",command=lambda:InicioOnline(cliente))
    botonVolver.pack(pady=10)
def Ahorcado(pal,cliente=None): #Pantalla del juego (se carga al principio de cada partida, y el argumento opcional "cliente" indica si se está jugando en modo online o no)
    global vidas
    global cancionActual
    vidas=6
    letrasdadas.clear()
    TkinterClear(root)
    if musica and cancionActual!="main":
        cancionActual="main"
        pygame.mixer.music.load(currdir+"\\Assets\\Musica\\mainMusic.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  
    root.geometry("600x550")
    #print(pal)
    adivinaTitulo=Label(root,text="Adivina la palabra",font=("Times New Roman",30))
    adivinaTitulo.pack(pady=10)
    palabraLabel=Label(root,text=Asterisca(pal,letrasdadas),font=("Times New Roman",15))
    palabraLabel.pack(pady=5)
    letraEntrada=Entry(root)
    letraEntrada.pack(pady=5)
    letraEntrada.focus_set()
    botonLetra=Button(root,text="Enviar",command=lambda:ProcesaLetra(pal,letraEntrada.get(),letrasdadas,palabraLabel,vidaLabel,letrasusadasLabel,letraEntrada,horcaLabel,cliente))
    botonLetra.pack(pady=10)
    letraEntrada.bind("<Return>",lambda event:ProcesaLetra(pal,letraEntrada.get(),letrasdadas,palabraLabel,vidaLabel,letrasusadasLabel,letraEntrada,horcaLabel,cliente))
    horcaLabel=Label(root,image=imagenes[6-vidas])
    horcaLabel.pack(pady=5)
    vidaLabel=Label(root,text="Vidas: "+str(vidas))
    vidaLabel.configure(fg="red")
    vidaLabel.pack(pady=5)
    letrasusadasLabel=Label(root,text=FormatLetrasUsadas(letrasdadas))
    letrasusadasLabel.pack(pady=5)
    if cliente==None:
        botonVolver=Button(root,text="Salir",command=lambda:Inicio())
        botonVolver.pack(pady=10)


def ProcesaLetra(pal,letra,letrasdadas,palabraLabel,vidaLabel,letrasusadasLabel,letraEntrada,horcaLabel,cliente=None): #Se ejecuta cada vez que el usuario envía una letra
    global vidas
    global cancionActual
    global efectosSonido
    if letra=="eumanito777": #Código debug para ganar
        for letra in pal:
            letrasdadas.append(letra)
        if cliente!=None:
            cliente.send("RESULT1".encode(FORMAT))
            return
        else:
            Finjuego(True,cliente,pal)
            return
    if letra=="flamenc0": #Código debug para perder
        vidas=0
        if cliente!=None:
            cliente.send("RESULT0".encode(FORMAT))
            return
        else:
            Finjuego(False,cliente,pal)
            return
    #Se comprueba que la letra sea válida
    if len(letra)<1:
        messagebox.showerror("Error","Introduce alguna letra")
        return
    if len(letra)>1 or not(letra.isalpha()):
        messagebox.showerror("Error","Introduce una sola letra")
        letraEntrada.delete(0,END)
        return
    if letra in letrasdadas:
        messagebox.showinfo("","Ya has introducido esa letra")
        letraEntrada.delete(0,END)
        return
    letrasdadas.append(letra.lower())
    #Ahora se comprueba si la letra está en la palabra o no
    if letra not in pal:
        cancionActual="incorrecto"
        incorrectoSonido=pygame.mixer.Sound(currdir+"\\Assets\\Musica\\incorrectoSound.mp3")
        if efectosSonido.get_busy()==False:
            efectosSonido.play(incorrectoSonido)
        vidas-=1
        if vidas==0:
            if cliente!=None:
                cliente.send("RESULT0".encode(FORMAT))
                return
            else:
                Finjuego(False,cliente,pal)
                return
        elif vidas==1:
            Pista(pal)
            
    else:
        cancionActual="correcto"
        correctoSonido=pygame.mixer.Sound(currdir+"\\Assets\\Musica\\correctoSound.mp3")
        if efectosSonido.get_busy()==False:
            efectosSonido.play(correctoSonido)        
        if Asterisca(pal,letrasdadas)==pal:
            if cliente!=None:
                cliente.send("RESULT1".encode(FORMAT))
                return
            else:
                Finjuego(True,cliente,pal)
                return
    # Se actualiza la información del GUI
    palabraLabel.config(text=Asterisca(pal,letrasdadas))
    vidaLabel.config(text="Vidas: "+str(vidas))
    horcaLabel.config(image=imagenes[6-vidas])
    letrasusadasLabel.config(text=FormatLetrasUsadas(letrasdadas))
    letraEntrada.delete(0,END)
def Pista(pal): #Busca una palabra que no se haya dicho ya y la muestra
    letrasrestantes=[]
    for letra in range(0,len(pal)-1):
        if Asterisca(pal,letrasdadas)[letra]=="*":
            letrasrestantes.append(letra)
    messagebox.showinfo("","Pista: La palabra contiene la letra: "+pal[random.choice(letrasrestantes)])
def Finjuego(gana,cliente=None,pal=None): #Se ejecuta cuando el usuario ha ganado o perdido (gana=True si ha ganado)
    global efectosSonido
    global cancionActual
    global vidas
    TkinterClear(root)
    root.geometry("400x300")
    if gana:
        ganaTitulo=Label(root,text="¡Has ganado!",font=("Times New Roman",30))
        ganaTitulo.config(fg="green")
        ganaTitulo.pack(pady=10)
        if musica and cancionActual!="gameOver":
            cancionActual="victoria"
            victoriaSonido=pygame.mixer.Sound(currdir+"\\Assets\\Musica\\victoriaMusic.mp3")
            efectosSonido.play(victoriaSonido)
    else:
        ganaTitulo=Label(root,text="¡Has perdido!",font=("Times New Roman",30))
        ganaTitulo.config(fg="red")
        ganaTitulo.pack(pady=10)
        if musica and cancionActual!="gameOver":
            cancionActual="gameOver"
            gameOverSonido=pygame.mixer.Sound(currdir+"\\Assets\\Musica\\gameOverMusic.mp3")
            efectosSonido.play(gameOverSonido)  
    if pal != None:
        palLabel=Label(root,text="La palabra era: "+pal,font=("Times New Roman",15))
        palLabel.pack(pady=5)
    if cliente!=None:
        explainLabel=Label(root,text="",font=("Times New Roman",12))
        if gana:
            if Asterisca(pal,letrasdadas)!=pal:
                explainLabel.config(text="¡El otro jugador se ha quedado sin vidas!")
                explainLabel.pack(pady=5)
        elif vidas>0:
                explainLabel.config(text="¡El otro jugador ha adivinado la palabra!")
                explainLabel.pack(pady=5)
        volverBoton=Button(root,text="Volver",command=lambda:InicioOnline(cliente))
        volverBoton.pack(pady=10)
    else:
        volverBoton=Button(root,text="Volver",command=lambda:Inicio())
        volverBoton.pack(pady=10)
def GeneraPalabra(dificultad): #Genera una palabra aleatoria de la dificultad elegida para las partidas offline (en las online las palabras se generan en el servidor)
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
        return palabraAadivinar
def InicioOffline(): #Carga la pantalla para las partidas offline (muy parecido a la de crear partida, pero sin el servidor)
    global musica
    global cancionActual
    TkinterClear(root)
    if musica and cancionActual!="menu":
        cancionActual="menu"
        pygame.mixer.music.load(currdir+"\\Assets\\Musica\\menuMusic.mp3")
        pygame.mixer.music.play(-1)
    root.geometry("400x300")
    CargaPalabras()
    tituloDificultad=Label(root,text="Elige dificultad",font=("Times New Roman",30))
    tituloDificultad.pack(pady=10)
    botonFacil=Button(root,text="Facil",command=lambda:Ahorcado(GeneraPalabra(1)))
    botonFacil.pack(pady=5)
    botonMedio=Button(root,text="Medio",command=lambda:Ahorcado(GeneraPalabra(2)))
    botonMedio.pack(pady=5)
    botonDificil=Button(root,text="Dificil",command=lambda:Ahorcado(GeneraPalabra(3)))
    botonDificil.pack(pady=5)
    explicacion=Label(root,text="Fácil: 5 letras.\nMedio: 9 letras.\nDificil: Sin limite de letras")
    explicacion.pack(pady=5)
    botonVolver=Button(root,text="Volver",command=lambda:Inicio())
    botonVolver.pack(pady=10)    
def CargaPalabras(): #Trata de cargar las palabras del archivo "diccionario.txt" si se juega offline 
    try:
        with open (currdir+"\\Assets\\diccionario.txt", "r",encoding="utf-8") as f:
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
        messagebox.showerror("Error","No se ha podido cargar la lista de palabras. Comprueba que el archivo diccionario.txt esté en la carpeta del programa")
Inicio()
root.mainloop()