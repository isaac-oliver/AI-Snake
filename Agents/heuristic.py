def choose_direction(snake):
    legal_moves = get_legal_moves(snake)
    if not legal_moves:
        return snake.direction
    best_score = float('-inf')
    best_move = ''
    for move in legal_moves:
        score = move_score(snake,move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move



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

    
def move_score(snake,move):
    score = (distance_score(snake,move) + space_score(snake,move)*6)
    return score

def distance_score(snake,move):
    snake_head = snake.snake_pos[0]
    if move == "RIGHT":
        distance = abs(snake_head[0] + 20 - snake.apple_pos[0]) + abs(snake_head[1] - snake.apple_pos[1])
    elif move == "LEFT":
        distance = abs(snake_head[0] - 20 - snake.apple_pos[0]) + abs(snake_head[1] - snake.apple_pos[1])
    elif move == "UP":
        distance = abs(snake_head[0] - snake.apple_pos[0]) + abs(snake_head[1] - 20 - snake.apple_pos[1])
    elif move == "DOWN":
        distance = abs(snake_head[0] - snake.apple_pos[0]) + abs(snake_head[1] + 20 - snake.apple_pos[1])    
    return -distance

def space_score(snake,move):
    score = 0
    snake_head = snake.snake_pos[0]
    if move == "RIGHT":
        new_head = [snake_head[0] + 20 , snake_head[1]]
    elif move == "LEFT":
        new_head = [snake_head[0] - 20 , snake_head[1]]
    elif move == "UP":
        new_head = [snake_head[0] , snake_head[1] - 20]
    elif move == "DOWN":
        new_head = [snake_head[0] , snake_head[1] + 20]
    neighbors = [[new_head[0] + 20, new_head[1]],  
    [new_head[0] - 20, new_head[1]],  
    [new_head[0], new_head[1] - 20],  
    [new_head[0], new_head[1] + 20]]
    for neighbor in neighbors:
        if neighbor not in snake.snake_pos and check_in_board(neighbor):
            score += 1
    return score



def check_in_board(pos):
    if pos[0] < 0 or pos[0] >= 400:
        return False
    elif pos[1] < 0 or pos[1] >= 400:
        return False
    else:
        return True