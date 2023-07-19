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
        self.healthbool = False
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
        
        self.heart.image = self.health_ani[self.health]
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
            gear_rect = self.gear_image.get_rect(center=(340, 150))
            surface.blit(self.gear_image, gear_rect)

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
            self.lastitem.append(gear_item) # TODO finish implementing this

            if gear_item in gear_stats:
                gear_data = gear_stats[gear_item]
                surface.blit(gear_data['image'], (290, 151))

                if gear_item < 5:
                    if gear_item not in self.equipped_gear:
                        self.equipped_gear.append(gear_item)
                        equipped_gear.append(gear_item)
                else:
                    if gear_item not in self.equipped_armor:
                        self.equipped_armor.append(gear_item)

                if self.addstats:
                    for equipped_item in self.equipped_gear:
                        if self.lastitem[-1] == equipped_item:
                            gear_data = gear_stats[equipped_item]
                            self.attackpower += gear_data['stats'][0]
                            self.defence += gear_data['stats'][1]
                            self.spellpower += gear_data['stats'][2]

                    for equipped_armor in self.equipped_armor:
                        if self.lastitem[-1] == equipped_armor:
                            gear_data = gear_stats[equipped_armor]
                            self.attackpower += gear_data['stats'][0]
                            self.defence += gear_data['stats'][1]
                            self.spellpower += gear_data['stats'][2]

                    self.addstats = False
                    self.gear.remove(gear_item)
                    if len(self.gear) > 1:
                        self.gear = []
                    self.unequipped_gear.append(gear_item)
                    self.reset_values()

            print("attack:", self.attackpower, "defence:", self.defence, "spellpower:", self.spellpower)
            print("equipped:", equipped_gear, "Gearlist:", self.gear, "unequipped:", self.unequipped_gear, "Class list:", self.equipped_gear)

        if self.addstats and not self.equipped_gear:
            self.reset_values()
            
    def reset_values(self):
        stats_mapping = {
            (0, 0): (4, 2, 1),
            (3, 0): (9, 4, 6),
            (3, 5): (13, 9, 8),
            (3, 5.1): (15, 14, 10),
            (3, 5.3): (18, 16, 14),
            (3, 5.4): (25, 24, 20),
            (3.1, 0): (10, 6, 11),
            (3.1, 5): (14, 11, 13),
            (3.1, 5.1): (16, 16, 15),
            (3.1, 5.3): (19, 18, 19),
            (3.1, 5.4): (26, 26, 25),
            (3.3, 0): (13, 10, 13),
            (3.3, 5): (17, 16, 15),
            (3.3, 5.1): (19, 20, 17),
            (3.3, 5.3): (22, 22, 21),
            (3.3, 5.4): (29, 30, 27),
            (3.4, 0): (18, 18, 21),
            (3.4, 5): (22, 23, 23),
            (3.4, 5.1): (24, 28, 25),
            (3.4, 5.3): (27, 30, 29),
            (3.4, 5.4): (34, 38, 35),
            (4, 0): (10, 4, 4),
            (4, 5): (14, 9, 6),
            (4, 5.1): (16, 14, 8),
            (4, 5.3): (19, 16, 12),
            (4, 5.4): (26, 24, 18),
            (4.1, 0): (14, 6, 7),
            (4.1, 5): (18, 11, 9),
            (4.1, 5.1): (20, 16, 11),
            (4.1, 5.3): (23, 18, 15),
            (4.1, 5.4): (30, 26, 21),
            (4.3, 0): (16, 10, 10),
            (4.3, 5): (20, 15, 12),
            (4.3, 5.1): (24, 28, 25),
            (4.3, 5.3): (27, 30, 29),
            (4.3, 5.4): (34, 38, 35),
            (4.4, 0): (24, 18, 15),
            (4.4, 5): (28, 23, 17),
            (4.4, 5.1): (30, 28, 19),
            (4.4, 5.3): (33, 30, 23),
            (4.4, 5.4): (40, 38, 29),
            (5, 0): (8, 5, 3),
            (5.1, 0): (10, 7, 5),
            (5.3, 0): (13, 14, 9),
            (5.4, 0): (20, 22, 15),
    }

        key = (self.equipped_gear[-1] if self.equipped_gear else 0, self.equipped_armor[-1] if self.equipped_armor else 0)
        self.attackpower, self.defence, self.spellpower = stats_mapping.get(key, (4, 2, 1))

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

            self.health -= 1
            self.heart.image = self.health_ani[self.health]
            self.healthbool = True
         
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
                self.update_attributes()
                if self.direction == 'RIGHT':
                    if self.leveled:
                        self.image = self.pygame.image.load("img/Player_Sprite_R_Level_Up.png").convert_alpha()
                elif self.direction == 'LEFT':
                    if self.leveled:
                        self.image = self.pygame.image.load("img/Player_Sprite2_L_level_up.png").convert_alpha()
                print(f"Congratulations! You leveled up to Level {self.level}!")
                
            else:
                 self.direction = self.direction
                #print("not enough exp")
        else:
            print("You have reached the maximum level.")
        

    def update_attributes(self):
        self.health = 5
        self.mana = 17
        self.leveled = False
    
    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)
        

    