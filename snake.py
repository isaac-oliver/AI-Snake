import pygame
pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
FPS = 10
FramePerSec = pygame.time.Clock()
snake_pos = [100, 300]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(snake_pos[0], snake_pos[1], 20, 20))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_pos[0] -= 20
    elif keys[pygame.K_RIGHT]:
        snake_pos[0] += 20
    elif keys[pygame.K_UP]:
        snake_pos[1] -= 20
    elif keys[pygame.K_DOWN]:
        snake_pos[1] += 20
    pygame.display.update()
    FramePerSec.tick(FPS)
pygame.quit()
