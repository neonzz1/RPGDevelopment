from Sprites import BaseSprite

ACC = 0.3
FRIC = -0.10

#TODO build proper leveling system

class Player(BaseSprite):
    def __init__(self, ground_group, hit_cooldown, health, mmanager, soundtrack):
        image_path = "img/Player_Sprite_R.png" # this sets self.image in the BaseSprite (This only sets this Sprites not all instances of the BaseSprite)
        super().__init__(image_path)
        self.rect = self.image.get_rect()
        self.gear_image = self.pygame.image.load("img/playergear.png").convert_alpha()
        self.ground_group = ground_group
        self.hit_cooldown = hit_cooldown
        self.jumping = False
        self.running = False
        self.attacking = False
        self.cooldown = False
        self.move_frame = 0
        self.attack_frame = 0
        self.attackpower = 4
        self.defence = 2
        self.spellpower = 1
        self.health = 5
        self.heart = health
        self.experience = 0
        self.level = 0
        self.levels = {0: 2, 1: 6, 2: 10, 3: 20, 4: 30, 5: 50, 6: 100, 7: 150, 8: 200, 9: 260, 10: 370}
        self.leveled = False
        self.show = False
        self.mana = 17
        self.magic_cooldown = 1
        self.slash = 0
        self.addstats = False
        self.mmanager = mmanager
        self.soundtrack = soundtrack
        self.equipped_gear = []
        self.unequipped_gear = []
        self.equipped_armor = []
        self.lastitem = []
        self.swordtrack = [self.pygame.mixer.Sound("sounds/sword1.wav"), self.pygame.mixer.Sound("sounds/sword2.wav")]
        self.movesound = [self.pygame.mixer.Sound("sounds/footstep00.ogg"), self.pygame.mixer.Sound("sounds/footstep01.ogg"),
                           self.pygame.mixer.Sound("sounds/footstep02.ogg"), self.pygame.mixer.Sound("sounds/footstep03.ogg"),
                           self.pygame.mixer.Sound("sounds/footstep04.ogg"), self.pygame.mixer.Sound("sounds/footstep05.ogg"), 
                           self.pygame.mixer.Sound("sounds/footstep06.ogg"), self.pygame.mixer.Sound("sounds/footstep07.ogg"),
                           self.pygame.mixer.Sound("sounds/footstep08.ogg"), self.pygame.mixer.Sound("sounds/footstep09.ogg")]
        self.gear = []
        #self.jumpsound = [self.pygame.mixer.Sound("sounds/")]
        self.skills = []
 
        # Position and direction
        self.vx = 0
        self.pos = self.vec((340, 240))
        self.vel = self.vec(0,0)
        self.acc = self.vec(0,0.5)
        self.direction = "RIGHT"

    def move(self):
        # not pefect will cause player moving to be FALSE if it's slowed too much
        if abs(self.vel.x) > 0.4:
            self.running = True
        else:
            self.running = False
        #print(self.running)
        get_pressed = self.pygame.key.get_pressed()
        if get_pressed[self.pygame.K_LEFT] or get_pressed[self.pygame.K_a]:
            self.acc.x = -ACC
        if get_pressed[self.pygame.K_RIGHT] or get_pressed[self.pygame.K_d]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.acc.x = 0
        if self.pos.x > self.width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.width

        self.rect.midbottom = self.pos
    def update(self, cursor, inv, surface):
        if not inv.hide: #TODO setup a player gear screen showing what's equipped and stats
            gear_rect = self.gear_image.get_rect(center = (340, 150))
            surface.blit(self.gear_image, gear_rect)

            gear_stats = {
            3: {'image': inv.staff, 'stats': (5, 2, 5)},
            3.1: {'image': inv.staff, 'stats': (6, 4, 10)},
            3.3: {'image': inv.staff, 'stats': (9, 8, 12)},
            3.4: {'image': inv.staff, 'stats': (14, 16, 20)},
            4: {'image': inv.sword, 'stats': (5, 2, 5)},
            4.1: {'image': inv.sword, 'stats': (10, 4, 6)},
            4.3: {'image': inv.sword, 'stats': (12, 8, 9)},
            4.4: {'image': inv.sword, 'stats': (20, 16, 14)},
            5: {'image': inv.helm, 'stats': (5, 2, 5)},
            5.1: {'image': inv.helm, 'stats': (10, 4, 6)},
            5.3: {'image': inv.helm, 'stats': (12, 8, 9)},
            5.4: {'image': inv.helm, 'stats': (20, 16, 14)}
        }
            for item in self.equipped_gear or self.equipped_armor:
                gear_data = gear_stats[item]
                if item >= 3 and item <= 4.4:
                    surface.blit(gear_data['image'], (290, 151))
                    print("attack: ", self.attackpower, "defence: ", self.defence, "spellpower: ", self.spellpower)
                if item >= 5:
                    surface.blit(gear_data['image'], (340, 99))
                    print("attack: ", self.attackpower, "defence: ", self.defence, "spellpower: ", self.spellpower)

        if cursor.wait == 1: return
        # Return to base frame if at end of movement sequence 
        if self.move_frame > 6:
                self.move_frame = 0
                return
        if not self.jumping and self.running and not self.leveled:  
            if self.vel.x > 0:
                self.mmanager.playsound(self.movesound[self.move_frame], 0.05)
                self.image = self.run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.mmanager.playsound(self.movesound[self.move_frame], 0.05)
                self.image = self.run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1
            #Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                    self.image = self.run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                    self.image = self.run_ani_L[self.move_frame]

    def equip_weapon(self, inv, surface):
        if not inv.hide: #TODO setup a player gear screen showing stats
            gear_rect = self.gear_image.get_rect(center = (340, 150))
            surface.blit(self.gear_image, gear_rect)
            # Create a dictionary to store the gear and their corresponding stats
        gear_stats = {
            3: {'image': inv.staff, 'stats': (5, 2, 5)},
            3.1: {'image': inv.staff, 'stats': (6, 4, 10)},
            3.3: {'image': inv.staff, 'stats': (9, 8, 12)},
            3.4: {'image': inv.staff, 'stats': (14, 16, 20)},
            4: {'image': inv.sword, 'stats': (6, 2, 3)},
            4.1: {'image': inv.sword, 'stats': (10, 4, 6)},
            4.3: {'image': inv.sword, 'stats': (12, 8, 9)},
            4.4: {'image': inv.sword, 'stats': (20, 16, 14)},
            5: {'image': inv.helm, 'stats': (4, 5, 2)},
            5.1: {'image': inv.helm, 'stats': (6, 10, 4)},
            5.3: {'image': inv.helm, 'stats': (9, 12, 8)},
            5.4: {'image': inv.helm, 'stats': (16, 20, 14)}
        }
        unequipped_gear = []
        equipped_gear = []

        for gear_item in self.gear:
            self.lastitem.append(gear_item) #TODO finish implementing this 
            if gear_item in gear_stats:
                gear_data = gear_stats[gear_item]
                surface.blit(gear_data['image'], (290, 151))# need to move this variable somehow
                if gear_item not in self.equipped_gear and gear_item < 5:
                    self.equipped_gear.append(gear_item)
                    equipped_gear.append(gear_item) # Add the equipped gear to the list
                elif gear_item not in self.equipped_armor and gear_item >= 5:
                    self.equipped_armor.append(gear_item)
                
                if self.addstats:

                    if len(self.equipped_gear) > 0:
                        if 3 in self.lastitem and 3.1 in self.lastitem:
                            if self.lastitem[-1] == 3.1:
                                self.equipped_gear.remove(3)
                                self.unequipped_gear.append(3)
                            else:
                                self.equipped_gear.remove(3.1)
                                self.unequipped_gear.append(3.1)
                        elif 3 in self.lastitem and 3.3 in self.lastitem:
                            if self.lastitem[-1] == 3.3:
                                self.equipped_gear.remove(3)
                                self.unequipped_gear.append(3)
                            else:
                                self.equipped_gear.remove(3.3)
                                self.unequipped_gear.append(3.3)
                        elif 3 in self.lastitem and 3.4 in self.lastitem:
                            if self.lastitem[-1] == 3.4: 
                                self.equipped_gear.remove(3)
                                self.unequipped_gear.append(3)
                            else:
                                self.equipped_gear.remove(3.4)
                                self.unequipped_gear.append(3.4)
                        if 3.1 in self.lastitem and 3.4 in self.lastitem:
                            if self.lastitem[-1] == 3.4:
                                self.equipped_gear.remove(3.1)
                                self.unequipped_gear.append(3.1)
                            else:
                                self.equipped_gear.remove(3.4)
                                self.unequipped_gear.append(3.4)
                        elif 3.1 in self.lastitem and 3.3 in self.lastitem:
                            if self.lastitem[-1] == 3.3:
                                self.equipped_gear.remove(3.1)
                                self.unequipped_gear.append(3.1)
                            else:
                                self.equipped_gear.remove(3.3)
                                self.unequipped_gear.append(3.3)
                        if 3.3 in self.lastitem and 3.4 in self.lastitem:
                            if self.lastitem[-1] == 3.4:
                                self.equipped_gear.remove(3.3)
                                self.unequipped_gear.append(3.3)
                            else:
                                self.equipped_gear.remove(3.4)
                                self.unequipped_gear.append(3.4)

                        if 3 in self.lastitem and 4 in self.lastitem:
                            if self.lastitem[-1] == 4:
                                self.equipped_gear.remove(3)
                                self.unequipped_gear.append(3)
                            else:
                                self.equipped_gear.remove(4)
                                self.unequipped_gear.append(4)
                        elif 3 in self.lastitem and 4.1 in self.lastitem:
                            if self.lastitem[-1] == 4.1:
                                self.equipped_gear.remove(3)
                                self.unequipped_gear.append(3)
                            else:
                                self.equipped_gear.remove(4.1)
                                self.unequipped_gear.append(4.1)
                        elif 3 in self.lastitem and 4.3 in self.lastitem:
                            if self.lastitem[-1] == 4.3:
                                self.equipped_gear.remove(3)
                                self.unequipped_gear.append(3)
                            else:
                                self.equipped_gear.remove(4.3)
                                self.unequipped_gear.append(4.3)
                        elif 3 in self.lastitem and 4.4 in self.lastitem:
                            if self.lastitem[-1] == 4.4:
                                self.equipped_gear.remove(3)
                                self.unequipped_gear.append(3)
                            else:
                                self.equipped_gear.remove(4.4)
                                self.unequipped_gear.append(4.4)
                        if 3.1 in self.lastitem and 4 in self.lastitem:
                            if self.lastitem[-1] == 4:
                                self.equipped_gear.remove(3.1)
                                self.unequipped_gear.append(3.1)
                            else:
                                self.equipped_gear.remove(4)
                                self.unequipped_gear.append(4)
                        elif 3.1 in self.lastitem and 4.1 in self.lastitem:
                            if self.lastitem[-1] == 4.1:
                                self.equipped_gear.remove(3.1)
                                self.unequipped_gear.append(3.1)
                            else:
                                self.equipped_gear.remove(4.1)
                                self.unequipped_gear.append(4.1)
                        elif 3.1 in self.lastitem and 4.3 in self.lastitem:
                            if self.lastitem[-1] == 4.3:
                                self.equipped_gear.remove(3.1)
                                self.unequipped_gear.append(3.1)
                            else:
                                self.equipped_gear.remove(4.3)
                                self.unequipped_gear.append(4.3)
                        elif 3.1 in self.lastitem and 4.4 in self.lastitem:
                            if self.lastitem[-1] == 4.4:
                                self.equipped_gear.remove(3.1)
                                self.unequipped_gear.append(3.1)
                            else:
                                self.equipped_gear.remove(4.4)
                                self.unequipped_gear.append(4.4)
                        if 3.3 in self.lastitem and 4 in self.lastitem:
                            if self.lastitem[-1] == 4:
                                self.equipped_gear.remove(3.3)
                                self.unequipped_gear.append(3.3)
                            else:
                                self.equipped_gear.remove(4)
                                self.unequipped_gear.append(4)
                        elif 3.3 in self.lastitem and 4.1 in self.lastitem:
                            if self.lastitem[-1] == 4.1:
                                self.equipped_gear.remove(3.3)
                                self.unequipped_gear.append(3.3)
                            else:
                                self.equipped_gear.remove(4.1)
                                self.unequipped_gear.append(4.1)
                        elif 3.3 in self.lastitem and 4.3 in self.lastitem:
                            if self.lastitem[-1] == 4.3:
                                self.equipped_gear.remove(3.3)
                                self.unequipped_gear.append(3.3)
                            else:
                                self.equipped_gear.remove(4.3)
                                self.unequipped_gear.append(4.3)
                        if 3.4 in self.lastitem and 4 in self.lastitem:
                            if self.lastitem[-1] == 4:
                                self.equipped_gear.remove(3.4)
                                self.unequipped_gear.append(3.4)
                            else:
                                self.equipped_gear.remove(4)
                                self.unequipped_gear.append(4)
                        elif 3.4 in self.lastitem and 4.1 in self.lastitem:
                            if self.lastitem[-1] == 4.1:
                                self.equipped_gear.remove(3.4)
                                self.unequipped_gear.append(3.4)
                            else:
                                self.equipped_gear.remove(4.1)
                                self.unequipped_gear.append(4.1)
                        elif 3.4 in self.lastitem and 4.3 in self.lastitem:
                            if self.lastitem[-1] == 4.3:
                                self.equipped_gear.remove(3.4)
                                self.unequipped_gear.append(3.4)
                            else:
                                self.equipped_gear.remove(4.3)
                                self.unequipped_gear.append(4.3)
                        elif 3.4 in self.lastitem and 4.4 in self.lastitem:
                            if self.lastitem[-1] == 4.4:
                                self.equipped_gear.remove(3.4)
                                self.unequipped_gear.append(3.4)
                            else:
                                self.equipped_gear.remove(4.4)
                                self.unequipped_gear.append(4.4)
                        if 4 in self.lastitem and 4.1 in self.lastitem:
                            if self.lastitem[-1] == 4.1:
                                self.equipped_gear.remove(4)
                                self.unequipped_gear.append(4)
                            else:
                                self.equipped_gear.remove(4.1)
                                self.unequipped_gear.append(4.1)
                        elif 4 in self.lastitem and 4.3 in self.lastitem:
                            if self.lastitem[-1] == 4.3:
                                self.equipped_gear.remove(4)
                                self.unequipped_gear.append(4)
                            else:
                                self.equipped_gear.remove(4.3)
                                self.unequipped_gear.append(4.3)
                        elif 4 in self.lastitem and 4.4 in self.lastitem:
                            if self.lastitem[-1] == 4.4:
                                self.equipped_gear.remove(4)
                                self.unequipped_gear.append(4)
                            else:
                                self.equipped_gear.remove(4.4)
                                self.unequipped_gear.append(4.4)
                    if len(self.equipped_armor) > 0:
                        if 5 in self.lastitem and 5.1 in self.lastitem:
                            if self.lastitem[-1] == 5.1:
                                self.equipped_armor.remove(5)
                                self.unequipped_gear.append(5)
                            else:
                                self.equipped_armor.remove(5.1)
                                self.unequipped_gear.append(5.1)
                        elif 5 in self.lastitem and 5.3 in self.lastitem:
                            if self.lastitem[-1] == 5.3:
                                self.equipped_armor.remove(5)
                                self.unequipped_gear.append(5)
                            else:
                                self.equipped_armor.remove(5.3)
                                self.unequipped_gear.append(5.3)
                        elif 5 in self.lastitem and 5.4 in self.lastitem:
                            if self.lastitem[-1] == 5.4:
                                self.equipped_armor.remove(5)
                                self.unequipped_gear.append(5)
                            else:
                                self.equipped_armor.remove(5.4)
                                self.unequipped_gear.append(5.4)
                        if self.unequipped_gear:
                            print("removed item_id", self.unequipped_gear[-1])
                    print("last Item:", self.lastitem[-1])
                    if len(self.equipped_gear) == 1:
                        for equipped_item in self.equipped_gear:
                            if self.lastitem[-1] == equipped_item: # prevents readding stats when armor is equipped
                                gear_data = gear_stats[equipped_item]
                                self.attackpower += gear_stats[equipped_item]['stats'][0]
                                self.defence += gear_stats[equipped_item]['stats'][1]
                                self.spellpower += gear_stats[equipped_item]['stats'][2]
                                #self.addstats = False
                    
                    for equipped_armor in self.equipped_armor:
                        if self.lastitem[-1] == equipped_armor: # prevents readding stats when a weapon is equipped
                            gear_data = gear_stats[equipped_armor]
                            self.attackpower += gear_stats[equipped_armor]['stats'][0]
                            self.defence += gear_stats[equipped_armor]['stats'][1]
                            self.spellpower += gear_stats[equipped_armor]['stats'][2]
                            #self.addstats = False

                    self.addstats = False
                    self.gear.remove(gear_item)

                    for gear_item in self.unequipped_gear:
                        if gear_item not in self.equipped_gear or gear_item not in self.equipped_armor:
                            self.reset_values()
                            self.unequipped_gear.remove(gear_item)
                            self.lastitem.remove(gear_item)
                    
            print("attack: ", self.attackpower, "defence: ", self.defence, "spellpower: ", self.spellpower)

            print("eqipped: ", equipped_gear, "Gearlist :", self.gear, "unequipped:", self.unequipped_gear, "Class list:", self.equipped_gear)
        
        # Additional code to handle resetting stats if no gear is equipped
        if self.addstats and not self.equipped_gear:
            self.reset_values()
            
    def reset_values(self):
        if not self.equipped_gear and not self.equipped_armor:
            self.attackpower = 4
            self.defence = 2
            self.spellpower = 1
        elif 3 in self.equipped_gear:
            if not self.equipped_armor:
                self.attackpower = 9
                self.defence = 4
                self.spellpower = 6
            elif 5 in self.equipped_armor:
                self.attackpower = 13
                self.defence = 9 
                self.spellpower = 8
            elif 5.1 in self.equipped_armor:
                self.attackpower = 15
                self.defence = 14
                self.spellpower = 10
            elif 5.3 in self.equipped_armor:
                self.attackpower = 18
                self.defence = 16
                self.spellpower = 14
            elif 5.4 in self.equipped_armor:
                self.attackpower = 25
                self.defence = 24
                self.spellpower = 20
        elif 3.1 in self.equipped_gear:
            if not self.equipped_armor:
                self.attackpower = 10
                self.defence = 6
                self.spellpower = 11
            elif 5 in self.equipped_armor:
                self.attackpower = 14
                self.defence = 11
                self.spellpower = 13
            elif 5.1 in self.equipped_armor:
                self.attackpower = 16
                self.defence = 16
                self.spellpower = 15
            elif 5.3 in self.equipped_armor:
                self.attackpower = 19 
                self.defence = 18
                self.spellpower = 19
            elif 5.4 in self.equipped_armor:
                self.attackpower = 26
                self.defence = 26
                self.spellpower = 25
        elif 3.3 in self.equipped_gear:
            if not self.equipped_armor:
                self.attackpower = 13
                self.defence = 10
                self.spellpower = 13
            elif 5 in self.equipped_armor:
                self.attackpower = 17
                self.defence = 16
                self.spellpower = 15
            elif 5.1 in self.equipped_armor:
                self.attackpower = 19
                self.defence = 20
                self.spellpower = 17
            elif 5.3 in self.equipped_armor:
                self.attackpower = 22
                self.defence = 22
                self.spellpower = 21
            elif 5.4 in self.equipped_armor:
                self.attackpower = 29
                self.defence = 30
                self.spellpower = 27
        elif 3.4 in self.equipped_gear:
            if not self.equipped_armor:
                self.attackpower = 18
                self.defence = 18
                self.spellpower = 21
            elif 5 in self.equipped_armor:
                self.attackpower = 22
                self.defence = 23
                self.spellpower = 23
            elif 5.1 in self.equipped_armor:
                self.attackpower = 24
                self.defence = 28
                self.spellpower = 25
            elif 5.3 in self.equipped_armor:
                self.attackpower = 27
                self.defence = 30
                self.spellpower = 29
            elif 5.4 in self.equipped_armor:
                self.attackpower = 34
                self.defence = 38
                self.spellpower = 35
        elif 4 in self.equipped_gear:
            if not self.equipped_armor:
                self.attackpower = 10
                self.defence = 4
                self.spellpower = 4
            elif 5 in self.equipped_armor:
                self.attackpower = 14
                self.defence = 9 
                self.spellpower = 6
            elif 5.1 in self.equipped_armor:
                self.attackpower = 16
                self.defence = 14 
                self.spellpower = 8
            elif 5.3 in self.equipped_armor:
                self.attackpower = 19
                self.defence = 16 
                self.spellpower = 12
            elif 5.4 in self.equipped_armor:
                self.attackpower = 26
                self.defence = 24 
                self.spellpower = 18
        elif 4.1 in self.equipped_gear:
            if not self.equipped_armor:
                self.attackpower = 14
                self.defence = 6
                self.spellpower = 7
            elif 5 in self.equipped_armor:
                self.attackpower = 18
                self.defence = 11 
                self.spellpower = 9
            elif 5.1 in self.equipped_armor:
                self.attackpower = 20
                self.defence = 16 
                self.spellpower = 11
            elif 5.3 in self.equipped_armor:
                self.attackpower = 23
                self.defence = 18
                self.spellpower = 15
            elif 5.4 in self.equipped_armor:
                self.attackpower = 30
                self.defence = 26
                self.spellpower = 21
        elif 4.3 in self.equipped_gear:
            if not self.equipped_armor:
                self.attackpower = 16
                self.defence = 10
                self.spellpower = 10
            elif 5 in self.equipped_armor:
                self.attackpower = 20
                self.defence = 15
                self.spellpower = 12
            elif 5.1 in self.equipped_armor:
                self.attackpower = 24
                self.defence = 28
                self.spellpower = 25
            elif 5.3 in self.equipped_armor:
                self.attackpower = 27
                self.defence = 30
                self.spellpower = 29
            elif 5.4 in self.equipped_armor:
                self.attackpower = 34
                self.defence = 38
                self.spellpower = 35
        elif 4.4 in self.equipped_gear:
            self.attackpower = 24
            self.defence = 18 
            self.spellpower = 15
        elif 5 in self.equipped_armor and not self.equipped_gear:
            self.attackpower = 8
            self.attackpower = 5
            self.spellpower = 3

    def attack(self, cursor):
        if cursor.wait == 1: return
        # If attack frame has reached end of sequence, return to base frame      
        if self.attack_frame > 10:
                self.attack_frame = 0
                self.attacking = False

        if self.attack_frame == 0:
            self.mmanager.playsound(self.swordtrack[self.slash], 0.05)
            self.slash += 1
            if self.slash >= 2:
                 self.slash = 0
        # Check direction for correct animation to display  
        if self.direction == "RIGHT" and not self.leveled:
                self.image = self.attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT" and not self.leveled:
                self.correction()
                self.image = self.attack_ani_L[self.attack_frame] 
    
        # Update the current attack frame  
        self.attack_frame += 1
    def jump(self):
        self.rect.x += 1
    
        # Check to see if payer is in contact with the ground
        hits = self.pygame.sprite.spritecollide(self, self.ground_group, False)
        
        self.rect.x -= 1
    
        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
        print(self.skills)

    def player_hit(self):
        if not self.cooldown:      
            self.cooldown = True # Enable the cooldown
            self.pygame.time.set_timer(self.hit_cooldown, 1000) # Resets cooldown in 1 second

            self.health = self.health - 1
            self.heart.image = self.health_ani[self.health]
         
        if self.health <= 0:
            self.kill()
            self.pygame.display.update()
            self.mmanager.stop()
            self.mmanager.playsoundtrack(self.soundtrack[2], -1, 0.1)
            self.pygame.display.update()
            
        #print("hit")

    def gravity_check(self):
        hits = self.pygame.sprite.spritecollide(self, self.ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
    def correction(self):
        # Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
                self.pos.x -= 20
        if self.attack_frame == 10:
                self.pos.x += 20
    
    def level_up(self):
        if self.level < len(self.levels) - 1:  # Check if there are more levels available
            level = self.level
            required_experience = self.levels[level]
            if self.experience >= required_experience:
                self.level += 1
                self.experience -= required_experience  # Deduct required experience from current level
                self.leveled = True  # Set the leveled flag to True
                if self.direction == 'RIGHT':
                    if self.leveled:
                        self.image = self.pygame.image.load("img/Player_Sprite_R_Level_Up.png").convert_alpha()
                elif self.direction == 'LEFT':
                    if self.leveled:
                        self.image = self.pygame.image.load("img/Player_Sprite2_L_level_up.png").convert_alpha()
                print(f"Congratulations! You leveled up to Level {self.level}!")
                self.update_attributes()
            else:
                 self.direction = self.direction
                #print("not enough exp")
        else:
            print("You have reached the maximum level.")
        self.update_attributes()

    def update_attributes(self):
         self.leveled = False
         self.health = 5
         self.mana = 17
    
    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)
        

    