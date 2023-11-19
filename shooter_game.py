#Создай собственный Шутер!
from pygame import *
from random import *

class GameSprite (sprite.Sprite):
    def __init__(self,player_image,player_x,player_y, size_x, size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed        
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() 
        if keys[K_LEFT]and self.rect.x>5:
            self.rect.x -=self.speed 
        if keys[K_RIGHT]and self.rect.x < win_width - 80:
            self.rect.x +=self.speed
    def fire (self):
        fir = Bullet("bullet .png",self.rect.centerx ,self.rect.top,70,90,-15)
        bullets.add(fir)

class Aste (GameSprite):
    def update(self):
       self.rect.y += self.speed



class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y == win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0 
            lost = lost+1


#mixer.init()
#mixer.music.load("space.mp3")
#mixer.music.play()

lost = 0
score =  0
lives = 3
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("shooter")
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))

rocket = Player("rocket.png",300,410, 50, 50,5)
monsters = sprite.Group()
bullets = sprite.Group()
astes = sprite.Group()


for i in range(1,6):
    monster = Enemy("ufo.png",randint(80,win_height - 80),-40,80,50,randint(1,3))
    monsters.add(monster)
for i in range(1,4):
    asteroid = Aste ("asteroid.png",randint(80,win_height - 80),-40,80,50,randint(2,4))
    astes.add(asteroid)

font.init()
font1 = font.SysFont("Arial",36)
font2 = font.SysFont("Arial",36)
font3 = font.SysFont("Arial",58)


clock= time.Clock()
game = True
while game: 
    FPS = 60
    clock.tick(FPS)
    window.blit(background,(0,0))
    text_lose = font1.render("пропущено:"+str(lost),20,(0,0,0))
    score_text = font2.render("сбито"+str(score),10,(0,0,0)) 
    win_text = font3.render("ВЫ ВЫИГРАЛИ!",15,(0,0,0))
    live_txt = font2.render("жизни"+str(lives),10,(0,0,0)) 
    if sprite.groupcollide(monsters,bullets,True,True): 
        score += 1
        monster = Enemy("ufo.png",randint(80,win_height - 80),-40,80,50,randint(1,3))
        monsters.add(monster)

    if sprite.spritecollide(rocket,monsters,True):  
        display.update()       
        monster.kill()         
        lost = 0
        window = display.set_mode((win_width,win_height))
        background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
        score =  0
        lives -= 1         
        rocket = Player("rocket.png",300,410, 50, 50,5)
        for i in range(1,6):
            monster = Enemy("ufo.png",randint(80,win_height - 80),-40,80,50,randint(1,3))
            monsters.add(monster)
        for i in range(1,4):
            asteroid = Aste ("asteroid.png",randint(80,win_height - 80),-40,80,50,randint(2,4))
            astes.add(asteroid)
        display.update()
    if sprite.spritecollide(rocket,astes,False):
        asteroid .kill()         
        lost = 0
        window = display.set_mode((win_width,win_height))
        background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
        score =  0
        lives -= 1
        rocket = Player("rocket.png",300,410, 50, 50,5)
        display.update()
                
    while score > 30: 
        for i in range(2,6):      
            monster = Enemy("ufo.png",80,win_height-80,40,80,50)
            monsters.add(monster)       
    if score > 80:
        monster.kill()        
        window.blit(win_text,(100,300))
        time.delay(2000)
        game = False
    if lost > 2:
        fail_text = font3.render("вас ВЫВЕРНУЛИ на ИЗНАНКУ!",15,(0,0,0))
        window.blit(fail_text,(100,300))
        time.delay(300)
        game = False
    if lives < 1 :
        game = False
    window.blit(score_text,(550,80))
    window.blit(live_txt,(550,50))
    window.blit(text_lose,(480,20))
    
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                  rocket.fire()
    
    rocket.update()
    rocket.reset()
    monsters.update()
    monsters.draw(window)
    bullets.update()
    bullets.draw(window)
    astes.update()
    astes.draw(window)
    display.update()