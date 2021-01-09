import sys
from random import randrange

import pygame

# Starting - 起始載入

pygame.init()
# 啟動pygame
screen = pygame.display.set_mode((576, 800))
# 設定視窗大小
clock = pygame.time.Clock()
# 設置幀率
game_font = pygame.font.Font('FlappyBirdFont.ttf', 50)
# 導入文字形式


# Importing Images and Sounds - 匯入圖片及聲音檔案

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
get_ready_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
hit_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')
death_sound = pygame.mixer.Sound('sounds/sfx_die.wav')


# Bird's Animation - 鳥的動畫

bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


# Game Variables - 遊戲中數值

floor_x = 0
gravity = 0.25
bird_movement = 0
game_start = False
score = 0
can_score = True
highest_score = 0
death_count = 0


# Spawn Pipes - 生成水管

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)


# Game Over Screen - 遊戲結束畫面

game_over_rect = game_over_surface.get_rect(center=(288, 700))
get_ready_rect = get_ready_surface.get_rect(center=(288, 300))


# 函式定義區

# 建構地板
def create_floor():
    screen.blit(floor_surface, (floor_x, 675))
    # 先畫一個式窗內的地板
    screen.blit(floor_surface, (floor_x + 576, 675))
    # 再畫一個地板,跟在剛剛的第一塊後面


# 創造水管
def create_pipe():
    random_pipe_ypos = randrange(335, 600)
    # 設定一個隨機變數(335-600),用來設定管子的y座標
    bottom_pipe = pipe_surface.get_rect(midtop=(600, random_pipe_ypos))
    # 建構出貼地的水管,使用剛剛的變數
    top_pipe = pipe_surface.get_rect(midbottom=(600, random_pipe_ypos - 300))
    # 建構出上方的水管,使用剛剛的變數減300

    return bottom_pipe, top_pipe


# 移動水管
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


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
            hit_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 750:
        death_sound.play()
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


def score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 98 < pipe.centerx < 102 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


def score_display(game_status):
    if game_status == "mid_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_status == "game_over" and death_count > 0:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(150, 175))
        screen.blit(score_surface, score_rect)

        highest_score_surface = game_font.render(f'Best: {int(highest_score)}', True, (255, 255, 255))
        highest_score_rect = highest_score_surface.get_rect(center=(450, 175))
        screen.blit(highest_score_surface, highest_score_rect)


def highest_score_update(score, highest_score):
    if score > highest_score:
        highest_score = score
    return highest_score


while True:
    for event in pygame.event.get():

        # Esc button triggered event - 右上角(x)按鈕
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Space button triggered event - 空白鍵觸發事件
        if event.type == pygame.KEYDOWN:

            # Space event during game - 遊戲中觸發空白鍵
            if event.key == pygame.K_SPACE and game_start == True:
                bird_movement = 0
                bird_movement -= 10

            # Space event when gameover - 結束時觸發空白鍵
            if event.key == pygame.K_SPACE and game_start == False:
                pipe_list.clear()
                bird_rect.center = (100, 400)
                bird_movement = 0
                game_start = True
                bird_movement -= 10
                score = 0
                can_score = True
                death_count += 1

        # Spawn pipes - 生成水管
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        # Bird's Animation - 鳥的動畫
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

        bird_surface, bird_rect = bird_animation()

    # Generate background - 生成背景
    screen.blit(bg_surface, (0, -150))

    # Generating moving floor - 生成會移動的地板
    create_floor()
    floor_x -= 1
    if floor_x == -576:
        floor_x = 0

    if game_start:
        # Bird's movement - 鳥的移動參數
        bird_movement = bird_movement + gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery = bird_rect.centery + bird_movement
        screen.blit(rotated_bird, bird_rect)
        check_collisions(pipe_list)

        # Generating moving pipes - 生成移動的水管
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Check game status - 更新/確認遊戲狀態
        game_start = check_collisions(pipe_list)

        # Display Score - 顯示當前分數
        score_check()
        score_display("mid_game")
    else:
        # Gameover Screen Display - 結束畫面顯示
        if death_count > 0:
            screen.blit(game_over_surface, game_over_rect)
        screen.blit(get_ready_surface, get_ready_rect)
        highest_score = highest_score_update(score, highest_score)
        score_display("game_over")

    # Update display
    pygame.display.update()
    clock.tick(120)
