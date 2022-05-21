import time
nombre=input("como te llamas ")
print("hola, "+nombre," es hora de jugar")
print(" ")
time.sleep(1)
print("comienza a adivinar")
time.sleep(0.5)
palabra="esternocleidomastoideo"
tupalabra=" "
vidas=5

while vidas > 0:
    fallos=0
    for letra in palabra:
        if letra in tupalabra:
            print(letra,end="")
        else:
            print("*",end="")
            fallos+=1
    if fallos==0:
        input()
        print("")
        print("felicidades, has ganado")
        input()
        break

    tuletra=input("introduce una letra: ")
    tupalabra+=tuletra

    if tuletra not in palabra:
        vidas-=1
        print("letra incorrecta")
        print("Te quedan ",+vidas," vidas")
    if vidas== 0:
        print("has perdido :(")
else:
    input()
    print("gracias por participar")
    input()
