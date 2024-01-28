class PlayerBullet:
    def __init__(self, x, y, mouse_x_2, mouse_y_2):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x_2
        self.mouse_y = mouse_y_2
        self.speed = 15
        self.angle = math.atan2(y - mouse_y_2, x - mouse_x_2)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, display1):
        global score, score1, score2
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        pygame.draw.circle(display1, (0, 0, 0), (self.x + 16, self.y + 16), 5)
        for enemy1 in enemy_1:
            if (enemy1.x - display_scroll[0] < self.x + 16 < enemy1.x - display_scroll[0] + 32 and
                    enemy1.y - display_scroll[1] < self.y + 16 < enemy1.y - display_scroll[1] + 30):

                enemy1.health -= 1
                if enemy1.health <= 0:
                    effects.append(SparkEffect(self.x, self.y))
                    enemy_1.remove(enemy1)
                    score2 += 80
                player_bullets.remove(self)

        for enemy2 in enemy_2:
            if (enemy2.x - display_scroll[0] < self.x + 16 < enemy2.x - display_scroll[0] + 32 and
                    enemy2.y - display_scroll[1] < self.y + 16 < enemy2.y - display_scroll[1] + 30):

                enemy2.health2 -= 1
                if enemy2.health2 <= 0:
                    effects.append(SparkEffect(self.x, self.y))
                    enemy_2.remove(enemy2)
                    score2 += 80
                player_bullets.remove(self)

        for enemy3 in enemy_3:
            if (enemy3.x - display_scroll[0] < self.x + 16 < enemy3.x - display_scroll[0] + 32 and
                    enemy3.y - display_scroll[1] < self.y + 16 < enemy3.y - display_scroll[1] + 30):

                enemy3.health3 -= 1
                if enemy3.health3 <= 0:
                    effects.append(SparkEffect(self.x, self.y))
                    enemy_3.remove(enemy3)
                    score2 += 80
                player_bullets.remove(self)