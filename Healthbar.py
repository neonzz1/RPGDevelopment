from Sprites import BaseSprite

class HealthBar(BaseSprite):
    def __init__(self):
        image_path = "img/hearts_full.png"
        super().__init__(image_path)
    
    def renders(self, surface):
        if self.hide == False:
            self.image = self.pygame.transform.scale(self.image, (220,60))
            surface.blit(self.image, (10, 0))