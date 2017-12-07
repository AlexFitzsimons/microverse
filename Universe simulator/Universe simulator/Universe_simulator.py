#importing useful things
import time
import pygame
import random
import math

pygame.init()


#colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
magenta = (255,0,255)
background = (black)

colourList = [white, red, green, blue, yellow, cyan, magenta]

simulationExit = False

print("Welcome to universe simulator!\nThis is a program that allows you to create and simulate a universe using different tools. First I will show you how to set up a universe:\nLets start by setting up the spacetime.")
timeScale = int(input("Time Scale. Please enter a number. This will be the number of game seconds per real time seconds (Tgs/Trts). an invalid character will result in 1 Tgs/Trts !!!this is under construction you input doesn't matter at the moment!!!"))
if type(timeScale) != int:
    timeScale = 1
spaceScale = int(input("Space Scale. Please enter an integer. This will be the resolution of the universe in pixels (n by n pixels) recomended is 800. one pixel = 1 kilometer"))
higgsAns = input("Enable Higgs Field. (y/n) default is on. *note having this turned off will result in all particles having no mass and so no gravity and always traveling at the speed of light. !!!This kinda works at the moment but the particles still have gravity!!!")
if higgsAns == "n" or higgsAns == "N":
    higgsField = False
    speed = 3/timeScale
else:
    higgsField = True

boundary = input("Enable a Boundary at the edge of the universe(y/n)")

print("loading universe...")
time.sleep(1)

#background stuff
screen = pygame.display.set_mode((spaceScale, spaceScale))#, pygame.FULLSCREEN)
pygame.display.set_caption('screen')
screen.fill(background)

tool = "m"

class Matter(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, xVel, yVel, permanence):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

       #the x and y components of velocity
       self.xVel = xVel
       self.yVel = yVel

       self.x = 0.0
       self.y = 0.0

       self.permanence = permanence

group = pygame.sprite.Group()
massSize = 1
colourIndex = 0
f = [-1, 1]
gravConst = float(6.67408 *(10 ** -13))
massOfMass = float(100)
delayTime = 0.01
Ax = 0
Ay = 0
c = 300
#each iteration is a game frame 
while not simulationExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulationExit = True
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_END]:
            simulationExit = True
        elif pressed[pygame.K_m]:
            tool = "m"
        elif pressed[pygame.K_s]:
            tool = "s"
        elif pressed[pygame.K_g]:
            tool = "g"
        elif pressed[pygame.K_l]:
            tool = "l"
        elif pressed[pygame.K_p]:
            tool = "p"
        clicking = list(pygame.mouse.get_pressed())[0]
        if clicking == True:
            placeOfClick = pygame.mouse.get_pos()
            if tool == "m" or tool == "s":
                if (list(placeOfClick)[0] > 0 and list(placeOfClick)[1] > 0) or (list(placeOfClick)[0] < (spaceScale - massSize) and list(placeOfClick)[1] < (spaceScale - massSize)):
                    if higgsField:
                        if tool == "m":
                            speed = random.randint(0, 300)
                            xSpeed = random.randint(-speed, speed)
                            upOrDown = random.choice(f)
                            ySpeed = upOrDown * (math.sqrt((speed ** 2) - (xSpeed ** 2)))
                            permanence = False
                            print("x speed = {}, y speed ={}".format(str(xSpeed), str(ySpeed)))
                        elif tool == "s":
                            xSpeed = 0
                            ySpeed = 0
                            permanence = False
                        elif tool == "p":
                            xSpeed = 0
                            ySpeed = 0
                            permanence = True
                    else:
                        speed = 300
                        xSpeed = random.randint(-speed, speed)
                        upOrDown = random.choice(f)
                        ySpeed = upOrDown * (math.sqrt((speed ** 2) - (xSpeed ** 2)))

                    sprite = Matter(colourList[colourIndex], massSize, massSize, xSpeed, ySpeed, permanence)
                    #colourIndex += 1
                   # if colourIndex == len(colourList):
                     #   colourIndex = 0
                    sprite.rect.x = list(placeOfClick)[0] 
                    sprite.rect.y = list(placeOfClick)[1] 
                    sprite.x = float(sprite.rect.x)   
                    sprite.y = float(sprite.rect.y) 
                    
                    group.add(sprite)
    screen.fill(background)            


    for sprite in group.sprites():
        if sprite.permanence == False:
            if boundary != "n":
                if (sprite.x + massSize) >= spaceScale-5 or sprite.x <= 5:
                    sprite.xVel = -(sprite.xVel)
                elif (sprite.y + massSize) >= spaceScale-5 or sprite.y <= 5:
                    sprite.yVel = -(sprite.yVel)
            sprite.x += (sprite.xVel * delayTime)
            sprite.y += (sprite.yVel * delayTime)
            sprite.rect.x = int(sprite.x)
            if sprite.x < 0:
                sprite.x = 0
            if sprite.x > spaceScale:
                sprite.x = spaceScale

            sprite.rect.y = int(sprite.y)
            if sprite.y < 0:
                sprite.y = 0
            if sprite.y > spaceScale:
                sprite.y = spaceScale

            #print("pos {}, {}  vel {}, {}".format(str(sprite.x),str(sprite.y),str(sprite.xVel),str(sprite.yVel)))
            #sprite.rect.move_ip(int(sprite.x), int(sprite.y))
            virtualGroup = group.sprites()
            if sprite.x > spaceScale or sprite.x < 0 or sprite.y > spaceScale or sprite.y < 0:
                a = 1/0
            for otherSprite in virtualGroup:
                if sprite != otherSprite:

                    distX = float((otherSprite.x - sprite.x) * 1000000)
                    distY = float((otherSprite.y - sprite.y) * 1000000)

                    # determining acceleration
                    Ax += (gravConst * ((massOfMass ** 2) * (distX ** 2))) / massOfMass
                    Ay += (gravConst * ((massOfMass ** 2) * (distY ** 2))) / massOfMass
                 
                    print (str(Ax), str(Ay))
                
                    # determining velocity with acceleration. This is only used in the next iteration
                    if sprite.x < otherSprite.x:
                        sprite.xVel = sprite.xVel + (Ax / 1000000 * delayTime)
                    else:
                        sprite.xVel = sprite.xVel - (Ax / 1000000 * delayTime)
                    if sprite.y < otherSprite.y:
                        sprite.yVel = sprite.yVel + (Ay / 1000000 * delayTime)
                    else:
                        sprite.yVel = sprite.yVel - (Ax / 1000000 * delayTime)

                    if distX == 0 and distY == 0:
                        sprite.xVel = sprite.xVel + otherSprite.xVel
                        sprite.yVel = sprite.yVel + otherSprite.yVel
                        otherSprite.xVel = sprite.xVel
                        otherSprite.yVel = sprite.yVel                                   
        else:
            sprite.xVel = 0
            sprite.yVel = 0

                #print("x velocity = {}, y velocity = {}".format(str(sprite.xVel), str(sprite.yVel)))
    group.draw(screen)       
    time.sleep(delayTime)
    pygame.display.update()

    
pygame.quit()
quit()
