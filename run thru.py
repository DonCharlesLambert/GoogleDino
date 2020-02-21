from tkinter import *
import time
import random

def animate():
    while True:
        canvas.move(cactus, -10, 0)
        canvas.move(ground, -10, 0)
        time.sleep(0.1)
        canvas.update()

        ground_x_pos = canvas.coords(ground)[0]
        if ground_x_pos < 200:
            canvas.move(ground, 400, 0)

        cactus_x_pos = canvas.coords(cactus)[0]
        if cactus_x_pos < 0:
            canvas.move(cactus, random.randint(700, 800), 0)


def key_down(e):
    print(e.char + " was pressed")


def key_up(e):
    print(e.char + " was released")

root = Tk()
canvas = Canvas(root, width=800, height=200)
canvas.pack()

cactus_image = PhotoImage(file=r'img\Cactus\10.png')
cactus = canvas.create_image(400, 165, image=cactus_image)

ground_image = PhotoImage(file=r'img\Ground.png')
ground = canvas.create_image(600, 180, image=ground_image)

canvas.bind("<KeyPress>", key_down)
canvas.bind("<KeyRelease>", key_up)
canvas.focus_set()

root.after(0, animate)
root.mainloop()

