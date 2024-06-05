from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__()
        self.image = image.load(pl_im)
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def reset(self): 
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        
    def update(self):
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed  

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.y, 'bullet.png', 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        
    def update(self):
        global lost
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, 650)
            self.speed = randint(1, 4)
            lost += 1

class Bullet(GameSprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        
    def update(self):
        if self.rect.y > -30:
            self.rect.y -= self.speed 
        else:
            self.kill()


win_size_w = 700
win_size_h = 500

run = True
FPS = 60
mode = 'menu'

lost = 0
_win_ = 0
_iter_ = 181
check = 0
_lab_ = 'CLICK START'
spisok_health = []

win = display.set_mode((win_size_w, win_size_h))
background = transform.scale(image.load('galaxy.jpg'), (win_size_w, win_size_h))

display.set_caption('SHOOTER')
win_icon = image.load('icon_win.png')
display.set_icon(win_icon)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.2)
fire_music = mixer.Sound('fire.ogg')

font.init()
_font_ = font.SysFont('Calibri', 30)
_font_1 = font.SysFont('Calibri', 70)
_label_ = _font_.render('Перезарядка оружия...', True, (255,0,0))

button = GameSprite(300, 250, 'start.png', 0)
button.image = transform.scale(button.image, (150, 150))
player = Player(340, 400, 'rocket.png', 10)

bullets = sprite.Group()
enemy = sprite.Group()
asteroids = sprite.Group()

_time_ = time.Clock()

def start():
    global lost, _win_, _iter_
    lost = 0
    _win_ = 0

    for i in enemy:
        i.kill()

    for i in bullets:
        i.kill()

    for i in asteroids:
        i.kill()       
    
    for i in range(3):
        i = Enemy(randint(0, 500), randint(-50, 0), 'ufo.png', randint(1, 2))
        enemy.add(i)

    i = Enemy(randint(0,500), randint(-50,0), 'asteroid_.png', 1)     
    asteroids.add(i)

    for i in spisok_health:
        i.kill()

    x = 550
    for i in range(3):
        health = GameSprite(x, 35, 'health.png', 0)
        x += 50
        spisok_health.append(health)

start()
while run:
    if mode == 'menu':
        win.blit(background, (0,0))
        button.reset()
        label = _font_1.render(_lab_, True, (255,255,255))
        win.blit(label, (210, 170))

    elif mode == 'play':
        win.blit(background, (0,0))

        lost_label = _font_.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        check_label = _font_.render('Счёт: ' + str(_win_), True, (255, 255, 255))

        win.blit(lost_label, (20, 30))
        win.blit(check_label, (20, 70))

        for i in spisok_health:
            i.reset()

        player.reset()
        player.update()

        enemy.draw(win)
        enemy.update()

        asteroids.draw(win)
        asteroids.update()

        bullets.draw(win)
        bullets.update() 

        sprites_list = sprite.groupcollide(bullets, enemy, True, True)
        _sprites_list_ = sprite.spritecollide(player, enemy, False)
        sprites_list_1 = sprite.spritecollide(player, asteroids, False)

        if check >= 5:
            _iter_ = 0
            check = 0
            
        if sprites_list_1:
            if len(spisok_health) >= 1:
                spisok_health.pop()
                asteroids.empty()
                i = Enemy(randint(0,500), randint(-50,0), 'asteroid_.png', 1)     
                asteroids.add(i)    
            else:   
                mode = 'lose'

        if _iter_ < 180:
            win.blit(_label_, (300,300))
        
        if sprites_list:
            _win_ += 1
            i = Enemy(randint(0, 500), randint(-50, 0), 'ufo.png', randint(1, 2))
            enemy.add(i)
            
        if _sprites_list_:
            mode = 'lose'

        elif lost >= 5:
            mode = 'lose'   

        elif _win_ >= 5:
            mode = 'win'   

    elif mode == 'win':
        _lab_ = 'YOU WIN!'
        start()
        mode = 'menu'

    elif mode == 'lose':
        _lab_ = 'YOU LOSE!'
        start()
        mode = 'menu'


    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE and _iter_ > 180:
            check += 1
            player.fire() 
            fire_music.play()  
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if mode == 'menu' and button.rect.collidepoint(e.pos[0], e.pos[1]):
                mode = 'play'


    _iter_ += 1
    _time_.tick(FPS)
    display.update()
