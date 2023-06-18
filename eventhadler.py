import pygame
from tkinter import filedialog
from tkinter import *

stage_delay = 5000

class EventHandler():
    def __init__(self, castle, button, background, ground, mmanger, soundtrack):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2
        self.enemy_generation2 = pygame.USEREVENT + 3
        self.stage_timer = pygame.USEREVENT + 5
        self.castle = castle
        self.stage_enemies = []
        self.stage = 1
        self.enemy_count = 0
        self.enemy_dead_count = 0
        self.button = button
        self.world = 0
        self.background = background
        self.ground = ground
        self.mmanager = mmanger
        self.soundtrack = soundtrack
        self.money = 0

        for x in range(1, 21):
            self.stage_enemies.append(int((x ** 2 / 2) + 1))
             
    def stage_handler(self):
            # Code for the Tkinter stage selection window
        self.root = Tk()
        self.root.geometry('200x170')
             
        button1 = Button(self.root, text = "Skyward Dungeon", width = 18, height = 2,
                            command = self.world1)
        button2 = Button(self.root, text = "Geurdo Dungeon", width = 18, height = 2,
                            command = self.world2)
        button3 = Button(self.root, text = "Hell Dungeon", width = 18, height = 2,
                            command = self.world3)
              
        button1.place(x = 40, y = 15)
        button2.place(x = 40, y = 65)
        button3.place(x = 40, y = 115)
             
        self.root.mainloop()

    def world1(self):   
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        self.world = 1
        self.button.imgdisp = 1
        self.castle.hide = True
        self.battle = True
        self.mmanager.playsoundtrack(self.soundtrack[1], -1, 0.05)
 
    def world2(self):
        self.root.destroy()
        self.background.image = pygame.image.load("img/desert.jpg").convert_alpha()
        self.ground.image = pygame.image.load("img/desert_ground.png").convert_alpha()
        self.mmanager.playsoundtrack(self.soundtrack[1], -1, 0.05)
 
        pygame.time.set_timer(self.enemy_generation2, 2500)
 
        self.world = 2
        self.button.imgdisp = 1
        self.castle.hide = True
        self.battle = True
      
    def world3(self):
        self.battle = True
        self.button.imgdisp = 1
        # Empty for now
        self.mmanager.playsoundtrack(self.soundtrack[1], -1, 0.05)
    def next_stage(self):  # Code for when the next stage is clicked            
        self.stage += 1
        self.button.imgdisp = 0
        
        print("Stage: "  + str(self.stage))

        self.enemy_count = 0
        self.dead_enemy_count = 0
        if self.world == 1:
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))
        elif self.world == 2:
            pygame.time.set_timer(self.enemy_generation2, 1500 - (50 * self.stage))

    def update(self, stage_display):
        if self.enemy_dead_count == self.stage_enemies[self.stage - 1]:
            self.enemy_dead_count = 0
            stage_display.clear = True
            stage_display.stage_clear()
            pygame.time.set_timer(self.stage_timer, stage_delay)
            print(self.enemy_count)
    
    def home(self, Enemies, Items, castle, background, ground):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0)
        pygame.time.set_timer(self.enemy_generation2, 0)
        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 0
        self.world = 0
    
        # Destroy any enemies or items lying around
        for group in Enemies, Items:
            for entity in group:
                entity.kill()
        
        # Bring back normal backgrounds
        castle.hide = False
        background.bgimage = pygame.image.load("img/Background.png").convert_alpha()
        ground.image = pygame.image.load("img/Ground.png").convert_alpha()