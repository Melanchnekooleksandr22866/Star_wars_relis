from pygame import *
from random import randint
import time

mixer.init()
mixer.music.load("nachalo.mp3") 
mixer.music.play()

button_images = {
    "easy": transform.scale(image.load("button_easy.png"), (300, 50)),
    "medium": transform.scale(image.load("button_easy.png"), (300, 50)),
    "hard": transform.scale(image.load("button_easy.png"), (300, 50)),
    "demon": transform.scale(image.load("button_easy.png"), (300, 50)),
    "open": transform.scale(image.load("button_easy.png"), (300, 50)),
    "without_mission": transform.scale(image.load("button_easy.png"), (300, 50))
}

music_list = {
    "easy": "easy.mp3",
    "medium": "medium.mp3",
    "hard": "hard.mp3",
    "demon": "demon.mp3",
    "open": "open.mp3",
    "without_mission": "without_mission.mp3"
}

fire_sound = mixer.Sound("laser.mp3")

score = 0
lost = 0
max_lost = 7
goal = 0
goal_list = {
    "easy": 11,
    "medium": 26,
    "hard": 51,
    "demon": 101,
    "open": 999999999999999999,
    "without_mission": 999999999999999999999
}

win_width = 700
win_height = 500

font.init()
font1 = font.Font(None, 80)
win_text = font1.render('Місія виконана!', True, (0, 255, 0))
lose_text = font1.render('        Місія проваленна!!!', True, (250, 0, 0))
font2 = font.Font(None, 36)

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

bullets = sprite.Group()

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

def draw_buttons():
    window.blit(button_images["easy"], (win_width // 2 - 150, 120))
    window.blit(button_images["medium"], (win_width // 2 - 150, 180))
    window.blit(button_images["hard"], (win_width // 2 - 150, 240))
    window.blit(button_images["demon"], (win_width // 2 - 150, 300))
    window.blit(button_images["open"], (win_width // 2 - 150, 360))
    window.blit(button_images["without_mission"], (win_width // 2 - 150, 420))
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
    elif 340 < pos[1] < 390:
        return "open"
    elif 400 < pos[1] < 450:
        return "without_mission"
    return None

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lost = lost + 1

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40

class End(GameSprite):
    def __init__(self, end_image, end_x, end_y, size_x, size_y, end_speed, fire_rate):
        super().__init__(end_image, end_x, end_y, size_x, size_y, end_speed)
        self.fire_rate = fire_rate
        self.last_shot = time.time()

    def update(self):
        if self.rect.x <= 0 or self.rect.x >= win_width - self.rect.width:
            self.speed = -self.speed
        self.rect.x += self.speed

        if time.time() - self.last_shot >= self.fire_rate:
            self.fire()
            self.last_shot = time.time()

    def fire(self):
        bullet = Bullet("pyli.png", self.rect.centerx, self.rect.bottom, 15, 40, 10)
        bullets.add(bullet)

player = Player("raketa.png", 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("monsters.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

meteors = sprite.Group()
for i in range(1, 6):
    meteor = Meteor("meteor.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    meteors.add(meteor)

init() 

background = transform.scale(image.load("background.jpg"), (win_width, win_height))
loading_screen = transform.scale(image.load("nachalo.png"), (win_width, win_height))
twow_window = transform.scale(image.load("Twowindow.jpg"), (win_width, win_height))

window = display.set_mode((win_width, win_height))
window.blit(loading_screen, (0, 0))
loading_text = font2.render("Обери складність місії:", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 150, win_height - 350))
loading_text = font2.render("Легка місія - натисніть 1", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 150, win_height - 300))
loading_text = font2.render("       Середня місія - натисніть 2", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 200, win_height - 250))
loading_text = font2.render("Важка місія - натисніть 3", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 150, win_height - 200))
loading_text = font2.render("Демон місія - натисніть 4", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 150, win_height - 150))
loading_text = font2.render("Відкритий режим - натисніть 0", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 150, win_height - 100))
loading_text = font2.render("Режим без місії - натисніть 6", 1, (255, 255, 255))
window.blit(loading_text, (win_width // 2 - 150, win_height - 50))
display.update()

game = True
finish = False
game_started = False
end = None

def two_window(level):
    two_window = display.set_mode((700, 500))
    two_window.blit(twow_window, (0, 0))
    font_two = font.Font(None, 36)
    if level == "easy":
        text_two = font_two.render("Привіт!", True, (255, 255, 255))
        two_window.blit(text_two, (300, 50))
        text_two = font_two.render("У тебе є місія", True, (255, 255, 255))
        two_window.blit(text_two, (270, 100))
        text_two = font_two.render("На нас знову напали Сітхи", True, (255, 255, 255))
        two_window.blit(text_two, (200, 150))
        text_two = font_two.render("Наша розвітка повідомляє", True, (255, 255, 255))
        two_window.blit(text_two, (195, 200))
        text_two = font_two.render("Що їх 10 кораблів", True, (255, 255, 255))
        two_window.blit(text_two, (240, 250))
        text_two = font_two.render("І ти можеш лише пропустити 7 ворогів", True, (255, 255, 255))
        two_window.blit(text_two, (135, 300))
        text_two = font_two.render("І поки ти їх не унічтожиш, не повертайся!", True, (255, 255, 255))
        two_window.blit(text_two, (120, 350))
        text_two = font_two.render("Через 9 секунд почнется гра!", True, (255, 255, 255))
        two_window.blit(text_two, (180, 450))
    elif level == "medium":
        text_two = font_two.render("Привіт!", True, (255, 255, 255))
        two_window.blit(text_two, (300, 50))
        text_two = font_two.render("У тебе є місія", True, (255, 255, 255))
        two_window.blit(text_two, (270, 100))
        text_two = font_two.render("На нас знову напали Сітхи", True, (255, 255, 255))
        two_window.blit(text_two, (200, 150))
        text_two = font_two.render("Наша розвітка повідомляє", True, (255, 255, 255))
        two_window.blit(text_two, (195, 200))
        text_two = font_two.render("Що їх 25 кораблів", True, (255, 255, 255))
        two_window.blit(text_two, (240, 250))
        text_two = font_two.render("І ти можеш лише пропустити 7 ворогів", True, (255, 255, 255))
        two_window.blit(text_two, (135, 300))
        text_two = font_two.render("І поки ти їх не унічтожиш, не повертайся!", True, (255, 255, 255))
        two_window.blit(text_two, (120, 350))
        text_two = font_two.render("Через 13 секунд почнется гра!", True, (255, 255, 255))
        two_window.blit(text_two, (180, 450))
    elif level == "hard":
        text_two = font_two.render("Привіт!", True, (255, 255, 255))
        two_window.blit(text_two, (300, 50))
        text_two = font_two.render("У тебе є місія", True, (255, 255, 255))
        two_window.blit(text_two, (270, 100))
        text_two = font_two.render("На нас знову напали Сітхи", True, (255, 255, 255))
        two_window.blit(text_two, (200, 150))
        text_two = font_two.render("Наша розвітка повідомляє", True, (255, 255, 255))
        two_window.blit(text_two, (195, 200))
        text_two = font_two.render("Що їх 50 кораблів", True, (255, 255, 255))
        two_window.blit(text_two, (240, 250))
        text_two = font_two.render("І ти можеш лише пропустити 7 ворогів", True, (255, 255, 255))
        two_window.blit(text_two, (135, 300))
        text_two = font_two.render("І поки ти їх не унічтожиш, не повертайся!", True, (255, 255, 255))
        two_window.blit(text_two, (120, 350))
        text_two = font_two.render("Через 9 секунд почнется гра!", True, (255, 255, 255))
        two_window.blit(text_two, (180, 450))
    elif level == "demon":
        text_two = font_two.render("Привіт!", True, (255, 255, 255))
        two_window.blit(text_two, (300, 50))
        text_two = font_two.render("У тебе є місія", True, (255, 255, 255))
        two_window.blit(text_two, (270, 100))
        text_two = font_two.render("На нас знову напали Сітхи", True, (255, 255, 255))
        two_window.blit(text_two, (200, 150))
        text_two = font_two.render("Наша розвітка повідомляє", True, (255, 255, 255))
        two_window.blit(text_two, (195, 200))
        text_two = font_two.render("Що їх 100 кораблів", True, (255, 255, 255))
        two_window.blit(text_two, (240, 250))
        text_two = font_two.render("І поки ти їх не унічтожиш, не повертайся!", True, (255, 255, 255))
        two_window.blit(text_two, (120, 350))
        text_two = font_two.render("І ти можеш лише пропустити 7 ворогів", True, (255, 255, 255))
        two_window.blit(text_two, (135, 300))
        text_two = font_two.render("Через 14 секунд почнется гра!", True, (255, 255, 255))
        two_window.blit(text_two, (180, 450))
    elif level == "open":
        text_two = font_two.render("Привіт!", True, (255, 255, 255))
        two_window.blit(text_two, (310, 50))
        text_two = font_two.render("Це відкритий режим", True, (255, 255, 255))
        two_window.blit(text_two, (240, 100))
        text_two = font_two.render("Тут у тебе безліч життів", True, (255, 255, 255))
        two_window.blit(text_two, (220, 150))
        text_two = font_two.render("І немає перемоги чи поразки", True, (255, 255, 255))
        two_window.blit(text_two, (190, 200))
        text_two = font_two.render("Щоб вийти з цього режиму", True, (255, 255, 255))
        two_window.blit(text_two, (200, 250))
        text_two = font_two.render("Тобі потрібно закрити вікно і все", True, (255, 255, 255))
        two_window.blit(text_two, (170, 300))
        text_two = font_two.render("Через 10 секунд почнется гра!", True, (255, 255, 255))
        two_window.blit(text_two, (190, 450))
    elif level == "without_mission":
        text_two = font_two.render("Привіт!", True, (255, 255, 255))
        two_window.blit(text_two, (300, 50))
        text_two = font_two.render("Це режим без місії", True, (255, 255, 255))
        two_window.blit(text_two, (240, 100))
        text_two = font_two.render("Де ти просто літаєш і вбиваєш Сітхів", True, (255, 255, 255))
        two_window.blit(text_two, (160, 150))
        text_two = font_two.render("Тут Сітхів безліч", True, (255, 255, 255))
        two_window.blit(text_two, (250, 200))
        text_two = font_two.render("Тому виграти не вийде", True, (255, 255, 255))
        two_window.blit(text_two, (210, 250))
        text_two = font_two.render("У тебе 7 життів, як і в місіях", True, (255, 255, 255))
        two_window.blit(text_two, (190, 300))
        text_two = font_two.render("Через 10 секунд почнется гра!", True, (255, 255, 255))
        two_window.blit(text_two, (180, 450))
    display.update()
    time.sleep(5 if level == "easy" else 9 if level == "medium" else 5 if level == "hard" else 10 if level == "demon" else 6 if level == "open" else 6 if level == "without_mission" else 15)
    two_window.fill((255, 255, 255))
    display.update()

    for i in range(3, 0, -1):
        window.fill((0, 0, 0))
        text_countdown = font1.render(str(i), True, (255, 255, 255))
        window.blit(text_countdown, (win_width // 2 - 20, win_height // 2 - 20))
        display.update()
        time.sleep(1)

    window.fill((0, 0, 0))
    text_go = font1.render("Go!", True, (255, 255, 255))
    window.blit(text_go, (win_width // 2 - 45, win_height // 2 - 20))
    display.update()
    time.sleep(1)

    return

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            pos = mouse.get_pos()
            level = check_button_click(pos)
            if level:
                goal = goal_list[level]
                mixer.music.load(music_list[level])  
                mixer.music.play()
                two_window(level)
                game_started = True
                finish = False
                window.blit(background, (0, 0))
                display.update()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    
    if not game_started:
        draw_buttons()

    if game_started:
        if not finish:
            window.blit(background, (0, 0))

            text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))

            text_lost = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lost, (10, 50))

            player.update()
            if end:
                end.update()
                end.reset()
                if sprite.spritecollide(player, bullets, True):
                    lost += 1
                if lost >= max_lost:
                    finish = True
                    window.blit(lose_text, (win_width // 3 - 250, win_height // 2 - 50))
                    display.update()
                    time.sleep(3)
                    game = False
                elif score >= goal:
                    finish = True
                    window.blit(win_text, (win_width // 2 - 200, win_height // 2 - 50))
                    display.update()
                    time.sleep(3)
                    game = False
            else:
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

                if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, meteors, True):
                    lost += 2

                if score >= goal:
                    end = End("raketa.png", win_width // 2 - 50, 50, 100, 100, 5, 1)
                elif lost >= max_lost:
                    end = End("raketa_lose.png", win_width // 2 - 50, 50, 100, 100, 5, 1)
            time.sleep(0.05)
