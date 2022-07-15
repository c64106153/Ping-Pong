#兵乓

import os
import pygame

# 遊戲初始化 + 創建視窗
Width = 1000
Height = 750
FPS=60

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((Width,Height))
screen.fill((0,0,0))
pygame.display.set_caption("兵乓")
clock = pygame.time.Clock()


# 載入圖片
background_img=pygame.image.load(os.path.join("pic","background.jpg")).convert()
screen.blit(background_img,(0,0))
ball_img=pygame.image.load(os.path.join("pic","ball.jpg")).convert()

# 載入音樂、音效
Hit=pygame.mixer.Sound(os.path.join("sound","hit.mp3"))
Hit.set_volume(0.2)
pygame.mixer.music.load(os.path.join("sound","backsound2.mp3"))
pygame.mixer.music.set_volume(0.4)

def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(None,size)
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def draw_init():
    draw_text(screen,'Press any buttom to start!',64, Width/2,Height*0.6)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                 waiting=False

pygame.display.set_icon(ball_img)

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((25,125))
        self.image.fill((255,255,0))
        self.rect=self.image.get_rect()
        self.rect.centerx = 50
        self.rect.centery = Height/2 
        self.speedy = 8
        self.score =0


    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedy

        if self.rect.top <0:
            self.rect.top = 0
        if self.rect.bottom >Height:
            self.rect.bottom = Height

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((25,125))
        self.image.fill((0,255,255))
        self.rect=self.image.get_rect()
        self.rect.centerx = Width-50
        self.rect.centery = Height/2 
        self.speedy = 8
        self.score =0


    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy

        if self.rect.top <0:
            self.rect.top = 0
        if self.rect.bottom >Height:
            self.rect.bottom = Height

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((25,25))
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.centerx = Width/2
        self.rect.centery = Height/2 
        self.speedx = 10
        self.speedy = 10
        self.hidden = False

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center=(Width/2,Height/2)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.hidden and now-self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = Width/2
            self.rect.bottom = Height /2
            self.speedx = self.nextspeedx
            self.speedy = 10
        if self.rect.top <0:
            self.rect.top = 0
            self.speedy *= -1
        if self.rect.bottom >Height:
            self.rect.bottom = Height
            self.speedy *= -1

        if self.rect.left <0:
            ball.hide()
            player2.score +=1
            self.nextspeedx=10
        if self.rect.right >Width:
            ball.hide()
            player1.score +=1
            self.nextspeedx=-10

    

all_sprites = pygame.sprite.Group()
player1 = Player1()
all_sprites.add(player1)
player2 = Player2()
all_sprites.add(player2)
ball = Ball()
all_sprites.add(ball)

pygame.mixer.music.play(-1)

running=True
show_init=True

# 遊戲迴圈
while running:
    if show_init:
        draw_init()
        show_init = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 碰撞判定
    hits=pygame.sprite.groupcollide([player1],[ball],False,False)
    for hit in hits:
         Hit.play()
         ball.speedx *=-1
    
    hits=pygame.sprite.groupcollide([player2],[ball],False,False)
    for hit in hits:
        Hit.play()
        ball.speedx *=-1

    #背景更新
    screen.fill((0,0,0))
    screen.blit(background_img,(0,0))
    draw_text(screen,'Player1: '+str(player1.score),50, Width/5,20)
    draw_text(screen,'Player2: '+str(player2.score),50, Width-200,20)  


    #gameover後重新設定
    if player1.score== 11:
        draw_text(screen,'Player1 Win!!',100, Width/2,Height/4)
        show_init=True
        all_sprites = pygame.sprite.Group()
        player1 = Player1()
        all_sprites.add(player1)
        player2 = Player2()
        all_sprites.add(player2)
        ball = Ball()
        all_sprites.add(ball)
        player1.score=0
        player2.score=0
        pygame.mixer.music.play(-1)
    
    if player2.score== 11:
        draw_text(screen,'Player2 Win!!',100, Width/2,Height/4)
        show_init=True
        all_sprites = pygame.sprite.Group()
        player1 = Player1()
        all_sprites.add(player1)
        player2 = Player2()
        all_sprites.add(player2)
        ball = Ball()
        all_sprites.add(ball)
        player1.score=0
        player2.score=0 
        pygame.mixer.music.play(-1)

    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.update()

