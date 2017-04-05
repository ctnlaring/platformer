import pygame, sys, random
from pygame.locals import *
from fractions import Fraction
from map0 import map0

pygame.init()
pygame.mixer.init()
pygame.font.init
screen = pygame.display.set_mode((768, 720))
health=5
shots=0
misses=0
kills=0
deaths=0
bshoot=0
enbx=0
enby=0
jumping=0
jumptime=0
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
        self.change_x = 0
        self.change_y = 0
        self.blocks = None
        global jumping
        global jumptime

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def jump(self):
        jumping = 12
        self.change_y = -2

    def update(self):
        if self.rect.right > 768:
            self.rect.right = 768
        if self.rect.left > 768:
            self.kill()
        if self.rect.top > 720:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()

        """for block in blocks:
            if block.rect.top >= self.rect.bottom:
                if block.rect.right >= self.rect.left:
                    if block.rect.left <= self.rect.right:"""

        #self.rect.move_ip(0,1)

        self.rect.x += self.change_x
        hitlist = pygame.sprite.groupcollide(blocks, players, False, False, collided = None)
        for block in hitlist:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
        hitlist = pygame.sprite.groupcollide(blocks, players, False, False, collided = None)
        for block in hitlist:
            if self.change_y >= 0:
                self.rect.bottom = block.rect.top
            else:
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


player = Player(275,400)
players = pygame.sprite.Group()
players.add(player)
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
bullets=pygame.sprite.Group()
enbullets=pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for x in map0:
    if map0[x] == 0:
        print "nothing here"
    if map0[x] == 1:
        block = Block(x*32,550)
        blocks.add(block)
        all_sprites.add(block)

while True:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_LCTRL:
                laser.play()
                shots+=1
                new_bullet = Bullet()
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_b:
                block = Block(random.randint(0,750),random.randint(0,550))
                blocks.add(block)
                all_sprites.add(block)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_SPACE:
                jumping = 0
                player.changespeed(0, 6)
        elif event.type == QUIT:
            sys.exit()
        """elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)"""

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
        screen.blit(kdrlabel, (50,250))
        screen.blit(hmrlabel, (50,350))
        pygame.display.flip()
        pygame.time.delay(5000)
        sys.exit()

    pygame.display.flip()
