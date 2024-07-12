import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """ 显示得分信息的类 """

    def __init__(self,ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用字体设置
        self.text_color = (220,20,60)
        self.font = pygame.font.SysFont(None,48)
        # 准备包含得分，最高得分和剩余飞船数的当前得分图像
        self.prep_score()
        self.prep_highest_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        ''' 将得分转换为一幅渲染的图像 '''
        rounded_score = round(self.stats.score,-1)
        score_str = f'score: {rounded_score:,}'
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.background_color)
        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_highest_score(self):
        """ 将最高分转化为渲染的图像 """
        highest_score  = round(self.stats.highest_score,-1)
        highest_score_str = f"your highest score:{highest_score:,}"
        self.highest_score_image = self.font.render(highest_score_str,True,self.text_color,self.settings.background_color)
        # 在屏幕顶部显示最高得分
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.screen_rect.top

    def check_highest_score(self):
        """ 检查是否诞生了新的最高得分 """
        if self.stats.score > self.stats.highest_score:
            self.stats.highest_score = self.stats.score
            self.prep_highest_score() 

    def prep_level(self):
        """ 将等级转换为渲染的图像 """
        level = self.stats.level
        level_str = f'level: {level}'
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.background_color)
        #等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 20
        
    def prep_ships(self):
        """ 显示还剩多少艘飞船 """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """ 在屏幕上显示得分，最高得分，等级和剩余飞船 """
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.highest_score_image,self.highest_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)