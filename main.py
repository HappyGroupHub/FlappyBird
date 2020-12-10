import pygame, sys

pygame.init()
screen = pygame.display.set_mode((576, 800))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/background-day.png')
bg_surface = pygame.transform.scale2x(bg_surface)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface,(0, 0))

    pygame.display.update()
    clock.tick(120)