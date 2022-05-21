from tkinter import *
from tkinter import messagebox
import random
#___________ Declaración de variables:
palabras = ['yellow','blue','green','red','cyan','pink','black']
palabra=[]; letras_todas = []; resultado = [] 
fallos = 1; n=5; res=True

def seguimosoNo():
    global n, res
    if(res==True):
        n=5  #intentos que te quedan
        eligePalabra()
    else:
        root.destroy() #Cerrar aplicación
    
def eligePalabra():
    global resultado,n,palabra
    palabra=list(random.choice(palabras))
    
    leftchances.configure(text='Quedan '+str(n)+' intentos')
    resultado=[]
    for i in range(len(palabra)):
        resultado.append("*")
    #Mostramos asteriscos por la etiqueta wordlabel:
    wordlabel.configure(text=resultado)
    #En la etiqueta ans ponemos un texto vacío:
    ans.configure(text='')

def hangman():
    global res, n,resultado, palabra
    #---letra_usuario guarda la letra tecleada:
    letra_usuario = letra.get()
    #Borramos el cuadro de texto donde hemos tecleado la letra:
    entrada1.delete(0,END)
    if(n>0):
        if n==2:
            #---Pista:
            ans.configure(text='Empieza por: ' + palabra[0])
        if(letra_usuario in palabra):
            for i in range(len(palabra)):
                if palabra[i] == letra_usuario:
                    resultado[i] = letra_usuario
            #Actualizamos wordlabel con las letras acertadas:
            wordlabel.configure(text=resultado)

            if resultado==palabra:
                ans.configure(text='Congratulations You won The game......')
                
                res = messagebox.askyesno("Notification",'Congratulations You won The game......\n want to play again ?')
                seguimosoNo()
            else:
                ans.configure(text='Estás a punto de conseguirlo...')
        else:
            n -= 1
            leftchances.configure(text='Quedan '+str(n)+' intentos')
    if(n<=0):
        ans.configure(text='OOps You Loss The game......')
        #Cambiamos la imagen:
        lblHorca=Label(root, image=imagen1, bd=0).place(x=600,y=150)
        #Preguntamos si queremos seguir jugando:
        res = messagebox.askyesno("Notification", 'OOps You Loss The game......\n want to play again ?')
        seguimosoNo()
   #---------------- FIN DEL MÓDULO hangman()---------------

        
#Creamos la ventana, etiquetas, etiqueta para la imagen, texto de entrada y botón:    
root = Tk()
root.geometry('800x500+300+100')
root.configure(bg='cyan')
root.title('Juego del Ahorcado')

#---------------------------  Diferentes etiquetas que aparecen en la ventana:
introlabel = Label(root,text='Welcome to Hangman Game',font=('arial',35,'bold'),bg='cyan')
introlabel.place(x=100,y=0)

wordlabel = Label(root,text='',font=('arial',55,'bold'),bg='cyan')
wordlabel.place(x=300,y=150)

leftchances = Label(root,text='',font=('arial',15,'bold'),bg='cyan')
leftchances.place(x=600,y=100)

ans = Label(root,text='',font=('arial',25,'bold'),bg='cyan')
ans.place(x=100,y=440)

#---------------------------  Imagen que debería ir variando en la función hangman:
imagen0 = PhotoImage(file="horca.gif")
imagen1 = PhotoImage(file="horca1.gif")
lblHorca=Label(root, image=imagen0, bd=0).place(x=600,y=150)


#----- Cuadro de texto de entrada para introducir la letra. La letra se almacena en la variable letra
letra = StringVar()
entrada1 = Entry(root,font=('arial',25,'bold'),relief=RIDGE,bd=5,bg='green',justify='center',fg='white',textvariable=letra)
entrada1.focus_set()
entrada1.place(x=210,y=250)
#------------------------------- Botón:
bt1 = Button(root,text='Prueba',font=('arial',15,'bold'),width=15,bd=5,bg='red',command=hangman)
bt1.place(x=300,y=350)

#------Comienzo del juego: llamamos al módulo eligePalabra()

eligePalabra()
root.mainloop()
