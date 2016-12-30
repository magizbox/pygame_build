import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

img = pygame.image.load("head.png")

FPS = 30
block_size = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")

font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()
direction = "left"

def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0):
    textSurf, textRect = text_objects(msg, color)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    # screen_text = font.render(msg, True, color)
    gameDisplay.blit(textSurf, textRect)


def snake(block_size, snakelist):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for position in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [position[0], position[1], block_size, block_size])


def gameLoop():
    global direction
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = -10
    lead_y_change = 0

    snakeLength = 1
    snakeList = [[-1, -1]] * (snakeLength - 1)
    randAppleX = round(random.randrange(0, display_width - block_size))  # / 10.0) * 10
    randAppleY = round(random.randrange(0, display_height - block_size))  # / 10.0) * 10
    while not gameExit:
        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("Game over", red, -50)
            message_to_screen("Press C to play again or Q to quit", black)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

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
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)

        AppleThickness = 30
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        snakeHead = [lead_x, lead_y]
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for segment in snakeList[:-1]:
            if segment == snakeHead:
                gameOver = True
        snake(block_size, snakeList)

        pygame.display.update()

        # if randAppleX <= lead_x <= randAppleX + AppleThickness and randAppleY <= lead_y <= randAppleY + AppleThickness:
        #     snakeLength += 1
        #     randAppleX = round(random.randrange(0, display_width - block_size))# / 10.0) * 10
        #     randAppleY = round(random.randrange(0, display_height - block_size))# / 10.0) * 10
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                snakeLength += 1
                randAppleX = round(random.randrange(0, display_width - block_size))  # / 10.0) * 10
                randAppleY = round(random.randrange(0, display_height - block_size))  # / 10.0) * 10

        clock.tick(FPS)


gameLoop()
pygame.quit()
quit()
