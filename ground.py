from Sprites import BaseSprite

class Ground(BaseSprite):
    def __init__(self):
        image_path = "img/Ground.png"
        super().__init__(image_path)
        self.rect = self.image.get_rect(center = (350, 350)) 