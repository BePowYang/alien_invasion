import pygame
import sys
import os
from pygame.sprite import Sprite
class Alien(Sprite):
    """ 表示单个外星人的类 """

    def __init__(self,ai_game):
        """ 初始化外星人并设置其起始位置 """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('alien_invasion/images/alien spaceship.bmp')
        self.rect = self.image.get_rect()
        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存外星人的精确水平位置
        self.x = float(self.rect.x)

        # 储存每个外星人的方向
        self.direction = self.settings.fleet_direction

    def check_edges(self):
        """ 如果外星人位于屏幕边缘,就返回True """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    def update(self):
        """ 向左或向右移动外星人 """
        self.x += self.settings.alien_speed * self.direction
        self.rect.x = self.x

def get_resource_path(relative_path):
    """ 获取资源文件的绝对路径 """
    if getattr(sys,'frozen',False):
        # 如果程序被pyinstaller打包成了exe文件，sys.frozen将为True
        application_path = sys._MEIPASS
    else:
        # 如果程序在python解释器中运行，使用脚本文件的当前工作目录
        application_path = os.path.dirname(os.path.abspath(__file__))

    # 根绝相对路径返回资源文件的绝对路径
    return os.path.join(application_path,relative_path)