import pygame, sys

pygame.init()
screen = pygame.display.set_mode((576, 800))
clock = pygame.time.Clock()

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x = 0

def moving_floor():
    screen.blit(floor_surface,(floor_x, 675))
    screen.blit(floor_surface,(floor_x + 576, 675))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface, (0, -150))
    moving_floor()
    floor_x = floor_x - 1
    if floor_x == -576:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)
