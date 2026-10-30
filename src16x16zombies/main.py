import pygame
from pathlib import Path
import random as rand


pygame.init()
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True
playing = False



ASSETS = Path(__file__).resolve().parent.parent / "assets"
SCALE = 2
distMove = 32
TILE = 32
KEY_MOVES = {
    pygame.K_w: (0, -distMove), pygame.K_UP: (0, -distMove),
    pygame.K_a: (-distMove, 0), pygame.K_LEFT: (-distMove, 0),
    pygame.K_s: (0, distMove), pygame.K_DOWN: (0, distMove),
    pygame.K_d: (distMove, 0), pygame.K_RIGHT: (distMove, 0)
    
}
REPEAT_DELAY = 150
ROCK_COUNT = 64
WEB_COUNT = 8
moveTimer = 150

PLAYER_IMAGES = [
    pygame.transform.scale_by(
    pygame.image.load(ASSETS / f"Player{i}.png").convert_alpha(), SCALE
    )
    for i in range(4)
    ]

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


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollide(player, obstacles, False):
            self.rect.x -= dx
            self.rect.y -= dy
        if pygame.sprite.spritecollide(player, webs, False):
            moveTimer = 1000
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
        self. image = image
        self.rect = self.image.get_rect(topleft=(tilex*TILE, tiley*TILE))


class Button:
    def __init__(self, text, rect, font, callback, color=(100, 100, 100), hoverColor=(125, 125, 125), textColor=(255, 255, 255)):
        self.label = font.render(text, False, textColor)
        self.rect = pygame.rect.Rect(rect)
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
        surface.blit(self.label, self,self.labelRect)



def StartGame():
    global state
    state = "playing"



buttonFont = pygame.font.Font(ASSETS / "Pixelta.ttf", 32)

startButton = Button("PLAY", ((256, 425), (85, 40)), buttonFont, StartGame)

obstacles = pygame.sprite.Group()
webs = pygame.sprite.Group()

rocks = []
for i in range(ROCK_COUNT):
    j = rand.randint(0, 15)
    k = rand.randint(0, 15)
    if j == 0 and k == 0:
        continue
    if j == 1 and k == 0:
        continue
    if j == 2 and k == 0:
        continue
    obstacles.add(Rock(j, k))
    rocks.append((j, k))

for i in range(WEB_COUNT):
    j = rand.randint(0, 15)
    k = rand.randint(0, 15)
    if j == 0 and k == 0:
        continue
    if j == 1 and k == 0:
        continue
    if j == 2 and k == 0:
        continue
    if (j, k) not in rocks:
        webs.add(Web(j, k))



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



while running:

    dt = clock.tick(60)
    moveTimer = max(0, moveTimer - dt)
    screen.fill((100, 100, 100))
    screen.blit(title, titleRect)
    screen.blit(description, descriptionRect)
    startButton.draw(screen)



    if state == "playing":
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

        key = None
        if queued is not None:
            key = queued
            queued = None
            moveTimer = REPEAT_DELAY
        elif held and moveTimer == 0:
            key = held[-1]
            moveTimer = REPEAT_DELAY

        if key is not None:
            player.move(*KEY_MOVES[key])


        player.update()




        # drawing stuff
        screen.fill((100, 100, 100))
        # stuff to be seen

            
            
        all_sprites.draw(screen)

        obstacles.draw(screen)

        webs.draw(screen)

        for i in range(17):
            pygame.draw.line(screen, (20, 20, 20), (i*32 - 1, 0), (i*32 - 1, 512), 2)
            pygame.draw.line(screen, (20, 20, 20), (0, i*32 - 1), (512, i*32 - 1), 2)




    pygame.display.flip()


pygame.quit()