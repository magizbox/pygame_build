import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    icon = pygame.image.load('resources/apple.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Slither")
    game = Game()
    game.game_intro()
