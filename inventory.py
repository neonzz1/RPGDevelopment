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
        gold = self.skillfont.render('Gold: ' + str(handler.money), True, (0, 255, 0))
        clicked = self.pygame.mouse.get_pressed()
        mouse = self.pygame.mouse.get_pos()
            #print("Rendering item:", item)
        #print(mouse)
        if not self.hide:
            
            surface.blit(self.imagee, (100,30)) #TODO make image placement function more dynamically
            #print(mouse)
            images = {
            3: ("img/staff_out.png", (30, 30), (125, 78)),
            3.1: ("img/staff_out.png", (30, 30), (303, 78)),
            3.3: ("img/staff_out.png", (30, 30), (123, 112)),
            3.4: ("img/staff_out.png", (30, 30), (161, 112)),
            4: ("img/sword_out.png", (40, 40), (161, 73)),
            4.1: ("img/sword_out.png", (40, 40), (235, 112)),
            4.3: ("img/sword_out.png", (40, 40), (304, 112)),
            4.4: ("img/sword_out.png", (40, 40), (126, 150)),
            5: ("img/helm_out.png", (40, 40), (197, 76)),
            5.1: ("img/helm_out.png", (40, 40), (197, 112)),
            5.3: ("img/helm_out.png", (40, 40), (270, 112)),
            5.4: ("img/helm_out.png", (40, 40), (270, 150)),
            6: ("img/hpotion_out.png", (30, 30), (242, 77)),
            6.1:("img/hpotion_out.png", (30, 30), (310, 150)),
            7: ("img/mpotion_out.png", (30, 30), (270, 77))
        }
            item_stats = {
            3: {'name': "staff", 'attack': "Attack: 5", 'defence': "Defence: 2", 'spellpower': "SpellPower: 5", 'level': '0'},
            3.1: {'name': "staff", 'attack': "Attack: 6", 'defence': "Defence: 4", 'spellpower': "SpellPower: 10", 'level': '1'},
            3.3: {'name': "staff", 'attack': "Attack: 9", 'defence': "Defence: 8", 'spellpower': "SpellPower: 12", 'level': '3'},
            3.4: {'name': "staff", 'attack': "Attack: 14", 'defence': "Defence: 16", 'spellpower': "SpellPower: 20", 'level': '4'},
            4: {'name': "sword", 'attack': "Attack: 5", 'defence': "Defence: 2", 'spellpower': "SpellPower: 5", 'level': '0'},
            4.1: {'name': "sword", 'attack': "Attack: 10", 'defence': "Defence: 4", 'spellpower': "SpellPower: 6", 'level': '1'},
            4.3: {'name': "sword", 'attack': "Attack: 12", 'defence': "Defence: 8", 'spellpower': "SpellPower: 9", 'level': '3'},
            4.4: {'name': "sword", 'attack': "Attack: 20", 'defence': "Defence: 16", 'spellpower': "SpellPower: 14", 'level': '4'},
            5: {'name': "helm", 'attack': "Attack: 4", 'defence': "Defence: 5", 'spellpower': "SpellPower: 2", 'level': '0'},
            5.1: {'name': "helm", 'attack': "Attack: 6", 'defence': "Defence: 10", 'spellpower': "SpellPower: 4", 'level': '1'},
            5.3: {'name': "helm", 'attack': "Attack: 9", 'defence': "Defence: 12", 'spellpower': "SpellPower: 8", 'level': '3'},
            5.4: {'name': "helm", 'attack': "Attack: 16", 'defence': "Defence: 20", 'spellpower': "SpellPower: 14", 'level': '4'},
            6: {'name': "Health Potion v1", 'info': "Gives you upto 5hp"},
            6.1: {'name': "Resurection Potion", 'info': "Resurection Time"},
            7: {'name': "Mana Potion v1", 'info': "Fills mana by 17 pts"}
        }
            colliding_item_rects = []
            for item, quantity in self.items.copy().items():
                if item in images:
                    image_path, image_size, image_position = images[item]
                    image = self.pygame.image.load(image_path).convert_alpha()
                    image = self.pygame.transform.scale(image, image_size)
                    image_rect = image.get_rect(center=image_position)

                    surface.blit(image, image_rect)

                    if quantity <= 0:
                        self.remove_items(item)

                    if image_rect.collidepoint(mouse):
                        if item in item_stats:
                            colliding_item_rects.append(image_rect)
                            stat_info = item_stats[item]
                            stat_img = self.pygame.image.load("img/status_bar.png").convert_alpha()
                            item_surf = self.pygame.Surface((120,120))
                            name = self.skillfont.render(stat_info['name'], True, (255, 255, 255))
                            name_rect = name.get_rect(center=(50, 10))
                            if item >= 6:
                                if stat_img.get_masks()[3]:
                                    print(stat_img.get_masks()[3])
                                name = self.invfont.render(stat_info['name'], True, (255, 255, 255))
                                name_rect = name.get_rect(center=(60, 10))
                                info = self.invfont.render('Info: \n' + stat_info['info'], True, (255, 255, 255))
                                info_rect = info.get_rect(center=(60,40))
                                item_surf.blit(info, info_rect)
                            else:
                                attack = self.skillfont.render(stat_info['attack'], True, (255, 255, 255))
                                attack_rect = attack.get_rect(center=(40, 40))
                                defence = self.skillfont.render(stat_info['defence'], True, (255, 255, 255))
                                defence_rect = defence.get_rect(center=(40, 60))
                                spell_power = self.skillfont.render(stat_info['spellpower'], True, (255, 255, 255))
                                spell_power_rect = spell_power.get_rect(center=(50, 80))
                                level_req = self.skillfont.render('Level Req: ' + stat_info['level'], True, (255, 255, 255))
                                level_req_rect = level_req.get_rect(center=(45, 100))
                                item_surf.blit(attack, attack_rect)
                                item_surf.blit(defence, defence_rect)
                                item_surf.blit(spell_power, spell_power_rect)
                                item_surf.blit(level_req, level_req_rect)

                            item_surf.blit(name, name_rect)
                            item_surf.blit(stat_img, image_rect)

                        if clicked[2]:
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
                            if item < 6 and item not in player.equipped_gear and item not in player.equipped_armor:
                                if player.level >= int(stat_info['level']):
                                    player.gear.append(item)
                                    player.equip_weapon(self, surface)
                                else:
                                    print('Level too low')
                            if self.do_once: #Used to fix too meny items being removed from one use
                                if quantity >= 1 and item != 6:
                                    self.items[item] -= 1
                                    self.do_once = False

                    if colliding_item_rects:
                        item_surf.set_alpha(200)
                        surface.blit(item_surf, colliding_item_rects[0])
                
                if quantity >= 1: #TODO edit font for all items and location for numbers greater than 3 
                    posx = image_position[0]
                    posy = image_position[1]
                    posx += 10

                    if item >= 6:
                        posx -= 15
                        posy -= 5

                    text = self.skillfont.render('{}'.format(quantity), True, (255,255,255))
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
                        player.showplayer = True
                        player.respawn()

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