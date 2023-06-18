from Sprites import BaseSprite

class Castle(BaseSprite):
    def __init__(self):
        image_path = "img/castle.png"
        super().__init__(image_path)
        self.hide = False
    
    def update(self, surface):
        if self.hide == False:
            surface.blit(self.image, (400, 80))