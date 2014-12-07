import pygame
from pygame.locals import *
import sys

# Global Variables
FPS = 300 # Frame per second

WINDOWWIDTH = 800
WINDOWHEIGHT = 500
LINETHICKNESS = 10
PADDLESIZE = WINDOWHEIGHT*15/100
PADDLEOFFSET = PADDLESIZE*40/100

#Color values
BLACK = (0,0,0)
WHITE = (255,255,255)

def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF,WHITE,ball)

#Draws the arena the game will be played in.
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), (LINETHICKNESS/4))

#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

def moveBall(ball,ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return  ball

#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

#Artificial Intelligence of computer player
def artificialIntelligence(ball, ballDirX, paddle2):
    #If ball is moving away from paddle, center bat
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= 1
    #if ball moving towards bat, track its movement.
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -=1
    return paddle2

#Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else: return 1


def main():

    pygame.init()

    global DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode( (WINDOWWIDTH,WINDOWHEIGHT) )
    pygame.display.set_caption('Hello Pong !!!')

    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT-PADDLESIZE)/2
    playerTwoPosition = playerOnePosition

    #Keeps track of ball direction
    ballDirX = -1
    ballDirY = -1

    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    drawArena()
    drawBall(ball)
    drawPaddle(paddle1)
    drawPaddle(paddle2)

    #pygame.mouse.set_visible(0)

    while True: #main game loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawBall(ball)
        drawPaddle(paddle1)
        drawPaddle(paddle2)

        ball = moveBall(ball,ballDirX,ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = artificialIntelligence (ball, ballDirX, paddle2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()