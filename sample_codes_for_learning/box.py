import pygame, sys, random
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
 
BOX_WIDTH = 5
BOX_HEIGHT = 5
 
BOX_COUNT = 100
 
# no changes here when using sprite groups
class Box(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BOX_WIDTH, BOX_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def update(self):
        self.rect.x += 1
        self.rect.y += 2
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -1 * BOX_HEIGHT
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -1 * BOX_WIDTH
 
pygame.init()
pygame.display.set_caption('Sprite Group Example')
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
 
# this is a how sprite group is created
boxes = pygame.sprite.Group()
 
for i in range(BOX_COUNT):
    tmp_x = random.randrange(0, SCREEN_WIDTH)
    tmp_y = random.randrange(0, SCREEN_HEIGHT)
    # all you have to do is add new sprites to the sprite group
    boxes.add(Box(white, [tmp_x, tmp_y]))
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(black)
 
    # to update or blitting just call the groups update or draw
    # notice there is no for loop
    # this will automatically call the individual sprites update method
    boxes.update()
    boxes.draw(screen)
 
    pygame.display.update()
    clock.tick(20)