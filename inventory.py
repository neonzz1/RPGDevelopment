from Sprites import BaseSprite

class inventory(BaseSprite):
    def __init__(self):
        image_path = "img/inventory.png"
        super().__init__(image_path)
        self.items = ["3","4","5","6","7"]
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
    
    def renderr(self, surface, handler, player):    
        gold = self.smallerfont.render('Gold: ' + str(handler.money), True, (0, 255, 0))
        clicked = self.pygame.mouse.get_pressed()
        #TODO fix image location
        if "3" in self.items:
            self.staff = self.pygame.image.load("img/staff.png").convert_alpha()
            staff_rect = self.staff.get_rect(center = (20,63))
            if staff_rect.collidepoint:
                if clicked[2]:
                    print("staff")#TODO add logic for equiping gear
        if "4" in self.items:
            self.sword = self.pygame.image.load("img/swordicon.png").convert_alpha()
            sword_rect = self.sword.get_rect(center = (50,53))
            if sword_rect.collidepoint:
                if clicked[2]:
                    print("sword")#TODO add logic for equiping gear
        if "5" in self.items:
            self.helm = self.pygame.image.load("img/helm.png").convert_alpha()
            helm_rect = self.helm.get_rect(center = (88,60))
            if helm_rect.collidepoint:
                if clicked[2]:
                    print("helm")#TODO add logic for equiping gear
        if "6" in self.items:
            self.hpotion = self.pygame.image.load("img/hpotion.png").convert_alpha()
            hpotion_rect = self.hpotion.get_rect(center = (128,62))
            if hpotion_rect.collidepoint:
                if clicked[2]:
                    player.health += 5
                    print("added health")
        if "7" in self.items:
            self.mpotion = self.pygame.image.load("img/mpotion.png").convert_alpha()
            mpotion_rect = self.mpotion.get_rect(center = (165,63))
            if mpotion_rect.collidepoint:
                if clicked[2]:
                   player.mana += 10
                   print("added mana")
        if not self.hide:
            
            surface.blit(self.imagee, (10,30)) #TODO scale and place images from helm down make image placement function more dynamically
            if "3" in self.items:
                self.staff = self.pygame.transform.scale(self.staff, (30,30))
                surface.blit(self.staff, staff_rect)
            if "4" in self.items:
                self.sword = self.pygame.transform.scale(self.sword, (40,40))
                surface.blit(self.sword, sword_rect)
            if "5" in self.items:
                self.helm = self.pygame.transform.scale(self.helm, (40,40))
                surface.blit(self.helm, helm_rect)
            if "6" in self.items:
                self.hpotion = self.pygame.transform.scale(self.hpotion, (30,30))
                surface.blit(self.hpotion, hpotion_rect)
            if "7" in self.items:
                self.mpotion = self.pygame.transform.scale(self.mpotion, (30,30))
                surface.blit(self.mpotion, mpotion_rect)
            #print('render called')

    def load_image(self, image_path):
        try:
            self.imagee = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))