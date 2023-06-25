from Sprites import BaseSprite

class inventory(BaseSprite):
    def __init__(self):
        image_path = "img/inventory.png"
        super().__init__(image_path)
        self.items = []
        self.imagee = None
        self.staff = None
        self.sword = None
        self.helm = None
        self.hpotion = None
        self.mpotion = None
        self.hide = True
        self.pressed = 0

        self.load_image(image_path)

    def toggle_visibility(self):
        self.pressed += 1
        if self.pressed == 1:
            self.hide = not self.hide
            self.pressed = 0
    
    def renderr(self, surface, handler):    
        gold = self.smallerfont.render('Gold: ' + str(handler.money), True, (0, 255, 0))
        if "3" in self.items:
            self.staff = self.pygame.image.load("img/staff.png").convert_alpha()
        if "4" in self.items:
            self.sword = self.pygame.image.load("img/swordicon.png").convert_alpha()
        if "5" in self.items:
            self.helm = self.pygame.image.load("img/helm.png").convert_alpha()
        if "6" in self.items:
            self.hpotion = self.pygame.image.load("img/hpotion.png").convert_alpha()
        if "7" in self.items:
            self.mpotion = self.pygame.image.load("img/mpotion.png").convert_alpha()
        if not self.hide:
            
            surface.blit(self.imagee, (10,30)) #TODO scale and place images from helm down
            if "3" in self.items:
                self.staff = self.pygame.transform.scale(self.staff, (30,30))
                surface.blit(self.staff, (20,63))
            if "4" in self.items:
                self.sword = self.pygame.transform.scale(self.sword, (40,40))
                surface.blit(self.sword, (50,53))
            if "5" in self.items:
                self.helm = self.pygame.transform.scale(self.helm, (30,30))
                surface.blit(self.helm, (93,60))
            if "6" in self.items:
                self.hpotion = self.pygame.transform.scale(self.hpotion, (30,30))
                surface.blit(self.hpotion, (20,63))
            if "7" in self.items:
                self.mpotion = self.pygame.transform.scale(self.mpotion, (30,30))
                surface.blit(self.mpotion, (20,63))
            #print('render called')

    def load_image(self, image_path):
        try:
            self.imagee = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))