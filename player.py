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
        self.attackvalue = 4
        self.defence = 2
        self.spellpower = 1
        self.health = 5
        self.heart = health
        self.experience = 0
        self.level = 0
        self.levels = {0: 2, 1: 6, 2: 10, 3: 20, 4: 30, 5: 50, 6: 200}
        self.leveled = False
        self.show = False
        self.mana = 17
        self.magic_cooldown = 1
        self.slash = 0
        self.mmanager = mmanager
        self.soundtrack = soundtrack
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
            for item in self.gear:
                if item == 3:
                    if 4 in self.gear:
                         self.gear.remove(3)
                    else:
                        surface.blit(inv.staff, (290, 151))
                        self.attackvalue += 5
                        self.defence += 2
                        self.spellpower += 5
                if item == 3.1: #TODO make the stats change spell power etc
                    if 3 in self.gear:
                        self.gear.remove(3)
                    else:
                        surface.blit(inv.staff, (290, 151))
                        self.attackvalue += 6
                        self.defence += 4
                        self.spellpower += 10
                if item == 3.3:
                    if 3 in self.gear:
                        self.gear.remove(3)
                    else:
                        surface.blit(inv.staff, (290, 151))
                        self.attackvalue += 9
                        self.defence += 8
                        self.spellpower += 12
                if item == 3.4:
                    if 3 in self.gear:
                        self.gear.remove(3)
                    else:
                        surface.blit(inv.staff, (290, 151))
                        self.attackvalue += 14
                        self.defence += 16
                        self.spellpower += 20
                if item == 4:
                    if 3 in self.gear:
                        self.gear.remove(4)
                    else:
                        surface.blit(inv.sword, (290, 141))
                if item == 5:
                    surface.blit(inv.helm, (320, 85))
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
        

    