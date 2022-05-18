import random,sys
wlist=[]
letrasdadas=[]
vidas=5
def Asterisca(pal):
    nuevapal=""
    for i in range (0,len(pal)):
        if pal[i] not in letrasdadas:
            nuevapal+="*"
        else:
            nuevapal+=pal[i]
    return nuevapal
    
def CargaPalabras():
    with open ("diccionario.txt", "r",encoding="utf-8") as f:
        for line in f:
            if "," in line:
                line=line[:line.find(",")]
            if line.isalpha() and len(line)>1:
                wlist.append(line.strip())
        f.close()
CargaPalabras()
nombre=input("Escribe tu nombre: ")
print("Hola",nombre," ,bienvenido al juego del ahorcado")
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
print(Asterisca(palabraAadivinar))
print("Tienes 5 vidas")
while vidas>0:
    letra=input("Escribe una letra: ")
    letra=letra.lower()
    if letra in letrasdadas:
        print("Ya has escrito esta letra")
    else:
        if letra.isalpha():
            letrasdadas.append(letra)
            if letra in palabraAadivinar:
                print("La letra",letra,"está en la palabra")
                print(Asterisca(palabraAadivinar))
            else:
                print("La letra",letra,"no está en la palabra")
                vidas-=1
                print("Te quedan",vidas,"vidas")
                print(Asterisca(palabraAadivinar))
        else:
            print("Escribe una LETRA")
    if palabraAadivinar==Asterisca(palabraAadivinar):
        print("Has ganado, ¡felicidades!")
        sys.exit()
print("Lo siento, has perdido")
print("La palabra era",palabraAadivinar)
print("Suerte para la próxima!")

            
