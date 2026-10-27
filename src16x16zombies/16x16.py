import pygame


pygame.init()
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True

playerPos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
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
                playerPos.y -= distMove
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                playerPos.x -= distMove
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                playerPos.y += distMove
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                playerPos.x += distMove
        if event.type == pygame.KEYUP and keyPressed:
            keyPressed = False


    screen.fill((200, 100, 100))
    pygame.draw.circle(screen, (0, 0, 0), playerPos, 15)





    pygame.display.flip()


    clock.tick(60) #fps 60
    

pygame.quit()