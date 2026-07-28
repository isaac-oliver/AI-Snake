#Choose Direction Function
def choose_direction(snake):
    #Get Legal Moves
    legal_moves = get_legal_moves(snake)
    if not legal_moves:
        return snake.direction
    #Determine Best Move Using Heuristics
    best_score = float('-inf')
    best_move = ''
    for move in legal_moves:
        score = move_score(snake,move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


#Get Legal Moves Function
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

#Calculate Score
def move_score(snake,move):
    score = (distance_score(snake,move) + space_score(snake,move))
    return score

#Score Based on Distance From Apple
def distance_score(snake,move):
    #Calculate Distance Based on Direction
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

#Score Based on How Much Space There is to Move a Certain Direction
def space_score(snake,move):
    #Calculate a New Head According to Possible Direction
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

    #Call Flood Function with New Head
    return flood_fill(snake,new_head)

def flood_fill(snake, new_head):
    #Initiate Lists
    visited = []
    queue = [new_head]
    #Loops Until Queue is Empty
    while queue:
        #Checks if First Item in Queue is an Empty Space
        current = queue.pop(0)
        if current in visited:
            continue
        if not check_in_board(current):
            continue
        if current in snake.snake_pos:
            continue
        #Adds the Space Being Checked to the Visited List if it is an Empty Space
        visited.append(current)
        #Adds the Surrounding Spaces as Neighbors of the Current Space
        x = current[0]
        y = current[1]
        neighbors = [[x+20,y],[x-20,y],[x,y-20],[x,y+20]]
        for neighbor in neighbors:
            if neighbor not in visited:
                if neighbor not in snake.snake_pos:
                    if check_in_board(neighbor):
                        queue.append(neighbor)
    return len(visited)

#Checks if a Coordinate is Within the Board Bounds
def check_in_board(pos):
    if pos[0] < 0 or pos[0] >= 400:
        return False
    elif pos[1] < 0 or pos[1] >= 400:
        return False
    else:
        return True