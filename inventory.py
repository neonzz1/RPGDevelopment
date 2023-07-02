from Sprites import BaseSprite

class inventory(BaseSprite):
    def __init__(self):
        image_path = "img/inventory.png"
        super().__init__(image_path)
        self.items = {3: 2, 3.4: 1}
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

    def remove_items(self, item):
        items_to_remove = []
        if item in self.items:
            self.items[item] -= 1
            if self.items[item] <= 0:
                items_to_remove.append(item)

        for item_to_remove in items_to_remove:
            del self.items[item_to_remove]
    
    def renderr(self, surface, handler, player):    
        gold = self.smallerfont.render('Gold: ' + str(handler.money), True, (0, 255, 0))
        clicked = self.pygame.mouse.get_pressed()
        mouse = self.pygame.mouse.get_pos()
        #TODO fix image location
            #print("Rendering item:", item)
            
        if not self.hide:
            
            surface.blit(self.imagee, (10,30)) #TODO make image placement function more dynamically
            #print(mouse)
            for item, quantity in self.items.copy().items():  # Iterate over a copy of the dictionary# current code not functional as dict changes during render
                if item == 3:
                    self.staff = self.pygame.image.load("img/staff_out.png").convert_alpha()
                    self.staff = self.pygame.transform.scale(self.staff, (30,30))
                    staff_rect = self.staff.get_rect(center = (35,78))
                    if staff_rect.collidepoint(mouse):
                        if clicked[2]:
                            print(player.gear)
                            if item not in player.gear:
                                player.addstats = True
                                player.gear.append(3)
                                self.remove_items(item)
                    if quantity > 1:
                        text = self.smallerfont.render(f"{quantity}", True, (0,0,255))
                        surface.blit(text, (30, 60))
                        surface.blit(self.staff, staff_rect)
                if item == 3.1:
                    self.staff1 = self.pygame.image.load("img/staff_out.png").convert_alpha()
                    self.staff1 = self.pygame.transform.scale(self.staff1, (30,30))
                    staff_rect1 = self.staff1.get_rect()
                    if staff_rect1.collidepoint(mouse):
                        if clicked[2]:
                            print(player.gear)
                            if item not in player.gear:
                                player.gear.append(3.1)
                                self.remove_items(item)
                    surface.blit(self.staff1, (200, 62))#TODO fine adjust
                if item == 3.3:
                    self.staff2 = self.pygame.image.load("img/staff_out.png").convert_alpha()
                    self.staff2 = self.pygame.transform.scale(self.staff2, (30,30))
                    staff_rect2 = self.staff2.get_rect()
                    if staff_rect2.collidepoint(mouse):
                        if clicked[2]:
                            print(player.gear)
                            if item not in player.gear:
                                player.gear.append(3.3)
                                self.remove_items(item)
                    surface.blit(self.staff2, (21, 100))
                if item == 3.4:
                    self.staff3 = self.pygame.image.load("img/staff_out.png").convert_alpha()
                    self.staff3 = self.pygame.transform.scale(self.staff3, (30,30))
                    staff_rect3 = self.staff3.get_rect(center = (70,117))
                    if staff_rect3.collidepoint(mouse):
                        if clicked[2]:
                            print(player.gear)
                            if item not in player.gear:
                                player.gear.append(3.4)
                                self.remove_items(item)
                    surface.blit(self.staff3, (55, 100))
                if item >= 4 and item <= 4.4:
                    self.sword = self.pygame.image.load("img/sword_out.png").convert_alpha()
                    self.sword = self.pygame.transform.scale(self.sword, (40,40))
                    sword_rect = self.sword.get_rect(center = (70,72.5))
                    if sword_rect.collidepoint(mouse):
                        if clicked[2]:
                            if item not in player.gear:
                                player.gear.append(4)
                                print(player.gear)
                                self.remove_items(item)
                    surface.blit(self.sword, (50,53))
                if item >= 5 and item <= 5.4:
                    self.helm = self.pygame.image.load("img/helm_out.png").convert_alpha()
                    self.helm = self.pygame.transform.scale(self.helm, (40,40))
                    helm_rect = self.helm.get_rect(center = (105,81))
                    if helm_rect.collidepoint(mouse):
                        if clicked[2]:
                            if item not in player.gear:
                                player.gear.append(5)
                                print(player.gear)
                                self.remove_items(item)
                    surface.blit(self.helm, (88,60))
                if item == 6:
                    self.hpotion = self.pygame.image.load("img/hpotion_out.png").convert_alpha()
                    self.hpotion = self.pygame.transform.scale(self.hpotion, (30,30))
                    hpotion_rect = self.hpotion.get_rect(center = (140,81))
                    if hpotion_rect.collidepoint(mouse):
                        if clicked[2]:
                            if player.health <= 4:
                                player.health += 5
                                self.remove_items(item)
                                print("added health")
                            print("too much health")
                    surface.blit(self.hpotion, (128,62))
                if item == 7:
                    self.mpotion = self.pygame.image.load("img/mpotion_out.png").convert_alpha()
                    self.mpotion = self.pygame.transform.scale(self.mpotion, (30,30))
                    mpotion_rect = self.mpotion.get_rect(center = (175,81))
                    if mpotion_rect.collidepoint(mouse):
                        if clicked[2]:
                            if player.mana <= 12:
                                player.mana += 10
                                self.remove_items(item)
                                print("added mana")
                    surface.blit(self.mpotion, (165,63))
                #print('render called')

    def load_image(self, image_path):
        try:
            self.imagee = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))