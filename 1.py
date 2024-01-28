import pygame
import math
import random
import sys

pygame.init()
pygame.mixer.music.load('music/melody.mp3')
pygame.mixer.music.play(-1)
vol = 0.2
pygame.mixer.music.set_volume(vol)
size = WIDTH, HEIGHT = 1000, 800
display = pygame.display.set_mode((1000, 600))
FPS = 60
bg = pygame.image.load("image/fon.png")
bg = pygame.transform.scale(bg, (1000, 600))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

score = 0
score1 = 0
score2 = 0
effects = []

hero_width = 66
hero_height = 62
hero_x = 100
hero_y = 200



player_hearts = 3
player_heart = pygame.image.load('image/heart.png')

player_walk_images = [pygame.image.load("image/player_walk_0.png"), pygame.image.load("image/player_walk_1.png"),
                      pygame.image.load("image/player_walk_2.png"), pygame.image.load("image/player_walk_3.png")]

player_weapon = pygame.image.load("image/shotgun.png").convert()
player_weapon.set_colorkey((255, 255, 255))

slime_animation_images = [pygame.image.load("image/slime_animation_0.png"),
                          pygame.image.load("image/slime_animation_1.png"),
                          pygame.image.load("image/slime_animation_2.png"),
                          pygame.image.load("image/slime_animation_3.png")]

slime_images = [pygame.image.load("image/slime.png"),
                pygame.image.load("image/slime1.png"),
                pygame.image.load("image/slime3.png"),
                pygame.image.load("image/slime5.png")]

slime_blue_images = [pygame.image.load("image/slime_blue1.png"),
                     pygame.image.load("image/slime_blue2.png"),
                     pygame.image.load("image/slime_blue3.png"),
                     pygame.image.load("image/slime_blue4.png")]

spark_images = [pygame.image.load("image/boom1.png"),
                pygame.image.load("image/boom2.png"),
                pygame.image.load("image/boom3.png"),
                pygame.image.load("image/boom4.png")]

heart_bonus_image = pygame.image.load("image/heart.png")


bg_img = pygame.image.load('image/fon.png')
bg_img = pygame.transform.scale(bg_img, (1000, 600))


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

display_scroll = [0, 0]

player_bullets = []

if __name__ == "__main__":
    running = True
    game_over_flag = False

    while running:

        display.blit(bg_img, (-display_scroll[0], -display_scroll[1]))
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

        if keys[pygame.K_a] and hero_x + hero_width < WIDTH:
            display_scroll[0] -= 5

            player.moving_left = True

            for bullet in player_bullets:
                bullet.x += 5

        if keys[pygame.K_d] and hero_x > 0:
            display_scroll[0] += 5

            player.moving_right = True

            for bullet in player_bullets:
                bullet.x -= 5

        if keys[pygame.K_w] and hero_y + hero_height < HEIGHT:
            display_scroll[1] -= 5

            for bullet in player_bullets:
                bullet.y += 5

        if keys[pygame.K_s] and hero_y > 0:
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

        for bonus in bonus1:
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
