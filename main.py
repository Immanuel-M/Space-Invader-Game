import pygame
import random
import math

#import mixer
from pygame import mixer

#Initialize pygame
#Needed to import pygame and for all games you create
pygame.init()
clock = pygame.time.Clock()

#create the screen and pixel dimensions
screen = pygame.display.set_mode((800,600))

#background Image
background = pygame.image.load('SpaceBackground.png')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)                 #music plays on loop

#Game title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png')
#Player placement
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
     #Enemy placement
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))           #random placement in x
    enemyY.append(random.randint(50,150))           #random placement in y
    enemyX_change.append(4)                         #speed
    enemyY_change.append(40)                        #pixel movement in Y-axis

#Bullet
#Ready - You cant see the bullet on the screen
#Fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0 #speed
bulletY_change = 10 #pixel movement in Y-axis
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game Over Tex
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250)) #display at center of screen


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True , (255,255,255))
    screen.blit(score, (x, y))

def player(x,y):
    #blit means to draw on screen)
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    #blit means to draw on screen)
    screen.blit(enemyImg[i], (x, y))

#function for firing bullet using spacebar
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10)) #bullet appears at center of spaceship

#distance formula for collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    #Condition if collision happens
    if distance < 27:
        return True
    else:
        return False


#Game Loop (Always Running) So that screen stays awake
running = True
while running:

    # Set Screen Color : RGB Background Values (0-255)
    screen.fill((120,50,180))
    #background Image(loading from upper left corner)
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        #checking if the closed button has been pressed
        if event.type == pygame.QUIT:
            running = False

        #if Keystroak is pressed, check if its right or left
        if event.type == pygame.KEYDOWN:
            #print("A keystroke has been pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5   #x-axis moving negative
            if event.key == pygame.K_RIGHT:
                playerX_change = 5    #x-axis moving positive
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #Adding sound when space is pressed
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()

                    #get the current x - coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)    


         #Condition when you release a pressed arrow key
        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Arithmetic formula for moving left and right:
    #This formula is whats used for the enemy and spaceship
    # 5 = 5 + -0.1 -> 5= 5 - 0.1
    # 5 = 5 + 0.1


    #Set player movment to corresponding keystroke
    playerX += playerX_change

    #X-Coordinate boundries set (736 is used because 64(image size) minus total x value (800))
    #(Prevents Spaceship from going out of bounds)
    if playerX  < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    #Enemy movement when it hits x - boundry
    for i in range (num_of_enemies):

        #Game Over
        if enemyY[i] > 440   : #Enemy comes within 200 pixels of the boarder
            for j in range (num_of_enemies):
                enemyY[j] = 2000 #makes sure enemies go below the screen to 2k Y pixels
            #Display Game over TEXT
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i] #moves down when hits left boundry
        elif enemyX[i] > 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i] #moves down when hits right boundry

        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #Sound when bullet hits
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bullet = 480            #resets bullet
            bullet_state = "ready"
            score_value += 1        #increase value everytime we hit enemy
            
            enemyX[i] = random.randint(0, 735) #random placement in x
            enemyY[i] = random.randint(50,150) #random placement in y


        enemy(enemyX[i], enemyY[i], i)


    #Bullet movement
    if bulletY <=0:     #resetting the bullet offscreen
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    
        

    #Call player function
    player(playerX, playerY)
    show_score(textX, textY)

    #Speed of Game
    clock.tick(60)

    #display results
    pygame.display.update() #so that updates show