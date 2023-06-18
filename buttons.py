from Sprites import BaseSprite

class PButton(BaseSprite):
    def __init__(self):
        image_path = "img/castle.png"
        super().__init__(image_path)
        self.vect = self.vec(620, 300)
        self.imgdisp = 0
    def render(self, num, cursor, surface):
        if (num == 0):
            self.image = self.pygame.image.load("img/home_small.png")
        elif (num == 1):
            if cursor.wait == 0:
                  self.image = self.pygame.image.load("img/pause_small.png")
            else:
                  self.image = self.pygame.image.load("img/play_small.png")
                               
        surface.blit(self.image, self.vect)