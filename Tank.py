import pygame as pg, sys
from pygame.locals import *
import math
import random
import time

pg.PAUSE = 0
math.PAUSE = 0
random.PAUSE = 0
time.PAUSE = 0

moveW = False
moveA = False
moveS = False
moveD = False
shoot = False
width, height = 1600, 900
white = (255, 255, 255)

mousePos = [0,0]
bullets = []
botBullets = []
destination = [random.randint(int(width//2), width), random.randint(0, height)]

tank = pg.image.load("DiepTank.png")
tank = pg.transform.smoothscale(tank, (120, 68))

botTank = pg.image.load("DiepBotTank.png")
botTank = pg.transform.smoothscale(botTank, (120, 68))

bullet = pg.image.load("bullet.png")
bullet = pg.transform.smoothscale(bullet, (30, 30))
bulletDimension = bullet.get_rect()

botBullet = pg.image.load("botBullet.png")
botBullet = pg.transform.smoothscale(botBullet, (30, 30))
botBulletDimension = botBullet.get_rect()

startTitle = pg.image.load("startTitle.png")
startTitle = pg.transform.smoothscale(startTitle, (width, height))

pg.init()
screen = pg.display.set_mode((width, height))
posX = int(width//2)
posY = int(height//2)
pos = [int(width * 0.25), int(height * 0.5)]
botPos = [int(width*0.75), int(height*0.5)]
pg.display.set_caption('Tanks')

blue = (85,206,255)
blueBackground = pg.Surface((int(width//2), height))
blueBackground.fill(blue)

red = (237, 41, 57)
redBackground = pg.Surface((int(width//2), height))
redBackground.fill(red)

green = (154, 223, 176)

white = (255, 255, 255)

font = pg.font.Font('Paul.ttf', 72)

font2 = pg.font.Font('Paul.ttf', 700)

font3 = pg.font.Font('Paul.ttf', 90)

font4 = pg.font.Font('Paul.ttf', 115)

font5 = pg.font.Font('Paul.ttf', 32)

three = font.render('3', True, white)
threeDimension = three.get_rect()

two = font.render('2', True, white)
twoDimension = two.get_rect()

one = font.render('1', True, white)
oneDimension = one.get_rect()

go = font.render('GO', True, white)
goDimension = go.get_rect()

modeText = font3.render('MODE:', True, white)
modeTextDimension = modeText.get_rect()

easy = font4.render('EASY', True, white)
easyDimension = easy.get_rect()
easyDimension[0] = int(width*0.25-easyDimension[2]//2-75)
easyDimension[1] = int(height//2-35)

medium = font4.render('MEDIUM', True, white)
mediumDimension = medium.get_rect()
mediumDimension[0] = int(width*0.5-mediumDimension[2]//2)
mediumDimension[1] = int(height//2-35)

hard = font4.render('HARD', True, white)
hardDimension = hard.get_rect()
hardDimension[0] = int(width*0.75-hardDimension[2]//2+75)
hardDimension[1] = int(height//2-35)

impossible = font4.render('IMPOSSIBLE', True, white)
impossibleDimension = impossible.get_rect()
impossibleDimension[0] = int(width*0.5-impossibleDimension[2]//2)
impossibleDimension[1] = int(height//2+130)

randomY = ['up', 'down']
randomX = ['left', 'right']

ballPos1 = [int(0+bulletDimension[2]//2 + 10), int(random.randint(0 + bulletDimension[2]//2, height))]
ballPos1Direction = [random.choice(randomY), random.choice(randomX)]
ballPos2 = [int(width-botBulletDimension[2]//2 - 10), int(random.randint(0 + botBulletDimension[2]//2, height))]
ballPos2Direction = [random.choice(randomY), random.choice(randomX)]

points = 0
botPoints = 0

mode = 0
bulletMode = 0
shootMode = 0
aimbot = False
leave = False

name = []
def menuBallBounce():
    global ballPos1, ballPos2, ballPos1Direction, ballPos2Direction
    if ballPos1Direction[0] == 'down':
        ballPos1[1] +=3
    elif ballPos1Direction[0] == 'up':
        ballPos1[1] -=3
    if ballPos1Direction[1] == 'left':
        ballPos1[0] -=3
    elif ballPos1Direction[1] == 'right':
        ballPos1[0] +=3
    if ballPos2Direction[0] == 'down':
        ballPos2[1] +=3
    elif ballPos2Direction[0] == 'up':
        ballPos2[1] -=3
    if ballPos2Direction[1] == 'left':
        ballPos2[0] -=3
    elif ballPos2Direction[1] == 'right':
        ballPos2[0] +=3
    if ballPos1[1] < 0 + bulletDimension[2]//2:
        ballPos1Direction[0] = 'down'
    elif ballPos1[1] > height - bulletDimension[2]//2:
        ballPos1Direction[0] = 'up'
    if ballPos1[0] < 0 + bulletDimension[2]//2:
        ballPos1Direction[1] = 'right'
    elif ballPos1[0] > width - bulletDimension[2]//2:
        ballPos1Direction[1] = 'left'
    if ballPos2[1] < 0 + botBulletDimension[2]//2:
        ballPos2Direction[0] = 'down'
    elif ballPos2[1] > height - botBulletDimension[2]//2:
        ballPos2Direction[0] = 'up'
    if ballPos2[0] < 0 + botBulletDimension[2]//2:
        ballPos2Direction[1] = 'right'
    elif ballPos2[0] > width - botBulletDimension[2]//2:
        ballPos2Direction[1] = 'left'
    screen.blit(bullet, ballPos1)
    screen.blit(botBullet, ballPos2)
    return ballPos1, ballPos2, ballPos1Direction, ballPos2Direction
        
        
def background():
    screen.blit(blueBackground, (0, 0))
    screen.blit(redBackground, (int(width//2), 0))
    
def point():
    global points, botPoints
    pointsText = font2.render(f'{points}', True, white)
    botPointsText = font2.render(f'{botPoints}', True, white)
    screen.blit(pointsText, (240, 70))
    screen.blit(botPointsText, (int(width*0.5 + 240), 70))
    
def movement(events):
    global pos, moveW, moveA, moveS, moveD
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                moveW = True
            if event.key == pg.K_s:
                moveA = True
            if event.key == pg.K_a:
                moveS = True
            if event.key == pg.K_d:
                moveD = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                moveW = False
            if event.key == pg.K_s:
                moveA = False
            if event.key == pg.K_a:
                moveS = False
            if event.key == pg.K_d:
                moveD = False
    if pos[1] - 3 >= 0 and moveW == True:
        pos[1]-=3
    if pos[1] + 3 <= height and moveA == True:
        pos[1]+=3
    if pos[0] - 3 >= 0 and moveS == True:
        pos[0]-=3
    if pos[0] + 3 <= int(width//2) and moveD == True:
        pos[0]+=3
    return pos, moveW, moveA, moveS, moveD

def rotate():
    global pos
    position = pg.mouse.get_pos()
    angle = math.atan2(position[1]-(pos[1]+32), position[0]-(pos[0]+26))
    tankrot = pg.transform.rotate(tank, 360-angle*57.29)
    tankpos = (pos[0]-tankrot.get_rect().width/2, pos[1]-tankrot.get_rect().height/2)
    return tankrot, tankpos

def shootBullet(events, mousePos):
    global pos, bullets, startTime2
    
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN and time.time() > startTime2 + 1:
            startTime2 = time.time()
            position = pg.mouse.get_pos()
            bullets.append([math.atan2(position[1]-(pos[1]), position[0]-(pos[0])), pos[0], pos[1]])
            
    for bulletPos in bullets:
        index = 0
        velx = math.cos(bulletPos[0])*5
        vely = math.sin(bulletPos[0])*5
        bulletPos[1]+=velx
        bulletPos[2]+=vely
        if bulletPos[1]<-64 or bulletPos[1]>width or bulletPos[2]<-64 or bulletPos[2]>height:
            bullets.pop(index)
        index+=1
        for projectile in bullets:
            bullet1 = pg.transform.rotate(bullet, 360-projectile[0]*57.29)
            screen.blit(bullet1, (projectile[1], projectile[2]))

def botMove():
    global destination, botPos
    if botPos[0] > destination[0] - 30 and botPos[0] < destination[0] + 30 and botPos[1] > destination[1] - 30 and botPos[1] < destination[1] + 30:
        destination = [random.randint(int(width//2), width), random.randint(0, height)]
    if botPos[0] < destination[0]:
        botPos[0] += mode
    else:
        botPos[0] -= mode
    if botPos[1] < destination[1]:
        botPos[1] += mode
    else:
        botPos[1] -= mode
def bot():
    global pos
    botMove()
    position = [pos[0], pos[1]]
    angle = math.atan2(position[1]-(botPos[1]+32), position[0]-(botPos[0]+26))
    botTankrot = pg.transform.rotate(botTank, 360-angle*57.29)
    botTankpos = (botPos[0]-botTankrot.get_rect().width/2, botPos[1]-botTankrot.get_rect().height/2)
    return botTankrot, botTankpos

def botShoot():
    global pos, botPos, botBullets, startTime
    
    if math.sqrt((pos[0]-botPos[0])**2+(pos[1]-botPos[1])**2) < 1000 and time.time()> startTime + shootMode:
        startTime = time.time()
        position = [pos[0], pos[1]]
        botBullets.append([math.atan2(position[1]-(botPos[1]), position[0]-(botPos[0])), botPos[0], botPos[1]])
            
    for bulletPos in botBullets:
        index = 0
        if aimbot == True:
            if bulletPos[1] < pos[0]:
                bulletPos[1]+=bulletMode
            elif bulletPos[1] > pos[0]:
                bulletPos[1]-=bulletMode
            if bulletPos[2] < pos[1]:
                bulletPos[2]+=bulletMode
            if bulletPos[2] > pos[1]:
                bulletPos[2]-=bulletMode
        else:
            velx = math.cos(bulletPos[0])*bulletMode
            vely = math.sin(bulletPos[0])*bulletMode
            bulletPos[1]+=velx
            bulletPos[2]+=vely
        if bulletPos[1]<-64 or bulletPos[1]>width or bulletPos[2]<-64 or bulletPos[2]>height:
            botBullets.pop(index)
        index+=1
        for projectile in botBullets:
            bullet1 = pg.transform.rotate(botBullet, 360-projectile[0]*57.29)
            screen.blit(bullet1, (projectile[1], projectile[2]))

def collision():
    global points, botPoints
    for bulletPos in bullets:
        if bulletPos[1] > botPos[0] - 30 and bulletPos[1] < botPos[0] + 30 and bulletPos[2] > botPos[1] - 30 and bulletPos[2] < botPos[1] + 30:
            pos[0] = int(width*0.25)
            pos[1] = int(height*0.5)
            botPos[0] = int(width*0.75)
            botPos[1] = int(height*0.5)
            bullets.clear()
            botBullets.clear()
            points+=1
            restart()
    for bulletPos in botBullets:
        if bulletPos[1] > pos[0] - 30 and bulletPos[1] < pos[0] + 30 and bulletPos[2] > pos[1] - 30 and bulletPos[2] < pos[1] + 30:
            pos[0] = int(width*0.25)
            pos[1] = int(height*0.5)
            botPos[0] = int(width*0.75)
            botPos[1] = int(height*0.5)
            bullets.clear()
            botBullets.clear()
            botPoints+=1
            restart()
def restart():
    background()
    point()
    screen.blit(tank, pos)
    screen.blit(botTank, botPos)
    screen.blit(three, (int(width//2 - threeDimension[2]//2), int(height//2 - threeDimension[3]//2)))
    pg.display.update()
    time.sleep(1)
    background()
    point()
    screen.blit(tank, pos)
    screen.blit(botTank, botPos)
    screen.blit(two, (int(width//2 - twoDimension[2]//2), int(height//2 - twoDimension[3]//2)))
    pg.display.update()
    time.sleep(1)
    background()
    point()
    screen.blit(tank, pos)
    screen.blit(botTank, botPos)
    screen.blit(one, (int(width//2 - oneDimension[2]//2), int(height//2 - oneDimension[3]//2)))
    pg.display.update()
    time.sleep(1)
    background()
    point()
    screen.blit(tank, pos)
    screen.blit(botTank, botPos)
    screen.blit(go, (int(width//2 - goDimension[2]//2), int(height//2 - goDimension[3]//2)))
    pg.display.update()
    time.sleep(1)

while leave == False:
    events = pg.event.get()
    mousePos = pg.mouse.get_pos()
    screen.fill(green)
    ballPos1, ballPos2, ballPos1Direction, ballPos2Direction = menuBallBounce()
    screen.blit(startTitle, (0, 0))
    screen.blit(modeText, (int(width//2-modeTextDimension[2]//2), int(height//2-160)))
    screen.blit(easy, (int(width*0.25-easyDimension[2]//2-75), int(height//2-35)))
    screen.blit(medium, (int(width*0.5-mediumDimension[2]//2), int(height//2-35)))
    screen.blit(hard, (int(width*0.75-hardDimension[2]//2+75), int(height//2-35)))
    screen.blit(impossible, (int(width*0.5-impossibleDimension[2]//2), int(height//2+130)))
    if mousePos[0] > easyDimension[0] and mousePos[0] < easyDimension[0] + easyDimension[2] and mousePos[1] > easyDimension[1] and mousePos[1] < easyDimension[1] + easyDimension[3]:
        pg.draw.rect(screen, white, (easyDimension[0] - 25, easyDimension[1] - 15, easyDimension[2] + 50, easyDimension[3] + 30), 7)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                mode = 2
                bulletMode = 4
                shootMode = 1.5
                leave = True
                break
    if mousePos[0] > mediumDimension[0] and mousePos[0] < mediumDimension[0] + mediumDimension[2] and mousePos[1] > mediumDimension[1] and mousePos[1] < mediumDimension[1] + mediumDimension[3]:
        pg.draw.rect(screen, white, (mediumDimension[0] - 25, mediumDimension[1] - 15, mediumDimension[2] + 50, mediumDimension[3] + 30), 7)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                mode = 3
                bulletMode = 5
                shootMode = 1
                leave = True
                break
    if mousePos[0] > hardDimension[0] and mousePos[0] < hardDimension[0] + hardDimension[2] and mousePos[1] > hardDimension[1] and mousePos[1] < hardDimension[1] + hardDimension[3]:
        pg.draw.rect(screen, white, (hardDimension[0] - 25, hardDimension[1] - 15, hardDimension[2] + 50, hardDimension[3] + 30), 7)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                mode = 5
                bulletMode = 7
                shootMode = 0.4
                leave = True
                break
    if mousePos[0] > impossibleDimension[0] and mousePos[0] < impossibleDimension[0] + impossibleDimension[2] and mousePos[1] > impossibleDimension[1] and mousePos[1] < impossibleDimension[1] + impossibleDimension[3]:
        pg.draw.rect(screen, white, (impossibleDimension[0] - 25, impossibleDimension[1] - 15, impossibleDimension[2] + 50, impossibleDimension[3] + 30), 7)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                mode = 6
                bulletMode = 9
                shootMode = 1
                aimbot = True
                leave = True
                break

    pg.display.update()

restart()
startTime = time.time()
startTime2 = time.time()
while True:
    events = pg.event.get()
    background()
    point()
    pos, moveW, moveA, moveS, moveD = movement(events)
    tankrot, tankpos = rotate()
    shootBullet(events, mousePos)
    screen.blit(tankrot, tankpos)
    collision()
    botTankrot, botTankpos = bot()
    screen.blit(botTankrot, botTankpos)
    botShoot()
    for event in events:
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
    time.sleep(0.001)