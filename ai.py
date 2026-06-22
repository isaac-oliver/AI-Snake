def choose_direction(snake_head,apple_pos):
    if snake_head[0] < apple_pos[0]:
        return "RIGHT"
    elif snake_head[0] > apple_pos[0]:
        return "LEFT"
    elif snake_head[1] < apple_pos[1]:
        return "DOWN"
    else:
        return "UP"