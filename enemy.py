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
        self.player_group = player_group
        self.player = player
        self.direction = random.randint(0,1) # 0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 2  # Randomised velocity of the generated enemy
        self.mana = random.randint(1, 3)  # Randomised mana amount obtained upon kill
        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235

    def move(self, cursor):
        if cursor.wait == 1: return
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
        
        # Activates upon either of the two expressions being true
        if hits and self.player.attacking or f_hits:
                if self.player.mana < 18: self.player.mana += self.mana # Release mana
                self.player.experience += 1   # Release expeiriance
                self.kill()
                
                rand_num = numpy.random.uniform(0, 100)
                item_no = 0
                if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                    item_no = 1
                elif rand_num > 5 and rand_num <= 15:
                    item_no = 2
                elif rand_num > 15 and rand_num <= 25:
                    item_no = 3
                elif rand_num > 25 and rand_num <= 35:
                    item_no = 4
                elif rand_num > 35 and rand_num <= 45:
                    item_no = 5
                elif rand_num > 45 and rand_num <= 55:
                    item_no = 6
                handler.enemy_dead_count += 1
                        #print("Enemy killed")
                if item_no != 0:
                    # Add Item to Items group
                    item = Item(item_no)
                    Items.add(item)
                    # Sets the item location to the location of the killed enemy
                    item.posx = self.pos.x
                    item.posy = self.pos.y
    
        # If collision has occured and player not attacking, call "hit" function            
        elif hits and not self.player.attacking:
                self.player.player_hit()

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
        if hits and self.player.attacking == True or f_hits:
            self.kill()
            handler.enemy_count - 1
            handler.enemy_dead_count += 1
             
            if self.player.mana < 18: self.player.mana += self.mana # Release mana
            self.player.experience += 1   # Release expeiriance
             
            rand_num = numpy.random.uniform(0, 100)
            item_no = 0
            if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                item_no = 1
            elif rand_num > 5 and rand_num <= 15:
                item_no = 2
            elif rand_num > 15 and rand_num <= 25:
                item_no = 3
            elif rand_num > 25 and rand_num <= 35:
                item_no = 4
            elif rand_num > 35 and rand_num <= 45:
                item_no = 5
            elif rand_num > 45 and rand_num <= 55:
                item_no = 6
 
            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y
            # If collision has occured and player not attacking, call "hit" function            
        elif hits and not self.player.attacking:
                self.player.player_hit()

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
        if self.move_frame > 9:
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
        if hits and self.player.attacking == True or f_hits:
            self.kill()
            handler.enemy_count - 1
            handler.enemy_dead_count += 1
             
            if self.player.mana < 18: self.player.mana += self.mana # Release mana
            self.player.experience += 1   # Release expeiriance
             
            rand_num = numpy.random.uniform(0, 100)
            item_no = 0
            if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                item_no = 1
            elif rand_num > 5 and rand_num <= 15:
                item_no = 2
            elif rand_num > 15 and rand_num <= 25:
                item_no = 3
            elif rand_num > 25 and rand_num <= 35:
                item_no = 4
            elif rand_num > 35 and rand_num <= 45:
                item_no = 5
            elif rand_num > 45 and rand_num <= 55:
                item_no = 6
 
            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y
            # If collision has occured and player not attacking, call "hit" function            
        elif hits and not self.player.attacking:
                self.player.player_hit()

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
           
      