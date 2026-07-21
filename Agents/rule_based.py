def choose_direction(snake):
    snake_pos = snake.snake_pos
    snake_head = snake.snake_pos[0]
    apple_pos = snake.apple_pos
    direction = snake.direction
    width = 400
    height = 400
    if check_collision(snake_pos,snake_head,direction) != False:
        return check_collision(snake_pos,snake_head,direction)
    else:
        if snake_head[0] < apple_pos[0]:
            if direction == "LEFT":
                if snake_head[1] > height - 20:
                    return "DOWN"
                else:
                    return "UP"
            else:
                return "RIGHT"
        elif snake_head[0] > apple_pos[0]:
            if direction == "RIGHT":
                if snake_head[1] > height - 20:
                    return "DOWN"
                else:
                    return "UP"
            else:
                return "LEFT"
        elif snake_head[1] < apple_pos[1]:
            if direction == "UP":
                if snake_head[0] > width - 20:
                    return "RIGHT"
                else:
                    return "LEFT"
            else:
                return "DOWN"
        elif snake_head[1] > apple_pos[1]:
            if direction == "DOWN":
                if snake_head[0] > width - 20:
                    return "RIGHT"
                else:
                    return "LEFT"
            else:
                return "UP"


def check_collision(snake_pos,snake_head,direction):
    if direction == "RIGHT":
        for block in snake_pos[1:]:
            if snake_head[0] + 20 == block[0] and snake_head[1] == block[1]:
                if snake_head[1] + 20 == block[1]:
                    return "DOWN"
                else:
                    return "UP"
    elif direction == "LEFT":
        for block in snake_pos[1:]:
            if snake_head[0] - 20 == block[0] and snake_head[1] == block[1]:
                if snake_head[1] + 20 == block[1]:
                    return "DOWN"
                else:
                    return "UP"
    elif direction == "UP":
        for block in snake_pos[1:]:
            if snake_head[0] == block[0] and snake_head[1] - 20 == block[1]:
                if snake_head[0] + 20 == block[0]:
                    return "RIGHT"
                else:
                    return "LEFT"
    elif direction == "DOWN":
        for block in snake_pos[1:]:
            if snake_head[0] == block[0] and snake_head[1] + 20 == block[1]:
                if snake_head[0] + 20 == block[0]:
                    return "RIGHT"
                else:
                    return "LEFT"
    return False


    
    