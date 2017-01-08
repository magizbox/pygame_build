import pygame

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

FPS = 30
block_size = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("3D")

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()


def draw_cube(startPoint, size):
    x, y = startPoint
    node_1 = [x, y]
    node_2 = [x + size, y]
    node_3 = [x, y + size]
    node_4 = [x + size, y + size]
    offset = int(size / 2)
    x_mid = int(display_width / 2)
    x_offset = -1 * int((startPoint[0] - x_mid))
    y_mid = int(display_height/ 2)
    y_offset = -1 * int((startPoint[1] - y_mid))
    if x_offset < -100:
        x_offset = -100
    if x_offset > 100:
        x_offset = 100
    node_5 = [node_1[0] + x_offset, node_1[1] - y_offset]
    node_6 = [node_2[0] + x_offset, node_2[1] - y_offset]
    node_7 = [node_3[0] + x_offset, node_3[1] - y_offset]
    node_8 = [node_4[0] + x_offset, node_4[1] - y_offset]

    pygame.draw.line(gameDisplay, white, node_1, node_2)
    pygame.draw.line(gameDisplay, white, node_3, node_4)
    pygame.draw.line(gameDisplay, white, node_1, node_3)
    pygame.draw.line(gameDisplay, white, node_2, node_4)

    pygame.draw.line(gameDisplay, white, node_5, node_6)
    pygame.draw.line(gameDisplay, white, node_7, node_8)
    pygame.draw.line(gameDisplay, white, node_5, node_7)
    pygame.draw.line(gameDisplay, white, node_6, node_8)

    pygame.draw.line(gameDisplay, white, node_1, node_5)
    pygame.draw.line(gameDisplay, white, node_2, node_6)
    pygame.draw.line(gameDisplay, white, node_3, node_7)
    pygame.draw.line(gameDisplay, white, node_4, node_8)

    pygame.draw.circle(gameDisplay, light_green, node_1, 5)
    pygame.draw.circle(gameDisplay, light_green, node_2, 5)
    pygame.draw.circle(gameDisplay, light_green, node_3, 5)
    pygame.draw.circle(gameDisplay, light_green, node_4, 5)
    pygame.draw.circle(gameDisplay, light_green, node_5, 5)
    pygame.draw.circle(gameDisplay, light_green, node_6, 5)
    pygame.draw.circle(gameDisplay, light_green, node_7, 5)
    pygame.draw.circle(gameDisplay, light_green, node_8, 5)


def gameLoop():
    location = [300, 200]
    size = 200

    current_move = 0
    gameExit = False

    z_move = 0
    x_move = 0
    y_move = 0
    z_location = 1

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = -5
                elif event.key == pygame.K_RIGHT:
                    x_move = 5
                elif event.key == pygame.K_UP:
                    y_move = -5
                    # z_move = -10
                elif event.key == pygame.K_DOWN:
                    y_move = 5
                    # z_move = 10
            elif event.type == pygame.KEYUP:
                if event.type == pygame.K_LEFT or pygame.K_RIGHT:
                    x_move = 0
                    current_move = 0
                if event.type == pygame.K_UP or pygame.K_DOWN:
                    y_move = 0
                    # z_move = 0
        gameDisplay.fill(black)
        size += z_move
        location[0] += x_move
        location[1] += y_move
        draw_cube(location, size)
        pygame.display.update()
        clock.tick(FPS)


gameLoop()
pygame.quit()
quit()
