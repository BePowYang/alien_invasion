class Settings:
    """ 储存游戏《Alien Invasion》中所有设置的类 """

    def __init__(self):
        """ 初始化游戏设置 """

        # 屏幕设置
        self.screen_width = 1100
        self.screen_height = 600
        self.background_color = (25,25,25)

        # 飞船设置
        self.ship_speed = 1.0

        # 子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,69,0)
        self.bullets_allowed = 3
