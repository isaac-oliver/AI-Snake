from collections import deque

DIRECTIONS = {
    'UP': (0, -1),
    'RIGHT': (1, 0),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
}
VECTOR_TO_DIRECTION = {value: key for key, value in DIRECTIONS.items()}


def _add(a, b):
    return a[0] + b[0], a[1] + b[1]


def _in_bounds(cell, width, height):
    return 0 <= cell[0] < width and 0 <= cell[1] < height


def _normalize_point(point):
    if point is None:
        return None
    if hasattr(point, 'x') and hasattr(point, 'y'):
        return int(point.x), int(point.y)
    if isinstance(point, (list, tuple)) and len(point) >= 2:
        return int(point[0]), int(point[1])
    raise ValueError('Unsupported point type: %r' % (point,))


def _normalize_snake(snake):
    if snake is None:
        return []
    if isinstance(snake, dict):
        snake = snake.get('positions') or snake.get('body') or snake.get('snake') or []
    return [_normalize_point(part) for part in snake]


def _safe_neighbors(cell, width, height, blocked):
    for delta in DIRECTIONS.values():
        candidate = _add(cell, delta)
        if _in_bounds(candidate, width, height) and candidate not in blocked:
            yield candidate


def _bfs(start, goal, blocked, width, height):
    if start == goal:
        return [start]
    queue = deque([start])
    parents = {start: None}
    while queue:
        current = queue.popleft()
        for neighbor in _safe_neighbors(current, width, height, blocked):
            if neighbor in parents:
                continue
            parents[neighbor] = current
            if neighbor == goal:
                path = [neighbor]
                while current is not None:
                    path.append(current)
                    current = parents[current]
                return list(reversed(path))
            queue.append(neighbor)
    return None


def _serpentine_cycle(width, height):
    cycle = {}
    if width % 2 == 0:
        path = []
        for y in range(height):
            row = range(width) if y % 2 == 0 else range(width - 1, -1, -1)
            for x in row:
                path.append((x, y))
    elif height % 2 == 0:
        path = []
        for x in range(width):
            col = range(height) if x % 2 == 0 else range(height - 1, -1, -1)
            for y in col:
                path.append((x, y))
    else:
        path = []
        for y in range(height):
            row = range(width) if y % 2 == 0 else range(width - 1, -1, -1)
            for x in row:
                path.append((x, y))
    for current, nxt in zip(path, path[1:]):
        cycle[current] = nxt
    if width % 2 == 0 or height % 2 == 0:
        cycle[path[-1]] = path[0]
    return cycle


def _vector_to_direction(vector):
    return VECTOR_TO_DIRECTION.get(vector)


def _parse_state(state):
    if isinstance(state, dict):
        snake = state.get('snake') or state.get('body') or state.get('snake_body')
        food = state.get('food') or state.get('apple') or state.get('target')
        width = state.get('width') or state.get('w') or state.get('cols') or state.get('columns')
        height = state.get('height') or state.get('h') or state.get('rows')
    else:
        snake = getattr(state, 'snake', None) or getattr(state, 'body', None) or getattr(state, 'snake_body', None)
        food = getattr(state, 'food', None) or getattr(state, 'apple', None) or getattr(state, 'target', None)
        width = getattr(state, 'width', None) or getattr(state, 'w', None) or getattr(state, 'cols', None) or getattr(state, 'columns', None)
        height = getattr(state, 'height', None) or getattr(state, 'h', None) or getattr(state, 'rows', None)
    snake = _normalize_snake(snake)
    if food is None:
        raise ValueError('State does not contain food position')
    food = _normalize_point(food)
    if width is None or height is None:
        raise ValueError('State does not contain board width/height')
    return snake, food, int(width), int(height)


class SnakeAgent:
    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height
        self.cycle = {}
        if width is not None and height is not None:
            self.cycle = _serpentine_cycle(width, height)

    def reset(self, width, height):
        if self.width != width or self.height != height:
            self.width = width
            self.height = height
            self.cycle = _serpentine_cycle(width, height)

    def get_action(self, state):
        snake, food, width, height = _parse_state(state)
        return self.next_action(snake, food, width, height)

    def next_action(self, snake, food, width, height):
        if not snake:
            raise ValueError('Snake body is empty')
        self.reset(width, height)
        head = snake[0]
        blocked = set(snake[:-1])
        path = _bfs(head, food, blocked, width, height)
        if path and len(path) > 1:
            next_cell = path[1]
            direction = _vector_to_direction((next_cell[0] - head[0], next_cell[1] - head[1]))
            if direction:
                return direction
        if head in self.cycle:
            next_cell = self.cycle[head]
            direction = _vector_to_direction((next_cell[0] - head[0], next_cell[1] - head[1]))
            if direction:
                return direction
        for action, delta in DIRECTIONS.items():
            candidate = _add(head, delta)
            if _in_bounds(candidate, width, height) and candidate not in blocked:
                return action
        return 'UP'


class RandomAgent:
    def __init__(self, width=None, height=None):
        self.agent = SnakeAgent(width, height)

    def get_action(self, state):
        return self.agent.get_action(state)

    def next_action(self, snake, food, width, height):
        return self.agent.next_action(snake, food, width, height)


Agent = RandomAgent
