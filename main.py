from tkinter import *
import time
import random


class DinoGame(object):
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(self.root, width=800, height=200)

        self.dino = Dino(self.canvas, (10, 150))

        self.cacti = []
        self.cactus_image = PhotoImage(file=r'img\Cactus\10.png')

        self.old_background = None
        self.bg_image = PhotoImage(file=r'img\Ground.png')
        self.background = self.canvas.create_image(0, 180, image=self.bg_image, anchor="nw")

        self.canvas.bind("<KeyPress>", self.key_down)
        self.canvas.bind("<KeyRelease>", self.key_up)
        self.canvas.pack()
        self.canvas.focus_set()
        self.root.after(0, self.animation)

    def animate_cactus(self):
        will_generate = random.randint(0, 100)
        if will_generate < 2:
            self.cacti.append(
                self.canvas.create_image(800, 150, image=self.cactus_image, anchor="nw")
            )
        for cactus in self.cacti:
            self.canvas.move(cactus, -10, 0)
            pos = self.canvas.coords(cactus)
            if pos[0] < 0:
                del cactus

    def animate_background(self):
        self.canvas.move(self.background, -10, 0)
        if self.old_background is not None:
            self.canvas.move(self.old_background, -10, 0)
        ground_pos = self.canvas.coords(self.background)
        if ground_pos[0] < -380:
            self.old_background = self.background
            self.background = self.canvas.create_image(800, 180, image=self.bg_image, anchor="nw")

    def key_down(self, e):
        self.dino.move(e.char)

    def key_up(self, e):
        self.dino.change_state("run")

    def animation(self):
        while True:
            self.dino.animate()
            self.animate_background()
            self.animate_cactus()
            time.sleep(0.05)
            if self.collision():
                exit()
            # check collision

    def collision(self):
        for cactus in self.cacti:
            pos = self.canvas.coords(cactus)
            if pos[0] - 15 <= self.dino.pos[0] <= pos[0]:
                if pos[1] - 40 <= self.dino.pos[1] <= pos[1]:
                    return True
        return False


class Dino:
    RUN = ["0", "1", "2", "3"]
    CROUCH = ["5", "6"]
    JUMP = ["0"]
    DEATH = ["4"]

    def __init__(self, canvas, pos):
        self.sprite = PhotoImage(file=r'img\Dinosaur\0.png')
        self.dino = canvas.create_image(pos, image=self.sprite, anchor="nw")
        self.base_height = pos[1]
        self.pos = canvas.coords(self.dino)
        self.animation_number = 0
        self.direction = 3
        self.speed = 7.5
        self.score = 0
        self.state = 'run'
        self.canvas = canvas

    def move(self, button):
        if button == "w" and self.pos[1] == self.base_height:
            self.change_state("jump")
        if button == "s" and not self.is_state("crouch"):
            self.change_state("crouch")
        self.canvas.update()

    def is_state(self, check):
        if self.state == check:
            return True
        return False

    def change_state(self, state):
        self.state = state
        self.animation_number = 0

    def animate_jump(self):
        jump_height = self.base_height - 75
        if self.is_state("jump") and self.pos[1] > jump_height:
            self.canvas.move(self.dino, 0, -15)

        elif self.base_height > self.pos[1] >= jump_height:
            self.change_state("run")
            self.canvas.move(self.dino, 0, 5)

        elif self.pos[1] == self.base_height:
            # self.change_state("run")
            pass

        self.pos = self.canvas.coords(self.dino)

    def animate(self):
        animation_list = self.RUN
        if self.is_state("jump"):
            animation_list = self.JUMP
        if self.is_state("crouch"):
            animation_list = self.CROUCH

        self.sprite = PhotoImage(file=r'img\Dinosaur\\' + animation_list[self.animation_number] + ".png")
        self.animation_number = (self.animation_number + 1) % len(animation_list)
        self.canvas.itemconfig(self.dino, image=self.sprite)
        self.animate_jump()
        self.canvas.update()

'''
class Bird:
    def __init__(self, canvas):
        self.sprite = PhotoImage(file=r'images\cheese.png')
        self.sprite = self.sprite.subsample(35, 35)
        self.cheese = canvas.create_image(random.randint(0, 375), random.randint(0, 375),
                                          image=self.sprite, anchor="nw")
        self.size = (self.sprite.width(), self.sprite.height())
        self.pos = canvas.coords(self.cheese)
        self.canvas = canvas

    def get_ate(self):
        self.canvas.delete(self.cheese)
'''

root = Tk()
# add a menu?
DinoGame(root)
# add a multiplayer option to og game
# add a single player maze game
root.mainloop()
