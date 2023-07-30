from Sprites import BaseSprite

class inventory(BaseSprite):
    def __init__(self):
        image_path = "img/inventory.png"
        super().__init__(image_path)
        self.items = {3: 1, 3.1: 1, 3.3: 1, 3.4: 1, 4: 1, 4.1: 1, 4.3: 1, 4.4: 1, 5: 1, 5.1: 1, 5.3: 1, 5.4: 1, 6: 2, 6.1: 1, 7: 1}
        self.imagee = None
        self.staff = None
        self.sword = None
        self.helm = None
        self.hpotion = None
        self.mpotion = None
        self.hide = True
        self.do_once = True
        self.pressed = 0

        self.load_image(image_path)

    def toggle_visibility(self):
        self.pressed += 1
        if self.pressed == 1:
            self.hide = not self.hide
            self.pressed = 0
        if not self.do_once:
            self.do_once = True #TODO find somewhere to put this that will work better

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
        #print(mouse)
        if not self.hide:
            
            surface.blit(self.imagee, (10,30)) #TODO make image placement function more dynamically
            #print(mouse)
            images = {
            3: ("img/staff_out.png", (30, 30), (35, 78)),
            3.1: ("img/staff_out.png", (30, 30), (213, 78)),
            3.3: ("img/staff_out.png", (30, 30), (33, 112)),
            3.4: ("img/staff_out.png", (30, 30), (71, 112)),
            4: ("img/sword_out.png", (40, 40), (71, 73)),
            4.1: ("img/sword_out.png", (40, 40), (145, 112)),
            4.3: ("img/sword_out.png", (40, 40), (214, 112)),
            4.4: ("img/sword_out.png", (40, 40), (36, 150)),
            5: ("img/helm_out.png", (40, 40), (107, 76)),
            5.1: ("img/helm_out.png", (40, 40), (107, 112)),
            5.3: ("img/helm_out.png", (40, 40), (180, 112)),
            5.4: ("img/helm_out.png", (40, 40), (180, 150)),
            6: ("img/hpotion_out.png", (30, 30), (142, 77)),
            6.1:("img/hpotion_out.png", (30, 30), (220, 150)),
            7: ("img/mpotion_out.png", (30, 30), (180, 77))
        }

        for item, quantity in self.items.copy().items():
            if item in images:
                image_path, image_size, image_position = images[item]
                image = self.pygame.image.load(image_path).convert_alpha()
                image = self.pygame.transform.scale(image, image_size)
                image_rect = image.get_rect(center=image_position)

                if quantity <= 0:
                    self.remove_items(item)

                if image_rect.collidepoint(mouse) and clicked[2]:
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
                    if item < 6 and item not in player.equipped_gear:
                            player.gear.append(item)
                            player.equip_weapon(self, surface)
                    if self.do_once: #Used to fix too menay items being removed from one use
                        if quantity >= 1 and item != 6:
                            self.items[item] -= 1
                            self.do_once = False
                    if item in player.equipped_gear:
                        player.unequipped_gear.append(item)
                    

                surface.blit(image, image_rect)
                if quantity >= 1: #TODO edit font for all items and location for numbers greater than 3 
                    posx = image_position[0]
                    posy = image_position[1]
                    posx += 10

                    if item >= 6:
                        posx -= 15
                        posy -= 5

                    text = self.smallerfont.render('{}'.format(quantity), True, (255,255,255))
                    surface.blit(text, (posx,posy))

                if item == 6 and image_rect.collidepoint(mouse) and clicked[2]:
                    if quantity < 1:
                        print(quantity)
                    elif player.health == 4:
                        player.health += 1
                        if quantity >= 1:
                            self.items[item] -= 1
                    elif player.health == 3:
                        player.health += 2
                        if quantity >= 1:
                            self.items[item] -= 1
                    elif player.health == 2:
                        player.health += 3
                        if quantity >= 1:
                            self.items[item] -= 1
                    elif player.health == 1:
                        player.health += 4
                        if quantity >= 1:
                            self.items[item] -= 1
                        print("added health")
                    else:
                        print("too much health")

                if item == 6.1 and image_rect.collidepoint(mouse) and clicked[2]:
                    if player.health > 0:
                        print("You cannot res your health is too high!")
                    elif player.health <= 0:
                        player.__init__()

                if item == 7 and image_rect.collidepoint(mouse) and clicked[2]:
                    if quantity < 1:
                        print(quantity)
                    if player.mana >= 0 and player.mana <= 12:
                        player.mana += 10
                        if quantity >= 1:
                            self.items[item] -= 1
                        print("added mana")

    def load_image(self, image_path):
        try:
            self.imagee = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))