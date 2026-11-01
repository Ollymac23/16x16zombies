import pygame
from pathlib import Path
import random as rand


pygame.init()
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True
stuck = False
timeBegin = 0
highScore = 0



ASSETS = Path(__file__).resolve().parent.parent / "assets"
SCALE = 2
ZOMBIE_COUNT = 6
distMove = 32
TILE = 32
KEY_MOVES = {
    pygame.K_w: (0, -distMove), pygame.K_UP: (0, -distMove),
    pygame.K_a: (-distMove, 0), pygame.K_LEFT: (-distMove, 0),
    pygame.K_s: (0, distMove), pygame.K_DOWN: (0, distMove),
    pygame.K_d: (distMove, 0), pygame.K_RIGHT: (distMove, 0)
    
}
REPEAT_DELAY = 150
ROCK_COUNT = 72
WEB_COUNT = 8
moveTimer = 150
state = "mainMenu"

PLAYER_IMAGES = [
    pygame.transform.scale_by(
    pygame.image.load(ASSETS / f"Player{i}.png").convert_alpha(), SCALE
    )
    for i in range(4)
    ]

def GenerateMove():
    direction = rand.randint(0, 3)
    match direction:
        case 0:
            move = (0, -distMove)
        case 1:
            move = (distMove, 0)
        case 2:
            move = (0, distMove)
        case 3:
            move = (-distMove, 0)
    return move

def GeneratePos():
    x = (rand.randint(0, 15))*TILE
    y = (rand.randint(0, 15))*TILE

    return (x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.health = 3
        self.image = PLAYER_IMAGES[self.health]
        self.rect = self.image.get_rect(center=(width, height))
        self.pos = pygame.Vector2(self.rect.center)


    def update(self):
        self.pos = pygame.Vector2(self.rect.center)
        self.image = PLAYER_IMAGES[self.health]
        self.rect = self.image.get_rect(center=self.pos)
        if pygame.sprite.spritecollide(player, finishFlag, False):
            FinishGame()

        if pygame.sprite.spritecollide(player, zombies, False):
            self.health -= 1


    def move(self, dx, dy):
        global stuck
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollide(player, obstacles, False):
            self.rect.x -= dx
            self.rect.y -= dy
        if pygame.sprite.spritecollide(player, webs, False):
            stuck = True
        if 0 > self.rect.x or self.rect.x > 510:
            self.rect.x -= dx
        if 0 > self.rect.y or self.rect.y > 510:
            self.rect.y -= dy


class Web(pygame.sprite.Sprite):
    def __init__(self, tilex, tiley, image=None):
        super().__init__()
        if image is None:
            image = pygame.Surface((TILE, TILE))
            image.fill((200, 200, 200))
        self. image = image
        self.rect = self.image.get_rect(topleft=(tilex*TILE, tiley*TILE))


class Rock(pygame.sprite.Sprite):
    def __init__(self, tilex, tiley, image=None):
        super().__init__()
        if image is None:
            image = pygame.Surface((TILE, TILE))
            image.fill((60, 60, 60))
        self.image = image
        self.rect = self.image.get_rect(topleft=(tilex*TILE, tiley*TILE))


class Zombie(pygame.sprite.Sprite):
    def __init__(self, image=None):
        super().__init__()
        if image is None:
            image = pygame.Surface((TILE, TILE))
            image.fill((64, 150, 64))
        self.image = image
        self.rect = self.image.get_rect()
        pos = GeneratePos()
        while pos in rocks:
            pos = GeneratePos()
        self.rect.topleft = pos


    def move(self):

        dx, dy = GenerateMove()

        self.rect.x += dx
        self. rect.y += dy

        while pygame.sprite.spritecollide(self, obstacles, False) or self.rect.x < 0 or self.rect.x > 510 or self.rect.y < 0 or self.rect.y > 510:
            self.rect.x -= dx
            self.rect.y -= dy

            dx, dy = GenerateMove()

            self.rect.x += dx
            self.rect.y += dy


class Flag(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        image = pygame.Surface((TILE, TILE))
        image.fill((0, 255, 0))
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (14*TILE, 14*TILE)


class Button:
    def __init__(self, text, rect, font, callback, color=(100, 100, 100), hoverColor=(125, 125, 125), textColor=(255, 255, 255)):
        self.label = font.render(text, False, textColor)
        self.rect = pygame.rect.Rect(rect)
        self.rect.center = rect[0]
        self.color = color
        self.hoverColor = hoverColor
        self.labelRect = self.label.get_rect(center=self.rect.center)
        self.callback = callback

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, self.hoverColor if hovered else self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (20, 20, 20), self.rect, 2, border_radius=4)
        surface.blit(self.label, self.labelRect)


def StartGame():
    global state
    state = "playing"
    global timeBegin
    timeBegin = pygame.time.get_ticks()

def FinishGame():
    global timeStop
    timeStop = pygame.time.get_ticks()
    global state
    state = "finished"

def UpdateHighScore(score):
    global highScore
    if highScore > score:
        highScore = score

def ReturnMenu():
    global state
    state = "mainMenu"


buttonFont = pygame.font.Font(ASSETS / "Pixelta.ttf", 32)

startButton = Button("PLAY", ((256, 400), (85, 40)), buttonFont, StartGame)
restartButton = Button("MAIN MENU", ((256, 464), (140, 40)), buttonFont, ReturnMenu)

obstacles = pygame.sprite.Group()
webs = pygame.sprite.Group()
zombies = pygame.sprite.Group()
finishFlag = pygame.sprite.Group()

finishFlag.add(Flag())



rocks = []
for i in range(ROCK_COUNT):
    j = rand.randint(0, 15)
    k = rand.randint(0, 15)
    if j < 3 and k <3:
        continue
    if j > 12 and k > 12:
        continue
    obstacles.add(Rock(j, k))
    rocks.append((j, k))

for i in range(WEB_COUNT):
    j = rand.randint(0, 15)
    k = rand.randint(0, 15)
    if j < 3 and k < 3:
        continue
    if j > 12 and k > 12:
        continue


    if (j, k) not in rocks:
        webs.add(Web(j, k))

for i in range(ZOMBIE_COUNT):
    zombies.add(Zombie())


player = Player(16, 16)
all_sprites = pygame.sprite.Group(player)
dt = 0
held = []
queued = None
titleFont = pygame.font.Font(ASSETS / "Pixelta.ttf", 64)
titleFont.align = pygame.FONT_CENTER
descriptionFont = pygame.font.Font(ASSETS / "Pixelta.ttf", 32)
descriptionFont.align = pygame.FONT_CENTER
title = titleFont.render("16x16", False, (255, 255, 255))
titleRect = title.get_rect(center=(256, 64))
description = descriptionFont.render("A tile based game. You must reach the green flag" \
" without being killed by the zombies. A score is" \
" calculated by speed and how many items you collect.", False, (255, 255, 255), wraplength=512,)
descriptionRect = description.get_rect(center=(256, 200))
frameCount = 0


while running:

    frameCount += 1
    dt = clock.tick(60)
    moveTimer = max(0, moveTimer - dt)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key in KEY_MOVES:
            held.append(event.key)
            queued = event.key

        elif event.type == pygame.KEYUP and event.key in held:
            held.remove(event.key)
        else:
            startButton.handleEvent(event)
            startButton.handleEvent(event)

    key = None
    if queued is not None:
        key = queued
        queued = None
        if stuck:
            moveTimer = 1000
            stuck = False
        else:
            moveTimer = REPEAT_DELAY
    elif held and moveTimer == 0:
        key = held[-1]
        if stuck:
            moveTimer = 1000
            stuck = False
        else:
            moveTimer = REPEAT_DELAY


    if key is not None:
        player.move(*KEY_MOVES[key])



    if state == "playing":

        player.update()

        # drawing stuff
        screen.fill((100, 100, 100))

        # stuff to be seen
        all_sprites.draw(screen)

        finishFlag.draw(screen)

        if frameCount % 45 == 0:
            for zombie in zombies:
                zombie.move()

        zombies.draw(screen)

        obstacles.draw(screen)

        webs.draw(screen)

        for i in range(17):
            pygame.draw.line(screen, (20, 20, 20), (i*32 - 1, 0), (i*32 - 1, 512), 2)
            pygame.draw.line(screen, (20, 20, 20), (0, i*32 - 1), (512, i*32 - 1), 2)


    elif state == "finished":


        time = (timeStop - timeBegin)/1000
        UpdateHighScore(time)
        screen.fill((100, 100, 100))
        highScoreText = titleFont.render(f"Best time: {highScore}s", False, (255, 255, 255))
        highScoreRect = highScoreText.get_rect()
        highScoreRect.center = (256, 128)
        screen.blit(highScoreText, highScoreRect)



        score = titleFont.render(f"Your time: {time}s", False, (255, 255, 255))
        scoreRect = score.get_rect()
        scoreRect.center = (256, 256)
        screen.blit(score, scoreRect)
        restartButton.draw(screen)


    elif state == "mainMenu":
        screen.fill((100, 100, 100))
        screen.blit(title, titleRect)
        screen.blit(description, descriptionRect)
        startButton.draw(screen)



    pygame.display.flip()


pygame.quit()