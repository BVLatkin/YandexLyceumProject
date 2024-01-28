class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        self.hearts = 3
        self.score = 0
        self.heart_image = pygame.image.load('image/heart.png')

    def handle_collisions(self):
        global player_hearts
        enemy_lists = [enemy_1, enemy_2, enemy_3]

        for enemy_list in enemy_lists:
            for enemy4 in enemy_list:
                if (self.x + self.width > enemy4.x - display_scroll[0] and
                        self.x < enemy4.x + 32 - display_scroll[0] and
                        self.y + self.height > enemy4.y - display_scroll[1] and
                        self.y < enemy4.y + 30 - display_scroll[1]):
                    player_hearts -= 1
                    if player_hearts > 0:
                        enemy_list.remove(enemy4)
                    else:
                        game_over()

    def handle_bonus_collisions1(self, bonuses):
        global player_bullets
        for bonus3 in bonuses:
            if bonus3.active and (
                    self.x + self.width > bonus3.x - display_scroll[0] and self.x < bonus3.x + 32 - display_scroll[0]
                    and self.y + self.height > bonus3.y - display_scroll[1]
                    and self.y < bonus3.y + 30 - display_scroll[1]):
                bonus3.active = False
                player_bullets.append(PlayerBullet(self.x, self.y, mouse_x, mouse_y))
                player_bullets.append(PlayerBullet(self.x, self.y, mouse_x, mouse_y))

    def handle_weapons(self, display1):
        mouse_x_1, mouse_y_1 = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x_1 - self.x, mouse_y_1 - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        player_weapon_copy = pygame.transform.rotate(player_weapon, angle)
        display1.blit(player_weapon_copy, (
            self.x + 15 - int(player_weapon_copy.get_width() / 2),
            self.y + 25 - int(player_weapon_copy.get_height() / 2)))

    def main(self, display1):
        self.animation_count = (self.animation_count + 1) % 16
        player_surface = pygame.Surface((32, 42), pygame.SRCALPHA)
        if self.moving_right:
            player_surface.blit(pygame.transform.scale(player_walk_images[self.animation_count // 4], (32, 42)), (0, 0))
        elif self.moving_left:
            player_surface.blit(pygame.transform.scale(
                pygame.transform.flip(player_walk_images[self.animation_count // 4], True, False), (32, 42)), (0, 0))
        else:
            player_surface.blit(pygame.transform.scale(player_walk_images[0], (32, 42)), (0, 0))
        display1.blit(player_surface, (self.x, self.y))
        if self.hearts <= 0:
            game_over()
        self.handle_weapons(display1)
        self.moving_right = False
        self.moving_left = False
        self.handle_collisions()

    def display_hearts(self, display1):
        heart_width = self.heart_image.get_width()
        heart_spacing = 10
        total_heart_width = (heart_width + heart_spacing) * player_hearts - heart_spacing
        start_x = (WIDTH - total_heart_width) // 2
        for i in range(player_hearts):
            display1.blit(self.heart_image, (start_x + i * (heart_width + heart_spacing), 10))

    def draw_hearts(self):
        heart_image = pygame.image.load('heart.png')
        for i in range(player_hearts):
            self.blit(heart_image,
                      (WIDTH // 2 - (player_hearts * heart_image.get_width()) // 2 + i * heart_image.get_width(), 10))

    def handle_bonus_collisions(self, bonuses):
        global player_hearts
        for bonus11 in bonuses:
            if bonus11.active and (self.x + self.width > bonus11.x - display_scroll[0] and
                                   self.x < bonus11.x + 32 - display_scroll[0] and
                                   self.y + self.height > bonus11.y - display_scroll[1] and
                                   self.y < bonus11.y + 30 - display_scroll[1]):
                bonus11.active = False
                player_hearts += 1