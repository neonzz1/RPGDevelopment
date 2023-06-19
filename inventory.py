from Sprites import BaseSprite

class inventory(BaseSprite):
    def __init__(self):
        image_path = "img/status_bar.png"
        super().__init__(image_path)
        self.items = []
        self.imagee = None
        self.hide = True
        self.pressed = 0

        self.load_image(image_path)

    def toggle_visibility(self):
        self.pressed += 1
        if self.pressed == 1:
            self.hide = not self.hide
            self.pressed = 0
    
    def renderr(self, surface, handler):    
        gold = self.smallerfont.render('Gold: ' + str(handler.money), True, (0, 0, 0))
        if not self.hide:
            surface.blit(self.imagee, (10,30))
            surface.blit(gold, (30,220))
            print('render called')

    def load_image(self, image_path):
        try:
            self.imagee = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))