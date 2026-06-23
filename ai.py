def choose_direction(snake_head,apple_pos,direction,width,height):
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
    