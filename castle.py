from Sprites import BaseSprite

class Castle(BaseSprite):
    def __init__(self):
        image_path = "img/castle.png"
        super().__init__(image_path)
        self.hide = False
    
    def update(self, surface):
        if not self.hide:
            surface.blit(self.image, (400, 80))