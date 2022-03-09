import pygame
from objects import PLAYER, BULLET
import Maps
import sys

clock = pygame.time.Clock()

class GAME:
    def __init__(self):
        self.WIDTH = 1500
        self.HEIGHT = 800
        self.game_over = False
        self.endgame = False
        self.level = 1

    def init_game(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game")
        return screen, surface

    def menu(self, screen):
        '''меню'''
        play = 0
        screen.fill('orange')

        font_1 = pygame.font.SysFont('arial', 100)
        text_1 = font_1.render('играть', True, (0, 0, 0), 'white')
        place_1 = text_1.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 160))
        font_2 = pygame.font.SysFont('arial', 100)
        text_2 = font_2.render('выход', True, (0, 0, 0), 'white')
        place_2 = text_2.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        screen.blit(text_1, place_1)
        screen.blit(text_2, place_2)
        if self.game_over:
            font_3 = pygame.font.SysFont('arial', 100)
            text_3 = font_3.render('Вы проиграли:(', True, (254, 11, 25), 'yellow')
            place_3 = text_3.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 300))
            screen.blit(text_3, place_3)
        elif self.endgame:
            font_3 = pygame.font.SysFont('arial', 100)
            text_3 = font_3.render('Вы выиграли!', True, (254, 11, 25), 'yellow')
            place_3 = text_3.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 300))
            screen.blit(text_3, place_3)
        pygame.display.update()
        while 1:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if place_1.collidepoint(mouse_position[0], mouse_position[1]):
                        play = 1
                    if place_2.collidepoint(mouse_position[0], mouse_position[1]):
                        sys.exit()
                if event.type == pygame.QUIT:
                    sys.exit()

            if play:
                break

    def events(self, screen, player):
        """обработка событий"""
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu(screen)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.mright = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.mright = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.mleft = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.mleft = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.mup = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.mup = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player.mdown = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player.mdown = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                new_bullet = BULLET(screen, player.rect.centerx, player.rect.centery, pos, 30,
                                    pygame.image.load('images/снаряд игрока.png'))
                player.bullets.add(new_bullet)

        vec = pygame.mouse.get_pos()
        player.rotate_(vec)

    def run(self):
        screen, surface = self.init_game()

        while True:
            self.menu(screen)
            flag = 1
            player = PLAYER(screen, 0, self.HEIGHT/2, 1, pygame.image.load('images/зеленый.png').convert_alpha())
            while flag == 1:
                tile_rects, enemies = Maps.read(surface, screen, self.level)
                while True:
                    screen.blit(surface, screen.get_rect())
                    self.events(screen, player)
                    player.update_person(tile_rects, screen)
                    player.bullets.update(tile_rects, player.bullets)
                    for enemy in enemies:
                        for bullet in player.bullets:
                            bullet.draw()
                            bullet.collisions_with_soldiers(enemy, player.bullets)
                        enemy.update(tile_rects)
                        enemy.shooting(player, tile_rects)
                        enemy.draw()
                        enemy.die(enemies)
                        enemy.update(tile_rects)
                    clock.tick(60)
                    pygame.display.flip()
                    if player.hp <=0:
                        flag = 0
                        self.game_over = True
                        self.level = 1
                        break

                    if player.rect.centerx > self.WIDTH:
                        if self.level == 2:
                            self.endgame = True
                            self.level = 0
                            flag = 0
                        self.level += 1
                        player.rect.centerx = 0
                        break

                pygame.display.flip()






game = GAME()
game.run()
