from board import Board
from common import Const, Utils
import pygame
from pygame.locals import *
import sys
import threading
import time


class UI(object):
    def __init__(self):
        pygame.init()
        self.width = Const.BOARD_size[0] * Const.UI_scale
        self.height = Const.BOARD_size[1] * Const.UI_scale
        self.size = [self.width, self.height]
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        pygame.display.set_caption("Lonely observer")
        self.surf_old = pygame.Surface(self.size, flags=SRCALPHA)
        self.surf_mid = pygame.Surface(self.size, flags=SRCALPHA)
        self.surf_new = pygame.Surface(self.size, flags=SRCALPHA)
        self.board = Board(self.update_new)
        self.cur_map = Utils.array2d(*Const.BOARD_size, -1)
        self.anchor = [0, 0]
        self.mag = 1
        self.disp_shadow = True
        threading.Thread(target=self.check_loop, daemon=True).start()
        self.ui_loop()

    def update_new(self, x, y, color, info=None):
        self.render_pixel(self.surf_new, x, y, color)
        self.cur_map[x][y] = color
        suffix = " ({})".format(info) if info is not None else ""
        print("{} {} {}{}".format(x, y, color, suffix))

    def get_pos(self, x, y):
        return [Const.UI_scale * x, Const.UI_scale * y]

    def render_pixel(self, surf, x, y, color):
        sx, sy = self.get_pos(x, y)
        rect = [sx, sy, Const.UI_scale, Const.UI_scale]
        pygame.draw.rect(surf, Const.PA_colors[color], rect)

    def render_init(self):
        self.surf_old.fill([255, 255, 255])
        for i in range(Const.BOARD_size[0]):
            for j in range(Const.BOARD_size[1]):
                color = self.board.map[i][j]
                self.render_pixel(self.surf_old, i, j, color)
                self.cur_map[i][j] = color
        self.surf_mid.fill([50, 50, 50, 220])
        self.surf_new.fill([0, 0, 0, 0])

    def render(self):
        tmp_size = [self.width * self.mag, self.height * self.mag]
        surf_old_scaled = pygame.transform.scale(self.surf_old, tmp_size)
        surf_new_scaled = pygame.transform.scale(self.surf_new, tmp_size)
        self.screen.fill([0, 0, 0])
        self.screen.blit(surf_old_scaled, self.anchor)
        if self.disp_shadow:
            self.screen.blit(self.surf_mid, [0, 0])
        self.screen.blit(surf_new_scaled, self.anchor)

    def update_anchor(self, dx=0, dy=0):
        nx = Utils.interval(self.width - self.mag *
                            Const.BOARD_size[0], 0, self.anchor[0] + dx)
        ny = Utils.interval(self.height - self.mag *
                            Const.BOARD_size[1], 0, self.anchor[1] + dy)
        self.anchor = [nx, ny]

    def check_loop(self):
        while True:
            for i in range(Const.BOARD_size[0]):
                for j in range(Const.BOARD_size[1]):
                    if self.board.map[i][j] != self.cur_map[i][j]:
                        self.update_new(i, j, self.board.map[i][j], "check")
            time.sleep(Const.UI_check_interval)

    def ui_loop(self):
        self.render_init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_DELETE:
                        self.render_init()
                    elif event.key == K_TAB:
                        self.disp_shadow = not self.disp_shadow
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.mag = Utils.interval(
                            1, Const.UI_max_magnification, self.mag + 1)
                        self.update_anchor()
                    elif event.button == 5:
                        self.mag = Utils.interval(
                            1, Const.UI_max_magnification, self.mag - 1)
                        self.update_anchor()
                elif event.type == pygame.MOUSEMOTION:
                    if any(event.buttons):
                        self.update_anchor(*event.rel)
            self.render()
            pygame.display.update()
            time.sleep(Const.UI_flush_interval)


if __name__ == "__main__":
    ui = UI()
