import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

img = pygame.image.load("head.png")
appleimg = pygame.image.load("apple.png")

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

FPS = 30
AppleThickness = 30
block_size = 20

eat_sound = pygame.mixer.Sound("eat.wav")
start_sound = pygame.mixer.Sound("start.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()


def pause():
    paused = True
    gameDisplay.fill(white)
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit", black, 25)
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


def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0, 0])


def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - AppleThickness))  # / 10.0) * 10
    randAppleY = round(random.randrange(0, display_height - AppleThickness))  # / 10.0) * 10
    return randAppleX, randAppleY


def text_objects(text, color, size="small"):
    if size == "small":
        font = smallfont
    if size == "medium":
        font = medfont
    if size == "large":
        font = largefont
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    # screen_text = font.render(msg, True, color)
    gameDisplay.blit(textSurf, textRect)


def game_intro():
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
        gameDisplay.fill(white)
        message_to_screen("Welcom to Slither", green, -100, "large")
        message_to_screen("The objective of the game is to ead red apples", black, -30)
        message_to_screen("The more apples you eat, the longer you get", black, 10)
        message_to_screen("If you run into yourself, or the edges, you die!", black, 50)
        message_to_screen("Press C to play or Q to quit", black, 180)
        pygame.display.update()
        clock.tick(15)


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
    direction = "left"
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = -10
    lead_y_change = 0

    snakeLength = 1
    snakeList = [[-1, -1]] * (snakeLength - 1)

    randAppleX, randAppleY = randAppleGen()
    pygame.mixer.Sound.play(start_sound)
    while not gameExit:
        if gameOver:
            pygame.mixer.Sound.play(game_over_sound)
            gameDisplay.fill(white)
            message_to_screen("Game over", red, -80, size="large")
            message_to_screen("Press C to play again or Q to quit", black, size="medium")
            pygame.display.update()
        while gameOver:
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
                elif event.key == pygame.K_p:
                    pause()
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)

        # pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))

        snakeHead = [lead_x, lead_y]
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for segment in snakeList[:-1]:
            if segment == snakeHead:
                gameOver = True
        snake(block_size, snakeList)

        score(snakeLength - 1)
        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                pygame.mixer.Sound.play(eat_sound)
                snakeLength += 1
                randAppleX, randAppleY = randAppleGen()

        clock.tick(FPS)


game_intro()
gameLoop()
pygame.quit()
quit()
