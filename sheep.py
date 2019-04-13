#Sheep Simulaotor
#Created By Charlie Mortimer
#Verison 1.3

#TO DO
#-DO WOLF FOOD
#-DO WOLF DEATH
#-DO WOLF BABIES

#importing modules
from tkinter import *
from random import *
import time
#setup window frame
root = Tk()
root.title("Sheep And Wolf Sim")
#easy to change window height and width
width = 500
height = 500
#actual canvas componenet where everything is draw onto
canvas = Canvas(root, width = width, height = height, border=0, highlightthickness=0)
canvas.pack()
#window class which contains the grid and grid draw
class Window:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        #calculating the rows and cols
        self.rows = int(width/10)
        self.cols = int(height/10)

        self.x = 0
        self.y = 0
        #assigns the grid to a array for each cell being a section of the grid
        self.grid = []
        #drawing grid
        for i in range(self.cols):
            for i in range(self.rows):
                self.grid.append([self.canvas.create_rectangle(self.x, self.y, self.x+10, self.y+10, fill="green"),0,randint(20,80)])
                self.x+=10
            self.x=0
            self.y+=10

#sheep class
class Sheep:
    def __init__(self, canvas, width, height, grid):
        self.canvas = canvas
        self.width = width
        self.height = height
        #sheeps pos is random for everysheep
        self.x = randint(10, (self.width-10)/10)*10
        self.y = randint(10, (self.height-10)/10)*10
        self.grid = grid
        #food is 0 at start
        self.food = 0
        #if it can repoduce
        self.repo = False
        #if it is dead
        self.dead = False
        #assigns random age for alternate death scenario
        self.age = randint(80,120)
        #ticks to determine life
        self.ticks = 0
        #draws the sheep
        self.Draw_Sheep()
        #get the coords of the sheep
        self.coords = self.canvas.coords(self.id)

    def Draw_Sheep(self):
        #draws the sheep
        self.id = self.canvas.create_rectangle(self.x, self.y, self.x+10, self.y+10, fill="White")

    def update(self):
        #age plus 1 
        self.ticks += 1
        #get the coords where it is currently
        self.coords = self.canvas.coords(self.id)
        #whats overlapping the coords
        self.ol = self.canvas.find_overlapping(self.coords[0]+3, self.coords[1]+3, self.coords[2]-3, self.coords[3]-3)
        #get the fill color of the cell which was got by the overlapping
        self.c = self.canvas.itemcget(self.grid[self.ol[0]-1][0], "fill")
        #if the current age is bigger or equal to the age of death
        if self.ticks >= self.age:
            #kills the sheep
            self.canvas.delete(self.id)
            self.dead = True
        #every 8 ticks it checks if the sheep has eaten enough
        elif self.ticks%8 == 0:
            #if it hasn't then it dies
            if self.food < 3:
                self.canvas.delete(self.id)
                self.dead = True
            else:
                #if it has it eats some food
                self.food -= 1

        #if the grass is green
        if self.c == "green":
            #consume grass turning it brown and adding one to food
            self.food += 1
            self.canvas.itemconfig(self.grid[self.ol[0]-1][0], fill="brown")
        #if its food is enough to repoduce then it will
        if self.food >= 10:
            self.food -= 10
            self.repo = True
    
    #movement sub routine
    def move(self):
        #picks a random direction
        self.dir = randint(1,4)
        #moves in that direction 1:NORTH 2:EAST 3:SOUTH 4:WEST
        if self.dir == 1 and self.coords[1]-10 > 0:
            self.canvas.move(self.id, 0, -10)
        elif self.dir == 2 and self.coords[2]+10 < self.width:
            self.canvas.move(self.id, 10, 0)
        elif self.dir == 3 and self.coords[3]+10 < self.height:
            self.canvas.move(self.id, 0, 10)
        elif self.dir == 4 and self.coords[0]-10 > 0:
            self.canvas.move(self.id, -10, 0)


#Wolf Class
class Wolf:
    def __init__(self, canvas, width, height, sheep):
        self.canvas = canvas
        self.width = width
        self.height = height
        #gets the sheep array to determine target
        self.sheep = sheep
        #what sheep its targeting
        self.sn = 0
        #pathfinding vars
        self.h = False
        self.v = False
        self.z = 0

        self.inter = 10
        #random starting position
        ex = randint(0,self.width/self.inter)*self.inter
        ey = randint(0,self.height/self.inter)*self.inter
        #wolf itself (its name node becuase i made this for a pathfinding visualisation)
        self.node = self.canvas.create_rectangle(ex, ey, ex+10, ey+10, fill="#515151")
    #movement snd target lock
    def Update(self):
        #finds the oldest sheep that isnt dead
        for i in range(len(self.sheep)):
            if self.sheep[i].dead == False:
                #sets it as target
                self.sn = i
                break
        #get coords for wolf
        self.coords = self.canvas.coords(self.node)
        #gets coords for target
        try:
            self.endc = self.canvas.coords(self.sheep[self.sn].id)
        except:
            self.move = True

        #This pathfinding is very basic and alternates horizontal and vertical movement until those coords match those of target
        #horizontal movement
        if self.move == True:
            self.dir = randint(1,4)
            if self.dir == 1:
                self.canvas.move(self.node, 0, -10)
            elif self.dir == 2:
                self.canvas.move(self.node, 10, 0)
            elif self.dir == 3:
                self.canvas.move(self.node, 0, 10)
            elif self.dir == 4:
                self.canvas.move(self.node, -10, 0)
                
        elif self.h == False:
            if self.coords[0] < self.endc[0]:
                self.canvas.move(self.node, 10, 0)
            elif self.coords[0] > self.endc[0]:
                self.canvas.move(self.node, -10, 0)
            self.h = True
            self.v = False
        #vertical movement
        elif self.v == False:
            if self.coords[1] < self.endc[1]:
                self.canvas.move(self.node, 0, 10)
            elif self.coords[1] > self.endc[1]:
                self.canvas.move(self.node, 0, -10)
            self.v = True
            self.h = False
        #if ontop of target
        if self.move == False and self.coords == self.endc:
            print("Eaten")
            self.food += 10
            #KILL
            self.sheep[self.sn].dead = True
            self.canvas.delete(self.sheep[self.sn].id)

        if self.b % 9 == 0:
            if self.food < 10:
                self.dead = True
            else:
                self.food -= 5
        self.b += 1

#the window 
win = Window(canvas,width, height)
#sheep array
shep = []

#wolf array
wulv = []


def SpawnSheep():
    shep.append(Sheep(canvas, width, height, win.grid))

def SpawnWolf():
    wulv.append(Wolf(canvas, width, height, shep))


sh = Button(root, text="Spawn Sheep", command=SpawnSheep)
sh.pack(side=LEFT)

l = Label(root, text="Speed:")
w = Scale(root, from_=1, to=10, orient=HORIZONTAL)

wl = Button(root, text="Spawn Wolf", command=SpawnWolf)
wl.pack(side=LEFT)
w.pack(side=RIGHT)
l.pack(side=RIGHT)
#GAME LOOP------------------------------------------------------------------------------------------------------------
while 1:
    #update screen
    root.update()
    root.update_idletasks()

    #if sheep is not dead then move and update
    for i in range(len(shep)):
        if shep[i].dead == True:
            pass
        else:
            shep[i].move()
            shep[i].update()
    #if sheep can reproduce then do so
    for i in range(len(shep)):
        if shep[i].repo == True:
            shep.append(Sheep(canvas, width, height, win.grid))
            shep[i].repo = False
    #loop for grass regrow
    for i in range(len(win.grid)):
        #if its reached its random regrow age then itll regrow back
        if canvas.itemcget(win.grid[i][0], "fill") == "brown":
            win.grid[i][1] += 1
            if win.grid[i][1] >= win.grid[i][2]:
                canvas.itemconfig(win.grid[i][0], fill="green")
                win.grid[i][1] = 0

    #wolf update
    for i in range(len(wulv)):
        wulv[i].Update()
    
    #loop delay
    time.sleep(1/w.get())

print("You Lose")

#END---------------------------------------------------------------------------------------------------------------------------------


