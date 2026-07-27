import math
def choose_direction(snake):
    width = 400
    height = 400
    legal_moves = get_legal_moves(snake)

def move_score(snake,move):
    score = 0
    distance = math.abs(snake.snake_pos[0] - snake.apple_pos[0]) + math.abs(snake.snake_pos[1] - snake.apple_pos[1])
                        
def get_legal_moves(snake):
    width = 400
    height = 400
    legal_moves = []
    #Add Legal Moves to List
    if canright(snake,width):
        legal_moves.append("RIGHT")
    if canleft(snake):
        legal_moves.append("LEFT")
    if canup(snake):
        legal_moves.append("UP")
    if candown(snake,height):
        legal_moves.append("DOWN")
    return legal_moves

#Is Right a Legal Move?
def canright(game,width):
    snake_head = game.snake_pos[0]
    for block in game.snake_pos[1:]:
        if snake_head[0] + 20 == block[0] and snake_head[1] == block[1]:
            return False
    if game.direction == "LEFT":
        return False
    elif snake_head[0] + 20 >= width:
        return False
    else:
        return True

#Is Left a Legal Move?
def canleft(game):
    snake_head = game.snake_pos[0]
    for block in game.snake_pos[1:]:
        if snake_head[0] - 20 == block[0] and snake_head[1] == block[1]:
            return False
    if game.direction == "RIGHT":
            return False
    elif snake_head[0] - 20 < 0:
        return False
    else: 
        return True

#Is Up a Legal Move?
def canup(game):
    snake_head = game.snake_pos[0]
    for block in game.snake_pos[1:]:
        if snake_head[0] == block[0] and snake_head[1] - 20 == block[1]:
            return False
    if game.direction == "DOWN":
        return False
    elif snake_head[1] - 20 < 0:
        return False
    else:
        return True

#Is Down a Legal Move?
def candown(game,height):
    snake_head = game.snake_pos[0]
    for block in game.snake_pos[1:]:
        if snake_head[0] == block[0] and snake_head[1] + 20 == block[1]:
            return False
    if game.direction == "UP":
        return False
    elif snake_head[1] + 20 >= height:
        return False
    else: 
        return True