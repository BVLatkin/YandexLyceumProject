import pygame
import math
import random
import sys
import os
pygame.init()
vol = 0.5
pygame.mixer.music.set_volume(vol)
size = WIDTH, HEIGHT = 1000, 800
display = pygame.display.set_mode((1000, 600))
FPS = 60
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
score = 0
score1 = 0
score2 = 0
effects = []
player_walk_images = [pygame.image.load("player_walk_0.png"), pygame.image.load("player_walk_1.png"),
                      pygame.image.load("player_walk_2.png"), pygame.image.load("player_walk_3.png")]
player_weapon = pygame.image.load("shotgun.png").convert()
player_weapon.set_colorkey((255, 255, 255))
slime_animation_images = [pygame.image.load("slime_animation_0.png"),
                          pygame.image.load("slime_animation_1.png"),
                          pygame.image.load("slime_animation_2.png"),
                          pygame.image.load("slime_animation_3.png")]
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
    def handle_weapons(self, display1):
        mouse_x_1, mouse_y_1 = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x_1 - self.x, mouse_y_1 - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        player_weapon_copy = pygame.transform.rotate(player_weapon, angle)
        display1.blit(player_weapon_copy, (
        self.x + 15 - int(player_weapon_copy.get_width() / 2), self.y + 25 - int(player_weapon_copy.get_height() / 2)))
    def main(self, display1):
        self.animation_count = (self.animation_count + 1) % 16
        player_surface = pygame.Surface((32, 42), pygame.SRCALPHA)
        if self.moving_right:
            player_surface.blit(pygame.transform.scale(player_walk_images[self.animation_count // 4], (32, 42)), (0, 0))
        display1.blit(player_surface, (self.x, self.y))
        self.handle_weapons(display1)
        self.moving_right = False
        self.moving_left = False
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
            enemy_1.remove(self)
            score += 80
        if self.reset_offset == 0:
            self.offset_x = random.randrange(-1000, 500)
            self.offset_y = random.randrange(-1000, 500)
            self.reset_offset = random.randrange(130, 150)
        else:
            self.reset_offset -= 1
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
                    enemy_1.remove(enemy1)
                    score2 += 80
                player_bullets.remove(self)
enemy_1 = [SlimeEnemy(1299, 467),
           SlimeEnemy(1400, 400),
           SlimeEnemy(500, 300),
           SlimeEnemy(400, 400),
           SlimeEnemy(800, 800),
           SlimeEnemy(1000, 400),
           SlimeEnemy(1500, 300)]
player = Player(400, 300, 32, 32)
display_scroll = [0, 0]
player_bullets = []
if __name__ == "__main__":
    running = True
    while running:
        display.fill((0, 0, 255))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
        for effect in effects[:]:
            if effect.main(display):
                effects.remove(effect)
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
        sum1 = score + score1 + score2
        score_text = pygame.font.SysFont('f', 24).render("Очки: " + str(sum1), True, (255, 255, 255))
        display.blit(score_text, (900, 10))
        if sum1 >= 1000:
            pygame.quit()
            quit()
        image = pygame.Surface([WIDTH, HEIGHT])
        image.blit(image, (0, 0))
        clock.tick(60)
        pygame.display.update()
