from pygame import *
from random import randint
import time

mixer.init()

music_dict = {
    "easy": "easy.mp3",
    "medium": "medium.mp3",
    "hard": "hard.mp3",
    "demon": "demon.mp3",
}

fire_sound = mixer.Sound("laser.mp3")

score = 0
lost = 0
max_lost = 7
goal = 0
goal_dict = {
    "easy": 11,
    "medium": 26,
    "hard": 51,
    "demon": 101,
}

win_width = 700
win_height = 500

font.init()
font1 = font.Font(None, 80)
win_text = font1.render('Місія виконана!', True, (0, 255, 0))
lose_text = font1.render('Місія провалена!', True, (250, 0, 0))
font2 = font.Font(None, 36)

# Класи ігрових об'єктів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("pyli.png", self.rect.centerx, self.rect.top, 15, 40, -25)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lost += 1

bullets = sprite.Group()

# Ігрові змінні
player = Player("raketa.png", 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
meteors = sprite.Group()

# Ініціалізація екрана
init()
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

button_images = {
    "easy": transform.scale(image.load("button_easy.png"), (300, 50)),
    "medium": transform.scale(image.load("button_easy.png"), (300, 50)),
    "hard": transform.scale(image.load("button_easy.png"), (300, 50)),
    "demon": transform.scale(image.load("button_easy.png"), (300, 50)),
}

def draw_buttons():
    window.blit(button_images["easy"], (win_width // 2 - 150, 120))
    window.blit(button_images["medium"], (win_width // 2 - 150, 180))
    window.blit(button_images["hard"], (win_width // 2 - 150, 240))
    window.blit(button_images["demon"], (win_width // 2 - 150, 300))
    
    easy_text = font2.render("Легка", 1, (255, 255, 255))
    medium_text = font2.render("Середня", 1, (255, 255, 255))
    hard_text = font2.render("Важка", 1, (255, 255, 255))
    demon_text = font2.render("Демон", 1, (255, 255, 255))

    window.blit(easy_text, (win_width // 2 - 50, 130))
    window.blit(medium_text, (win_width // 2 - 50, 190))
    window.blit(hard_text, (win_width // 2 - 50, 250))
    window.blit(demon_text, (win_width // 2 - 50, 310))
    display.update()

def check_button_click(pos):
    if 100 < pos[1] < 150:
        return "easy"
    elif 160 < pos[1] < 210:
        return "medium"
    elif 220 < pos[1] < 270:
        return "hard"
    elif 280 < pos[1] < 330:
        return "demon"
    return None

game = True
game_started = False
goal = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            pos = mouse.get_pos()
            if not game_started:
                level = check_button_click(pos)
                if level:
                    goal = goal_dict[level]
                    mixer.music.load(music_dict[level])
                    mixer.music.play()
                    game_started = True
                    lost = 0
                    score = 0
                    monsters.empty()
                    meteors.empty()
                    for i in range(1, 6):
                        monster = Enemy("monsters.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                        monsters.add(monster)
                    for i in range(1, 6):
                        meteor = Enemy("meteor.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                        meteors.add(meteor)
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    fire_sound.play()
                    player.fire()
                elif e.key == K_ESCAPE:
                    game = False

    if not game_started:
        draw_buttons()
    else:
        window.blit(background, (0, 0))
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lost = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        player.update()
        monsters.update()
        meteors.update()
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy("monsters.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        monsters.draw(window)
        meteors.draw(window)
        bullets.draw(window)
        player.reset()
        display.update()

        if score >= goal:
            window.blit(win_text, (win_width // 2 - 200, win_height // 2 - 50))
            display.update()
            time.sleep(3)
            game_started = False
        elif lost >= max_lost:
            window.blit(lose_text, (win_width // 2 - 200, win_height // 2 - 50))
            display.update()
            time.sleep(3)
            game_started = False
    time.sleep(0.05)

quit()
