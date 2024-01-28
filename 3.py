class SlimeEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = slime_animation_images
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-1000, 500)
        self.offset_y = random.randrange(-1000, 500)
        self.health = 5
        self.hit_counter = 0

    def main(self, display1):
        global score
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.health <= 0:
            effects.append(SparkEffect(self.x, self.y))
            enemy_1.remove(self)
            score += 80

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-1000, 500)
            self.offset_y = random.randrange(-1000, 500)
            self.reset_offset = random.randrange(130, 150)
        else:
            self.reset_offset -= 1
        if player.x + self.offset_x > self.x - display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 1
        if player.y + self.offset_y > self.y - display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 1
        display1.blit(pygame.transform.scale(self.animation_images[self.animation_count // 4], (32, 30)),
                      (self.x - display_scroll[0], self.y - display_scroll[1]))
