import pygame
from time import sleep
from sys import exit
from random import randint

# // Pygame STUFF
pygame.init()

screenSize = [1280, 720]
screen = pygame.display.set_mode((screenSize[0], screenSize[1]))
pygame.display.set_caption("hello fish")
clock = pygame.time.Clock()


class Pipe():
    def __init__(self, pipeSurf):
        self.pipeSurf = pipeSurf
        self.pipeSurf.fill((0, 255, 100))


        heightOffset = randint(-200, 185)        
        self.pipeRect = pipeSurf.get_rect(center = (screenSize[0] + 100, (screenSize[0] // 15) - 165 + heightOffset))
        self.pipeRect2 = pipeSurf.get_rect(center = (screenSize[0] + 100, (screenSize[0] // 15) + 705 + heightOffset))

                

    
class Rigidbody():
    def __init__(self, weight, useGravity):
        self.weight = weight
        self.useGravity = useGravity

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

# // Functions
def lerp(a, z, t):
    return a * (1 - t) + z * t

def DoQuitPygame():
    pygame.display.quit()
    pygame.quit()
    exit()
    


def DoInput():
    global jumping, retry
    for event in pygame.event.get():
        if event == pygame.QUIT:
            DoQuitPygame()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and alive:
                jumping = True

    pressedKeys = pygame.key.get_pressed()
    
    if pressedKeys[pygame.K_ESCAPE]:
        DoQuitPygame()
    if pressedKeys[pygame.K_r]:
        return "r"


def DoGravity():
    global gravityVelocityY, jumping
    if not jumping:
        gravityVelocityY = lerp(gravityVelocityY, gravity * playerRB.weight, 0.05) #* playerRB.weight + velocityY ** 2)
    else:
        gravityVelocityY //= 8
    return gravityVelocityY

def DoJump():
    global jumpingVelocityY, jumping, jumpingThing
    if jumping:
        #the jumpvelocity needs to = something before being lerped back to 0
        jumpingVelocityY = jumpPotential
        jumping = False
            
    jumpingVelocityY = lerp(jumpingVelocityY, 0, jumpPower)

    return jumpingVelocityY
        
def DoPlayerMovement():
    playerRect.move_ip(0, DoGravity() + DoJump()) 


def DoPipeMovement():
    for i in range(len(pipes) - 1):
        if alive:
            pipes[i].pipeRect.move_ip(pipeSpeed, 0)
            pipes[i].pipeRect2.move_ip(pipeSpeed, 0)

def DoCollisions():
    global alive
    for i in range(len(pipes) - 1):
        if playerRect.colliderect(pipes[i].pipeRect) or playerRect.colliderect(pipes[i].pipeRect2):
            alive = False 

    if playerRect.top < 0:
        playerRect.top = 0

    if playerRect.colliderect(floorRect):
        alive = False
        playerRect.bottom = floorRect.top


def DoPoint():
    global score, nowScoreDelay, lastScoreDelay
    nowScoreDelay = pygame.time.get_ticks()
    if pipes[0].pipeRect.right < playerRect.right and alive and nowScoreDelay - lastScoreDelay > 800:
        score += 1
        lastScoreDelay = pygame.time.get_ticks()
            

def DoRender():
    screen.fill((0, 155, 255))

    for i in range(len(pipes) - 1):
        if pipes[i].pipeRect.centerx < -50:
            del pipes[i]
        screen.blit(pipes[i].pipeSurf, pipes[i].pipeRect)
        screen.blit(pipes[i].pipeSurf, pipes[i].pipeRect2)

    screen.blit(floorSurf, floorRect)
      
        
    screen.blit(playerSurf, playerRect)

    scoreText = font.render(str(score), False, (255, 255, 255))
    screen.blit(scoreText, (screenSize[0]//2, 0))

    #EVERY OBJECT SHOULD HAVE A VISIBLE BOOL TO AVOID THIS
    if not alive:
        retryText = font1.render("Press \"R\" to retry\nPress \"ESCAPE\" to quit", False, (255, 255, 255))
        screen.blit(retryText, (screenSize[0]//4, screenSize[1]//2))
  
    pygame.display.update()
    clock.tick(50)


while True:
    # // Variables
    #TEXT
    fontSize = (screenSize[0] * screenSize[1]) // 7500
    font = pygame.font.SysFont("Arial", fontSize)
    font1 = pygame.font.SysFont("Arial", fontSize//2)
    score = 0
    nowScoreDelay = 0
    lastScoreDelay = 0

    #PLAYER
    playerSurf = pygame.Surface((screenSize[0] // 15, screenSize[0] // 15))
    playerSurf.fill((255, 175, 0))
    playerRect = playerSurf.get_rect(center = (screenSize[0] // 15, screenSize[0] // 15))
    alive = True

    #FLOOR
    floorSurf = pygame.Surface((screenSize[0], screenSize[0] // 15))
    floorSurf.fill((255, 255, 0))
    floorRect = floorSurf.get_rect(center = (screenSize[0] // 2, screenSize[0] - screenSize[0] * 0.425))

    #PIPE
    pipeSpeed = -5
    pipeDelay = 110
    pipes = [Pipe(pygame.Surface((screenSize[0] // 15, screenSize[0] // 2)))]


    #PHYSICS
    playerRB = Rigidbody(3, True)
    velocityX = 0
    jumpingVelocityY = 0
    gravityVelocityY = 0
    jumping = False
    jumpPotential = -20
    jumpPower = 0.0085
    if playerRB.useGravity == True:
        gravity = 9.81
    else:
        gravity = 0
        
    sleep(0.5)
    # // Game Loop
    while True:
        pipeDelay += 1
        if pipeDelay % 125 == 0 and alive == True:
            pipes.append(Pipe(pygame.Surface((screenSize[0] // 15, screenSize[0] // 2))))

        
        if DoInput() == 'r':
            break
        DoPlayerMovement()
        DoPipeMovement()
        DoCollisions()
        DoPoint()
        DoRender()
    continue