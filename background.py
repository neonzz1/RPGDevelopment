from Sprites import BaseSprite

class Background(BaseSprite):
    def __init__(self):
        image_path = "img/Background.png"
        super().__init__(image_path)
        self.bgX = 0
        self.bgY = 0
        