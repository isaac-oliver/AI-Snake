#Choose Direction Function
def choose_direction(snake):
    #Get Legal Moves
    legal_moves = get_legal_moves(snake)
    if not legal_moves:
        return snake.direction
    #Determine Best Move Using Heuristics
    best_score = float('-inf')
    best_move = ''
    can_escape = can_reach_tail(snake, snake.snake_pos[0])
    for move in legal_moves:
        if can_escape:
            score = escape_score(snake,move)
        else:
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
    space = space_score(snake,move)
    score = 0
    if space < len(snake.snake_pos):
        trap_penalty = -100
    else:
        trap_penalty = 0
    score += distance_score(snake,move)
    score += space*7
    score += trap_penalty
    score += exit_score(snake,move)
    score += wall_penalty(snake,move)*2

    return score

#Tells Snake to Oscillate Between Two Directions to Escape a Trap
def escape_score(snake,move):
    score = 0
    if body_wall(snake) == "VERTICAL":
        if move == "RIGHT" or move == "LEFT":
            score += 200
    elif body_wall(snake) == "HORIZONTAL":
        if move == "UP" or move == "DOWN":
            score += 200
    score += space_score(snake,move)*7
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

#Produces a New Head Position Based on the Move
def new_head(snake,move):
    snake_head = snake.snake_pos[0]
    if move == "RIGHT":
        new_head = [snake_head[0] + 20 , snake_head[1]]
    elif move == "LEFT":
        new_head = [snake_head[0] - 20 , snake_head[1]]
    elif move == "UP":
        new_head = [snake_head[0] , snake_head[1] - 20]
    elif move == "DOWN":
        new_head = [snake_head[0] , snake_head[1] + 20]
    return new_head

#Score Based on How Much Space There is to Move a Certain Direction
def space_score(snake,move):
    #Call Flood Function with New Head
    return flood_fill(snake,new_head(snake,move))

def body_wall(snake):
    max_x = snake.snake_pos[0][0]
    max_y = snake.snake_pos[0][1]
    min_x = snake.snake_pos[0][0]
    min_y = snake.snake_pos[0][1]
    for pos in snake.snake_pos:
        if pos[0] > max_x:
            max_x = pos[0]
        if pos[0] < min_x:
            min_x = pos[0]
    for pos in snake.snake_pos:
        if pos[1] > max_y:
            max_y = pos[1]
        if pos[1] < min_y:
            min_y = pos[1]
        
    width = max_x - min_x
    height = max_y - min_y
    if width < height:
        return "VERTICAL"
    else:
        return "HORIZONTAL"

#Checks Space Using Flood Fill Algorithm
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

#Check if the snake is trapped
def can_reach_tail(snake, snake_head):
    #Variables
    queue = [snake_head]
    visited = []
    #Using Flood Fill to Check if the Snake can Reach its Tail
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        if not check_in_board(current):
            continue
        if current in snake.snake_pos[:-1]:
            continue
        #Tail is Found
        if current == snake.snake_pos[-1]:
            return True
        visited.append(current)
        x = current[0]
        y = current[1]
        neighbors = [[x+20,y],[x-20,y],[x,y-20],[x,y+20]]
        for neighbor in neighbors:
            if neighbor not in visited:
                if neighbor not in snake.snake_pos[:-1]:
                    if check_in_board(neighbor):
                        queue.append(neighbor)
    return False

#Penalty for Moves that Lead to Dead Ends
def exit_score(snake,move):
    #Variables
    snake_head = new_head(snake,move)
    exits = 0
    neighbors = [
        [snake_head[0] + 20, snake_head[1]],
        [snake_head[0] - 20, snake_head[1]],
        [snake_head[0], snake_head[1] + 20],
        [snake_head[0], snake_head[1] - 20],
    ]

    for neighbor in neighbors:
        if (
            check_in_board(neighbor)
            
        ):
            exits += 1

    if exits == 0:
        return -1000
    elif exits == 1:
        return -100
    else:
        return 0

#Moves that Lead to Walls are Penalized if the Snake is Long
def wall_penalty(snake,move):
    #Variables
    snake_head = new_head(snake,move)
    penalty = 0
    apple = False
    neighbors = [
            [snake_head[0] + 20, snake_head[1]],
            [snake_head[0] - 20, snake_head[1]],
            [snake_head[0], snake_head[1] + 20],
            [snake_head[0], snake_head[1] - 20],
        ]
    #Check if Apple is Touching Wall
    for neighbor in neighbors:
        if neighbor == snake.apple_pos:
            apple = True
    #Penalty for Moves that Lead to Walls if the Snake is Long and the Apple is Not Touching a Wall
    if len(snake.snake_pos) > 40:
        if not apple:
            if snake_head[0] < 20 or snake_head[0] >= 380:
                penalty -= 10
            if snake_head[1] < 20 or snake_head[1] >= 380:
                penalty -= 10
    return penalty