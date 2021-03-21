import pygame
import sys
import random
import os
font = 'data/sprites/BebasNeue-Bold.ttf'

# PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Floor
def drawFloor():
    screen.blit(floor, (floorX,450))
    screen.blit(floor, (floorX + 288, 450))

# Pipes
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos-150))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

# Collision
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
        
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        death_sound.play()
        return False
    
    return True

# Rotate Bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2.5, 1)
    return new_bird

# Bird Animation
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect

# Score
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255)) 
        score_rect = score_surface.get_rect(center = (144,60))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255)) 
        score_rect = score_surface.get_rect(center = (144,60))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255)) 
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 64)
pygame.init()


game_font = pygame.font.Font(font,40)

screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
pygame.display.set_caption('Slappy Birb')

# Game Veriables
gravity = 0.35
bird_movement = 0
game_active = True
score = 0
high_score = 0
score_sound_countdown = 100

game_over_surface = pygame.image.load('data/sprites/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,240))


bird_downflap = pygame.image.load('data/sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('data/sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('data/sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))

bg = pygame.image.load('data/sprites/background-day.png').convert()

floor = pygame.image.load('data/sprites/base.png').convert()

pipe_surface = pygame.image.load('data/sprites/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1000)
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,100)
pipe_height = [200,225,250,275,300,325,350,375,400]


fps = 60
floorX = 0

flap_sound = pygame.mixer.Sound('data/audio/wing.wav')
hit_sound = pygame.mixer.Sound('data/audio/hit.wav')
death_sound = pygame.mixer.Sound('data/audio/die.wav')
score_sound = pygame.mixer.Sound('data/audio/point.wav')

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6                          
                score += 1
                flap_sound.play()  
                score_sound_countdown -= 10          
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0   
                score_sound_countdown = 100

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())   

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg, (0,0))
    
    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)




        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        
        score_display('main_game')
        if score_sound_countdown <=0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    
    # Floor
    floorX -= 3
    drawFloor()
    if floorX <= -288:
        floorX = 0

    # Collisions

    
    
    
    pygame.display.update()
    clock.tick(fps)

    

