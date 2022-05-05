import pynput

a=input()
teclado=pynput.keyboard.Controller()
for i in range(6):
    teclado.press("0")
    teclado.release("0")
teclado.press("1")
teclado.release("1")