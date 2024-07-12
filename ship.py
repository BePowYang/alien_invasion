import pygame
import sys
import os
from pygame.sprite import Sprite

class Ship(Sprite):
    """ 管理飞船的类 """

    def __init__(self,ai_game):
        """ 初始化飞船并设置其初始位置 """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('alien_invasion\images\spaceship.bmp')
        self.rect = self.image.get_rect()
        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x中储存小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        """ 根据移动标志调整飞船的位置 """
        # 更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed    
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 更新飞船而不是rect对象的y值
        if self.moving_top and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # 根据self.x和y更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y
    
    def center_ship(self):
        """ 让飞船在屏幕底端居中 """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """ 在指定位置绘制飞船 """
        self.screen.blit(self.image,self.rect)

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
