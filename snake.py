import pygame # type: ignore
import random
from ai import choose_direction
pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
FPS = 60
score = 0
scoretxt=""
direction = "RIGHT"
next_direction = "RIGHT"
FramePerSec = pygame.time.Clock()
snake_pos = [[100, 300],[80, 300],[60, 300]]
apple_pos = [200,300]
length = 0
key = "RIGHT"
running = True
move_del = 200
lastmove = 0
current_time = 0
old_direction = "RIGHT"
def game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("Arial", 50)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    screentxt = "Final Score: " + str(score)
    score_font = pygame.font.SysFont("Arial", 30)
    score_text = score_font.render(screentxt, True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    exit()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    current_time = pygame.time.get_ticks()
    
    #Screen Setup
    scoretxt = "Score: " + str(score)
    score_font = pygame.font.SysFont("Arial", 20)
    score_text = score_font.render(scoretxt, True, (0, 0, 255))
    screen.fill((0, 0, 0))
    screen.blit(score_text, (WIDTH - score_text.get_width() ,HEIGHT - score_text.get_height()))

    #Draw Snake
    length = 0
    for pos in snake_pos:
        pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 20, 20))
        length = length + 1
    
    #AI Decision/User Input
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        key = "RIGHT"
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        key = "LEFT"
    elif pygame.key.get_pressed()[pygame.K_UP]:
        key = "UP"
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        key = "DOWN"
    #key = choose_direction(snake_pos,snake_pos[0], apple_pos,direction,WIDTH,HEIGHT)

    #Snake Head
    new_head = snake_pos[0].copy()
    
    #Draw Apple
    pygame.draw.rect(screen, (255, 0, 0), (apple_pos[0], apple_pos[1], 20, 20))

    #Prevent Snake from going back on itself
    if key == "RIGHT" and direction != "LEFT":
        next_direction = "RIGHT"
    elif key == "LEFT" and direction != "RIGHT":
        next_direction = "LEFT"
    elif key == "UP" and direction != "DOWN":
        next_direction = "UP"
    elif key == "DOWN" and direction != "UP":
        next_direction = "DOWN"
    
    #Key to Move Direction
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

        #Check if Snake Eats Apple
        if new_head == apple_pos:
            score = score + 1
            
            #Generate New Apple Position
            apple_pos = [random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20]
            for block in snake_pos:
                if apple_pos == block:
                    apple_pos = [random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20]
        else:
            snake_pos.pop()

    #Check for Collisions
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        game_over()
    for block in snake_pos[1:]:
        if new_head == block:
            game_over()
    
    pygame.display.update()
    FramePerSec.tick(FPS)
pygame.quit()
