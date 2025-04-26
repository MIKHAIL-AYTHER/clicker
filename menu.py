from pygame import *
from random import randint

# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("menu_fone.jpg"),(win_width, win_height))

finish = False
run = True

class Button:
    pass


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False


    window.blit(background, (0, 0))





    display.update()
    time.delay(50)

