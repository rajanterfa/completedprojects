from turtle import *
import tkinter.messagebox
import tkinter
import random
import math
import datetime

screenMinX = -500
screenMinY = -500
screenMaxX = 500
screenMaxY = 500

class LaserBeam(RawTurtle):
    def __init__(self,canvas,x,y,direction,dx,dy):
        super().__init__(canvas)
        self.penup()
        self.goto(x,y)
        self.setheading(direction)
        self.color("Green")
        self.lifespan = 200
        self.__dx = math.cos(math.radians(direction))*2 + dx
        self.__dy = math.sin(math.radians(direction))*2 + dy
        self.shape("laser") #this shape has already been registered.

    def getLifeSpan(self):
        return self.lifespan
    def getLaserDx(self):
        return self.__dx
    def getLaserDy(self):
        return self.__dy
    def getRadius(self):
        return 4

    def laserMove(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)
        self.lifespan = self.lifespan - 1




class Ghost(RawTurtle):
    def __init__(self,canvasobj,dx,dy,x,y,size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.goto(x,y)
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        if self.__size==3:
            self.shape("blueghost.gif")
        elif self.__size==2:
            self.shape("pinkghost.gif")

    #Moves the ghost from its current position to a new position
    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    #returns the apprximate "radius" of the Ghost object
    def getRadius(self):
        return self.__size * 10 - 5
    def getGhostDx(self):
        return self.__dx
    def getGhostDy(self):
        return self.__dy
    def setGhostDx(self,newx):
        self.__dx = newx
    def setGhostDy(self,newy):
        self.__dy = newy


class FlyingTurtle(RawTurtle):
    def __init__(self,canvasobj,dx,dy,x,y,size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.color("purple")
        self.goto(x,y)
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        self.shape("turtle")
    def getFTDx(self):
        return self.__dx
    def getFTDy(self):
        return self.__dy
    def setFTDx(self,xdx):
        self.__dx = xdx
    def setFTDy(self,ydy):
        self.__dy = ydy

    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    def turboBoost(self):
        angle = self.heading()
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        self.__dx = self.__dx + x
        self.__dy = self.__dy + y

    def stopTurtle(self):
        angle = self.heading()
        self.__dx = 0
        self.__dy = 0

    def getRadius(self):
        return 2


def intersect(obj1, obj2):
    intersection = math.sqrt((obj2.xcor() - obj1.xcor())** 2 + (obj2.ycor() - obj1.ycor()) ** 2)
    centers = obj1.getRadius() + obj2.getRadius()
    if intersection < centers:
        return True
    else:
        return False




def main():

    # Start by creating a RawTurtle object for the window.
    firstwindow = tkinter.Tk()
    firstwindow.title("Turtle Saves the World!")
    canvas = ScrolledCanvas(firstwindow,600,600,600,600)
    canvas.pack(side = tkinter.LEFT)
    t = RawTurtle(canvas)

    screen = t.getscreen()
    screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
    screen.register_shape("blueghost.gif")
    screen.register_shape("pinkghost.gif")
    screen.register_shape("laser",((-2,-4),(-2,4),(2,4),(2,-4)))
    frame = tkinter.Frame(firstwindow)
    frame.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
    scoreVal = tkinter.StringVar()
    scoreVal.set("0")

    scoreTitle = tkinter.Label(frame,text="Score")
    scoreTitle.pack()
    scoreFrame = tkinter.Frame(frame,height=2, bd=1, relief=tkinter.SUNKEN)
    scoreFrame.pack()
    score = tkinter.Label(scoreFrame,height=2,width=20,textvariable=scoreVal,fg="Yellow",bg="black")
    t.ht()


    score.pack()

    livesTitle = tkinter.Label(frame, text="Extra Lives Remaining")
    livesTitle.pack()
    livesFrame = tkinter.Frame(frame,height=30,width=60,relief=tkinter.SUNKEN)
    livesFrame.pack()
    livesCanvas = ScrolledCanvas(livesFrame,150,40,150,40)
    livesCanvas.pack()
    livesTurtle = RawTurtle(livesCanvas)
    livesTurtle.ht()
    livesScreen = livesTurtle.getscreen()
    life1 = FlyingTurtle(livesCanvas,0,0,-35,0,1)
    life2 = FlyingTurtle(livesCanvas,0,0,0,0,1)
    life3 = FlyingTurtle(livesCanvas,0,0,35,0,1)
    lives = [life1, life2, life3]

    screen.tracer(10)

    #Tiny Turtle!
    flyingturtle = FlyingTurtle(canvas,0,0,(screenMaxX-screenMinX)/2+screenMinX,(screenMaxY-screenMinY)/2 + screenMinY,3)



    #A list to keep track of all the ghosts
    ghosts = []
    dead_ghosts = []

    alive_pink= []
    dead_pink = []

    lasers = []
    dead_lasers = []

    #Create some ghosts and randomly place them around the screen
    for numofghosts in range(6):
        dx = random.random()*6  - 4
        dy = random.random()*6  - 4
        x = random.random() * (screenMaxX - screenMinX) + screenMinX
        y = random.random() * (screenMaxY - screenMinY) + screenMinY

        ghost = Ghost(canvas,dx,dy,x,y,3)

        ghosts.append(ghost)



    # lasers = []
    # for numoflasers in range (6):
    #     dx =
    def play():
        #start counting time for the play function
        ##LEAVE THIS AT BEGINNING OF play()
        start = datetime.datetime.now()

        if len(dead_pink)==12:
            return tkinter.messagebox.showinfo("You Win!!", "You saved the world!")

        # Move the turtle
        flyingturtle.move()

        for time in lasers:
            if time.lifespan == 0:
                dead_lasers.append(time)
                lasers.remove(time)
            time.laserMove()

        for deadlasers in dead_lasers:
            deadlasers.goto(-screenMinX*2, -screenMinY*2)
            deadlasers.ht()


        #Move the ghosts
        for each_ghost in ghosts:
            each_ghost.move()
        for pinky in alive_pink:
            pinky.move()

        temporary = scoreVal.get()
        temporary = int(temporary)

        #when a laser hits a pink ghost
        for laser in lasers:
            for ghost in ghosts:
                if intersect (ghost,laser)==True:
                    for pink in range(2):
                        if pink == 1:
                            dx = random.random() * 2-6
                            dy = random.random() *- 2 + 6
                        else:
                            dx = random.random() *- 2 + 6
                            dy = random.random() * 2 - 6
                        x = ghost.xcor()
                        y = ghost.ycor()
                        pinky = Ghost(canvas,dx,dy,x,y,2)
                        pinky.move()
                        alive_pink.append(pinky)

                    temporary += 20
                    dead_ghosts.append(ghost)
                    ghosts.remove(ghost)
                    ghost.goto(-screenMinX*2, -screenMinY*2)
                    ghost.ht()
                    dead_lasers.append(laser)
                    lasers.remove(laser)
                    laser.goto(-screenMinX*2, -screenMinY*2)
                    laser.ht()
                    scoreVal.set(str(temporary))
        #when a laser hits a pink ghost
        for laser in lasers:
            for pinky in alive_pink:
                if intersect (pinky,laser)==True:
                    temporary += 30
                    dead_pink.append(pinky)
                    alive_pink.remove(pinky)
                    pinky.goto(-screenMinX*2, -screenMinY*2)
                    pinky.ht()
                    dead_lasers.append(laser)
                    lasers.remove(laser)
                    laser.goto(-screenMinX*2, -screenMinY*2)
                    laser.ht()
                    scoreVal.set(str(temporary))

        #when a blue ghost and tiny collide
        for ghost in ghosts:
            for life in lives:
                if intersect(ghost,flyingturtle):
                    for pink in range(2):
                        if pink == 1:
                            dx = random.random() * 2-6
                            dy = random.random() *- 2 + 6
                        else:
                            dx = random.random() *- 2 + 6
                            dy = random.random() * 2 - 6
                        x = ghost.xcor()
                        y = ghost.ycor()
                        pinky = Ghost(canvas,dx,dy,x,y,2)
                        pinky.move()
                        alive_pink.append(pinky)
                    lives.remove(life)
                    life.goto(-screenMinX*2, -screenMinY*2)
                    tkinter.messagebox.showinfo("Rough :/", "You lost a life")
                    dead_ghosts.append(ghost)
                    ghosts.remove(ghost)

                    ghost.goto(-screenMinX*2, -screenMinY*2)
                    ghost.ht()
                    flyingturtle.move()
        #when a pink ghost and tiny collide
        for pinky in alive_pink:
            for life in lives:
                if intersect (pinky,flyingturtle):
                    lives.remove(life)
                    life.goto(-screenMinX*2, -screenMinY*2)
                    tkinter.messagebox.showinfo("Rough :/", "You lost a life")
                    dead_pink.append(pinky)
                    alive_pink.remove(pinky)
                    pinky.goto(-screenMinX*2, -screenMinY*2)
                    pinky.ht()
                    flyingturtle.move()

        if len(lives) == 0:
            return tkinter.messagebox.showinfo("Ouch :/", "You lost all your lives...")



        #stop counting time for the play function
        ##LEAVE THIS AT END OF ALL CODE IN play()
        end = datetime.datetime.now()
        duration = end - start

        millis = duration.microseconds / 1000.0




        # Set the timer to go off again
        screen.ontimer(play,int(10-millis))




    # Set the timer to go off the first time in 5 milliseconds
    screen.ontimer(play, 5)

    #Turn turtle 7 degrees to the left
    def turnLeft():
        flyingturtle.setheading(flyingturtle.heading()+10)

    #Turn turtle 7 degrees to the right
    def turnRight():
        flyingturtle.setheading(flyingturtle.heading()-10)

    def fireLaser():
        laser = LaserBeam(canvas,flyingturtle.xcor(),flyingturtle.ycor(),flyingturtle.heading(),flyingturtle.getFTDx(),flyingturtle.getFTDy())
        lasers.append(laser)


    #turboBoost turtle
    def forward():
        flyingturtle.turboBoost()

    #stop Turtle
    def stop():
        flyingturtle.stopTurtle()

    #Call functions above when pressing relevant keys
    screen.onkeypress(turnRight,"Right")
    screen.onkeypress(turnLeft,"Left")
    screen.onkeypress(forward,"Up")
    screen.onkeypress(stop, "Down")
    screen.onkeypress(fireLaser,"space")


    screen.listen()
    tkinter.mainloop()



if __name__ == "__main__":
    main()
