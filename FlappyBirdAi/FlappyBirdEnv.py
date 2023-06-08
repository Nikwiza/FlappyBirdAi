# Imports for pygame

import pygame, sys, time
from settings import *
from sprites import BG, Ground, Bird, Obstacle
from random import randint

# Imports for AI env

from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random


class Game(Env):
    def __init__(self):

        # Window setup
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI")

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.agents = pygame.sprite.Group()

        # Sprite init
        BG(self.all_sprites)
        Ground([self.all_sprites, self.collision_sprites])
        self.bird = Bird(self.all_sprites)

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, PIPE_SPAWN_SPEED)
        self.timestamp = 0

        # Font 
        self.score = 0

        #Ai
       
        self.action_space = Discrete(2)
        self.observation_space = Box(low=-WINDOW_WIDTH, high=WINDOW_WIDTH, shape = (1, 5), dtype=np.float32)
        
        self.clock = pygame.time.Clock()
        pygame.init()


    def display_score(self):
        
        self.font = pygame.font.Font(None, SCORE_SIZE)
        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(topleft = (0, 0))
        self.display_surface.blit(score_surf, score_rect)

    def collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False, pygame.sprite.collide_mask)\
            or self.bird.rect.top <=0 :
            self.timestamp = pygame.time.get_ticks()//1000
            self.done = True


    def step(self, action):
        
        # Time elapsed since last itteration
        # dt = time.time()- self.last_time_temp
        # last_time = time.time()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #         self.bird.jump()
            # If action is 1 the bird will jump, if not it won't
            if event.type == self.obstacle_timer:
        
                # Generating Upper and Lower pipe
                upper = Obstacle([self.all_sprites, self.collision_sprites], WINDOW_HEIGHT+randint(20,180), 'Up')
                Obstacle([self.all_sprites, self.collision_sprites], upper.rect.top - PIPE_GAP, 'Down')

        #Check if the bird needs to jump
        if action :
            self.bird.jump()

        # Updating observations

        self.all_sprites.update(ANIMATION_SPEED)
        self.collisions()

        # Updating score

        if pygame.time.get_ticks()//1000 - self.timestamp > 1:
            self.score += 1
            self.timestamp = pygame.time.get_ticks()//1000

        # Observations

        if len(self.collision_sprites.sprites()) <= 1:
            distance_to_lower_pipe_x = WINDOW_WIDTH
            distance_to_lower_pipe_y = WINDOW_WIDTH
            pipe_height = WINDOW_HEIGHT
        else:
            distance_to_lower_pipe_x = self.collision_sprites.sprites()[1].rect.topleft[0] - self.bird.rect.x
            distance_to_lower_pipe_y = self.collision_sprites.sprites()[1].rect.topleft[1] - self.bird.rect.y
            pipe_height = self.collision_sprites.sprites()[1].rect.top
        agent_velocity = self.bird.direction
        agent_y = self.bird.rect.y

        self.observation = [distance_to_lower_pipe_x, distance_to_lower_pipe_y, agent_velocity, pipe_height, agent_y]
        self.observation = np.array(self.observation)

        # Calculating rewards

        if self.done:
            self.reward -= 1000
        # else :
        #     self.reward +=2

        # if self.score > self.previous_score:
        #     self.reward +=20
        
        
        


        info = {}
        self.render()

        return self.observation, self.reward, self.done, info
        

    def render(self):

            self.display_surface.fill("black")
            self.all_sprites.draw(self.display_surface)
            self.agents.draw(self.display_surface)
            self.display_score()
            pygame.display.update()
            self.clock.tick(FPS)

    def reset(self):

        # Variables
        self.done = False

        # Resrtarting Sprites
        self.bird.kill()
        self.bird = Bird(self.all_sprites)
        for sprite in self.collision_sprites:
            if not isinstance(sprite, Ground):
                sprite.kill()

        # Initial observation

        distance_to_lower_pipe_x = WINDOW_WIDTH
        distance_to_lower_pipe_y = WINDOW_WIDTH
        agent_velocity = 0
        pipe_height = WINDOW_HEIGHT
        agent_y = self.bird.rect.y

        #Initial reward
        self.reward = 0
        self.previous_score = self.score
        self.score = 0


        self.observation = [distance_to_lower_pipe_x, distance_to_lower_pipe_y, agent_velocity, pipe_height, agent_y]
        self.observation = np.array(self.observation)


        self.render()

        return self.observation

        

