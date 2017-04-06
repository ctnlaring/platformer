import pygame, sys, random
from pygame.locals import *
from fractions import Fraction
from map0 import map0
from map1 import map1
import menu as dm

pygame.init()
pygame.mixer.init()
pygame.font.init
screen = pygame.display.set_mode((768, 720))
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
health=5
shots=0
misses=0
kills=0
deaths=0
bshoot=0
enbx=0
enby=0
level=map0
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 3550)
font = pygame.font.SysFont("monospace", 55)
pygame.display.set_caption('Platformer Test')
explosion=pygame.image.load("img/block.png")
explosionsnd = pygame.mixer.Sound('img/explosion.wav')
laser=pygame.mixer.Sound("img/laser.wav")
background = pygame.image.load("img/back.png")
healthlabel = font.render(str(health), 1, (255,255,255))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.image = pygame.image.load('img/man.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(x,y))
        self.rect.y = y
        self.rect.x = x
        self.xspeed = 0
        self.yspeed = 0
        self.blocks = None
        self.jumptime = 0

    def setspeed(self, x, y):
        self.xspeed = x
        self.yspeed = y

    def jump(self):
        for block in blocks:
            if self.rect.bottom == block.rect.top:
                self.jumptime = 8

    def update(self):
        if self.rect.right > 768:
            self.rect.right = 768
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.top > 720:
            self.kill()
            sys.exit()

        """for block in blocks:
            if block.rect.top >= self.rect.bottom:
                if block.rect.right >= self.rect.left:
                    if block.rect.left <= self.rect.right:"""

        if self.jumptime > 0:
            self.jumptime = self.jumptime -1
            self.yspeed = -15
        else:
            self.yspeed = 15


        self.rect.x += self.xspeed
        for block in pygame.sprite.groupcollide(blocks, players, False, False, collided = None):
            if self.rect.bottom >= block.rect.top:
                if self.xspeed > 0:
                    self.rect.right = block.rect.left
                if self.xspeed < 0:
                    self.rect.left = block.rect.right

        self.rect.y += self.yspeed
        for block in pygame.sprite.groupcollide(blocks, players, False, False, collided = None):
            if self.yspeed > 0:
                self.rect.bottom = block.rect.top
            if self.yspeed < 0:
                self.rect.top = block.rect.bottom

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('img/enemy.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(720,500))
    def update(self):
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > 768:
            self.kill()
        if self.rect.top > 720:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()

        global health
        global deaths
        self.rect.move_ip(-2,0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('img/bullet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(player.rect.x+8,player.rect.y+8))
    def update(self):
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > 768:
            self.kill()
        if self.rect.top > 720:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()

        self.rect.move_ip(8,0)
        if self.rect.right < 0:
            self.kill()

class EnBullet(pygame.sprite.Sprite):
    def __init__(self):
        super(EnBullet, self).__init__()
        self.image = pygame.image.load('img/bullet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(enbx+42,enby+128))
    def update(self):
        self.rect.move_ip(8,0)
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > 768:
            self.kill()
        if self.rect.top > 720:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Block, self).__init__()
        self.image = pygame.image.load('img/block.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(x,y))
    def update(self):
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > 768:
            self.kill()
        if self.rect.top > 720:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()


player = Player(20,592)
players = pygame.sprite.Group()
players.add(player)
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
bullets=pygame.sprite.Group()
enbullets=pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for i, linenum in enumerate(level):
    for j, blocktype in enumerate(linenum):
        if blocktype == 1:
            block = Block(j*32,i*32)
            blocks.add(block)
            all_sprites.add(block)

while True:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                screen.fill(blue)
                pygame.display.update()
                choose = dm.dumbmenu(screen, [
                    'Resume',
                    'Maps',
                    'Quit Game'], 64,64,None,32,1.4,green,red)

                if choose == 2:
                    sys.exit()
                elif choose == 1:
                    screen.fill(blue)
                    pygame.display.update()
                    choose = dm.dumbmenu(screen, [
                    'Map 1',
                    "Map2"], 64,64,None,32,1.3,green,red)
                    if choose == 0:
                        for block in blocks:
                                    block.kill()
                        level = map0
                        for i, linenum in enumerate(level):
                            for j, blocktype in enumerate(linenum):
                                if blocktype == 1:
                                    block = Block(j*32,i*32)
                                    blocks.add(block)
                                    all_sprites.add(block)
                    elif choose == 1:
                        for block in blocks:
                                    block.kill()
                        level = map1
                        for i, linenum in enumerate(level):
                            for j, blocktype in enumerate(linenum):
                                if blocktype == 1:
                                    block = Block(j*32,i*32)
                                    blocks.add(block)
                                    all_sprites.add(block)

            elif event.key == K_LCTRL:
                laser.play()
                shots+=1
                new_bullet = Bullet()
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
            if event.key == pygame.K_LEFT:
                player.setspeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.setspeed(3, 0)
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_b:
                block = Block(random.randint(0,750),random.randint(0,550))
                blocks.add(block)
                all_sprites.add(block)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.setspeed(0, 0)
            elif event.key == pygame.K_RIGHT:
                player.setspeed(0, 0)
        elif event.type == QUIT:
            sys.exit()
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)



    screen.blit(background, (0, 0))
    player.update()
    enemies.update()
    blocks.update()
    bullets.update()
    enbullets.update()
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    if pygame.sprite.groupcollide(bullets, blocks, True, True, collided = None):
        pass
    if pygame.sprite.groupcollide(bullets, enemies, True, True, collided = None):
        kills+=1
    if pygame.sprite.groupcollide(enemies, players, True, True, collided = None):
        health=0
    if health==0:
        if shots != 0 & deaths != 0:
            kdr = Fraction(kills, deaths)
            hmr = Fraction(kills, shots-kills)
        else:
            kdr = Fraction(1,1)
            hmr = Fraction(1,1)

        kdrlabel = font.render("KDR - "+str(kdr.numerator)+":"+str(kdr.denominator), 1, (255,255,255))
        hmrlabel = font.render("HMR - "+str(hmr.numerator)+":"+str(hmr.denominator), 1, (255,255,255))
        screen.blit(background, (0,0))
        screen.blit(font.render("You Failed", 1, (255,255,255)), (50,150))
        pygame.display.flip()
        sys.exit()

    pygame.display.flip()
