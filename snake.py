import os
import pygame # type: ignore
import random
from ai import choose_direction
pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font_path = os.path.join(os.path.dirname(__file__), "Anta-Regular.ttf")
font_title = pygame.font.Font(font_path, 40)
font_name = pygame.font.Font(font_path,20)
font_player_ctrl = pygame.font.Font(font_path, 15)
font_ai_ctrl = pygame.font.Font(font_path, 15)
font_score = pygame.font.Font(font_path, 24)
font_game_over = pygame.font.Font(font_path, 40)
font_score_over = pygame.font.Font(font_path, 25)
font_restart = pygame.font.Font(font_path, 15)
scoretxt=""
running = True
FramePerSec = pygame.time.Clock()
FPS = 60
highscore = 0
restart_game = False
game_state = "MENU"

def game_start():
    global control
    status = True
    text = font_title.render("Snake Game", True, (0, 255, 0))
    name_text = font_name.render("By: Isaac Oliver", True, (0, 255, 0))
    game_image = pygame.image.load("Snake Game Image.png")
    player_ctrl_txt_1 = font_player_ctrl.render("Player Control", True, (255, 0, 0))
    player_ctrl_txt_2 = font_player_ctrl.render("Player Control", True, (0, 255, 0))
    ai_ctrl_txt_1 = font_ai_ctrl.render("AI Control", True, (255, 0, 0))
    ai_ctrl_txt_2 = font_ai_ctrl.render("AI Control", True, (0, 255, 0))
    while status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, 200))
        screen.blit(game_image, (WIDTH // 2 - game_image.get_width() // 2, 80))
        player_ctrl = pygame.Rect(WIDTH // 2 - 75, 245, 150, 40)
        ai_ctrl = pygame.Rect(WIDTH // 2 - 75, 290, 150, 40)
        if player_ctrl.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 0, 0), player_ctrl, 2, border_radius=5)
            screen.blit(player_ctrl_txt_1, (WIDTH // 2 - 75 + 10, 245 + 10))
            if pygame.mouse.get_pressed()[0]:
                control = "PLAYER"
                status = False
        else:
            screen.blit(player_ctrl_txt_2, (WIDTH // 2 - 75 + 10, 245 + 10))
            pygame.draw.rect(screen, (0, 255, 0), player_ctrl, 2, border_radius=5)
        if ai_ctrl.collidepoint(pygame.mouse.get_pos()):
            screen.blit(ai_ctrl_txt_1, (WIDTH // 2 - 75 + 10, 290 + 10))
            pygame.draw.rect(screen, (255, 0, 0), (ai_ctrl), 2, border_radius=5)
            if pygame.mouse.get_pressed()[0]:
                control = "AI"
                status = False
        else:
            screen.blit(ai_ctrl_txt_2, (WIDTH // 2 - 75 + 10, 290 + 10))
            pygame.draw.rect(screen, (0, 255, 0), (ai_ctrl), 2, border_radius=5)
        

        pygame.display.update()
        FramePerSec.tick(FPS)

        
        
        
def game_over():
    global highscore
    global game_state
    status = True
    game_over_txt = font_game_over.render("Game Over", True, (255, 0, 0))
    txt_score = "Final Score: " + str(score)
    txt_highscore = "High Score: " + str(highscore)
    score_text = font_score_over.render(txt_score, True, (0, 255, 0))
    highscore_text = font_score_over.render(txt_highscore, True, (0, 255, 0))
    restart_txt_1 = font_restart.render("Restart", True, (255, 0, 0))
    restart_txt_2 = font_restart.render("Restart", True, (0, 255, 0))
    quit_txt_1 = font_restart.render("Quit", True, (255, 0, 0))
    quit_txt_2 = font_restart.render("Quit", True, (0, 255, 0))
    if score > highscore:
        highscore = score
    while status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))
        text = font_game_over.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2 - 90))
        screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2 - 60 ))
        restart_game = pygame.Rect(WIDTH // 2 - 75, 245, 150, 40)
        quit_game = pygame.Rect(WIDTH // 2 - 75, 290, 150, 40)
        if restart_game.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 0, 0), restart_game, 2, border_radius=5)
            screen.blit(restart_txt_1, (WIDTH // 2 - 75 + 10, 245 + 10))
            if pygame.mouse.get_pressed()[0]:
                # Wait for mouse release so the menu doesn't immediately register the same click
                while pygame.mouse.get_pressed()[0]:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    FramePerSec.tick(FPS)
                reset_game()
                status = False
                game_state = "MENU"

                

        else:
            screen.blit(restart_txt_2, (WIDTH // 2 - 75 + 10, 245 + 10))
            pygame.draw.rect(screen, (0, 255, 0), restart_game, 2, border_radius=5)
        if quit_game.collidepoint(pygame.mouse.get_pos()):
            screen.blit(quit_txt_1, (WIDTH // 2 - 75 + 10, 290 + 10))
            pygame.draw.rect(screen, (255, 0, 0), quit_game, 2, border_radius=5)
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                exit()
        else:
            screen.blit(quit_txt_2, (WIDTH // 2 - 75 + 10, 290 + 10))
            pygame.draw.rect(screen, (0, 255, 0), quit_game, 2, border_radius=5)
        pygame.display.update()
    



def reset_game():
    global direction
    direction = "RIGHT"
    global next_direction
    next_direction = "RIGHT"
    global FramePerSec
    FramePerSec = pygame.time.Clock()
    global snake_pos
    snake_pos = [[100, 300],[80, 300],[60, 300]]
    global apple_pos
    apple_pos = [200,300]
    global globallength
    globallength = 0
    global key
    key = "RIGHT"
    global move_del
    move_del = 200
    global lastmove
    lastmove = 0
    global current_time
    current_time = 0
    global GRAY
    GRAY = (40,40,40)
    global FPS
    FPS = 60
    global score
    score = 0
    global status
    status = True
    global control
    control = "PLAYER"
    


def play_game():
    global score
    global direction
    global next_direction
    global apple_pos
    global snake_pos
    global game_state
    global lastmove
    global key
    global current_time
    global move_del
    global WIDTH
    global HEIGHT
    global GRAY
    global FPS
    global FramePerSec
    global scoretxt
    global score_text
    global font_score
    global screen
    #Screen Setup
    screen.fill((5, 5, 5))

    for i in range(0, WIDTH, 20):
        pygame.draw.line(screen, GRAY, (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 20):
        pygame.draw.line(screen, GRAY, (0, i), (WIDTH, i), 1)
    
    #Draw Snake
    length = 0
    for pos in snake_pos:
        if length == 0:
            pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 20, 20),2, border_radius=3)
        else:
            pygame.draw.rect(screen, (0, 255, 0), (pos[0]+1, pos[1]+1, 18, 18),2, border_radius=3)
        length = length + 1
    
    #Draw Apple
    pygame.draw.rect(screen, (255, 0, 0), (apple_pos[0], apple_pos[1], 20, 20), 2, border_radius=3)

    #Display Score
    scoretxt = "Score: " + str(score)
    score_text = font_score.render(scoretxt, True, (0, 0, 255))
    screen.blit(score_text, (WIDTH - score_text.get_width() ,score_text.get_height()-35))
    
    #AI Decision/User Input
    if control == "AI":
        key = choose_direction(snake_pos,snake_pos[0], apple_pos,direction,WIDTH,HEIGHT)
    else:
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            key = "RIGHT"
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            key = "LEFT"
        elif pygame.key.get_pressed()[pygame.K_UP]:
            key = "UP"
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            key = "DOWN"
    

    #Snake Head
    new_head = snake_pos[0].copy()

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
        game_state = "GAME_OVER"
        return
    for block in snake_pos[1:]:
        if new_head == block:
            game_state = "GAME_OVER"
            return
    
    pygame.display.update()
    FramePerSec.tick(FPS)



reset_game()
game_start()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    current_time = pygame.time.get_ticks()
    
    if game_state == "MENU":
        game_start()
        game_state = "PLAYING"
    elif game_state == "PLAYING":
        play_game()
    elif game_state == "GAME_OVER":
        game_over()

pygame.quit()
