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

def Inicio():
    root.title("HGclientGUI")
    root.geometry("300x200")
    #Haz un titulo que diga: Ahorcado, céntralo y ponlo grande
    titulo=Label(root,text="Ahorcado",font=("Arial",30))
    titulo.pack(pady=10)
    #Haz un boton que diga: Iniciar partida online
    botonOnline=Button(root,text="Iniciar partida online",command=InicioOnline)
    botonOnline.pack(pady=5)
    #Haz un boton que diga: Iniciar partida offline a la derecha del boton anterior
    botonOffline=Button(root,text="Iniciar partida offline",command=InicioOffline)
    botonOffline.pack(pady=5)
    #Haz un boton que diga: Salir
    botonSalir=Button(root,text="Salir",command=lambda:root.destroy())
    botonSalir.pack(pady=10)
def InicioOnline():
    pass
def InicioOffline():
    pass
root=Tk()
Inicio()
root.mainloop()