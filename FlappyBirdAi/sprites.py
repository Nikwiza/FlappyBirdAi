import pygame
from settings import *
from random import randint

class BG(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        background_image = pygame.image.load('assets/images/background.png').convert()
        image_width = WINDOW_WIDTH*IMAGE_SCALE
        image_height = WINDOW_HEIGHT*IMAGE_SCALE

        resized_image = pygame.transform.scale(background_image, (image_width, image_height))

        self.image = pygame.Surface((image_width*2, image_height))
        self.image.blit(resized_image, (0,0))
        self.image.blit(resized_image, (image_width,0))
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -=300 * dt
        if self.rect.centerx<=0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x) 

class Ground(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        ground_surface = pygame.image.load('assets/images/ground.png').convert_alpha()

        # Scaling ground
        height = ground_surface.get_height()*0.4
        width = ground_surface.get_width()*IMAGE_SCALE
        resized_image = pygame.transform.scale(ground_surface, (width, height))

        # Doubling the ground

        self.image = pygame.Surface((width*2, height))
        self.image.blit(resized_image, (0,0))
        self.image.blit(resized_image, (width,0))

        # Positioning ground
        self.rect = self.image.get_rect(bottomleft = (0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.pos.x -=360*dt
        if(self.rect.centerx<=0):
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
        
class Bird(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        
        # Image
        bird_image = pygame.image.load('assets/images/player.png').convert_alpha()
        self.image = pygame.transform.scale(bird_image, pygame.math.Vector2(bird_image.get_size())*CHARACTER_SIZE)
        self.reload_image = self.image

        # Position
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Movement
        self.gravity = GRAVITY
        self.direction = 0

        # Mask
        self.mask = pygame.mask.from_surface(self.image)


    def spinTest(self):
        self.testSpin+=0.1

    def apply_gravity (self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)


    def jump(self):
        self.direction = -JUMP_HEIGHT

    def reload(self):
        self.image = self.reload_image


    def rotate(self):

        # The animation on rotozoom might be better than on rotate
        rotated_image = pygame.transform.rotozoom(self.image, -self.direction * ROTATION_SPEED, 1) 
        self.image = rotated_image
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.apply_gravity(dt)
        self.reload()
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group, height, orientation):
        super().__init__(group)

        # Set the image
        pipe_image = pygame.image.load('assets/images/whole_pipe.png').convert_alpha()
        self.image = pygame.transform.scale(pipe_image, pygame.math.Vector2(pipe_image.get_size())*PIPE_SCALE)

        # Set tipe of pipe (Up or Down facing)
        x = WINDOW_WIDTH + 40
        if orientation == 'Up':
            self.rect = self.image.get_rect(midbottom = (x, height))
        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midbottom = (x, height))
        
        self.pos = pygame.math.Vector2(self.rect.bottomright)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 400*dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -10:
            self.kill()



        
