import random

import pygame

from apple import Apple
from snake import Snake

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

pygame.init()
display_width = 800
display_height = 600

FPS = 30
block_size = 20

img = pygame.image.load("resources/head.png")
appleimg = pygame.image.load("resources/apple.png")

game_display = pygame.display.set_mode((display_width, display_height))
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()

apple_thickness = 30

eat_sound = pygame.mixer.Sound("resources/eat.wav")
start_sound = pygame.mixer.Sound("resources/start.wav")
game_over_sound = pygame.mixer.Sound("resources/game_over.wav")


class Game:
    def __init__(self):
        self.display_width = display_width
        self.display_height = display_height
        self.create_apple()
        self.create_snake()

    def create_apple(self):
        randAppleX = round(random.randrange(0, display_width - apple_thickness))  # / 10.0) * 10
        randAppleY = round(random.randrange(0, display_height - apple_thickness))  # / 10.0) * 10
        self.apple = Apple(randAppleX, randAppleY)

    def create_snake(self):
        x = display_width / 2
        y = display_height / 2
        self.snake = Snake(x, y)

    def game_pause(self):
        paused = True
        game_display.fill(white)
        self.message_to_screen("Paused", black, -100, "large")
        self.message_to_screen("Press C to continue or Q to quit", black, 25)
        pygame.display.update()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
            clock.tick(5)

    def text_objects(self, text, color, size="small"):
        if size == "small":
            font = smallfont
        if size == "medium":
            font = medfont
        if size == "large":
            font = largefont
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_to_screen(self, msg, color, y_displace=0, size="small"):
        textSurf, textRect = self.text_objects(msg, color, size)
        textRect.center = (display_width / 2), (display_height / 2) + y_displace
        # screen_text = font.render(msg, True, color)
        game_display.blit(textSurf, textRect)

    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.game_loop()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
            game_display.fill(white)
            self.message_to_screen("Welcome to Slither", green, -100, "large")
            self.message_to_screen("The objective of the game is to ead red apples", black, -30)
            self.message_to_screen("The more apples you eat, the longer you get", black, 10)
            self.message_to_screen("If you run into yourself, or the edges, you die!", black, 50)
            self.message_to_screen("Press C to play or Q to quit", black, 180)
            pygame.display.update()
            clock.tick(15)

    def draw_snake(self, block_size):
        snakelist = self.snake.list
        direction = self.snake.direction
        if direction == "right":
            head = pygame.transform.rotate(img, 270)
        if direction == "left":
            head = pygame.transform.rotate(img, 90)
        if direction == "up":
            head = img
        if direction == "down":
            head = pygame.transform.rotate(img, 180)
        game_display.blit(head, (snakelist[-1][0], snakelist[-1][1]))
        for position in snakelist[:-1]:
            pygame.draw.rect(game_display, green, [position[0], position[1], block_size, block_size])

    def draw_apple(self):
        game_display.blit(appleimg, (self.apple.x, self.apple.y))

    def is_eat(self):
        apple_x = self.apple.x
        apply_y = self.apple.y
        apple_thickness = self.apple.apple_thick_ness
        lead_x = self.snake.x
        lead_y = self.snake.y
        if lead_x > apple_x and lead_x < apple_x + apple_thickness or lead_x + block_size > apple_x and lead_x + block_size < apple_x + apple_thickness:
            if lead_y > apply_y and lead_y < apply_y + apple_thickness or lead_y + block_size > apply_y and lead_y + block_size < apply_y + apple_thickness:
                return True
        return False

    def update(self):
        self.snake.update()

    def game_over(self):
        pygame.mixer.Sound.play(game_over_sound)
        game_display.fill(white)
        self.message_to_screen("Game over", red, -80, size="large")
        self.message_to_screen("Press C to play again or Q to quit", black, size="medium")
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
                    if event.key == pygame.K_c:
                        self.create_snake()
                        self.game_loop()

    def game_loop(self):
        pygame.mixer.Sound.play(start_sound)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.snake.move_right()
                    elif event.key == pygame.K_UP:
                        self.snake.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.snake.move_down()
                    elif event.key == pygame.K_p:
                        self.game_pause()
            self.update()
            self.draw()
            if self.snake.is_die(self):
                self.game_over()
                return
            if self.is_eat():
                pygame.mixer.Sound.play(eat_sound)
                self.snake.eat()
                self.create_apple()
            clock.tick(FPS)

    def draw_score(self, score):
        text = smallfont.render("Score: " + str(score), True, black)
        game_display.blit(text, [0, 0])

    def draw(self):
        game_display.fill(white)
        self.draw_apple()
        self.draw_snake(block_size)
        self.draw_score(self.snake.length - 1)
        pygame.display.update()
