from Sprites import BaseSprite

class inventory(BaseSprite):
    def __init__(self):
        image_path = "img/inventory.png"
        super().__init__(image_path)
        self.items = {3: 1, 3.4: 1, 5: 1, 5.1: 1, 4: 1, 6: 1, 7: 1}
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
            images = {
            3: ("img/staff_out.png", (30, 30), (35, 78)),
            3.1: ("img/staff_out.png", (30, 30), (200, 62)),
            3.3: ("img/staff_out.png", (30, 30), (21, 100)),
            3.4: ("img/staff_out.png", (30, 30), (71, 112)),
            4: ("img/sword_out.png", (40, 40), (71, 73)),
            4.1: ("img/sword_out.png", (40, 40), (71, 73)),
            4.2: ("img/sword_out.png", (40, 40), (50, 53)),
            4.3: ("img/sword_out.png", (40, 40), (50, 53)),
            4.4: ("img/sword_out.png", (40, 40), (50, 53)),
            5: ("img/helm_out.png", (40, 40), (107, 76)),
            5.1: ("img/helm_out.png", (40, 40), (103, 112)),
            6: ("img/hpotion_out.png", (30, 30), (142, 77)),
            7: ("img/mpotion_out.png", (30, 30), (180, 77))
        }

        for item in self.items.copy():
            if item in images:
                image_path, image_size, image_position = images[item]
                image = self.pygame.image.load(image_path).convert_alpha()
                image = self.pygame.transform.scale(image, image_size)
                image_rect = image.get_rect(center=image_position)

                if image_rect.collidepoint(mouse) and clicked[2]:
                    if item not in player.gear:
                        player.addstats = True
                        if item >= 3 and item <= 3.4:
                            self.staff = self.pygame.image.load("img/staff_out.png").convert_alpha()
                            self.staff = self.pygame.transform.scale(self.staff, (30, 30))
                        if item >= 4 and item <= 4.4:
                            self.sword = self.pygame.image.load("img/sword_out.png").convert_alpha()
                            self.sword = self.pygame.transform.scale(self.sword, (40, 40))
                        if item >= 5 and item <= 5.4:
                            self.helm = self.pygame.image.load("img/helm_out.png").convert_alpha()
                            self.helm = self.pygame.transform.scale(self.helm, (30, 30))
                        player.gear.append(item)
                        self.remove_items(item)
                        player.equip_weapon(self, surface)

                surface.blit(image, image_rect)

                if item == 6 and image_rect.collidepoint(mouse) and clicked[2]:
                    if player.health == 4:
                        player.health += 1
                        self.remove_items(item)
                    elif player.health == 3:
                        player.health += 2
                        self.remove_items(item)
                    elif player.health == 2:
                        player.health += 3
                        self.remove_items(item)
                    elif player.health == 1:
                        player.health += 4
                        self.remove_items(item)
                        print("added health")
                    else:
                        print("too much health")

                if item == 7 and image_rect.collidepoint(mouse) and clicked[2]:
                    if player.mana <= 12:
                        player.mana += 10
                        self.remove_items(item)
                        print("added mana")

    def load_image(self, image_path):
        try:
            self.imagee = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))