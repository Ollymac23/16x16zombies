import pygame



pygame.init()
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.health = 3
        self.image = pygame.image.load(f"/assests/Player{self.health}.png").convert_alpha()
        self.rect = self.image.get_rect(center=(width, height))
        self.pos = pygame.Vector2(self.rect.center)
    def Update(self, move):
        self.image = pygame.image.load(f"/assets/Player{self.health}.png")
        self.rect = self.image.get_rect(center=self.pos)
        self.pos += move
        self.rect.center = self.pos



player = Player(screen.get_width()/2, screen.get_height()/2)


moveVect = pygame.Vector2(0, 0)
dt = 0
keyPressed = False
distMove = 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and keyPressed == False:
            keyPressed = True
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                 moveVect.y-= distMove
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                moveVect.x -= distMove
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                moveVect.y += distMove
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                moveVect.x += distMove
        if event.type == pygame.KEYUP and keyPressed:
            keyPressed = False


    


    screen.fill((200, 100, 100))
    player.update(moveVect)







    pygame.display.flip()


    clock.tick(60) #fps 60
    

pygame.quit()