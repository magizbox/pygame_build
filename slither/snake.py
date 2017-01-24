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
