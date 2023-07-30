import pygame
from pygame.sprite import AbstractGroup

color_light = (170,170,170)
WIDTH = 700

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, image_path) -> None:
        super().__init__()
        #Variables every sprite needs access too
        self.image = pygame.image.load(image_path).convert_alpha()
        self.vec = pygame.math.Vector2
        self.hide = False
        self.pygame = pygame
        self.width = WIDTH
        # defining a font
        self.headingfont = pygame.font.SysFont("Verdana", 40)
        self.regularfont = pygame.font.SysFont('Corbel',25)
        self.smallerfont = pygame.font.SysFont('Corbel',20) 
        self.text = self.regularfont.render('LOAD' , True , color_light)
        self.moveani_L = [pygame.image.load("img/demon_L.png").convert_alpha(), pygame.image.load("img/demon_L_2.png").convert_alpha(),
                          pygame.image.load("img/demon_L_3.png").convert_alpha(), pygame.image.load("img/demon_L_4.png").convert_alpha(),
                          pygame.image.load("img/demon_L_5.png").convert_alpha(), pygame.image.load("img/demon_L_6.png").convert_alpha(),
                          pygame.image.load("img/demon_L_7.png").convert_alpha(), pygame.image.load("img/demon_L_8.png").convert_alpha(),
                          pygame.image.load("img/demon_L_9.png").convert_alpha(), pygame.image.load("img/demon_L.png").convert_alpha()]
        
        self.moveani_R = [pygame.image.load("img/demon_R.png").convert_alpha(), pygame.image.load("img/demon_R_2.png").convert_alpha(),
                          pygame.image.load("img/demon_R_3.png").convert_alpha(), pygame.image.load("img/demon_R_4.png").convert_alpha(),
                          pygame.image.load("img/demon_R_5.png").convert_alpha(), pygame.image.load("img/demon_R_6.png").convert_alpha(),
                          pygame.image.load("img/demon_R_7.png").convert_alpha(), pygame.image.load("img/demon_R_8.png").convert_alpha(),
                          pygame.image.load("img/demon_R.png").convert_alpha()]
        #Player animations
        self.run_ani_R = [pygame.image.load("img/Player_Sprite_R.png").convert_alpha(), pygame.image.load("img/Player_Sprite2_R.png").convert_alpha(),
             pygame.image.load("img/Player_Sprite3_R.png").convert_alpha(),pygame.image.load("img/Player_Sprite4_R.png").convert_alpha(),
             pygame.image.load("img/Player_Sprite5_R.png").convert_alpha(),pygame.image.load("img/Player_Sprite6_R.png").convert_alpha(),
             pygame.image.load("img/Player_Sprite_R.png").convert_alpha()]
        self.run_ani_L = [pygame.image.load("img/Player_Sprite_L.png").convert_alpha(), pygame.image.load("img/Player_Sprite2_L.png").convert_alpha(),
             pygame.image.load("img/Player_Sprite3_L.png").convert_alpha(),pygame.image.load("img/Player_Sprite4_L.png").convert_alpha(),
             pygame.image.load("img/Player_Sprite5_L.png").convert_alpha(),pygame.image.load("img/Player_Sprite6_L.png").convert_alpha(),
             pygame.image.load("img/Player_Sprite_L.png").convert_alpha()]

        self.attack_ani_R = [pygame.image.load("img/Player_Sprite_R.png").convert_alpha(), pygame.image.load("img/Player_Attack_R.png").convert_alpha(),
                pygame.image.load("img/Player_Attack2_R.png").convert_alpha(),pygame.image.load("img/Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("img/Player_Attack3_R.png").convert_alpha(),pygame.image.load("img/Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("img/Player_Attack4_R.png").convert_alpha(),pygame.image.load("img/Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("img/Player_Attack5_R.png").convert_alpha(),pygame.image.load("img/Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("img/Player_Sprite_R.png").convert_alpha()]
        self.attack_ani_L = [pygame.image.load("img/Player_Sprite_L.png").convert_alpha(), pygame.image.load("img/Player_Attack_L.png").convert_alpha(),
                pygame.image.load("img/Player_Attack2_L.png").convert_alpha(),pygame.image.load("img/Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("img/Player_Attack3_L.png").convert_alpha(),pygame.image.load("img/Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("img/Player_Attack4_L.png").convert_alpha(),pygame.image.load("img/Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("img/Player_Attack5_L.png").convert_alpha(),pygame.image.load("img/Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("img/Player_Sprite_L.png").convert_alpha()]
        self.health_ani = [pygame.image.load("img/hearts_0.png").convert_alpha(), pygame.image.load("img/hearts_1.png").convert_alpha(),
              pygame.image.load("img/hearts_2.png").convert_alpha(), pygame.image.load("img/hearts_3.png").convert_alpha(),
              pygame.image.load("img/hearts_4.png").convert_alpha(), pygame.image.load("img/hearts_full.png").convert_alpha()]
        self.showplayer = True
        
#renders all images on the screen other than healthbar
    def render(self, surface, cursor):
        if cursor.wait == 1: return
        self.surface = surface
        if hasattr(self, 'rect'):
            if self.showplayer == True:
                surface.blit(self.image, self.rect)
        elif hasattr(self, 'bgX') and hasattr(self, 'bgY'):
            surface.blit(self.image, (self.bgX, self.bgY))
        #else:
            #surface.blit(self.image, (10,10))