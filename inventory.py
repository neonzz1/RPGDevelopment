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
    
    def renderr(self, surface, handler, player):    
        gold = self.smallerfont.render('Gold: ' + str(handler.money), True, (0, 255, 0))
        clicked = self.pygame.mouse.get_pressed()
        mouse = self.pygame.mouse.get_pos()
        #print(mousex, mousey)
        #TODO fix image location
        for item in self.items:

            if item == "3":
                self.staff = self.pygame.image.load("img/staff_out.png").convert_alpha()
            
            if item == "4":
                self.sword = self.pygame.image.load("img/sword_out.png").convert_alpha()
                
            if item == "5":
                self.helm = self.pygame.image.load("img/helm_out.png").convert_alpha()
                
            if item == "6":
                self.hpotion = self.pygame.image.load("img/hpotion_out.png").convert_alpha()
                
            if item == "7":
                self.mpotion = self.pygame.image.load("img/mpotion_out.png").convert_alpha()
            
        if not self.hide:
            
            surface.blit(self.imagee, (10,30)) #TODO scale and place images from helm down make image placement function more dynamically
            if "3" in self.items:
                self.staff = self.pygame.transform.scale(self.staff, (30,30))
                staff_rect = self.staff.get_rect(center = (35,81))
                if staff_rect.collidepoint(mouse):
                    if clicked[2]:
                        print(player.gear)
                        player.gear.append("3")
                        self.items.remove("3")
                surface.blit(self.staff, staff_rect)
            if "4" in self.items:
                self.sword = self.pygame.transform.scale(self.sword, (40,40))
                sword_rect = self.sword.get_rect(center = (70,72.5))#TODO fine adjust
                if sword_rect.collidepoint(mouse):
                    if clicked[2]:
                        player.gear.append("4")
                        print(player.gear)
                        self.items.remove("4")
                surface.blit(self.sword, sword_rect)
            if "5" in self.items:
                self.helm = self.pygame.transform.scale(self.helm, (40,40))
                helm_rect = self.helm.get_rect(center = (105,81))
                if helm_rect.collidepoint(mouse):
                    if clicked[2]:
                        player.gear.append("5")
                        print(player.gear)
                        self.items.remove("5")
                surface.blit(self.helm, (88,60))
            if "6" in self.items:
                self.hpotion = self.pygame.transform.scale(self.hpotion, (30,30))
                hpotion_rect = self.hpotion.get_rect(center = (140,81))
                if hpotion_rect.collidepoint(mouse):
                    if clicked[2]:
                        if player.health <= 4:
                            player.health += 5
                            self.items.remove("6")
                            print("added health")
                        print("too much health")
                surface.blit(self.hpotion, (128,62))
            if "7" in self.items:
                self.mpotion = self.pygame.transform.scale(self.mpotion, (30,30))
                mpotion_rect = self.mpotion.get_rect(center = (175,81))
                if mpotion_rect.collidepoint(mouse):
                    if clicked[2]:
                        if player.mana <= 12:
                            player.mana += 10
                            self.items.remove("7")
                            print("added mana")
                surface.blit(self.mpotion, (165,63))
            #print('render called')

    def load_image(self, image_path):
        try:
            self.imagee = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))