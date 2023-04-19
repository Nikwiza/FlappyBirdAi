import pygame, sys, time
from settings import *
from sprites import BG, Ground, Bird, Obstacle
from random import randint

class Game:
    def __init__(self):
        
        # Window setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI")
        self.clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Sprite init
        BG(self.all_sprites)
        Ground([self.all_sprites, self.collision_sprites])
        self.bird = Bird(self.all_sprites)

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

    def collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False, pygame.sprite.collide_mask)\
            or self.bird.rect.top <=0 :
            pygame.quit()
            sys.exit()

    def run(self):
        
        last_time = time.time()

        # Game loop
        while True:

            # Time elapsed since last itteration
            dt = time.time()-last_time
            last_time = time.time()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump()
                if event.type == self.obstacle_timer:
            
                    # Generating Upper and Lower pipe
                    upper = Obstacle([self.all_sprites, self.collision_sprites], WINDOW_HEIGHT+randint(20,180), 'Up')
                    Obstacle([self.all_sprites, self.collision_sprites], upper.rect.top - PIPE_GAP, 'Down')

            # Game logic



            self.all_sprites.update(dt)
            self.collisions()
            self.display_surface.fill("black")
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.run()