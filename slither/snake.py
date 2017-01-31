class Snake:
    def __init__(self, x, y):
        self.direction = "left"
        self.x = x
        self.y = y
        self.x_change = -10
        self.y_change = 0
        self.length = 1
        self.list = []
        self.block_size = 20

    def move_left(self):
        self.direction = "left"
        self.x_change = -self.block_size
        self.y_change = 0

    def move_right(self):
        self.direction = "right"
        self.x_change = self.block_size
        self.y_change = 0

    def move_up(self):
        self.direction = "up"
        self.x_change = 0
        self.y_change = -self.block_size

    def move_down(self):
        self.direction = "down"
        self.x_change = 0
        self.y_change = self.block_size

    def update(self):
        self.x += self.x_change
        self.y += self.y_change
        snake_head = [self.x, self.y]
        self.list.append(snake_head)

        if len(self.list) > self.length:
            del self.list[0]

    def is_die(self, game):
        if self.is_boundary(game):
            return True
        snake_head = [self.x, self.y]
        for segment in self.list[:-1]:
            if segment == snake_head:
                return True
        return False

    def is_boundary(self, game):
        display_width = game.display_width
        display_height = game.display_height
        return self.x >= display_width or self.x < 0 or self.y >= display_height or self.y < 0
