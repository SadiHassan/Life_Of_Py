import sys
import pygame
import random
from pygame.locals import *
FPS = 0
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 25
PADDLE_GAP_WITH_BOTTOM = 25
PADDLE_Y = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_GAP_WITH_BOTTOM
PADDLE_X = 10
NAME_OF_GAME = 'WordBricks'
BOX_WIDTH = 1
BOX_HEIGHT = 4
BOX_COUNT = 700
BRICK_WIDTH = 80
BRICK_HEIGHT = 20
BRICK_COUNT = 1000
SPEED = 5
WHITE = (255,255,255)
BLACK = (0,0,0)

ballDirX = -SPEED
ballDirY = -SPEED

class Box(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BOX_WIDTH, BOX_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def update(self):
        self.rect.x += 0
        self.rect.y += 1
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = -1 * BOX_HEIGHT
        if self.rect.x > WINDOW_WIDTH:
            self.rect.x = -1 * BOX_WIDTH

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def update(self):
        return


def load_image(name, colorkey=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    return image, image.get_rect()

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('btn1.png', -1)

        self.rect[0] = PADDLE_X
        self.rect[1] = WINDOW_HEIGHT - self.rect[3] - PADDLE_GAP_WITH_BOTTOM
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect[0] = pos[0]
        #print self.rect
        #print pos[0], self.rect
        if self.punching:
            self.rect.move_ip(5, 10)

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ball.png',-1)
        self.rect.top = WINDOW_HEIGHT - 100

    def detectCollisionPaddle(self,paddle):
        global ballDirX, ballDirY
        #if self.rect.bottom >= paddle.rect.top and self.rect.left >= paddle.rect.left and self.rect.right <= paddle.rect.right:
        if self.rect.colliderect(paddle):
               ballDirY = ballDirY * (-1)

    def update(self):
        pos = pygame.mouse.get_pos()
        global ballDirX, ballDirY

        if self.rect.top <= 0:
            ballDirY = ballDirY*(-1)
        if self.rect.bottom >= WINDOW_HEIGHT:
            ballDirY = ballDirY*(-1)

        if self.rect.left <= 0:
            ballDirX = ballDirX*(-1)
        if self.rect.right >= WINDOW_WIDTH:
            ballDirX = ballDirX*(-1)

        flag = False
        i = 0
        for paddle in bricks:
            '''
            if ballDirY < 0:
                if self.rect.top <= paddle.rect.bottom and self.rect.top >= paddle.rect.top and self.rect.left >= paddle.rect.left and self.rect.right <= paddle.rect.right:
                    ballDirY = ballDirY * (-1)
                    bricks.remove(paddle)
                    flag = True
                    i = i + 1
            if flag:
                break

            if ballDirY > 0:
                if self.rect.bottom >= paddle.rect.top and self.rect.bottom <= paddle.rect.bottom and self.rect.left >= paddle.rect.left and self.rect.right <= paddle.rect.right:
                    ballDirY = ballDirY * (-1)
                    bricks.remove(paddle)
                    flag = True
                    i = i + 1
            if flag:
                break
            '''

            if self.rect.colliderect(paddle):
               ballDirY = ballDirY * (-1)
               bricks.remove(paddle)
               break

        self.rect.left = self.rect.left + ballDirX
        self.rect.top = self.rect.top + ballDirY
        #print "hi : " , i

def drawPaddle(paddle):
    pygame.draw.rect(SCREEN, WHITE, paddle)

def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption(NAME_OF_GAME)

    #Keeps track of ball direction
    boxes = pygame.sprite.Group()
    for i in range(BOX_COUNT):
        tmp_x = random.randrange(0, WINDOW_WIDTH)
        tmp_y = random.randrange(0, WINDOW_HEIGHT)
        # all you have to do is add new sprites to the sprite group
        boxes.add(Box(WHITE, [tmp_x, tmp_y]))

    global bricks
    bricks = pygame.sprite.Group()

    i = j = 0
    while i < WINDOW_WIDTH:
        j = 50
        while j < WINDOW_HEIGHT*40/100:
            R = random.randrange(1, 250)
            G = random.randrange(1, 250)
            B = random.randrange(1, 250)
            bricks.add(Brick((R,G,B), [i , j]))
            j = j + BRICK_HEIGHT + 10
        i = i + BRICK_WIDTH + 10


    global SCREEN
    SCREEN = pygame.display.set_mode( ( WINDOW_WIDTH , WINDOW_HEIGHT ) )

    background_image = pygame.image.load('img3.jpg')
    background_image_convert = background_image.convert()
    image_rect = background_image_convert.get_rect()


    ballDirX = -1
    ballDirY = -1
    


    paddle_ob = Paddle()
    ball_ob = Ball()
    allsprites = pygame.sprite.RenderPlain((paddle_ob,ball_ob))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            #elif event.type == pygame.locals.MOUSEMOTION:
                #mousex, mousey = event.pos
                #paddle_ob.update()


        #drawPaddle(paddle)
        #SCREEN.blit(paddle_image_convert,[PADDLE_X,PADDLE_Y])
        ball_ob.detectCollisionPaddle(paddle_ob)
        allsprites.update()
        SCREEN.blit(background_image_convert,image_rect)
        allsprites.draw(SCREEN)

        boxes.update()
        boxes.draw(SCREEN)

        bricks.update()
        bricks.draw(SCREEN)

        pygame.display.flip()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    main()
