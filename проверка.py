import pygame
import math
import random
import sys

pygame.init()
pygame.mixer.music.load('melody.mp3')
pygame.mixer.music.play(-1)
vol = 0.5
pygame.mixer.music.set_volume(vol)
size = WIDTH, HEIGHT = 1000, 800
display = pygame.display.set_mode((1000, 600))
FPS = 60
bg = pygame.image.load("fon.png")
bg = pygame.transform.scale(bg, (1000, 600))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

score = 0
score1 = 0
score2 = 0
effects = []

player_hearts = 3
player_heart = pygame.image.load('heart.png')

player_walk_images = [pygame.image.load("player_walk_0.png"), pygame.image.load("player_walk_1.png"),
                      pygame.image.load("player_walk_2.png"), pygame.image.load("player_walk_3.png")]

player_weapon = pygame.image.load("shotgun.png").convert()
player_weapon.set_colorkey((255, 255, 255))

slime_animation_images = [pygame.image.load("slime_animation_0.png"),
                          pygame.image.load("slime_animation_1.png"),
                          pygame.image.load("slime_animation_2.png"),
                          pygame.image.load("slime_animation_3.png")]

slime_images = [pygame.image.load("slime.png"),
                pygame.image.load("slime1.png"),
                pygame.image.load("slime3.png"),
                pygame.image.load("slime5.png")]

slime_blue_images = [pygame.image.load("slime_blue1.png"),
                     pygame.image.load("slime_blue2.png"),
                     pygame.image.load("slime_blue3.png"),
                     pygame.image.load("slime_blue4.png")]

coin_bonus_image = pygame.image.load("bonus.png")

spark_images = [pygame.image.load("boom1.png"),
                pygame.image.load("boom2.png"),
                pygame.image.load("boom3.png"),
                pygame.image.load("boom4.png")]

heart_bonus_image = pygame.image.load("heart.png")
image_1 = pygame.image.load('fon_im.png')


window = pygame.display.set_mode((1000, 600))
bg_img = pygame.image.load('fon.png')
bg_img = pygame.transform.scale(bg_img,(1000, 600))
x = 50
y = 425

def game_over():
    game_over_text = pygame.font.SysFont('f', 199).render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    display.fill((0, 0, 0))
    display.blit(game_over_text, game_over_rect)
    pygame.mixer.music.stop()
    pygame.display.flip()

    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def game_over1():
    game_over_text = pygame.font.SysFont('f', 199).render("WIN!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    display.fill((0, 0, 0))
    display.blit(game_over_text, game_over_rect)
    pygame.mixer.music.stop()
    pygame.display.flip()

    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def terminate():
    pygame.quit()
    sys.exit()


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
        self.heart_image = pygame.image.load('heart.png')

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


class SlimeEnemy1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = slime_images
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-1000, 500)
        self.offset_y = random.randrange(-1000, 500)
        self.health2 = 3

    def main(self, display1):
        global score1
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.health2 <= 0:
            effects.append(SparkEffect(self.x, self.y))
            enemy_2.remove(self)
            score1 += 80

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-1000, 500)
            self.offset_y = random.randrange(-1000, 500)
            self.reset_offset = random.randrange(178, 389)
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


class SlimeEnemy2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = slime_blue_images
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-1000, 500)
        self.offset_y = random.randrange(-1000, 500)
        self.health3 = 2
        self.hit_counter = 0

    def main(self, display1):
        global score2
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.health3 <= 0:
            effects.append(SparkEffect(self.x, self.y))
            enemy_3.remove(self)
            score2 += 80

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


class BonusCoin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
        self.animation_images = coin_bonus_image

    def main(self, display1):
        if self.active:
            display1.blit(pygame.transform.scale(self.animation_images, (32, 30)),
                          (self.x - display_scroll[0], self.y - display_scroll[1]))


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

        for bonus4 in bonus_coin:
            bonus4.main(display1)

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


enemy_1 = [SlimeEnemy(1299, 467),
           SlimeEnemy(1400, 400),
           SlimeEnemy(500, 300),
           SlimeEnemy(400, 400),
           SlimeEnemy(800, 800),
           SlimeEnemy(1000, 400),
           SlimeEnemy(1500, 300)]

enemy_2 = [SlimeEnemy1(1299, 467),
           SlimeEnemy1(1400, 400),
           SlimeEnemy1(1500, 180),
           SlimeEnemy1(1200, 1000),
           SlimeEnemy1(700, 400),
           SlimeEnemy1(1500, 1000)]

enemy_3 = [SlimeEnemy2(1000, 467),
           SlimeEnemy2(1133, 400),
           SlimeEnemy2(800, 180),
           SlimeEnemy2(1500, 467),
           SlimeEnemy2(1133, 1500),
           SlimeEnemy2(300, 1200)]

bonus1 = [Bonus(1000, 800),
          Bonus(90, 85),
          Bonus(1900, 300)]

player = Player(400, 300, 32, 32)

bonus_coin = [BonusCoin(500, 800)]

display_scroll = [0, 0]

player_bullets = []


class SparkEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = spark_images
        self.animation_count = 0

    def main(self, display1):
        if self.animation_count >= len(self.images) * 4:
            return True

        display1.blit(self.images[self.animation_count // 4], (self.x, self.y))
        self.animation_count += 1
        return False


if __name__ == "__main__":
    running = True
    game_over_flag = False

    while running:

        window.blit(bg_img, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if player.hearts <= 0:
            running = False
            game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

        for effect in effects[:]:
            if effect.main(display):
                effects.remove(effect)

        if player_hearts == 0:
            pygame.quit()
            quit()

        keys = pygame.key.get_pressed()

        pygame.draw.rect(display, (255, 255, 255), (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))

        if keys[pygame.K_a]:
            display_scroll[0] -= 5

            player.moving_left = True

            for bullet in player_bullets:
                bullet.x += 5

        if keys[pygame.K_d]:
            display_scroll[0] += 5

            player.moving_right = True

            for bullet in player_bullets:
                bullet.x -= 5

        if keys[pygame.K_w]:
            display_scroll[1] -= 5

            for bullet in player_bullets:
                bullet.y += 5

        if keys[pygame.K_s]:
            display_scroll[1] += 5

            for bullet in player_bullets:
                bullet.y -= 5

        player.main(display)

        for bullet in player_bullets:
            bullet.main(display)

        for enemy in enemy_1:
            enemy.main(display)

        for enemy in enemy_2:
            enemy.main(display)

        for enemy in enemy_3:
            enemy.main(display)

        for bonus in bonus1:
            bonus.main(display)

        for bonus in bonus_coin:
            bonus.main(display)

        player.display_hearts(display)

        player.handle_bonus_collisions(bonus1)

        sum1 = score + score1 + score2

        score_text = pygame.font.SysFont('f', 24).render("Очки: " + str(sum1),
                                                         True, (255, 255, 255))

        display.blit(score_text, (900, 10))

        if sum1 >= 1000:
            game_over1()

        image = pygame.Surface([WIDTH, HEIGHT])
        image.blit(image, (0, 0))

        clock.tick(60)
        pygame.display.update()
