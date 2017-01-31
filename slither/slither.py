import pygame
from game import Game

pygame.init()
icon = pygame.image.load('resources/apple.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Slither")

if __name__ == '__main__':
    game = Game()
    game.game_intro()
