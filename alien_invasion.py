import pygame
# 导入设置
from settings import Settings
from game_stats import GameStats 
from scoreboard import Scoreboard 
from button import Button 
# 导入飞船类
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
# 定义一个窗口函数
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    # 创建窗口大小
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    # 创建窗口名称)
    pygame.display.set_caption("P")
     # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例cls
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship=Ship(ai_settings,screen)
    # 创建一个用于存储子弹的编组
    bullets=Group()
     # 创建一个用于存储外星人的编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen,ship, aliens) 
     # 创建一个外星人
    # alien = Alien(ai_settings, screen) 
    # 开始游戏主循环
    while True:
      # 监视键盘和鼠标事件
      gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
    #   gf.check_events(ai_settings,screen,ship,bullets)
      if stats.game_active: 
       ship.update()
       gf.update_bullets(ai_settings, screen, stats,sb,ship, aliens,bullets)
      gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,bullets) 
    #   gf.update_screen(ai_settings, screen, ship, aliens, bullets)
      pygame.display.flip()
      gf.update_screen(ai_settings, screen, stats,sb, ship, aliens, bullets, play_button) 
run_game()
