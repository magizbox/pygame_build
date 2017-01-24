import pygame
import random
from game import Game

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

img = pygame.image.load("resources/head.png")
appleimg = pygame.image.load("resources/apple.png")

icon = pygame.image.load('resources/apple.png')
pygame.display.set_icon(icon)

FPS = 30
apple_thickness = 30
block_size = 20

eat_sound = pygame.mixer.Sound("resources/eat.wav")
start_sound = pygame.mixer.Sound("resources/start.wav")
game_over_sound = pygame.mixer.Sound("resources/game_over.wav")

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()

game = Game()

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - apple_thickness))  # / 10.0) * 10
    randAppleY = round(random.randrange(0, display_height - apple_thickness))  # / 10.0) * 10
    return randAppleX, randAppleY



def snake(block_size, snakelist):
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


def game_loop():
    global direction
    direction = "left"
    game_exit = False
    game_over = False

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = -10
    lead_y_change = 0

    snakeLength = 1
    snakeList = [[-1, -1]] * (snakeLength - 1)

    randAppleX, randAppleY = randAppleGen()
    pygame.mixer.Sound.play(start_sound)
    while not game_exit:
        if game_over:
            pygame.mixer.Sound.play(game_over_sound)
            game_display.fill(white)
            game.message_to_screen("Game over", red, -80, size="large")
            game.message_to_screen("Press C to play again or Q to quit", black, size="medium")
            pygame.display.update()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    game.pause()
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        game_display.fill(white)

        # pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        game_display.blit(appleimg, (randAppleX, randAppleY))

        snake_head = [lead_x, lead_y]
        snakeList.append(snake_head)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for segment in snakeList[:-1]:
            if segment == snake_head:
                game_over = True
        snake(block_size, snakeList)

        game.score(snakeLength - 1)
        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + apple_thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_thickness:
            if lead_y > randAppleY and lead_y < randAppleY + apple_thickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_thickness:
                pygame.mixer.Sound.play(eat_sound)
                snakeLength += 1
                randAppleX, randAppleY = randAppleGen()

        clock.tick(FPS)


if __name__ == '__main__':
    game.game_intro()
    game_loop()
    pygame.quit()
    quit()
