import os
import sys
import pygame # type: ignore
import random

# Add parent directory to path to import Agents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Agents.rule_based import choose_direction as choose_direction_rb
from Agents.random import choose_direction as choose_direction_random
from Agents.a_star import choose_direction as choose_direction_a_star
from Agents.heuristic import choose_direction as choose_direction_hueristic
from Agents.hamiltonian import choose_direction as choose_direction_hamiltonian
from Agents.q_learning import choose_direction as choose_direction_q_learning
from Agents.deep_q import choose_direction as choose_direction_deep_q
pygame.init()

#Game Tab Setup
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

#Fonts
font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Anta-Regular.ttf")
font_title = pygame.font.Font(font_path, 40)
font_name = pygame.font.Font(font_path,20)
font_player_ctrl = pygame.font.Font(font_path, 15)
font_ai_ctrl = pygame.font.Font(font_path, 15)
font_score = pygame.font.Font(font_path, 24)
font_game_over = pygame.font.Font(font_path, 40)
font_score_over = pygame.font.Font(font_path, 25)
font_restart = pygame.font.Font(font_path, 15)

#Variables Setup
scoretxt=""
running = True
FramePerSec = pygame.time.Clock()
highscore = 0
restart_game = False

gray = (40,40,40)

class Game:
    def __init__(self):
        self.highscore = 0
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.snake_pos = [[100, 300],[80, 300],[60, 300]]
        self.apple_pos = [200,300]
        self.key = "RIGHT"
        self.move_del = 200
        self.lastmove = 0
        self.current_time = 0
        self.FPS = 60
        self.control = "PLAYER"
        self.game_state = "MENU"

    def play_game(self):
        #Screen Setup
        screen.fill((5, 5, 5))
        self.current_time = pygame.time.get_ticks()
        for i in range(0, WIDTH, 20):
            pygame.draw.line(screen, gray, (i, 0), (i, HEIGHT), 1)
        for i in range(0, HEIGHT, 20):
            pygame.draw.line(screen, gray, (0, i), (WIDTH, i), 1)
    
        #Draw Snake
        length = 0
        for pos in self.snake_pos:
            if length == 0:
                pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 20, 20),2, border_radius=3)
            else:
                pygame.draw.rect(screen, (0, 255, 0), (pos[0]+1, pos[1]+1, 18, 18),2, border_radius=3)
            length = length + 1
    
        #Draw Apple
        pygame.draw.rect(screen, (255, 0, 0), (self.apple_pos[0], self.apple_pos[1], 20, 20), 2, border_radius=3)

        #Display Score
        scoretxt = "Score: " + str(self.score)
        score_text = font_score.render(scoretxt, True, (0, 0, 255))
        screen.blit(score_text, (WIDTH - score_text.get_width() ,score_text.get_height()-35))
    
        #AI Decision/User Input
        if self.control == "RULE BASED":
            self.key = choose_direction_rb(self)
        elif self.control == "RANDOM":
            self.key = choose_direction_random(self)
        elif self.control == "HAMILTONIAN":
            self.key = choose_direction_hamiltonian(self)
        elif self.control == "A*":
            self.key = choose_direction_a_star(self)
        elif self.control == "HUERISTIC":
            self.key = choose_direction_hueristic(self)
        elif self.control == "Q-LEARNING":
            self.key = choose_direction_q_learning(self)
        elif self.control == "DEEP Q-LEARNING":
            self.key = choose_direction_deep_q(self)
        else:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.key = "RIGHT"
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.key = "LEFT"
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.key = "UP"
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.key = "DOWN"
    

        #Snake Head
        new_head = self.snake_pos[0].copy()

        #Prevent Snake from going back on itself
        if self.key == "RIGHT" and self.direction != "LEFT":
            self.next_direction = "RIGHT"
        elif self.key == "LEFT" and self.direction != "RIGHT":
            self.next_direction = "LEFT"
        elif self.key == "UP" and self.direction != "DOWN":
            self.next_direction = "UP"
        elif self.key == "DOWN" and self.direction != "UP":
            self.next_direction = "DOWN"
    
        #Key to Move Direction
        if self.current_time - self.lastmove > self.move_del:
            self.direction = self.next_direction
        
            if self.direction == "RIGHT":
                new_head[0] += 20
            elif self.direction == "LEFT":
                new_head[0] -= 20
            elif self.direction == "UP":
                new_head[1] -= 20
            elif self.direction == "DOWN":
                new_head[1] += 20
            self.lastmove = self.current_time
            self.snake_pos.insert(0, new_head)

            #Check if Snake Eats Apple
            if new_head == self.apple_pos:
                self.score = self.score + 1

                #Generate New Apple Position
                self.apple_pos = [random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20]
                for block in self.snake_pos:
                    if self.apple_pos == block:
                        self.apple_pos = [random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20]
            else:
                self.snake_pos.pop()

        #Check for Collisions
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            self.game_state = "GAME_OVER"
            return
        for block in self.snake_pos[1:]:
            if new_head == block:
                self.game_state = "GAME_OVER"
                return
    
        pygame.display.update()
        FramePerSec.tick(self.FPS)



    #Game Start Menu
    def game_start(self):
        #Initialize variables
        status = True
        text = font_title.render("Snake Game", True, (0, 255, 0))
        name_text = font_name.render("By: Isaac Oliver", True, (0, 255, 0))
        game_image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)), "Snake Game Image.png"))
        player_ctrl_txt_1 = font_player_ctrl.render("Player Control", True, (255, 0, 0))
        player_ctrl_txt_2 = font_player_ctrl.render("Player Control", True, (0, 255, 0))
        ai_ctrl_txt_1 = font_ai_ctrl.render("AI Control", True, (255, 0, 0))
        ai_ctrl_txt_2 = font_ai_ctrl.render("AI Control", True, (0, 255, 0))

        #Run Menu Loop
        while status:
            mouse_pos = pygame.mouse.get_pos()

            #Control Selection (Player/AI)
            player_ctrl = pygame.Rect(WIDTH // 2 - 75, 245, 150, 40)
            ai_ctrl = pygame.Rect(WIDTH // 2 - 75, 290, 150, 40)

            #Check Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if player_ctrl.collidepoint(event.pos):
                        self.control = "PLAYER"
                        self.game_state = "PLAYING"
                        status = False
                    elif ai_ctrl.collidepoint(event.pos):
                        self.control = "AI"
                        self.game_state = "AI MENU"
                        status = False

            #Menu Setup
            screen.fill((0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))
            screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, 200))
            screen.blit(game_image, (WIDTH // 2 - game_image.get_width() // 2, 80))

            if player_ctrl.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), player_ctrl, 2, border_radius=5)
                screen.blit(player_ctrl_txt_1, (WIDTH // 2 - 75 + 10, 245 + 10))
            else:
                screen.blit(player_ctrl_txt_2, (WIDTH // 2 - 75 + 10, 245 + 10))
                pygame.draw.rect(screen, (0, 255, 0), player_ctrl, 2, border_radius=5)
            if ai_ctrl.collidepoint(mouse_pos):
                screen.blit(ai_ctrl_txt_1, (WIDTH // 2 - 75 + 10, 290 + 10))
                pygame.draw.rect(screen, (255, 0, 0), (ai_ctrl), 2, border_radius=5)
            else:
                screen.blit(ai_ctrl_txt_2, (WIDTH // 2 - 75 + 10, 290 + 10))
                pygame.draw.rect(screen, (0, 255, 0), (ai_ctrl), 2, border_radius=5)

            #Update Display
            pygame.display.update()
            FramePerSec.tick(self.FPS)

    #AI Selection Menu
    def ai_menu(self):
        #Initialize variables
        status = True
        title = font_title.render("AI Selection", True, (0, 255, 0))
        rule_based_txt_1 = font_player_ctrl.render("Rule Based", True, (255, 0, 0))
        rule_based_txt_2 = font_player_ctrl.render("Rule Based", True, (0, 255, 0))
        random_txt_1 = font_player_ctrl.render("Random", True, (255, 0, 0))
        random_txt_2 = font_player_ctrl.render("Random", True, (0, 255, 0))
        hamiltonian_txt_1 = font_player_ctrl.render("Hamiltonian", True, (255, 0, 0))
        hamiltonian_txt_2 = font_player_ctrl.render("Hamiltonian", True, (0, 255, 0))
        heuristic_txt_1 = font_player_ctrl.render("Heuristic", True, (255, 0, 0))
        heuristic_txt_2 = font_player_ctrl.render("Heuristic", True, (0, 255, 0))
        a_star_txt_1 = font_player_ctrl.render("A*", True, (255, 0, 0))
        a_star_txt_2 = font_player_ctrl.render("A*", True, (0, 255, 0))
        q_learning_txt_1 = font_player_ctrl.render("Q-Learning", True, (255, 0, 0))
        q_learning_txt_2 = font_player_ctrl.render("Q-Learning", True, (0, 255, 0))
        deep_q_txt_1 = font_player_ctrl.render("Deep Q-Learning", True, (255, 0, 0))
        deep_q_txt_2 = font_player_ctrl.render("Deep Q-Learning", True, (0, 255, 0))

        #Run Menu Loop
        while status:
            mouse_pos = pygame.mouse.get_pos()

            #AI Selection Buttons
            rule_based = pygame.Rect(WIDTH // 2 -155, 130, 150, 40)
            random_ai = pygame.Rect(WIDTH // 2 - 155, 175, 150, 40)
            hamiltonian_ai = pygame.Rect(WIDTH // 2 - 155, 220, 150, 40)
            heuristic_ai = pygame.Rect(WIDTH // 2 + 5, 130, 150, 40)
            a_star_ai = pygame.Rect(WIDTH // 2 + 5, 175, 150, 40)
            q_learning_ai = pygame.Rect(WIDTH // 2 + 5, 220, 150, 40)
            deep_q_ai = pygame.Rect(WIDTH // 2 - 75, 265, 150, 40)

            #Check Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if rule_based.collidepoint(event.pos):
                        self.control = "RULE BASED"
                        self.game_state = "PLAYING"
                        status = False
                    elif random_ai.collidepoint(event.pos):
                        self.control = "RANDOM"
                        self.game_state = "PLAYING"
                        status = False
                    elif hamiltonian_ai.collidepoint(event.pos):
                        self.control = "HAMILTONIAN"
                        self.game_state = "PLAYING"
                        status = False
                    elif heuristic_ai.collidepoint(event.pos):
                        self.control = "HEURISTIC"
                        self.game_state = "PLAYING"
                        status = False
                    elif a_star_ai.collidepoint(event.pos):
                        self.control = "A*"
                        self.game_state = "PLAYING"
                        status = False
                    elif q_learning_ai.collidepoint(event.pos):
                        self.control = "Q-LEARNING"
                        self.game_state = "PLAYING"
                        status = False
                    elif deep_q_ai.collidepoint(event.pos):
                        self.control = "DEEP Q-LEARNING"
                        self.game_state = "PLAYING"
                        status = False

            #Menu Setup
            screen.fill((0, 0, 0))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

            if rule_based.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), rule_based, 2, border_radius=5)
                screen.blit(rule_based_txt_1, (WIDTH // 2 - 155 + 10, 130 + 10))
            else:
                screen.blit(rule_based_txt_2, (WIDTH // 2 - 155 + 10, 130 + 10))
                pygame.draw.rect(screen, (0, 255, 0), rule_based, 2, border_radius=5)
            if random_ai.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), random_ai, 2, border_radius=5)
                screen.blit(random_txt_1, (WIDTH // 2 - 155 + 10, 175 + 10))
            else:
                screen.blit(random_txt_2, (WIDTH // 2 - 155 + 10, 175 + 10))
                pygame.draw.rect(screen, (0, 255, 0), random_ai, 2, border_radius=5)
            if hamiltonian_ai.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), hamiltonian_ai, 2, border_radius=5)
                screen.blit(hamiltonian_txt_1, (WIDTH // 2 - 155 + 10, 220 + 10))
            else:
                screen.blit(hamiltonian_txt_2, (WIDTH // 2 - 155 + 10, 220 + 10))
                pygame.draw.rect(screen, (0, 255, 0), hamiltonian_ai, 2, border_radius=5)
            if heuristic_ai.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), heuristic_ai, 2, border_radius=5)
                screen.blit(heuristic_txt_1, (WIDTH // 2 + 5 + 10, 130 + 10))
            else:
                screen.blit(heuristic_txt_2, (WIDTH // 2 + 5 + 10, 130 + 10))
                pygame.draw.rect(screen, (0, 255, 0), heuristic_ai, 2, border_radius=5)
            if a_star_ai.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), a_star_ai, 2, border_radius=5)
                screen.blit(a_star_txt_1, (WIDTH // 2 + 5 + 10, 175 + 10))
            else:
                screen.blit(a_star_txt_2, (WIDTH // 2 + 5 + 10, 175 + 10))
                pygame.draw.rect(screen, (0, 255, 0), a_star_ai, 2, border_radius=5)
            if q_learning_ai.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), q_learning_ai, 2, border_radius=5)
                screen.blit(q_learning_txt_1, (WIDTH // 2 + 5 + 10, 220 + 10))
            else:
                screen.blit(q_learning_txt_2, (WIDTH // 2 + 5 + 10, 220 + 10))
                pygame.draw.rect(screen, (0, 255, 0), q_learning_ai, 2, border_radius=5)
            if deep_q_ai.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), deep_q_ai, 2, border_radius=5)
                screen.blit(deep_q_txt_1, (WIDTH // 2 - 75 + 10, 265 + 10))
            else:
                screen.blit(deep_q_txt_2, (WIDTH // 2 - 75 + 10, 265 + 10))
                pygame.draw.rect(screen, (0, 255, 0), deep_q_ai, 2, border_radius=5)

            pygame.display.update()
            FramePerSec.tick(self.FPS)




        
    #Game Over Menu
    def game_over(self):
        #Set High Score
        if self.score > self.highscore:
            self.highscore = self.score

        #Initialize variables
        status = True
        game_over_txt = font_game_over.render("Game Over", True, (255, 0, 0))
        txt_score = "Final Score: " + str(self.score)
        txt_highscore = "High Score: " + str(self.highscore)
        score_text = font_score_over.render(txt_score, True, (0, 255, 0))
        highscore_text = font_score_over.render(txt_highscore, True, (0, 255, 0))
        restart_txt_1 = font_restart.render("Restart", True, (255, 0, 0))
        restart_txt_2 = font_restart.render("Restart", True, (0, 255, 0))
        quit_txt_1 = font_restart.render("Quit", True, (255, 0, 0))
        quit_txt_2 = font_restart.render("Quit", True, (0, 255, 0))

        

        #Run Menu Loop
        while status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #Menu Setup and Display "Game Over" Text and Score/High Score
            screen.fill((0, 0, 0))
            text = font_game_over.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_txt, (WIDTH // 2 - game_over_txt.get_width() // 2, HEIGHT // 2 - game_over_txt.get_height() // 2 - 100))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + game_over_txt.get_height() // 2 - 90))
            screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 + game_over_txt.get_height() // 2 - 60 ))
            restart_game = pygame.Rect(WIDTH // 2 - 75, 245, 150, 40)
            quit_game = pygame.Rect(WIDTH // 2 - 75, 290, 150, 40)

            #Restart/Quit Buttons Selection
            if restart_game.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 0, 0), restart_game, 2, border_radius=5)
                screen.blit(restart_txt_1, (WIDTH // 2 - 75 + 10, 245 + 10))
                if pygame.mouse.get_pressed()[0]:
                    # Wait for mouse release so the menu doesn't immediately register the same click (debugging menu state overlap issue)
                    while pygame.mouse.get_pressed()[0]:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                        FramePerSec.tick(self.FPS)
                    self.reset_game()
                    status = False
                    self.game_state = "MENU"
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


game = Game()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    current_time = pygame.time.get_ticks()
    
    if game.game_state == "MENU":
        Game.game_start(game)
    elif game.game_state == "PLAYING":
        Game.play_game(game)
    elif game.game_state == "GAME_OVER":
        Game.game_over(game)
    elif game.game_state == "AI MENU":
        Game.ai_menu(game)

pygame.quit()
