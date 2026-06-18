import pygame # type: ignore
pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
FPS = 60
direction = "RIGHT"
FramePerSec = pygame.time.Clock()
snake_pos = [100, 300]
running = True
move_del = 250
lastmove = 0
current_time = 0
def game_over():
    font = pygame.font.SysFont("Arial", 50)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    exit()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(snake_pos[0], snake_pos[1], 20, 20))
    key = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    if key[pygame.K_RIGHT]:
        direction = "RIGHT"
    elif key[pygame.K_LEFT]:
        direction = "LEFT"
    elif key[pygame.K_UP]:
        direction = "UP"
    elif key[pygame.K_DOWN]:
        direction = "DOWN"
        
    if current_time - lastmove > move_del:

        if direction == "RIGHT":
            snake_pos[0] += 20
        elif direction == "LEFT":
            snake_pos[0] -= 20
        elif direction == "UP":
            snake_pos[1] -= 20
        elif direction == "DOWN":
            snake_pos[1] += 20
        lastmove = current_time
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over()
    pygame.display.update()
    FramePerSec.tick(FPS)
pygame.quit()
