import pygame


def draw():
    screen.fill(pygame.Color('Yellow'))
# # инициализация Pygame:
pygame.init()
# размеры окна:
a = int(input())
size = width, height = 155, 155
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
# формирование кадра:
# команды рисования на холсте
# ...
# ...
# смена (отрисовка) кадра:
draw()
pygame.display.flip()
# ожидание закрытия окна:
while pygame.event.wait().type != pygame.QUIT:
    pass
# завершение работы:
pygame.quit()