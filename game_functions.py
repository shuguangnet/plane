# 导入库
import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

# 导入设置
# 响应按键
def check_keydown_events(event,ai_settings,screen,ship,bullets):
   if event.key ==pygame.K_RIGHT:
      ship.moving_right=True
   elif event.key ==pygame.K_LEFT:
      ship.moving_left=True
   elif event.key ==pygame.K_SPACE:
       fire_bullet(ai_settings,screen,ship,bullets)
      # 创建一颗子弹，并将其加入到编组bullets中
   # 快捷结束键Q
   elif event.key==pygame.K_q:
      sys.exit()
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets)<ai_settings.bullets_allowed:
      #  for ship in ships.sprites():
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
# 响应松开
def check_keyup_events(event,ship):
   if event.key ==pygame.K_RIGHT:
      ship.moving_right=False
   elif event.key ==pygame.K_LEFT:
      ship.moving_left=False
# 响应按键和鼠标事件

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type==pygame.KEYDOWN:
           check_keydown_events(event,ai_settings,screen,ship,bullets)
           if event.key==pygame.K_RIGHT:
              ship.moving_right = True
           elif event.key==pygame.K_LEFT:
              ship.moving_left = True
            #   向右移动飞船
            #   ship.rect.centerx+=1
        elif event.type==pygame.KEYUP:
           if event.key==pygame.K_RIGHT:
              ship.moving_right = False
           elif event.key==pygame.K_LEFT:
              ship.moving_left = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
             mouse_x, mouse_y = pygame.mouse.get_pos()
             check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y) 
def check_play_button(ai_settings, screen, stats,sb,play_button,ship, aliens,bullets,mouse_x, mouse_y): 
   """在玩家单击Play按钮时开始新游戏"""
   button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
   if button_clicked and not stats.game_active:
   # if play_button.rect.collidepoint(mouse_x, mouse_y): 
      # 重置游戏设置
      ai_settings.initialize_dynamic_settings() 
      # 隐藏光标
      pygame.mouse.set_visible(False) 
      # 重置游戏统计信息
      stats.reset_stats()
      stats.game_active = True 
      # 重置记分牌图像
      sb.prep_score() 
      sb.prep_high_score() 
      sb.prep_level()
      sb.prep_ships()
     # 清空外星人列表和子弹列表
      aliens.empty() 
      bullets.empty() 
      # 创建一群新的外星人，并让飞船居中
      create_fleet(ai_settings, screen, ship, aliens) 
      ship.center_ship() 
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
  # 更新屏幕上的图像并更新到新屏幕上
  # 绘制背景
  screen.fill(ai_settings.bg_color)
    # 绘制飞船
    # 显示得分
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  ship.blitme()
 
  aliens.draw(screen)
  # 如果游戏处于非活动状态，就显示Play按钮
  sb.show_score()
  if not stats.game_active: 
     play_button.draw_button()
  sb.show_score()
  pygame.display.flip()
def update_bullets(ai_settings, screen,stats,sb, ship, aliens,bullets):
   bullets.update()
        # 删除已消失的子弹
   for bullet in bullets.copy():
      if bullet.rect.bottom<=0:
        bullets.remove(bullet)
   check_bullet_alien_collisions(ai_settings, screen, stats,sb,ship, aliens, bullets)
   # 检查是否有子弹击中了外星人
   # 如果是这样，就删除相应的子弹和外星人
def check_bullet_alien_collisions(ai_settings, screen, stats,sb,ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) 
    if collisions: 
      for aliens in collisions.values(): 
         stats.score += ai_settings.alien_points * len(aliens) 
         sb.prep_score() 
      check_high_score(stats, sb) 
    if len(aliens) == 0:
      # 删除现有的子弹，加快游戏节奏，并创建一群新的外星人
       bullets.empty() 
       ai_settings.increase_speed()
       # 提高等级
       stats.level += 1
       sb.prep_level()
       create_fleet(ai_settings, screen, ship, aliens) 

def get_number_aliens_x(ai_settings, alien_width):  
 # 计算一行可容纳多少个外星人
#  alien = Alien(ai_settings, screen)
#  alien_width = alien.rect.width
 available_space_x = ai_settings.screen_width - 2 * alien_width
 number_aliens_x = int(available_space_x / (2 * alien_width)) 
 return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height): 
 """计算屏幕可容纳多少行外星人"""
 available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height) 
 number_rows = int(available_space_y / (2 * alien_height)) 
 return number_rows
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
   """创建一个外星人并将其放在当前行""" 
   alien = Alien(ai_settings, screen) 
   alien_width = alien.rect.width
   alien.x = alien_width + 2 * alien_width * alien_number 
   alien.rect.x = alien.x 
   alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
   aliens.add(alien) 
 
def create_fleet(ai_settings, screen, ship, aliens): 
  """创建外星人群""" 
  # 创建一个外星人，并计算每行可容纳多少个外星人
#   alien = Alien(ai_settings, screen) 
  alien = Alien(ai_settings, screen) 
  alien_width = alien.rect.width 
  available_space_x = ai_settings.screen_width - 2 * alien_width 
  number_aliens_x = int(available_space_x / (2 * alien_width))
#   number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
  number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height) 
  # 创建外星人群
  for row_number in range(number_rows):
     for alien_number in range(number_aliens_x): 
        create_alien(ai_settings, screen, aliens, alien_number,row_number) 
 # 创建第一行外星人
#  for alien_number in range(number_aliens_x): 
#    create_alien(ai_settings, screen, aliens, alien_number) 
def check_fleet_edges(ai_settings,aliens): 
 """有外星人到达边缘时采取相应的措施""" 
 for alien in aliens.sprites(): 
  if alien.check_edges(): 
    change_fleet_direction(ai_settings, aliens) 
    break 
 
def change_fleet_direction(ai_settings, aliens): 
 """将整群外星人下移，并改变它们的方向""" 
 for alien in aliens.sprites():
    alien.rect.y += ai_settings.fleet_drop_speed 
 ai_settings.fleet_direction *= -1
 
# def update_aliens(ai_settings,ship,aliens): 
#   """ 
#   检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
#   """
#   check_fleet_edges(ai_settings,aliens)
#   aliens.update()
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets): 
  """响应被外星人撞到的飞船""" 
  if stats.ships_left > 0:
    # 将ships_left减1 
    stats.ships_left -= 1 
    # 更新记分牌
    sb.prep_ships()
    # 清空外星人列表和子弹列表
    aliens.empty() 
    bullets.empty() 
 
    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens) 
    ship.center_ship() 
 
 # 暂停
    sleep(0.5) 
  else: 
   stats.game_active = False 
   pygame.mouse.set_visible(True) 
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets): 
 """检查是否有外星人到达了屏幕底端""" 
 screen_rect = screen.get_rect() 
 for alien in aliens.sprites():
  if alien.rect.bottom >= screen_rect.bottom: 
   # 像飞船被撞到一样进行处理
   ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets) 
   break 
def update_aliens(ai_settings, screen,stats, sb, ship, aliens, bullets):
   # 检测外星人和飞船之间的碰撞
  check_fleet_edges(ai_settings, aliens)
  aliens.update() 
  if pygame.sprite.spritecollideany(ship,aliens):
   ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets) 
   # 检查是否有外星人到达屏幕底端
   check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
def check_high_score(stats, sb): 
   """检查是否诞生了新的最高得分""" 
   if stats.score > stats.high_score: 
      stats.high_score = stats.score 
      sb.prep_high_score() 