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
        self.image = load_image('spaceship.bmp')
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

def load_image(filename):
    current_path = os.path.dirname(sys.argv[0])
    image_path = os.path.join(current_path,'images',filename)


    try:
        image = pygame.image.load(image_path)
    except pygame.error as e:
        print("加载图片时发生错误:", e)
        print("图片文件路径:", image_path)
        raise SystemExit
    return image

