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

img = pygame.image.load("resources/head.png")
appleimg = pygame.image.load("resources/apple.png")

game_display = pygame.display.set_mode((display_width, display_height))
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()

apple_thickness = 30


class Game:
    def __init__(self):
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
    def pause(self, game_display):
        paused = True
        game_display.fill(white)
        Game.message_to_screen("Paused", black, -100, "large")
        Game.message_to_screen("Press C to continue or Q to quit", black, 25)
        pygame.display.update()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
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
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            game_display.fill(white)
            self.message_to_screen("Welcom to Slither", green, -100, "large")
            self.message_to_screen("The objective of the game is to ead red apples", black, -30)
            self.message_to_screen("The more apples you eat, the longer you get", black, 10)
            self.message_to_screen("If you run into yourself, or the edges, you die!", black, 50)
            self.message_to_screen("Press C to play or Q to quit", black, 180)
            pygame.display.update()
            clock.tick(15)

    def draw_score(self, score):
        text = smallfont.render("Score: " + str(score), True, black)
        game_display.blit(text, [0, 0])

    def draw_snake(self, block_size, snakelist):
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

    def is_boundary(self):
        return self.snake.x >= display_width or self.snake.x < 0 or self.snake.y >= display_height or self.snake.y < 0

    def update(self):
        self.snake.update()
