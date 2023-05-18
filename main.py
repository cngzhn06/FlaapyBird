import random
import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

pencere_width=479
pencere_height=459

pencere = pygame.display.set_mode((pencere_width,pencere_height))
pygame.display.set_caption('Flappy Bird')

# Font
font = pygame.font.SysFont('Bauhaus 93', 60)

#font rengi
beyaz=(255,255,255)

# zemin kaydırma    
z_scroll=0
scroll_speed=4
ucus = False
oyun_bitti = False
borugap = 150
boru_frekans= 1500 #milisaniye
son_boru= pygame.time.get_ticks() - boru_frekans
skor=0
passboru=False

# arka planlar
ap= pygame.image.load('arkaplan.png')
zemin = pygame.image.load('zeminn.png')
buton_img =pygame.image.load('restart.png')

def yazi(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    pencere.blit(img, (x,y))

def resetle():
    borular.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(pencere_height / 2)
    skor = 0
    return skor


class Kus(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'kus{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center= [x,y]
        self.vel = 0
        self.clicked=False
    def update(self):

        if ucus == True:
            #yercekimi
            self.vel +=0.5
            if self.vel >8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        self.counter += 1
        flap_cooldown = 5

        if oyun_bitti == False:
            #zıplama
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked==False:
                self.clicked=True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked=False
            if self.counter > flap_cooldown:
                self.counter=0
                self.index +=1
                if self.index >= len(self.images):
                    self.index=0
            self.image = self.images[self.index]

            #rotate
            self.image=pygame.transform.rotate(self.images[self.index],self.vel -2)

        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)

class boru(pygame.sprite.Sprite):
    def __init__(self,x ,y,pozisyon):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('boru1.png')
        self.rect = self.image.get_rect()
        #Konum 1 alttan ve aşşağında
        if pozisyon == 1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y- int(borugap / 2)]
        if pozisyon == -1:
            self.rect.topleft = [x , y + int(borugap) / 2]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0 :
            self.kill()

class buton():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):

        eylem=False

        #mouse pozisyonu
        pos = pygame.mouse.get_pos()

        #mouse kontrol
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                eylem = True

        #draw buton
        pencere.blit(self.image, (self.rect.x, self.rect.y))

        return eylem

kuslar = pygame.sprite.Group()
borular = pygame.sprite.Group()

flappy = Kus(100,int(pencere_height / 2))
kuslar.add(flappy)

#tekrar butonu yaratıyoruz

btn=buton(pencere_width//2 - 50, pencere_height//2 - 100,buton_img)
devam = True
while devam:

    clock.tick(fps)

    # arka plan
    pencere.blit(ap,(0,0))

    kuslar.draw(pencere)
    kuslar.update()
    borular.draw(pencere)

    # zemin
    pencere.blit(zemin, (z_scroll, 359))

    #skor
    if len(borular) > 0:
        if kuslar.sprites()[0].rect.left > borular.sprites()[0].rect.left\
            and kuslar.sprites()[0].rect.right < borular.sprites()[0].rect.right\
            and passboru == False:
                passboru = True
        if passboru == True:
            if kuslar.sprites()[0].rect.left > borular.sprites()[0].rect.right :
                skor +=1
                passboru=False

    yazi(str(skor),font,beyaz,int(pencere_width / 2 ),20)

    # çarpışma
    if pygame.sprite.groupcollide(kuslar,borular,False,False) or flappy.rect.top < 0:
        oyun_bitti=True

    if flappy.rect.bottom >=359:
        oyun_bitti = True
        ucus = False

    if oyun_bitti== False and ucus==True:

        #yeni boru oluşturma
        suan=pygame.time.get_ticks()
        if suan - son_boru > boru_frekans:
            boruyukseklik= random.randint(-50,50)
            btmboru = boru(pencere_width, int(pencere_height / 2) + boruyukseklik, -1)
            topboru = boru(pencere_width, int(pencere_height / 2) + boruyukseklik, 1)
            borular.add(btmboru)
            borular.add(topboru)
            son_boru = suan

        z_scroll -= scroll_speed
        if abs(z_scroll) > 35:
            z_scroll=0

        borular.update()

    # oyun bittiğinden sıfırla
    if oyun_bitti==True:
        if btn.draw() == True:
            oyun_bitti= False
            skor = resetle()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            devam=False
        if event.type == pygame.MOUSEBUTTONDOWN and ucus==False and oyun_bitti==False:
            ucus=True

    pygame.display.update()

pygame.quit()



