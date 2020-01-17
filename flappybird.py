from pygame.locals import *
import pygame
from random import randint
import sys


class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 635))
        self.bird = pygame.Rect(65, 50, 50, 50)

        self.background = pygame.image.load("flappy.jpg").convert()
        self.bird_icon = [pygame.image.load("osipenko.png").convert_alpha(),
                            pygame.image.load("osipenko.png").convert_alpha(),
                            pygame.image.load("osipenko.png")]
        self.uWall = pygame.image.load("bottom.png").convert_alpha()
        self.dWall = pygame.image.load("top.png").convert_alpha()

        self.prosvet = 165 # Высота просвета
        self.X_axis = 400 # спавн колонн (уменьшается со временем)
        self.Y_axis = 350 # позиция птички (сравнивается с просветом)
        self.jAmplifer = 10 # задержка начала падения
        self.jSpeed = 10 # ускорение падения
        self.gravitation = 5 
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.height = randint(-110, 300)

    def updateWalls(self):
        self.X_axis -= 2 # стены... они двигаются
        if self.X_axis < -100: # Когда стена уходит за край экрана она
            # перемещается в изначальное положение
            self.X_axis = 410
            self.counter += 1 # счёт
            self.height = randint(-110, 300)

    def cycle(self):
        # А вот тут симуляция физики с поправкой на баланс
        if self.jAmplifer: 
            self.jSpeed -= 1
            self.Y_axis -= self.jSpeed
            self.jAmplifer -= 1
        else:
            self.Y_axis += self.gravitation
            self.gravitation += 0.2

        self.bird[1] = self.Y_axis
        # верхний триггер
        uRect = pygame.Rect(self.X_axis,
                             360 + self.prosvet - self.height + 10,
                             self.uWall.get_width() - 10,
                             self.uWall.get_height())
        # нижний триггер
        dRect = pygame.Rect(self.X_axis,
                               0 - self.prosvet - self.height - 10,
                               self.dWall.get_width() - 10,
                               self.dWall.get_height())
        # Смэрть
        if uRect.colliderect(self.bird) or dRect.colliderect(self.bird):
            self.dead = True

        if not 0 < self.bird[1] < 720: # если улетела - возраждаем
            self.bird[1] = 50
            self.Y_axis = 50
            self.dead = False
            self.counter = 0
            self.X_axis = 410
            self.height = randint(-110, 110)
            self.gravitation = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("NokiaCellphone", 50)

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jAmplifer = 10
                    self.gravitation = 5
                    self.jSpeed = 10
            # Строки 95-104 об обновлении экрана, всё стирается и рисуется вновь
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.uWall,
                             (self.X_axis, 360 + self.prosvet - self.height))
            self.screen.blit(self.dWall,
                             (self.X_axis, 0 - self.prosvet - self.height))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))

            if self.dead:
                self.sprite = 2 # при смерти замена картинки

            elif self.jAmplifer:
                self.sprite = 1 # при прыжке вверх 2 картинка (недоработано)

            self.screen.blit(self.bird_icon[self.sprite], (70, self.Y_axis))

            if not self.dead:
                self.sprite = 0 # при падении 1 картинка

            self.updateWalls()
            self.cycle()
            pygame.display.update()



if __name__ == "__main__":
    FlappyBird().run()