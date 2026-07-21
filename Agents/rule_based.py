import random
def choose_direction(snake):
    snake_head = snake.snake_pos[0]
    apple_pos = snake.apple_pos
    width = 400
    height = 400
    legal_moves = []
    if canright(snake,width):
        legal_moves.append("RIGHT")
    if canleft(snake):
        legal_moves.append("LEFT")
    if canup(snake):
        legal_moves.append("UP")
    if candown(snake,height):
        legal_moves.append("DOWN")

    if not legal_moves:
        return snake.direction
    for move in legal_moves:
        if move == "RIGHT":
            if snake_head[0] < apple_pos[0]:
                return move
        elif move == "LEFT":
            if snake_head[0] > apple_pos[0]:
                return move
        elif move == "UP":
            if snake_head[1] > apple_pos[1]:
                return move
        elif move == "DOWN":
            if snake_head[1] < apple_pos[1]:
                return move
    
    if snake.direction in legal_moves:
        return snake.direction
    else:
        return random.choice(legal_moves)          
    

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






    
    