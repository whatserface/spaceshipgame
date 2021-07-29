#Создай собственный Шутер!
from pygame import *
from random import randint, randrange
import math
win_w, win_h = 700, 500
init()
FPS, clock = 60, time.Clock()
import time as t
window = display.set_mode((win_w, win_h))
mixer.init()
'''mixer.music.load('space.ogg')
mixer.music.play()'''
display.set_caption('ШуТаР')
engine, game = True, True
miss = 0
shot = 0
fire_sound = mixer.Sound('fire.ogg')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    score = 0
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 25, 40)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y > 500 and self.image.get_width() != 81:
            miss += 1
            self.rect.x = randrange(1, win_w, 80)
            self.rect.y = randrange(5, 30, 5)
class Bullet(GameSprite):
    var = True
    def update(self, defender, bulls):
        global shot
        global FPS
        if win_h < self.rect.y < 0:
            self.kill()
        if defender == monsters:
            self.rect.y += self.speed
            for df in defender:
                if self.rect.colliderect(df):
                    shot += 1
                    df.rect.x = randrange(1, win_w, 80)
                    df.rect.y = randrange(5, 25, 5)
                    self.kill()
        elif defender == ship:
            if self.var:
                self.px, self.py = ship.rect.center #position of ship
                self.dx, self.dy = self.px - self.rect.x, self.py - self.rect.y
                self.stepx, self.stepy = self.dx/FPS, self.dy/FPS
                self.radians = math.atan2(-self.dy, self.dx)
                self.image = transform.rotate(self.image, math.degrees(self.radians)+270)
                self.var = False
            if self.rect.y < self.py:
                self.rect.x += self.stepx
                self.rect.y += self.stepy
            else:
                self.kill()
            if self.rect.colliderect(ship.rect):
                boss.score += 1
                self.kill()
        elif defender == boss:
            self.rect.y += self.speed
            if self.rect.colliderect(boss):
                ship.score += 1
                self.kill()
class Boss(GameSprite):
    bullets = sprite.Group()
    score = 0
    def say(self):
        while self.rect.y < 0:
            self.rect.y += 3.5
            time.delay(5)
        self.f0nt = font.SysFont('Arial', 25)
        self.phrase = self.f0nt.render('FIGHT OR DIE', True, (255, 0, 0))
        window.blit(boss.phrase, (boss.rect.centerx-50, boss.rect.y + 65))
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 3, 25, 40)
        self.bullets.add(bullet)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randrange(1, win_w-74, 75), randrange(0, 45, 3), randint(1, 2), 80, 50)
    monsters.add(monster)
ship = Player('rocket.png', win_w/2, win_h-100, 5, 80, 100)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, win_w - 80), -40, randint(2, 4)/2, 81, 50)
    asteroids.add(asteroid)
f0nt = font.SysFont('Arial', 50)
b0SS_f0nt = font.SysFont('Arial', 150)
missed = f0nt.render('Пропущено: ' + str(miss), True, (255, 255, 255))
shoted = f0nt.render('Убито: ' + str(shot), True, (255, 255, 255))
loose = f0nt.render('YOU LOST', True, (153, 153, 0))
win = f0nt.render('YOU WON!', True, (252, 223, 3))
bullets = sprite.Group()
boss = Boss('ufo.png', win_w/2 - 90, -255, 0, 180, 115)
cut_scene = True
previous_time = 0
ptime = 0
life = 3
rel = False
num_fire = 0
once = True
w1n = None
while engine:
    window.blit(background, (0, 0))
    window.blit(shoted, (0, 0))
    window.blit(missed, (0, 50))
    ship.reset()
    if sprite.spritecollide(ship, asteroids, True):
        life -= 1
    if sprite.spritecollide(ship, monsters, False) or miss > 7 or life <= 0:
        game, w1n = False, False
    elif shot > 9:
        if once:
            ptime = t.time()
            once = False
            monsters.empty()
            asteroids.empty()
        if game:
            boss.bullets.draw(window)
            bullets.update(boss, bullets)
            boss.bullets.update(ship, boss.bullets)
            boss.reset()
        if cut_scene and (t.time() - ptime) < 4:
            boss.say()
            ship.score = 0
        else:
            cut_scene = False
        if not cut_scene and (t.time() - previous_time) > 1.5:
            previous_time = t.time()
            boss.fire()
        if not cut_scene and ship.score > 4:
            game, w1n = False, True
        if not cut_scene and boss.score > 1:
            game, w1n = False, False
    if game:
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update(monsters, bullets)
        if rel:
            now_time = t.time()
            if now_time - last_time < rel:
                reloading = f0nt.render("Wait, reloading...", True, (255, 0, 0))
                window.blit(reloading, (win_w/2 - 75, win_h - 60))
            else:
                num_fire = 0
                rel = False
        shoted = f0nt.render('Убито: ' + str(shot), True, (255, 255, 255))
        missed = f0nt.render('Пропущено: ' + str(miss), True, (255, 255, 255))
        rel_time, b_left = (2, 5) if monsters else (1, 1)
    else:
        if w1n:
            window.blit(win, (win_w/2-50, win_h/2-50))
        else:
            window.blit(loose, (win_w/2-50, win_h/2-50))
    for e in event.get():
        if e.type == QUIT:
            engine = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and game:
                if num_fire < b_left and not rel:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= b_left and not rel:
                    last_time = t.time()
                    rel = True
    display.update()
    clock.tick(FPS)
    time.delay(10)