import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((576, 800))
clock = pygame.time.Clock()

# Importing Images
bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
bird_surface = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert())

# Variables' Initial Value
floor_x = 0
bird_rect = bird_surface.get_rect(center=(100, 400))

# Game Variables
gravity = 0.25
bird_movement = 0


def moving_floor():
    screen.blit(floor_surface, (floor_x, 675))
    screen.blit(floor_surface, (floor_x + 576, 675))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = bird_movement - 12

    screen.blit(bg_surface, (0, -150))
    bird_movement = bird_movement + gravity
    bird_rect.centery = bird_rect.centery + bird_movement
    screen.blit(bird_surface, bird_rect)
    moving_floor()
    floor_x = floor_x - 1
    if floor_x == -576:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)

    test change
   
