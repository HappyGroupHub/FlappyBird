import sys
import pygame
from random import randrange

# Starting
pygame.init()
screen = pygame.display.set_mode((576, 800))
clock = pygame.time.Clock()

# Importing Images
bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
bird_surface = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert())
pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())

# Objects' Locations and Variables
floor_x = 0
bird_rect = bird_surface.get_rect(center=(100, 400))

# Game Variables
gravity = 0.25
bird_movement = 0

# Spawn Pipes
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)


def create_floor():
    screen.blit(floor_surface, (floor_x, 675))
    screen.blit(floor_surface, (floor_x + 576, 675))


def create_pipe():
    random_pipe_ypos = randrange(300, 575)
    bottom_pipe = pipe_surface.get_rect(midtop=(600, random_pipe_ypos))
    top_pipe = pipe_surface.get_rect(midbottom=(600, random_pipe_ypos - 300))

    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 900:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


while True:
    for event in pygame.event.get():

        # Esc button triggered event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Space button triggered event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 10

        # Spawn pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Generate background
    screen.blit(bg_surface, (0, -150))

    # Bird's movement
    bird_movement = bird_movement + gravity
    bird_rect.centery = bird_rect.centery + bird_movement
    screen.blit(bird_surface, bird_rect)

    # Generating moving floor
    create_floor()
    floor_x -= 1
    if floor_x == -576:
        floor_x = 0

    # Generating moving pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Update display
    pygame.display.update()
    clock.tick(120)
