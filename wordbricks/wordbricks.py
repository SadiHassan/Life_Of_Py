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
BOX_WIDTH = 2
BOX_HEIGHT = 4
BOX_COUNT = 700
BRICK_WIDTH = 80
BRICK_HEIGHT = 20
BRICK_COUNT = 0
SPEED = 3
WHITE = (255,255,255)
BLACK = (0,0,0)
GAME_OVER = False
SCORE = 0
BRICK_SOUND_1 = 0
BRICK_SOUND_2 = 0
PADDLE_SOUND = 0
WALL_SOUND = 0
GAME_OVER_SOUND = 0

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

    def __init__(self, file_name, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(str(file_name) , -1)
        self.rect.topleft = pos
        self.rect.width = BRICK_WIDTH
        self.rect.height = BRICK_HEIGHT
        self.alive = 0
        self.loadnow = False

    def update(self):

        global bricks
        for paddle in bricks:
            if paddle.alive == 1 and paddle.loadnow:
                paddle.image, hudai = load_image('brick_1_0.jpg' , -1)
                paddle.loadnow = False
            elif paddle.alive == 2 and paddle.loadnow:
                paddle.image, hudai = load_image('brick_2_0.jpg' , -1)
                paddle.loadnow = False
            elif paddle.alive == 3 :
                bricks.remove(paddle)

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
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('btn1.png', -1)

        self.rect[0] = PADDLE_X
        self.rect[1] = WINDOW_HEIGHT - self.rect[3] - PADDLE_GAP_WITH_BOTTOM
        self.punching = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect[0] = pos[0]
        if self.punching:
            self.rect.move_ip(5, 10)

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ball.png',-1)
        self.rect.top = WINDOW_HEIGHT - 200

    def detectCollisionPaddle(self,paddle):
        global ballDirX, ballDirY, GAME_OVER, BRICK_SOUND, GAME_OVER_SOUND
        if self.rect.colliderect(paddle):
               ballDirY = ballDirY * (-1)
               PADDLE_SOUND.play()
        if self.rect.bottom >= WINDOW_HEIGHT:
            GAME_OVER = True
            GAME_OVER_SOUND.play()

    def update(self):

        pos = pygame.mouse.get_pos()
        global ballDirX, ballDirY, WALL_SOUND
        global BRICK_COUNT, GAME_OVER, SCORE

        if self.rect.top <= 0:
            ballDirY = ballDirY*(-1)
            WALL_SOUND.play()

        if self.rect.bottom >= WINDOW_HEIGHT:
            ballDirY = ballDirY*(-1)
            WALL_SOUND.play()

        if self.rect.left <= 0:
            ballDirX = ballDirX*(-1)
            WALL_SOUND.play()

        if self.rect.right >= WINDOW_WIDTH:
            ballDirX = ballDirX*(-1)
            WALL_SOUND.play()

        flag = False

        for paddle in bricks:
            if self.rect.colliderect(paddle):
               ballDirY = ballDirY * (-1)
               if paddle.alive == 0:
                paddle.alive = 1
                BRICK_SOUND_1.play()
               elif paddle.alive == 1:
                paddle.alive = 2
                BRICK_SOUND_1.play()
               elif paddle.alive == 2:
                paddle.alive = 3
                BRICK_COUNT -= 1
                BRICK_SOUND_2.play()
                SCORE += 10
                if BRICK_COUNT == 0:
                    GAME_OVER = True
                    GAME_OVER_SOUND.play()
               paddle.loadnow = True
               break

        self.rect.left = self.rect.left + ballDirX
        self.rect.top = self.rect.top + ballDirY

def drawPaddle(paddle):
    pygame.draw.rect(SCREEN, WHITE, paddle)

def main():
    global SCREEN, BRICK_SOUND, PADDLE_SOUND, BRICK_SOUND_1, BRICK_SOUND_2, WALL_SOUND, GAME_OVER_SOUND, SCORE
    pygame.mixer.init(44100, -16, 1, 512)
    #pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

    PADDLE_SOUND = pygame.mixer.Sound('HIT.WAV')
    BRICK_SOUND_1 = pygame.mixer.Sound('BRICK1.WAV')
    BRICK_SOUND_2 = pygame.mixer.Sound('BRICK2.WAV')
    WALL_SOUND = pygame.mixer.Sound('WALL.wav')
    GAME_OVER_SOUND = pygame.mixer.Sound('GAME_OVER_SOUND.wav')

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption(NAME_OF_GAME)


    SCREEN = pygame.display.set_mode( ( WINDOW_WIDTH , WINDOW_HEIGHT ) )
    boxes = pygame.sprite.Group()
    for i in range(BOX_COUNT):
        tmp_x = random.randrange(0, WINDOW_WIDTH)
        tmp_y = random.randrange(0, WINDOW_HEIGHT)
        boxes.add(Box(WHITE, [tmp_x, tmp_y]))

    global bricks, BRICK_COUNT
    bricks = pygame.sprite.Group()

    i = j = 0
    while i < WINDOW_WIDTH:
        j = 50
        while j < WINDOW_HEIGHT*30/100:
            R = random.randrange(1, 250)
            G = random.randrange(1, 250)
            B = random.randrange(1, 250)
            bricks.add(Brick('brick_0_0.jpg', [i , j]))
            BRICK_COUNT = BRICK_COUNT + 1
            j = j + BRICK_HEIGHT + 10
        i = i + BRICK_WIDTH + 10

    background_image = pygame.image.load('img3.jpg')
    background_image_convert = background_image.convert()
    image_rect = background_image_convert.get_rect()

    ballDirX = -1
    ballDirY = -1

    paddle_ob = Paddle()
    ball_ob = Ball()
    allsprites = pygame.sprite.RenderPlain((paddle_ob,ball_ob))

    font = pygame.font.Font(None, 72)
    score_font = pygame.font.Font(None, 20)

    while True:
        #GAME_OVER = True

        SCREEN.blit(background_image_convert,image_rect)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        if GAME_OVER:

            text = font.render("Ends are forever.. :)", True, WHITE)
            text_rect = text.get_rect()
            text_x = SCREEN.get_width() / 2 - text_rect.width / 2
            text_y = SCREEN.get_height() / 2 - text_rect.height / 2
            SCREEN.blit(text, [text_x, text_y])
            boxes.update()
            boxes.draw(SCREEN)
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
            continue

        SCREEN.blit(background_image_convert,image_rect)
        ball_ob.detectCollisionPaddle(paddle_ob)
        allsprites.update()
        allsprites.draw(SCREEN)

        score_text = score_font.render("Score " + str(SCORE), True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_x = SCREEN.get_width() - score_text_rect.width - 10
        score_text_y = 0

        SCREEN.blit(score_text, [score_text_x, score_text_y])

        boxes.update()
        boxes.draw(SCREEN)

        bricks.update()
        bricks.draw(SCREEN)

        pygame.display.flip()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    main()