from Sprites import BaseSprite

class Bolt(BaseSprite):
    def __init__(self, x, y, d):
        image_path = "bolt.png"
        super().__init__(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x + 15
        self.rect.y = y + 20
        self.direction = d
    
    def fire(self):
        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = pygame.image.load("bolt.png")
                surface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("bolt.png")
                surface.blit(self.image, self.rect)