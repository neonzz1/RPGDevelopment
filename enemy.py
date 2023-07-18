from Sprites import BaseSprite
import random
import numpy
from items import Item
from magic import Bolt

#TODO make enemy heath and bosses etc 

class Enemy(BaseSprite):
    def __init__(self, hit_cooldown, player_group, player):
        image_path = "img/Enemy.png"
        super().__init__(image_path)
        self.rect = self.image.get_rect()     
        self.pos = self.vec(0,0)
        self.vel = self.vec(0,0)
        self.direction = random.randint(0,1) # 0 for Right, 1 for Left
        self.hit_cooldown = hit_cooldown
        self.can_be_hit = True
        self.hit_cooldown_counter = 10
        self.spell_hit_counter = 5
        self.player_group = player_group
        self.player = player
        self.direction = random.randint(0,1) # 0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 2  # Randomised velocity of the generated enemy
        self.health = 4
        self.mana = random.randint(1, 3)  # Randomised mana amount obtained upon kill
        self.quantity = None
        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235

    def move(self, cursor):
        if cursor.wait == 1 or not self.can_be_hit: return
        # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (self.width-20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos # Updates rect
    
    def update(self, handler, Items, Spells):
        # Checks for collision with the Player
        hits = self.pygame.sprite.spritecollide(self, self.player_group, False)
        
        # Checks for collision with Spells
        f_hits = self.pygame.sprite.spritecollide(self, Spells, False)

        if self.health <= 0:
            if self.player.mana < 18: self.player.mana += self.mana # Release mana
            self.player.experience += 1   # Release expeiriance
            handler.enemy_count - 1
            handler.enemy_dead_count += 1
            self.kill()
            item_logic(self)
            if self.item_no != 0:
                Items.add(self.item)

        # Activates upon either of the two expressions being true
        if hits and self.player.attacking and self.can_be_hit: #TODO more testing
                print(self.health)
                self.health -= 1
                self.can_be_hit = False
    
        # If collision has occured and player not attacking, call "hit" function            
        elif hits and not self.player.attacking:
                self.player.player_hit()

        if not self.can_be_hit:
            #print(self.hit_cooldown_counter)
            self.hit_cooldown_counter -= 1
            if self.hit_cooldown_counter == 0:
                self.can_be_hit = True
                self.hit_cooldown_counter = 10

        if self.spell_hit_counter > 0:
            self.spell_hit_counter -= 1
           
        # if spell collision and enemy can be hit is true then take health based on skill
        if f_hits and self.can_be_hit:
            spell_logic(self) #Works but needs work as any spell will insta kill

def spell_logic(self):
            if self.spell_hit_counter == 0:
                if not self.can_be_hit:
                    self.player.mana += 1
                    print("mana added")
                if 'fireball' in self.player.skills:
                    if self.player.spellpower <= 4:
                        self.health -= 1
                    elif self.player.spellpower >= 9 and self.player.spellpower <= 10:
                        self.health -= 2
                    elif self.player.spellpower < 18:
                        self.health -= 3
                    elif self.player.spellpower >= 18:
                        self.health -= 4
                    self.can_be_hit = False
                    self.spell_hit_counter = 5
def item_logic(self):
        rand_num = numpy.random.uniform(0, 100)
        self.item_no = 0
        if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
            self.item_no = 1
        elif rand_num > 5 and rand_num <= 15:
            self.item_no = 2
        elif rand_num >= 15 and rand_num <= 25:
            self.quantity = 1
            if rand_num >= 18 and rand_num <= 21:
                    self.item_no = 3.1
            elif rand_num >= 21 and rand_num <= 23:
                    self.item_no = 3.3
            elif rand_num >= 24 and rand_num <= 25:
                    self.item_no = 3.4
            else:
                self.item_no = 3
        elif rand_num >= 25 and rand_num <= 35:
            self.quantity = 1
            if rand_num >= 28 and rand_num <= 31:
                self.item_no = 4.1
            elif rand_num >= 31 and rand_num <= 33:
                self.item_no = 4.3
            elif rand_num >= 34 and rand_num <= 35:
                self.item_no = 4.4
            else:
                self.item_no = 4
        elif rand_num >= 35 and rand_num <= 45:
            self.quantity = 1
            if rand_num >= 38 and rand_num <= 41:
                self.item_no = 5.1
            elif rand_num >= 41 and rand_num <= 43:
                self.item_no = 5.3
            elif rand_num >= 44 and rand_num <= 45:
                self.item_no = 5.4
            else:
                self.item_no = 5
        elif rand_num >= 45 and rand_num <= 55:
                self.quantity = 1
                self.item_no = 6
        #elif rand_num >= 55 and rand_num <= 65:
            #self.quantity = 1
            #self.item_no = 7
        #elif rand_num > 65 and rand_num < 75:
            #self.item_no = 8
        elif rand_num >= 75:
            self.item_no = 0
        if self.item_no != 0:
            # Add Item to Items group
            self.item = Item(self.item_no, self.quantity)
            # Sets the item location to the location of the killed enemy
            self.item.posx = self.pos.x
            self.item.posy = self.pos.y
class Enemy2(BaseSprite):
    def __init__(self, Playergroup, Spells, player, handler, Items, Bolts):
        image_path = "img/enemy2.png"
        super().__init__(image_path)
        self.Playergroup = Playergroup
        self.Spells = Spells
        self.player = player
        self.handler = handler
        self.Items = Items
        self.pos = self.vec(0,0)
        self.vel = self.vec(0,0)
        self.wait = 0
        self.wait_status = False
        self.turning = 0
        self.health = 5
        self.can_be_hit = True
        self.hit_cooldown_counter = 10
        self.spell_hit_counter = 5
        self.quantity = None
        self.Bolts = Bolts

 
        self.direction = random.randint(0,1) # 0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon

        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 250
            print(self.pos)
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 250

        if self.direction == 0: self.image = self.pygame.image.load("img/enemy2.png")
        if self.direction == 1: self.image = self.pygame.image.load("img/enemy2_L.png")
        self.rect = self.image.get_rect()  

    def move(self, cursor):
        if cursor.wait == 1: return
        #print("moving")
        # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (self.width-20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        if self.wait > 60:
            self.wait_status = True
        elif int(self.wait) <= 0:
            self.wait_status = False
         # Updates positon with new values     
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        
        if self.wait_status:
            rand_num = numpy.random.uniform(0, 50)
            if int(rand_num) == 25:
                bolt = Bolt(self.pos.x, self.pos.y, self.direction, self.Playergroup, self.player)
                self.Bolts.add(bolt)

        self.rect.topleft = self.pos # Updates rect
        
        if (self.direction_check(self.player)):
            self.turn()
            self.wait = 90
            self.turning = 1

    def update(self, handler, Items, Spells):
        # Checks for collision with the Player
        hits = self.pygame.sprite.spritecollide(self, self.Playergroup, False)
 
        # Checks for collision with Spells
        f_hits = self.pygame.sprite.spritecollide(self, Spells, False)
 
        # Activates upon either of the two expressions being true
        if self.health <= 0:
            if self.player.mana < 18: self.player.mana += self.mana # Release mana
            self.player.experience += 1   # Release expeiriance
            handler.enemy_count - 1
            handler.enemy_dead_count += 1
            self.kill()
            item_logic(self)
            if self.item_no != 0:
                Items.add(self.item)

        # Activates upon either of the two expressions being true
        if hits and self.player.attacking and self.can_be_hit: #TODO more testing
                print(self.health)
                self.health -= 1
                self.can_be_hit = False
    
        # If collision has occured and player not attacking, call "hit" function            
        elif hits and not self.player.attacking:
                self.player.player_hit()

        if not self.can_be_hit:
            #print(self.hit_cooldown_counter)
            self.hit_cooldown_counter -= 1
            if self.hit_cooldown_counter == 0:
                self.can_be_hit = True
                self.hit_cooldown_counter = 10

        # if spell collision and enemy can be hit is true then take health based on skill
        if f_hits and self.can_be_hit:
            spell_logic(self) #Works but needs work as any spell will insta kill        

        if self.direction == 0:
            self.image = self.pygame.image.load("img/enemy2.png")
        elif self.direction == 1:
            self.image = self.pygame.image.load("img/enemy2_L.png")
                
    def direction_check(self, player):
        if (player.pos.x - self.pos.x < 0 and self.direction == 0):
            return 1
        elif (player.pos.x - self.pos.x > 0 and self.direction == 1):
            return 1
        else:
            return 0 
    def turn(self):
        if self.wait > 0:
            self.wait -= 1
            #print("wait too high")
            return
        elif int(self.wait) <= 0:
            self.turning = 0
        if (self.direction):
            self.direction = 0
            self.image = self.pygame.image.load("img/enemy2.png")
        else:
            self.direction = 1
            self.image = self.pygame.image.load("img/enemy2_L.png")

class Demon(BaseSprite):
    #TODO add magic(Fireball) and animation
    #TODO work out what causes the right animation glitch
    def __init__(self, Playergroup, Spells, player, handler, Items, Bolts):
        image_path = "img/Demon_R.png"
        super().__init__(image_path)
        self.Playergroup = Playergroup
        self.Spells = Spells
        self.player = player
        self.handler = handler
        self.Items = Items
        self.health = 10
        self.can_be_hit = True
        self.hit_cooldown_counter = 10
        self.spell_hit_counter = 5
        self.pos = self.vec(0,0)
        self.vel = self.vec(0,0)
        self.wait = 0
        self.wait_status = False
        self.turning = 0
        self.Bolts = Bolts
        self.move_frame = 0
 
        self.direction = random.randint(0,1) # 0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon

        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 250
            print(self.pos)
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 250

        if self.direction == 0: self.image = self.pygame.image.load("img/demon_R.png")
        if self.direction == 1: self.image = self.pygame.image.load("img/demon_L.png")
        self.rect = self.image.get_rect()  

    def move(self, cursor):
        if cursor.wait == 1: return
        #print("moving")
        # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (self.width-20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        if self.wait > 60:
            self.wait_status = True
        elif int(self.wait) <= 0:
            self.wait_status = False
         # Updates positon with new values     
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        
        if self.wait_status:
            rand_num = numpy.random.uniform(0, 50)
            if int(rand_num) == 25:
                bolt = Bolt(self.pos.x, self.pos.y, self.direction, self.Playergroup, self.player)
                self.Bolts.add(bolt)

        self.rect.topleft = self.pos # Updates rect
        
        if (self.direction_check(self.player)):
            self.turn()
            self.wait = 90
            self.turning = 1

    def update(self, handler, Items, Spells):
        if self.move_frame > 8:
            self.move_frame = 0

        if self.vel.x > 0:
            if self.direction == 0:
                self.image = self.moveani_R[self.move_frame]
                self.direction = 0
            else:
                self.image = self.moveani_L[self.move_frame]
                self.direction = 1
            self.move_frame += 1
        # Checks for collision with the Player
        hits = self.pygame.sprite.spritecollide(self, self.Playergroup, False)
 
        # Checks for collision with Spells
        f_hits = self.pygame.sprite.spritecollide(self, Spells, False)
 
        # Activates upon either of the two expressions being true
        if self.health <= 0:
            if self.player.mana < 18: self.player.mana += self.mana # Release mana
            self.player.experience += 1   # Release expeiriance
            handler.enemy_count - 1
            handler.enemy_dead_count += 1
            self.kill()
            item_logic(self)
            if self.item_no != 0:
                Items.add(self.item)

        # Activates upon either of the two expressions being true
        if hits and self.player.attacking and self.can_be_hit: #TODO more testing
                print(self.health)
                self.health -= 1
                self.can_be_hit = False
    
        # If collision has occured and player not attacking, call "hit" function            
        elif hits and not self.player.attacking:
                self.player.player_hit()

        if not self.can_be_hit:
            #print(self.hit_cooldown_counter)
            self.hit_cooldown_counter -= 1
            if self.hit_cooldown_counter == 0:
                self.can_be_hit = True
                self.hit_cooldown_counter = 10

        # if spell collision and enemy can be hit is true then take health based on skill
        if f_hits and self.can_be_hit:
            spell_logic(self) #Works but needs work as any spell will insta kill        


    def direction_check(self, player):
        if (player.pos.x - self.pos.x < 0 and self.direction == 0):
            return 1
        elif (player.pos.x - self.pos.x > 0 and self.direction == 1):
            return 1
        else:
            return 0 
    def turn(self):
        if self.wait > 0:
            self.wait -= 1
            #print("wait too high")
            return
        elif int(self.wait) <= 0:
            self.turning = 0
        if (self.direction):
            self.direction = 0
            self.image = self.pygame.image.load("img/demon_R.png").convert_alpha()
        else:
            self.direction = 1
            self.image = self.pygame.image.load("img/demon_L.png").convert_alpha()
           
      