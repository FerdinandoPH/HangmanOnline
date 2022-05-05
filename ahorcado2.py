try:
    import os, random, time,sys,unidecode
except:
    import os, random, time,sys
    os.system("pip install unidecode")
    print("Unidecode instalado. Reinicia el programa")
    a=input("Pulsa enter para cerrar el programa")
    sys.exit()
wlist=[]
letrasdadas=[]
vidas=6
currdir=os.path.dirname(os.path.abspath(__file__))
def CargaPalabras():
    with open (currdir+"\\diccionario.txt", "r",encoding="utf-8") as f:
        for line in f:
            if "," in line:
                line=line[:line.find(",")]
            if line.isalpha() and len(line)>1:
                wlist.append(unidecode.unidecode(line.strip()))
        f.close()
def Asterisca(pal):
    nuevapal=""
    for i in range (0,len(pal)):
        if pal[i] not in letrasdadas:
            nuevapal+="*"
        else:
            nuevapal+=pal[i]
    return nuevapal
    
CargaPalabras()
#Create ascii art for the hangman game
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''']
print("Bievenido al")
print("*********************************************************")
print("                 JUEGO DEL AHORCADO                      ")     
print("*********************************************************")               
print("¿Qué dificultad quieres?")
print("1.Facil (hasta 5 letras)")
print("2.Medio (hasta 9 letras)")
print("3.Dificil (sin límite)")
dificultad=int(input("Elige una opción (1,2,3): "))
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
print("Tienes 6 vidas")
while vidas>0:
    print(HANGMAN_PICS[6-vidas])
    print("\n")
    print("Palabra: ",Asterisca(palabraAadivinar))
    print("Letras usadas: ",letrasdadas)
    letra=input("Escribe una letra: ")
    letra=letra.lower()
    if letra in letrasdadas:
        print("Ya has escrito esta letra")
    else:
        if letra.isalpha():
            letrasdadas.append(letra)
            if letra in palabraAadivinar:
                print("La letra",letra,"está en la palabra")
            else:
                print("La letra",letra,"no está en la palabra")
                vidas-=1
                print("Te quedan",vidas,"vidas")
        else:
            print("Escribe una LETRA")
    if palabraAadivinar==Asterisca(palabraAadivinar):
        print("¡Sí, la palabra era",palabraAadivinar,"!")
        print("Has ganado, ¡felicidades!")
        sys.exit()
    time.sleep(0.5)
print(HANGMAN_PICS[6])
print("Lo siento, has perdido")
print("La palabra era",palabraAadivinar)
print("Suerte para la próxima!")                           