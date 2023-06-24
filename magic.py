from Sprites import BaseSprite

class Magic(BaseSprite):
    def __init__(self, player):
        image_path = "img/fireball1_R.png"
        super().__init__(image_path)
        self.player = player
        self.direction  = player.direction
        #Sets the image dependant on player direction
        if self.direction == "RIGHT":
            self.image = self.pygame.image.load("img/fireball1_R.png")
        else:
            self.image = self.pygame.image.load("img/fireball1_L.png")  

        self.rect = self.image.get_rect(center = player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40
    def fire(self, surface):
        self.player.magic_cooldown = 0
        # Runs while the fireball is still within the screen w/ extra margin
        if -10 < self.rect.x < 710:
                if self.direction == "RIGHT":
                    self.image = self.pygame.image.load("img/fireball1_R.png")
                    surface.blit(self.image, self.rect)
                else:
                    self.image = self.pygame.image.load("img/fireball1_L.png")
                    surface.blit(self.image, self.rect)
                    
                if self.direction == "RIGHT":
                    self.rect.move_ip(12, 0)
                else:
                    self.rect.move_ip(-12, 0)   
        else:
                self.kill()
                self.player.magic_cooldown = 1
                self.player.attacking = False

class Bolt(BaseSprite):
    def __init__(self, x, y, d, player_group, player):
        image_path = "img/bolt.png"
        super().__init__(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x + 15
        self.rect.y = y + 20
        self.direction = d
        self.player_group = player_group
        self.player = player
    
    def fire(self, surface):
        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            else:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            if self.direction == 0:
                self.rect.move_ip(12,0)
            else:
                self.rect.move_ip(-12,0)
        else:
            self.kill()
        hits = self.pygame.sprite.spritecollide(self, self.player_group, False)
        if hits:
            self.player.player_hit()
            self.kill()

class Energy_blast(BaseSprite):
    def __init__(self, player):
        image_path = "img/bolt.png"
        super().__init__(image_path)
        self.player = player
        self.direction  = player.direction

        if self.direction == "RIGHT":
            self.image = self.pygame.image.load("img/fireball1_R.png")
        else:
            self.image = self.pygame.image.load("img/fireball1_L.png")  

        self.rect = self.image.get_rect(center = player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40
        
    
    def fire(self, surface):
        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            else:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            if self.direction == 0:
                self.rect.move_ip(12,0)
            else:
                self.rect.move_ip(-12,0)
        else:
            self.kill()

class Death_ball(BaseSprite):
    def __init__(self, player):
        image_path = "img/deathball1_R.png"
        super().__init__(image_path)
        self.player = player
        self.direction  = player.direction

        if self.direction == "RIGHT":
            self.image = self.pygame.image.load("img/deathball1_R.png")
        else:
            self.image = self.pygame.image.load("img/deathball1_L.png")

        self.rect = self.image.get_rect(center = player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40
    
    def fire(self, surface):
        if -10 < self.rect.x < 710:
            if self.direction == "RIGHT":
                self.image = self.pygame.image.load("img/deathball1_R.png")
                surface.blit(self.image, self.rect)
            else:
                self.image = self.pygame.image.load("img/deathball1_L.png")
                surface.blit(self.image, self.rect)
            if self.direction == 0:
                self.rect.move_ip(12,0)
            else:
                self.rect.move_ip(-12,0)
        else:
            self.kill()

class Fired(BaseSprite):
    def __init__(self, player):
        image_path = "img/bolt.png"
        super().__init__(image_path)
        self.player = player
        self.direction  = player.direction
        self.rect = self.image.get_rect(center = player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40
    
    def fire(self, surface):
        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            else:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            if self.direction == 0:
                self.rect.move_ip(12,0)
            else:
                self.rect.move_ip(-12,0)
        else:
            self.kill()
        hits = self.pygame.sprite.spritecollide(self, self.player_group, False)
        if hits:
            self.player.player_hit()
            self.kill()

class Fireballv2(BaseSprite):
    def __init__(self, player):
        image_path = "img/bolt.png"
        super().__init__(image_path)
        self.player = player
        self.direction  = player.direction
        self.rect = self.image.get_rect(center = player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40
    
    def fire(self, surface):
        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            else:
                self.image = self.pygame.image.load("img/bolt.png")
                surface.blit(self.image, self.rect)
            if self.direction == 0:
                self.rect.move_ip(12,0)
            else:
                self.rect.move_ip(-12,0)
        else:
            self.kill()