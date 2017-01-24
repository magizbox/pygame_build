import pygame
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

fire_sound = pygame.mixer.Sound("resources/gun.wav")
explosion_sound = pygame.mixer.Sound("resources/explosion.wav")
FPS = 30
block_size = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tanks")

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()

tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWith = 5
barrier_width = 50

ground_height = 30

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


def tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [
        (x - 27, y - 2),
        (x - 26, y - 5),
        (x - 25, y - 8),
        (x - 23, y - 12),
        (x - 20, y - 14),
        (x - 18, y - 15),
        (x - 15, y - 17),
        (x - 13, y - 19),
        (x - 11, y - 21)
    ]
    pygame.draw.circle(gameDisplay, black, (x, y), tankHeight / 2)
    pygame.draw.rect(gameDisplay, black, (x - tankHeight, y, tankWidth, tankHeight))
    position = possibleTurrets[turPos]
    pygame.draw.line(gameDisplay, black, (x, y), position, turretWidth)

    for i in range(-15, 20, 5):
        pygame.draw.circle(gameDisplay, black, (x - i, y + 20), wheelWith)
    return position

def enemy_tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [
        (x + 27, y - 2),
        (x + 26, y - 5),
        (x + 25, y - 8),
        (x + 23, y - 12),
        (x + 20, y - 14),
        (x + 18, y - 15),
        (x + 15, y - 17),
        (x + 13, y - 19),
        (x + 11, y - 21)
    ]
    pygame.draw.circle(gameDisplay, black, (x, y), tankHeight / 2)
    pygame.draw.rect(gameDisplay, black, (x - tankHeight, y, tankWidth, tankHeight))
    position = possibleTurrets[turPos]
    pygame.draw.line(gameDisplay, black, (x, y), position, turretWidth)

    for i in range(-15, 20, 5):
        pygame.draw.circle(gameDisplay, black, (x - i, y + 20), wheelWith)
    return position

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
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                print "press control"
                game_controls()
            if action == "play":
                gameLoop()
            if action == "main":
                print "press main"
                game_intro()
    else:
        pygame.draw.rect(gameDisplay, color, (x, y, w, h))
    text_to_button(text, black, x, y, w, h)


def barrier(xlocation, randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay, black, [xlocation, display_height - randomHeight, barrier_width, randomHeight])
def explosion(x, y, size=50):
    pygame.mixer.Sound.play(explosion_sound)
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        startPoint = x, y
        colorChoices = [red, light_red, yellow, light_yellow]
        magnitude = 1
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1*magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1*magnitude, magnitude)
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0, 4)], (exploding_bit_x, exploding_bit_y), random.randrange(2, 5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False

def fireShell(xy, tankx, tanky, turPos, power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY):
    pygame.mixer.Sound.play(fire_sound)
    damage = 0
    fire = True
    startingShell = list(xy)
    print("FIRE!", xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(startingShell[0], startingShell[1])
        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

        startingShell[0] -= (12 - turPos) * 2
        startingShell[1] += int(((startingShell[0] - xy[0]) * 0.015/(power/50.0)) ** 2 - (turPos + turPos / (12 - turPos)))
        if startingShell[1] > display_height - ground_height:
            print("last shell: ", startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]*display_height - ground_height)/startingShell[1])
            hit_y = int(display_height - ground_height)
            print("Impact:", hit_x, hit_y)
            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                damage = 25
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                damage = 15
            elif enemyTankX + 20> hit_x > enemyTankX - 20:
                damage = 10
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                damage = 5
            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("last shell: ", startingShell[0], startingShell[1])
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage

def e_fireShell(xy, tankx, tanky, turPos, power, xlocation, barrier_width, randomHeight, pTankX, pTankY):
    pygame.mixer.Sound.play(fire_sound)
    currentPower = 1
    powerFound = False
    damange = 0
    while not powerFound:
        currentPower += 1
        if currentPower > 100:
            powerFound = True
        fire = True
        startingShell = list(xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            print(startingShell[0], startingShell[1])
            # pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

            startingShell[0] += (12 - turPos) * 2
            gun_power = random.randrange(int(currentPower * 0.6), int(currentPower * 1.3))
            startingShell[1] += int(((startingShell[0] - xy[0]) * 0.015/(gun_power/50.0)) ** 2 - (turPos + turPos / (12 - turPos)))
            if startingShell[1] > display_height - ground_height:
                hit_x = int((startingShell[0]*display_height - ground_height)/startingShell[1])
                hit_y = int(display_height - ground_height)
                # explosion(hit_x, hit_y)
                if pTankX + 25 > hit_x > pTankX - 25:
                    print("target acquired!")
                    powerFound = True
                if pTankX + 10 > hit_x > pTankX - 10:
                    damange = 25
                if pTankX + 15 > hit_x > pTankX - 15:
                    damange = 20
                if pTankX + 20 > hit_x > pTankX - 20:
                    damange = 10
                if pTankX + 25 > hit_x > pTankX - 25:
                    damange = 5
                fire = False

            check_x_1 = startingShell[0] <= xlocation + barrier_width
            check_x_2 = startingShell[0] >= xlocation
            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(startingShell[0])
                hit_y = int(startingShell[1])
                # explosion(hit_x, hit_y)
                fire = False
    fire = True
    startingShell = list(xy)
    print("FIRE!", xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(startingShell[0], startingShell[1])
        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

        startingShell[0] += (12 - turPos) * 2
        startingShell[1] += int(((startingShell[0] - xy[0]) * 0.015/(currentPower/50.0)) ** 2 - (turPos + turPos / (12 - turPos)))
        if startingShell[1] > display_height - ground_height:
            print("last shell: ", startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]*display_height - ground_height)/startingShell[1])
            hit_y = int(display_height - ground_height)
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("last shell: ", startingShell[0], startingShell[1])
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False
        pygame.display.update()
        clock.tick(60)
    return damange

def power(level):
    text = smallfont.render("Power: " + str(level) + "%", True, black)
    gameDisplay.blit(text, [display_width / 2, 0])


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

def show_game_over():
    game_over = True
    while game_over:
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
        message_to_screen("Game Over!", green, -100, "large")
        message_to_screen("You died", black, -30)

        button("play again", 150, 500, 100, 50, green, light_green, action="play")
        button("controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("quit", 550, 500, 100, 50, red, light_red, action="quit")
        pygame.display.update()
        clock.tick(15)

def show_game_win():
    game_win = True
    while game_win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("You won!", green, -100, "large")
        message_to_screen("Congratulation", black, -30)

        button("play again", 150, 500, 100, 50, green, light_green, action="play")
        button("controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("quit", 550, 500, 100, 50, red, light_red, action="quit")
        pygame.display.update()
        clock.tick(15)

def get_health_color(health):
    color = green
    if health > 75:
        color = green
    elif health > 50:
        color = yellow
    else:
        color = red
    return color
def health_bars(player_health, enemy_heath):
    player_health_color = get_health_color(player_health)
    enemy_heath_color = get_health_color(enemy_heath)
    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_heath_color, (20, 25, enemy_heath, 25))
def gameLoop():
    gameExit = False
    gameOver = False
    player_health = 100
    enemy_health = 100
    mainTankX = display_width * 0.9
    mainTankY = display_height - ground_height - tankHeight
    tankMove = 0
    currentTurPos = 0
    changeTur = 0

    enemyTankX = display_width * 0.1
    enemyTankY = display_height - ground_height - tankHeight

    fire_power = 50
    power_change = 0

    xlocation = (display_width / 2) + random.randint(-0.1 * display_width, 0.1 * display_width)
    randomHeight = random.randrange(display_height * 0.1, display_height * 0.6)

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
                    tankMove = -5
                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                elif event.key == pygame.K_UP:
                    changeTur = 1
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    e_damage = fireShell(gun, mainTankX, mainTankY, currentTurPos, fire_power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY)
                    p_damage = e_fireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, xlocation, barrier_width, randomHeight, mainTankX, mainTankY)
                    player_health -= p_damage
                    player_health = max(0, player_health)
                    enemy_health -= e_damage
                    enemy_health = max(0, enemy_health)
                    possibleMovement = ["f", "r"]
                    moveIndex = random.randrange(0, 2)
                    for x in range(random.randrange(0, 10)):
                        if display_width * 0.3 > enemyTankX > display_width * 0.03:
                            if possibleMovement[moveIndex] == "f":
                               enemyTankX += 5
                            if possibleMovement[moveIndex] == "r":
                                enemyTankX -= 5
                            gameDisplay.fill(white)
                            health_bars(player_health, enemy_health)
                            gun = tank(mainTankX, mainTankY, currentTurPos)
                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
                            fire_power += power_change
                            power(fire_power)
                            barrier(xlocation, randomHeight, barrier_width)
                            gameDisplay.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])
                            pygame.display.update()
                            clock.tick(FPS)
                elif event.key == pygame.K_a:
                    power_change -= 1
                elif event.key == pygame.K_d:
                    power_change += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0
        # gameDisplay.fill(white)
        mainTankX += tankMove
        currentTurPos += changeTur
        currentTurPos = min(currentTurPos, 8)
        currentTurPos = max(currentTurPos, 0)

        if mainTankX - (tankWidth / 2) < xlocation + barrier_width:
            mainTankX += 5

        gameDisplay.fill(white)
        health_bars(player_health, enemy_health)
        gun = tank(mainTankX, mainTankY, currentTurPos)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
        fire_power += power_change

        fire_power = max(1, min(100, fire_power))
        power(fire_power)
        barrier(xlocation, randomHeight, barrier_width)
        gameDisplay.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])
        pygame.display.update()
        clock.tick(FPS)
        # tank(mainTankX, mainTankY, currentTurPos)
        if player_health == 0:
            show_game_over()
        elif enemy_health == 0:
            show_game_win()

if __name__ == '__main__':
    gameLoop()
    pygame.quit()
    quit()
