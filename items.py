from Sprites import BaseSprite

#TODO finish coding in new items
      
class Item(BaseSprite):
    def __init__(self, itemtype):
        if itemtype == 1: image_path = "img/heart.png"
        elif itemtype == 2: image_path = "img/coin.png"
        elif itemtype == 3: image_path = "img/staff.png"
        elif itemtype == 4: image_path = "img/swordicon.png"
        elif itemtype == 5: image_path = "img/helm.png"
        else: image_path = "img/heart.png"
        super().__init__(image_path)
        
        self.rect = self.image.get_rect()
        self.type = itemtype
        self.posx = 0
        self.posy = 0
        self.itemsound = ["sounds/handleCoins.ogg", "sounds/metalClick.ogg"]

    def render(self, surface):
      self.rect.x = self.posx
      self.rect.y = self.posy
      surface.blit(self.image, self.rect)

    def update(self, Playergroup, player, health, handler, inventory, mmanager):
      """
      :param Player Group: Pygame sprite Group,
      :param player: Player class
      :param Health: Health class
      :param handler: Eventhandler
      """
      hits = self.pygame.sprite.spritecollide(self, Playergroup, False)
      # Code to be activated if item comes in contact with player
      if hits:
            #TODO create random variables for each item spawned
            if player.health < 5 and self.type == 1:
                player.health += 1
                health.image = player.health_ani[player.health]
                self.kill()
            if self.type == 2:
                mmanager.playsoundtrack(self.itemsound[0], -1, 0.05)
                handler.money += 1
                self.kill()
            if self.type == 3:
                mmanager.playsoundtrack(self.itemsound[1], -1, 0.05)
                inventory.items.append(self.type)
                self.kill()
            if self.type == 4:
                mmanager.playsoundtrack(self.itemsound[1], -1, 0.05)
                inventory.items.append(self.type)
                self.kill()
            if self.type == 5:
                mmanager.playsoundtrack(self.itemsound[1], -1, 0.05)
                inventory.items.append(self.type)
                self.kill()
            if self.type == 6:
                mmanager.playsoundtrack(self.itemsound[1], -1, 0.05)
                inventory.items.append(self.type)
                self.kill()
            else:
                print('Out of range!!')