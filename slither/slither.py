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

icon = pygame.image.load('resources/apple.png')
pygame.display.set_icon(icon)

FPS = 30
block_size = 20

eat_sound = pygame.mixer.Sound("resources/eat.wav")
start_sound = pygame.mixer.Sound("resources/start.wav")
game_over_sound = pygame.mixer.Sound("resources/game_over.wav")

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")

clock = pygame.time.Clock()

game = Game()


def game_loop():
    game_exit = False
    game_over = False

    snakeLength = 1
    snakeList = [[-1, -1]] * (snakeLength - 1)

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
                    game.snake.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.snake.move_right()
                elif event.key == pygame.K_UP:
                    game.snake.move_up()
                elif event.key == pygame.K_DOWN:
                    game.snake.move_down()
                elif event.key == pygame.K_p:
                    game.pause()
        if game.is_boundary():
            game_over = True

        game.update()
        game_display.fill(white)

        game.draw_apple()
        snake_head = [game.snake.x, game.snake.y]
        snakeList.append(snake_head)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for segment in snakeList[:-1]:
            if segment == snake_head:
                game_over = True
        game.draw_snake(block_size, snakeList)

        game.draw_score(snakeLength - 1)
        pygame.display.update()

        apple_x = game.apple.x
        apply_y = game.apple.y
        apple_thickness = game.apple.apple_thick_ness
        lead_x = game.snake.x
        lead_y = game.snake.y
        if lead_x > apple_x and lead_x < apple_x + apple_thickness or lead_x + block_size > apple_x and lead_x + block_size < apple_x + apple_thickness:
            if lead_y > apply_y and lead_y < apply_y + apple_thickness or lead_y + block_size > apply_y and lead_y + block_size < apply_y + apple_thickness:
                pygame.mixer.Sound.play(eat_sound)
                snakeLength += 1
                game.create_apple()

        clock.tick(FPS)


if __name__ == '__main__':
    game.game_intro()
    game_loop()
    pygame.quit()
    quit()
