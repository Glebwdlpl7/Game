import pygame
import numpy as np
from pygame.sprite import Group



class OBJECT:
    '''класс объектов игры'''
    def __init__(self, screen, x, y, v, image):
        self.screen = screen
        self.image = image
        self.image0 = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = v

    def draw(self):  # output
        """рисует объект"""
        self.screen.blit(self.image, self.rect)

    def collision(self, tiles):
        """столкновения со стенами"""
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        for tile in tiles:
            self.rect.centerx += 5
            if self.rect.colliderect(tile):
                collision_types['right'] = True
            self.rect.centerx -= 5

            self.rect.centerx -= 5
            if self.rect.colliderect(tile):
                collision_types['left'] = True
            self.rect.centerx += 5

            self.rect.centery -= 5
            if self.rect.colliderect(tile):
                collision_types['bottom'] = True
            self.rect.centery += 5

            self.rect.centery += 5
            if self.rect.colliderect(tile):
                collision_types['top'] = True
            self.rect.centery -= 5

        return collision_types

    def rotate_(self, point):
        '''поворот объекта'''
        vec = point

        try:
            if vec[0] - self.rect.centerx >= 0:
                angle = np.arctan((vec[1] - self.rect.centery) / (vec[0] - self.rect.centerx))
            else:
                angle = np.arctan((vec[1] - self.rect.centery) / (vec[0] - self.rect.centerx)) + np.pi

        except ZeroDivisionError:
            if vec[1] - self.rect.centery >= 0:
                angle = np.pi / 2
            else:
                angle = 3 * np.pi / 2

        self.image = pygame.transform.rotozoom(self.image0, -90 - 180 * angle / np.pi, 1)
        self.image.get_rect().center = self.rect.center



class PLAYER(OBJECT):
    '''игрок'''
    def __init__(self,screen, x, y, v, image):
        super().__init__(screen, x, y, v, image)
        self.mright = False
        self.mleft = False
        self.mup = False
        self.mdown = False
        self.hp = 100
        self.bullets = Group()

    def update_person(self, tiles, screen):
        """обновление позиции игрока"""
        collisions = self.collision(tiles)
        if self.mright == True and collisions['right'] == False:
            self.rect.centerx += 5

        if self.mleft == True and collisions['left'] == False:
            self.rect.centerx -= 5

        if self.mup == True and collisions['bottom'] == False:
            self.rect.centery -= 5

        if self.mdown == True and collisions['top'] == False:
            self.rect.centery += 5


        self.draw()
        '''рисуем хп'''
        pygame.draw.rect(screen, 'green', (50, 10, 3 * self.hp, 50))
        self.screen.blit(pygame.image.load('images/картинка зеленого.png'), pygame.image.load('images/картинка зеленого.png').get_rect())




class ENEMY(pygame.sprite.Sprite, OBJECT):
    '''враги'''
    def __init__(self, screen, x, y, v, image):
        OBJECT.__init__(self, screen, x, y, v, image)
        pygame.sprite.Sprite.__init__(self)
        self.hp = 20
        self.test_bullets = Group()
        self.bullets = Group()
        self.frequency = 0
        self.ex_speed = 0

    def update(self, tiles):
        """обновление позиции врагов"""
        collisions = self.collision(tiles)

        if collisions['bottom'] == True or collisions['top'] == True:
            self.speed = self.speed * (-1)

        self.rect.centery += self.speed

    def shooting(self, player, tiles):
        '''стрельба врагов'''
        view = False            # Видит ли враг игрока
        if self.speed != 0:
            self.ex_speed = self.speed
        bullet = BULLET(self.screen, self.rect.centerx, self.rect.centery, (player.rect.centerx, player.rect.centery), 30,  pygame.image.load('images/снаряд.png'))
        self.test_bullets.add(bullet)
        self.test_bullets.update(tiles, self.test_bullets)
        for bullet in self.test_bullets:
            if bullet.rect.colliderect(player):
                self.speed = 0
                self.frequency +=1
                view = True
                break
        if view == False:
            self.speed = self.ex_speed
            self.rotate_((self.rect.centerx, self.rect.centery + self.speed))
        elif view:
            self.rotate_((player.rect.centerx, player.rect.centery))
            if self.frequency % 40 == 0:
                bullet = BULLET(self.screen, self.rect.centerx, self.rect.centery, (player.rect.centerx, player.rect.centery), 30, pygame.image.load('images/снаряд.png'))
                self.bullets.add(bullet)

        for bullet in self.bullets:
            bullet.update(tiles, self.bullets)
            bullet.collisions_with_soldiers(player, self.bullets)
            bullet.draw()


    def die(self, enemies):
        '''смерть врага'''
        if self.hp <= 0:
            enemies.remove(self)





class BULLET(pygame.sprite.Sprite, OBJECT):
    '''пули'''
    def __init__(self, screen, x, y,loc, v, image):
        OBJECT.__init__(self, screen, x, y, v, image)
        pygame.sprite.Sprite.__init__(self)
        self.x0 = x
        self.y0 = y
        self.loc = loc

    def update(self, tiles, bullets):
        """перемещение пулю"""
        self.rect.centerx += self.speed * ((self.loc[0] - self.x0) / np.sqrt((self.loc[0] - self.x0) ** 2 + (self.loc[1] - self.y0) ** 2))
        self.rect.centery += self.speed * ((self.loc[1] - self.y0) / np.sqrt((self.loc[0] - self.x0) ** 2 + (self.loc[1] - self.y0) ** 2))
        self.collisions_with_tiles(tiles, bullets)



    def collisions_with_tiles(self, tiles, bullets):
        '''столкновение со стенами'''
        for tile in tiles:
            if self.rect.colliderect(tile):
                bullets.remove(self)

    def collisions_with_soldiers(self, soldier, bullets):
        '''попадание в объект'''
        if self.rect.colliderect(soldier):
            bullets.remove(self)
            soldier.hp -= 10
