
import random
import sys,os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Agents.rule_based import choose_direction as choose_direction_rb
from Agents.random import choose_direction as choose_direction_random
from Agents.a_star import choose_direction as choose_direction_a_star
from Agents.heuristic import choose_direction as choose_direction_heuristic
from Agents.hamiltonian import choose_direction as choose_direction_hamiltonian
from Agents.q_learning import choose_direction as choose_direction_q_learning
from Agents.deep_q import choose_direction as choose_direction_deep_q
from Game.snake import Game as SnakeGame


def playgame(agent):
    game = SnakeGame()
    done = False
    moves = 0
    max_moves = 20000
    while not done and moves < max_moves:

        if agent == "RULE BASED":
            game.key = choose_direction_rb(game)
        elif agent == "RANDOM":
            game.key = choose_direction_random(game)
        elif agent == "HAMILTONIAN":
            game.key = choose_direction_hamiltonian(game)
        elif agent == "A*":
            game.key = choose_direction_a_star(game)
        elif agent == "HEURISTIC":
            game.key = choose_direction_heuristic(game)
        elif agent == "Q-LEARNING":
            game.key = choose_direction_q_learning(game)
        elif agent == "DEEP Q-LEARNING":
            game.key = choose_direction_deep_q(game)

        new_head = game.snake_pos[0].copy()

        if game.key == "RIGHT" and game.direction != "LEFT":
            game.next_direction = "RIGHT"
        elif game.key == "LEFT" and game.direction != "RIGHT":
            game.next_direction = "LEFT"
        elif game.key == "UP" and game.direction != "DOWN":
            game.next_direction = "UP"
        elif game.key == "DOWN" and game.direction != "UP":
            game.next_direction = "DOWN"
        
        game.direction = game.next_direction
        
        move_snake(game, new_head)

        if new_head == game.apple_pos:
            game.score = game.score + 1
            #Generate New Apple Position
            while True:
                game.apple_pos = [random.randint(0, (game.width - 20) // 20) * 20,
                    random.randint(0, (game.height - 20) // 20) * 20]
        
                if game.apple_pos not in game.snake_pos:
                    break
        else:
            game.snake_pos.pop()
        if new_head[0] < 0 or new_head[0] >= game.width or new_head[1] < 0 or new_head[1] >= game.height:
            done = True
        for block in game.snake_pos[1:]:
            if new_head == block:
                done = True
        moves += 1
    return game.score, moves

def move_snake(snake, new_head):
    if snake.direction == "RIGHT":
        new_head[0] += 20
    elif snake.direction == "LEFT":
        new_head[0] -= 20
    elif snake.direction == "UP":
        new_head[1] -= 20
    elif snake.direction == "DOWN":
        new_head[1] += 20
    else:
        raise ValueError("Invalid direction")
    
    snake.snake_pos.insert(0, new_head)
    return

if __name__ == "__main__":
    total_score = 0
    total_moves = 0
    for i in range(100):
        score, moves = playgame("HEURISTIC")
        total_score += score
        total_moves += moves
        print(f"Game {i+1}: Score = {score}, Moves = {moves}")
    print(f"Average Score: {total_score / 100}, Average Moves: {total_moves / 100}")