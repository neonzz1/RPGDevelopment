from Sprites import BaseSprite

class ManaBar(BaseSprite):
    def __init__(self):
        image_path = "img/mana_full.png"
        super().__init__(image_path)
    
    def renders(self, surface):
        if not self.hide:
            self.image = self.pygame.transform.scale(self.image, (220,60))
            surface.blit(self.image, (220, 0))