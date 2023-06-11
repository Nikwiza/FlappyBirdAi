import random
import sys
import pygame
from pygame.locals import *

# Global Variables

window_height = 499
window_width = 600

# Window initialization

window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
fps = 32
background_image = 'assets/images/background.png'
ground_image = 'assets/images/ground.png'
pipe_upper_image = 'assets/images/pipe_upper.png'
pipe_lower_image = 'assets/images/pipe_lower.png'
player = 'assets/images/player.png'

if __name__ == "__main__":
    # Initializing the whindow
    pygame.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird QL')

    #The game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.display.update()
        fps_clock.tick(fps)


