import sys
import pygame
from random import randrange

# Starting
pygame.init()
screen = pygame.display.set_mode((576, 800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('FlappyBirdFont.ttf', 50)

# Importing Images
bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())

# Bird's Animation
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Objects' Locations and Variables
floor_x = 0

# Game Variables
gravity = 0.25
bird_movement = 0
game_start = True
score = 0
highest_score = 0

# Spawn Pipes
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)


def create_floor():
    screen.blit(floor_surface, (floor_x, 675))
    screen.blit(floor_surface, (floor_x + 576, 675))


def create_pipe():
    random_pipe_ypos = randrange(335, 600)
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


def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 750:
        return False
    else:
        return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_status):
    if game_status == "mid_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 75))
        screen.blit(score_surface, score_rect)
    if game_status == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 135))
        screen.blit(score_surface, score_rect)

        highest_score_surface = game_font.render(f'Best: {int(highest_score)}', True, (255, 255, 255))
        highest_score_rect = highest_score_surface.get_rect(center=(288, 75))
        screen.blit(highest_score_surface, highest_score_rect)


def highest_score_update(score, highest_score):
    if score > highest_score:
        highest_score = score
    return highest_score


while True:
    for event in pygame.event.get():

        # Esc button triggered event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Space button triggered event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_start == True:
                bird_movement = 0
                bird_movement -= 10
            if event.key == pygame.K_SPACE and game_start == False:
                pipe_list.clear()
                bird_rect.center = (100, 400)
                bird_movement = 0
                game_start = True
                bird_movement -= 10
                score = 0

        # Spawn pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        # Bird's Animation
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

        bird_surface, bird_rect = bird_animation()

    # Generate background
    screen.blit(bg_surface, (0, -150))

    # Generating moving floor
    create_floor()
    floor_x -= 1
    if floor_x == -576:
        floor_x = 0

    if game_start:
        # Bird's movement
        bird_movement = bird_movement + gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery = bird_rect.centery + bird_movement
        screen.blit(rotated_bird, bird_rect)
        check_collisions(pipe_list)

        # Generating moving pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Check game status
        game_start = check_collisions(pipe_list)

        # Display Score
        score += 0.01
        score_display("mid_game")
    else:
        highest_score = highest_score_update(score, highest_score)
        score_display("game_over")

    # Update display
    pygame.display.update()
    clock.tick(120)
