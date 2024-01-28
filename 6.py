class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
        self.image = heart_bonus_image

    def main(self, display1):
        if self.active:
            display1.blit(pygame.transform.scale(self.image, (32, 30)),
                          (self.x - display_scroll[0], self.y - display_scroll[1]))