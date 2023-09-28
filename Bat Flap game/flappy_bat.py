import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_fly_1 = pygame.image.load('graphics/player/bat_1.png').convert_alpha()
        player_fly_2 = pygame.image.load('graphics/player/bat_2.png').convert_alpha()
        
        player_fly_1 = pygame.transform.rotozoom(player_fly_1, 0 , 1)
        player_fly_2 = pygame.transform.rotozoom(player_fly_2, 0 , 1)
        
        self.player_fly = [player_fly_1, player_fly_2]
        
        self.image = self.player_fly[0]
        self.rect = self.image.get_rect(midbottom = (200, 400))
        self.hitbox = (self.rect.x - 15, self.rect.y - 10, 96, 55)
        self.gravity = 0
        
        self.flap_sound = pygame.mixer.Sound('audio/wing_flap.mp3')
        self.flap_sound.set_volume(0.5)
        
    def input(self):
        self.flap_sound.play()
        self.gravity = -19
        self.image = self.player_fly[1]
            
    def apply_gravity(self):
        self.gravity += .9
        self.rect.y += self.gravity
        
    def reset(self):
        self.rect.y = 100
        self.gravity = -5
        
    def collision(self, objects):
        if objects:
            for obj in objects:
                if pygame.Rect.colliderect(self.hitbox, obj.hitbox):
                    objects.empty()
                    global game_active 
                    game_active = False
            
    def update(self, space_pressed, reset, objects):
        if reset == True: 
            self.reset()
        else:
            self.apply_gravity()
            
            if space_pressed == True: 
                self.input()   
                
            if self.gravity > -7: 
                self.image = self.player_fly[0]
                 
            if self.rect.bottom >= 650 or self.rect.top <= -165:
                global game_active 
                game_active = False
                
            self.hitbox = (self.rect.x + 15, self.rect.y + 10, 85, 45)
            self.hitbox = pygame.Rect(self.hitbox)
            
            self.collision(objects)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type,height,gap):
        super().__init__()
        
        if type == 'top':
            spike = pygame.image.load('graphics/ceiling spikes/ceil_2.png').convert_alpha()
            y_pos = height - gap
        else:
            spike = pygame.image.load('graphics/floor spikes/floor_2.png').convert_alpha()
            y_pos = height + gap
   
        self.image = spike
        self.rect = self.image.get_rect(midbottom = (1100 ,y_pos))
        self.hitbox = (self.rect.x - 60, self.rect.y, self.rect.width - 150, self.rect.height)
        
    def update(self):
        self.rect.x -= 6
        self.hitbox = (self.rect.x + 85, self.rect.y, self.rect.width - 175, self.rect.height)
        self.hitbox = pygame.Rect(self.hitbox)
        self.destroy()
            
    def destroy(self):
        if self.rect.x < -150:
            self.kill()

def screen_update():
    global screen_x
    if screen_x  <= -900:
        screen_x = 0
    screen.blit(bg_surf, (screen_x, 0))
    screen_x -= 1

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = score_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (500, 50))
    screen.blit(score_surf, score_rect)
    return current_time

pygame.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("My Game")
game_active = False
start_time = 0
bg_surf = pygame.image.load('graphics/cave_bg.png').convert()
screen_x = 0
bg_music = pygame.mixer.Sound('audio/game_music.mp3')
bg_music.play(loops = -1)

#Object Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
clock = pygame.time.Clock() 

#Start Screen
title_bat = pygame.image.load('graphics/intro screen/title_bat_48-1.png.png').convert()
transColor = title_bat.get_at((0,0))
title_bat_rect = title_bat.get_rect(center = (500, 300))

title_font = pygame.font.Font('font/font_1.ttf', 50)
title_surf = title_font.render("Flappy Bat", 0, (0, 0, 0))
title_rect = title_surf.get_rect(center = (500, 100))

score_font = pygame.font.Font('font/font_1.ttf', 40)
instruct_surf = score_font.render('Press Space to Start', 0, (0, 0, 0))
instruct_rect = instruct_surf.get_rect(center = (500, 550))
score = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.update(True, False, obstacle_group)
            if event.type == obstacle_timer:
                gap = randint(700, 1000) // 2
                height = randint(400, 600)
                obstacle_group.add(Obstacle('top', height, gap))
                obstacle_group.add(Obstacle('bot', height, gap))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen_x = 0
                x = player.update(False, True, obstacle_group)
                game_active = True
                start_time = pygame.time.get_ticks()
                
    if game_active:
        screen_update()
        score = display_score()
        
        player.draw(screen)
        player.update(False, False, obstacle_group)
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
    else:
         obstacle_group.empty()
         screen.fill((189, 189, 189))
         screen.blit(title_surf, title_rect)
        
         title_bat.set_colorkey(transColor) 
         screen.blit(title_bat, title_bat_rect)
        
         if score == 0:
            screen.blit(instruct_surf, instruct_rect)
         else:
            score_message = score_font.render(f'Your Score: {score}', False,  (0, 0, 0))
            score_message_rect = score_message.get_rect(center = (500, 550)) 
            screen.blit(score_message, score_message_rect)
            
    pygame.display.update()
    clock.tick(60)