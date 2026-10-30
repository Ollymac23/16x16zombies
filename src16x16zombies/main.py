import pygame
from pathlib import Path
import random as rand


pygame.init()
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True




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
font = pygame.font.Font(ASSETS / "dogicabold.ttf", 32)
title = font.render("16x16", False, (255, 255, 255))
titleRect = title.get_rect(center=(256, 64))

playing = False

while running:

    dt = clock.tick(60)

    screen.fill((100, 100, 100))
    screen.blit(title, titleRect)




    while playing:
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()



    

pygame.quit()