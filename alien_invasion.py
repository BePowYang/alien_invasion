import sys
import os
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """ 管理游戏资源和行为的类 """
    def __init__(self):
        """ 初始化游戏并创建游戏资源 """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.play_button = Button(self,'Play')
        self.scoreboard = Scoreboard(self)

        self._create_fleet()

        # 设置背景色
        self.background_color = self.settings.background_color

    def run_game(self):
        """ 开始游戏主循环 """
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            
    def _check_events(self):
        ''' 监视键盘和鼠标事件 '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)   
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self,event):
        """ 响应按键 """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_top = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
   
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False
    
    def _check_fleet_edges(self):
        """ 有外星人到达边缘时采取相应措施 """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction(alien.rect.x)
                break
    
    def _check_aliens_bottom(self):
        """ 检查是否有外星人到达屏幕底端 """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break
    
    def _check_play_button(self,mouse_pos):
        """ 在玩家单击Play按钮时开始新游戏 """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            self._start_game()

    
    def _start_game(self):
        if not self.stats.game_active:
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_bullet_alien_collision(self):
        """ 响应子弹和外星人的碰撞 """
        # 检查是否有子弹击中了外星人,如果是就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_highest_score()
        # 外星人被消灭完时，消除现有子弹并再创建一批新的外星人
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 提高等级
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _change_fleet_direction(self,alien_x):
        """ 将触碰到边缘的那一排外星人下移，并改变它们的方向 """
        for alien in self.aliens.sprites():
            if alien.rect.x == alien_x:
                alien.rect.y += self.settings.fleet_drop_speed
                alien.direction *= -1

    def _fire_bullet(self):
        """ 创建一颗子弹,并将其加入编组bullets中 """
        if len(self.bullets) <= self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ 更新子弹位置，并删除消失的子弹 """
        # 更新子弹位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查并响应子弹与外星人的碰撞
        self._check_bullet_alien_collision()
            
    def _update_aliens(self):
        """ 检查外星人的位置与碰撞 """
        # 检查是否有外星人位于屏幕边缘,并更新外星人群中外星人的位置
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        # 检查外星人到达屏幕底端
        self._check_aliens_bottom()

    def _ship_hit(self):      
        """ 响应飞船被外星人撞到 """
        if self.stats.ships_left > 0:
            # 将ships_left减1并更新剩余飞船数
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            # 清空余下的外星人和子弹
            self.bullets.empty()
            self.aliens.empty()
            # 创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5) 
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _create_fleet(self):
        """ 创建aliens群 """
        # 创建外星人类实例方便调用
        alien = Alien(self)
        # 计算可创建外星人的空间宽度和外星人的间距
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # 计算可创建外星人的行数和行之间的间距
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (8 * alien_height) -ship_height
        number_rows = available_space_y // (2 * alien_height)
        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        """ 创建一个外星人并将其放在当前行 """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _update_screen(self): 
        """ 更新屏幕上的图像，并切换到新屏幕 """
        self.screen.fill(self.settings.background_color)
        # 绘制飞船
        self.ship.blitme()
        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 绘制外星人
        self.aliens.draw(self.screen)
        # 绘制得分
        self.scoreboard.show_score()
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()