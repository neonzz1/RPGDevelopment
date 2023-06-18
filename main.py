import pygame
import sys
from pygame.locals import *
from background import Background
from ground import Ground
from player import Player
from enemy import Enemy, Enemy2
from castle import Castle
from eventhadler import EventHandler
from Healthbar import HealthBar
from stagedisplay import StageDisplay
from statusbar import StatusBar
from cursor import Cursor
from buttons import PButton
from magic import Magic
from music import MusicManager
from Manabar import ManaBar
from inventory import inventory

def main():
    
# freq, size, channel, buffsize
    pygame.mixer.pre_init(44100, 16, 1, 512)

    pygame.init()  # Begin pygame
    
    # Declaring variables to be used through the program
    HEIGHT = 350
    WIDTH = 700
    ACC = 0.3
    FRIC = -0.10
    FPS = 60
    FPS_CLOCK = pygame.time.Clock()
    COUNT = 0

    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Game")

    #TODO make better images so reduction is consistant 
    #TODO make pause menus
    #TODO make 

    mana_ani = [pygame.image.load("img/mana_0.png").convert_alpha(), pygame.image.load("img/mana_1.png").convert_alpha(),
              pygame.image.load("img/mana_2.png").convert_alpha(), pygame.image.load("img/mana_3.png").convert_alpha(),
              pygame.image.load("img/mana_4.png").convert_alpha(), pygame.image.load("img/mana_5.png").convert_alpha(),
              pygame.image.load("img/mana_6.png").convert_alpha(), pygame.image.load("img/mana_7.png").convert_alpha(),
              pygame.image.load("img/mana_8.png").convert_alpha(), pygame.image.load("img/mana_9.png").convert_alpha(),
              pygame.image.load("img/mana_10.png").convert_alpha(), pygame.image.load("img/mana_11.png").convert_alpha(),
              pygame.image.load("img/mana_12.png").convert_alpha(), pygame.image.load("img/mana_13.png").convert_alpha(),
              pygame.image.load("img/mana_14.png").convert_alpha(), pygame.image.load("img/mana_15.png").convert_alpha(),
              pygame.image.load("img/mana_16.png").convert_alpha(), pygame.image.load("img/mana_17.png").convert_alpha(),
              pygame.image.load("img/mana_18.png").convert_alpha(), pygame.image.load("img/mana_19.png").convert_alpha(),
              pygame.image.load("img/mana_20.png").convert_alpha(), pygame.image.load("img/mana_21.png").convert_alpha(),
              pygame.image.load("img/mana_22.png").convert_alpha(), pygame.image.load("img/mana_full.png").convert_alpha()]

    soundtrack = ["sounds/background_village.wav", "sounds/battle_music.wav", "sounds/gameover.wav"]
    swordtrack = [pygame.mixer.Sound("sounds/sword1.wav"), pygame.mixer.Sound("sounds/sword2.wav")]
    fsound = pygame.mixer.Sound("sounds/fireball_sound.wav")
    hit = pygame.mixer.Sound("sounds/enemy_hit.wav")
 
    mmanager = MusicManager()
    mmanager.playsoundtrack(soundtrack[0], -1, 0.05)

    # Attack animation for the RIGHT
    

    background = Background()
    ground = Ground()
    ground_group = pygame.sprite.Group()
    ground_group.add(ground)
    hit_cooldown = pygame.USEREVENT + 1
    health = HealthBar()
    mana = ManaBar()
    player = Player(ground_group, hit_cooldown, health, mmanager, soundtrack, swordtrack)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    Enemies = pygame.sprite.Group()
    castle = Castle()
    button = PButton()
    handler = EventHandler(castle, button, background, ground, mmanager, soundtrack)
    stage_display = StageDisplay(handler, surface)
    status_bar = StatusBar()
    cursor = Cursor()
    Fireballs = pygame.sprite.Group()
    Items = pygame.sprite.Group()
    Bolts = pygame.sprite.Group()
    inv = inventory()
    
    while 1:
        pygame.event.pump()

        player.gravity_check()
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            # Will run when the close window button is clicked    
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.VIDEORESIZE:
                pygame.display._resize_event(event)
            if event.type == handler.enemy_generation:
                if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                    enemy = Enemy(hit_cooldown, player_group, player)
                    Enemies.add(enemy)
                    handler.enemy_count += 1
            if event.type == handler.enemy_generation2:
                if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                    enemy = Enemy2(player_group, Fireballs, player, handler, Items, Bolts)
                    Enemies.add(enemy)
                    handler.enemy_count += 1
            # For events that occur upon clicking the mouse (left click) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
                    if button.imgdisp == 1:
                        cursor.pause()
                    elif button.imgdisp == 0:
                        handler.home(Enemies, Items, castle, background, ground)
            # Event handling for a range of different key presses    
            if event.type == pygame.KEYDOWN and cursor.wait == 0:
                if event.key == pygame.K_e and 450 < player.rect.x < 550:
                    handler.stage_handler()
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_k:
                    if player.attacking == False:   
                        player.attack(cursor)
                        player.attacking = True
                if event.key == pygame.K_m and player.magic_cooldown == 1:
                    if player.mana >= 1:
                        player.mana -= 1
                        mana.image = mana_ani[player.mana]
                        player.attacking = True
                        fireball = Magic(player)
                        Fireballs.add(fireball)
                        mmanager.playsound(fsound, 0.3)
                if event.key == pygame.K_i:
                    inv.hide = False
                    inv.renderr(surface, handler)
            if event.type == handler.stage_timer:
                if handler.battle == True and len(Enemies) == 0:
                        handler.next_stage()
                        stage_display.display = True
                

            if event.type == hit_cooldown:
                player.cooldown = False
                pygame.time.set_timer(hit_cooldown, 0)
        #render background ang floor
        background.render(surface, cursor)
        ground.render(surface, cursor)
        #Player related functions
        if player.health > 0:
            player.render(surface, cursor)
        player.move()
        player.update(cursor)
        if player.attacking:
            player.attack(cursor)
        for level, xp_required in player.levels.items(): #TODO fix level system
            if player.experience >= xp_required and not player.leveled:
                player.level_up()
                xp_required = player.levels[player.level + 1]
                print("Level Up! You reached level {}!".format(player.level))
                break
        #render health images
        health.renders(surface)
        mana.renders(surface)
        #sprite functions
        if stage_display.display:
            stage_display.move_display()
        if stage_display.clear:
            stage_display.stage_clear()

        for ball in Fireballs:
            ball.fire(surface)
        for bolt in Bolts:
            bolt.fire(surface)
        for entity in Enemies:
            entity.render(surface, cursor)
            entity.move(cursor)
            entity.update(handler, Items, Fireballs)
            #print("sprire")
        for i in Items:
            i.render(surface)
            i.update(player_group, player, health, handler, inv)   	
        surface.blit(status_bar.surf, (580, 5))
        status_bar.update_draw(handler, player, FPS_CLOCK, surface)
        handler.update(stage_display)
        castle.update(surface)
        button.render(button.imgdisp, cursor, surface)
        cursor.hover(mouse, surface)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)
if __name__ == '__main__':
    main()