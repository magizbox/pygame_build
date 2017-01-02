import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
green = (34, 177, 76)
light_green = (0, 255, 0)

display_width = 800
display_height = 600

# img = pygame.image.load("head.png")
# appleimg = pygame.image.load("apple.png")

# icon = pygame.image.load('apple.png')
# pygame.display.set_icon(icon)

FPS = 30
AppleThickness = 30
block_size = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tanks")

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


def game_controls():
    is_control = True
    while is_control:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("Controls", green, -100, "large")
        message_to_screen("Fire: Spacebar", black, -30)
        message_to_screen("Move Turret: Up and Down arrows", black, 10)
        message_to_screen("Move Tank: Left and Right arrow", black, 50)
        message_to_screen("Pause: P", black, 90)

        button("play", 150, 500, 100, 50, green, light_green, action="play")
        button("main menu", 350, 500, 100, 50, yellow, light_yellow, action="main")
        button("quit", 550, 500, 100, 50, red, light_red, action="quit")
        pygame.display.update()
        clock.tick(15)

def text_to_button(msg, color, x, y, w, h, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((x + w / 2), y + h / 2)
    gameDisplay.blit(textSurf, textRect)


def button(text, x, y, w, h, color, active_color, action=None):
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > cursor[0] > x and y + h > cursor[1] > y:
        c = active_color
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "main":
                game_intro()
    else:
        c = color
    pygame.draw.rect(gameDisplay, c, (x, y, w, h))
    text_to_button(text, black, x, y, w, h)


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
        message_to_screen("Welcome to Tanks!", green, -100, "large")
        message_to_screen("The objective of the game is to shot and destroy", black, -30)
        message_to_screen("the enemy tank before they destroy you.", black, 10)
        message_to_screen("The more enemies you destroy, the harder they get.", black, 50)

        button("play", 150, 500, 100, 50, green, light_green, action="play")
        button("controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("quit", 550, 500, 100, 50, red, light_red, action="quit")
        pygame.display.update()
        clock.tick(15)


def gameLoop():
    gameExit = False
    gameOver = False

    while not gameExit:
        if gameOver:
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
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_p:
                    pause()
        gameDisplay.fill(white)
        pygame.display.update()
        clock.tick(FPS)


game_intro()
gameLoop()
pygame.quit()
quit()
