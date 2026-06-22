import pygame # type: ignore
import random
pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
FPS = 60
score = 0
direction = "RIGHT"
next_direction = "RIGHT"
FramePerSec = pygame.time.Clock()
snake_pos = [[100, 300],[80, 300],[60, 300]]
apple_pos = [200,300]
length = 3
running = True
move_del = 250
lastmove = 0
current_time = 0
old_direction = "RIGHT"
old_direction = "RIGHT"
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
    for pos in snake_pos:
        pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 20, 20))
    key = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    new_head = snake_pos[0].copy()
    
    pygame.draw.rect(screen, (255, 0, 0), (apple_pos[0], apple_pos[1], 20, 20))

    if key[pygame.K_RIGHT] and direction != "LEFT":
        next_direction = "RIGHT"
    elif key[pygame.K_LEFT] and direction != "RIGHT":
        next_direction = "LEFT"
    elif key[pygame.K_UP] and direction != "DOWN":
        next_direction = "UP"
    elif key[pygame.K_DOWN] and direction != "UP":
        next_direction = "DOWN"
    
    if current_time - lastmove > move_del:
        direction = next_direction
        
        if direction == "RIGHT":
            new_head[0] += 20
        elif direction == "LEFT":
            new_head[0] -= 20
        elif direction == "UP":
            new_head[1] -= 20
        elif direction == "DOWN":
            new_head[1] += 20
        lastmove = current_time
        snake_pos.insert(0, new_head)
        if new_head == apple_pos:
            apple_pos = [random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20]
            for block in snake_pos:
                if apple_pos == block:
                    apple_pos = [random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20]
        else:
            snake_pos.pop()

    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        game_over()
    for block in snake_pos[1:]:
        if new_head == block:
            game_over()
    
    pygame.display.update()
    FramePerSec.tick(FPS)
pygame.quit()
