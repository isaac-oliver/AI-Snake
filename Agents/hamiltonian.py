def choose_direction(snake):
    snake_head = snake.snake_pos[0]
    if snake_head == [380,300] and snake.direction == "RIGHT":
        return "UP"
    if snake_head == [380,0] and snake.direction == "UP":
        return "LEFT"
    if snake_head == [0,380]:
        return "RIGHT"
    if snake_head == [380,380]:
        return "UP"
    for i in list(range(0,380,20)):
        if snake_head == [i,0] and snake.direction == "LEFT":
            return "DOWN"
    for i in list(range(20,380,20)):
        if snake_head == [i,360] and snake.direction == "LEFT":
            return "UP"
    for i in list (range(20,380,20)):
        if snake_head == [i,360] and snake.direction == "DOWN":
            return "LEFT"
        if snake_head == [i,0] and snake.direction == "UP":
            return "LEFT"

    