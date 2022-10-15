import pygame
from pygame.locals import *
import sys
import traceback
from random import *
import bg_loading
import myplane
import enemy
import bullet
import supply

pygame.init()
pygame.mixer.init()

bg_size = width,height = 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战--CHB")
clock = pygame.time.Clock()

# 游戏是否开始
start = False

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

# 载入游戏音乐
pygame.mixer.music.load("music/game_music.ogg")
pygame.mixer.music.set_volume(0.7)
bullet_sound = pygame.mixer.Sound("music/bullet.wav")
bullet_sound.set_volume(0.7)
loading_sound = pygame.mixer.Sound("music/button.wav")
loading_sound.set_volume(0.4)
enemy1_down_sound = pygame.mixer.Sound("music/enemy1_down.wav")
enemy1_down_sound.set_volume(0.8)
enemy2_down_sound = pygame.mixer.Sound("music/enemy2_down.wav")
enemy2_down_sound.set_volume(0.8)
enemy3_down_sound = pygame.mixer.Sound("music/enemy3_down.wav")
enemy3_down_sound.set_volume(0.8)
me_down_sound = pygame.mixer.Sound("music/me_down.wav")
me_down_sound.set_volume(0.8)
enemy3_flying_sound = pygame.mixer.Sound("music/enemy3_flying.wav")
enemy3_flying_sound.set_volume(1)
get_bomb_sound = pygame.mixer.Sound("music/get_bomb.wav")
get_bomb_sound.set_volume(0.8)
get_bullet_sound = pygame.mixer.Sound("music/get_bullet.wav")
get_bullet_sound.set_volume(0.8)
use_bomb_sound = pygame.mixer.Sound("music/use_bomb.wav")
use_bomb_sound.set_volume(0.8)
supply_sound = pygame.mixer.Sound("music/supply.wav")
supply_sound.set_volume(1)
upgrade_sound = pygame.mixer.Sound("music/upgrade.wav")
upgrade_sound.set_volume(0.6)

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        e1.energy_fill = 1
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc

def inc_energy(target,inc):
    for each in target:
        each.energy_fill += 1


def main():
    global start

    pygame.mixer.music.play(-1)

    #背景
    background = bg_loading.Backgroud_Roll(bg_size)

    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    enemies = pygame.sprite.Group()

    # 生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)

    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 8
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 12
    for i in range(BULLET2_NUM // 3):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
        bullet2.append(bullet.Bullet1(me.rect.midtop))

    # 子弹存放
    bullets = []

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf",36)

    # 标志是否暂停游戏
    paused = False
    paused_nor_image = pygame.image.load("photo/pause_nor.png").convert_alpha()
    paused_pressed_image = pygame.image.load("photo/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("photo/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("photo/resume_pressed.png").convert_alpha()
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left,paused_rect.top = (width - paused_rect.width - 10),10
    paused_image = paused_nor_image

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.ttf",48)
    gameover_nor_image = pygame.image.load("photo/gameover_nor.png").convert_alpha()
    gameover_pressed_image = pygame.image.load("photo/gameover_pressed.png").convert_alpha()
    gameover_rect = gameover_nor_image.get_rect()
    gameover_image = gameover_nor_image
    again_nor_image = pygame.image.load("photo/again_nor.png").convert_alpha()
    again_pressed_image = pygame.image.load("photo/again_pressed.png").convert_alpha()
    again_rect = again_nor_image.get_rect()
    again_image = again_nor_image

    # 游戏初始界面
    start_nor_image = pygame.image.load("photo/start_nor.png").convert_alpha()
    start_pressed_image = pygame.image.load("photo/start_pressed.png").convert_alpha()
    start_rect = start_nor_image.get_rect()
    start_image = start_nor_image
    exit_nor_image = pygame.image.load("photo/exit_nor.png").convert_alpha()
    exit_pressed_image = pygame.image.load("photo/exit_pressed.png").convert_alpha()
    exit_rect = exit_nor_image.get_rect()
    exit_image = exit_nor_image
    regular_button_image = pygame.image.load("photo/regular_button.png").convert_alpha()
    regular_button_rect = regular_button_image.get_rect()
    back_button_image = pygame.image.load("photo/back_button.png").convert_alpha()
    back_button_rect = regular_button_image.get_rect()
    regular_image = pygame.image.load("photo/regular.png").convert_alpha()
    regular_rect = regular_image.get_rect()
    name_image = pygame.image.load("photo/name.png").convert_alpha()
    name_rect = name_image.get_rect()

    # 加载界面
    bg_loading_image = pygame.image.load("photo/bg_loading.png").convert_alpha()
    loading_sign = False
    loading = bg_loading.Loading(bg_size)

    # 设置难度级别
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load("photo/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf",48)
    bomb_num = 3

    # 每30秒发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)

    # 补给时间计时器
    SUPPLY_TIME = 30
    count_time = 0
    COUNT_TIME = USEREVENT
    pygame.time.set_timer(COUNT_TIME,1 * 1000)

    # 超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # 标志是否使用超级子弹
    is_double_bullet = False

    # 查看规则
    open_regular = False

    # 接触我方无敌状态定时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 生命数量
    life_image = pygame.image.load("photo/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 4

    # 用于阻止重复打开记录文件
    recorded = False

    # 用于切换图片
    switch_image = True

    # 用于延迟
    delay = 100
    BULLET_DELAY = 10
    bullet_delay = BULLET_DELAY

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN and start:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(COUNT_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                        paused_image = resume_pressed_image
                    else:
                        pygame.time.set_timer(COUNT_TIME, 1 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        paused_image = paused_pressed_image

            elif event.type == MOUSEMOTION:
                if start:
                    if paused_rect.collidepoint(event.pos):
                        if paused:
                            paused_image = resume_pressed_image
                        else:
                            paused_image = paused_pressed_image
                    else:
                        if paused:
                            paused_image = resume_nor_image
                        else:
                            paused_image = paused_nor_image
                    if life_num == 0:
                        if again_rect.collidepoint(event.pos):
                            again_image = again_pressed_image
                        else:
                            again_image = again_nor_image
                        if gameover_rect.collidepoint(event.pos):
                            gameover_image = gameover_pressed_image
                        else:
                            gameover_image = gameover_nor_image
                else:
                    if start_rect.collidepoint(event.pos):
                        start_image = start_pressed_image
                    else:
                        start_image = start_nor_image
                    if exit_rect.collidepoint(event.pos):
                        exit_image = exit_pressed_image
                    else:
                        exit_image = exit_nor_image

            elif event.type == KEYDOWN and start and life_num and not paused:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        use_bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == COUNT_TIME:
                count_time += 1

            # 发放补给包
            if count_time >= SUPPLY_TIME:
                supply_sound.play()
                count_time = 0
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME,0)

        # 根据用户的得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            # 增加3架小型敌机、2架中型敌机和1架大型敌机
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升敌机的速度
            inc_speed(small_enemies,1)
            # 增加我方飞机子弹速度
            BULLET_DELAY = 8
            bullet_delay = BULLET_DELAY
            BULLET1_NUM = 10
            for i in range(BULLET1_NUM):
                bullet1.append(bullet.Bullet1(me.rect.midtop))
            BULLET2_NUM = 15
            for i in range(BULLET2_NUM // 3):
                bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
                bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
                bullet2.append(bullet.Bullet1(me.rect.midtop))

        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升敌机的速度
            inc_speed(small_enemies, 1)
            # 增加我方飞机子弹速度
            BULLET_DELAY = 7
            bullet_delay = BULLET_DELAY
            BULLET1_NUM = 12
            for i in range(BULLET1_NUM):
                bullet1.append(bullet.Bullet1(me.rect.midtop))
            BULLET2_NUM = 18
            for i in range(BULLET2_NUM // 3):
                bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
                bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
                bullet2.append(bullet.Bullet1(me.rect.midtop))

        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies,1)
            # 增加我方飞机子弹速度
            BULLET_DELAY = 4
            bullet_delay = BULLET_DELAY
            BULLET1_NUM = 24
            for i in range(BULLET1_NUM):
                bullet1.append(bullet.Bullet1(me.rect.midtop))
            BULLET2_NUM = 36
            for i in range(BULLET2_NUM // 3):
                bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
                bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
                bullet2.append(bullet.Bullet1(me.rect.midtop))
            # 缩短补给包发放时间
            SUPPLY_TIME = 25

        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies,1)
            # 增加小型敌机血量
            inc_energy(small_enemies,1)
            # 增加我方飞机子弹速度
            BULLET_DELAY = 3
            bullet_delay = BULLET_DELAY
            BULLET1_NUM = 36
            for i in range(BULLET1_NUM):
                bullet1.append(bullet.Bullet1(me.rect.midtop))
            BULLET2_NUM = 54
            for i in range(BULLET2_NUM // 3):
                bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
                bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
                bullet2.append(bullet.Bullet1(me.rect.midtop))
            # 缩短补给包发放时间
            SUPPLY_TIME = 20

        # 背景动画
        if life_num and not paused and start:
            background.move()
        screen.blit(background.image,background.rect1)
        screen.blit(background.image,background.rect2)
        

        if life_num and not paused and start:
            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    bomb_num += 1
                    bomb_supply.active = False

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,18 * 1000)
                    bullet_supply.active = False

            # 发射子弹
            if not(bullet_delay % BULLET_DELAY):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx + 33, me.rect.centery))
                    bullets[bullet2_index + 2].reset(me.rect.midtop)
                    bullet2_index = (bullet2_index + 3) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False

            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),\
                                     (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),2)

                    # 即将出现在画面中，播放音效
                    if each.rect.bottom == -50:
                        enemy3_flying_sound.play(-1)
                else:
                    # 毁灭
                    if not (delay % 5):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_flying_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image,each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),\
                                     (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),2)
                else:
                    # 毁灭
                    if not (delay % 5):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not (delay % 5):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1,me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not (delay % 5):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME,3 * 1000)

            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render("× %d" % bomb_num,True,WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image,(10,height - 10 - bomb_rect.height))
            screen.blit(bomb_text,(20 + bomb_rect.width,height - 5 - text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num - 1):
                    screen.blit(life_image,(width-10-(i+1)*life_rect.width , height-10-life_rect.height))

        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()

            # 停止发放补给包
            pygame.time.set_timer(COUNT_TIME,0)

            if not recorded:
                recorded = True
                # 读取历史最高得分
                with open("record.txt","r") as f:
                    record_score = int(f.read())

                # 如果玩家得分高于历史最高得分，则存档
                if score > record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))

            record_score_text = score_font.render("Best : %d" % record_score,True,WHITE)
            screen.blit(record_score_text,(50,50))

            gameover_text1 = gameover_font.render("Your Score",True,WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left,gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2 , height // 2
            screen.blit(gameover_text1,gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score),True,WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left,gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2,\
                                                                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2,gameover_text2_rect)

            again_rect.left,again_rect.top = (width - again_rect.width) // 2 , gameover_text2_rect.bottom + 50
            screen.blit(again_image,again_rect)

            gameover_rect.left,gameover_rect.top = (width - gameover_rect.width) // 2 , again_rect.bottom + 10
            screen.blit(gameover_image,gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()

        # 绘制游戏初始界面
        if not start and not loading_sign:
            pygame.mixer.music.stop()
            pygame.time.set_timer(COUNT_TIME, 0)

            # 读取历史最高得分
            with open("record.txt","r") as f:
                record_score = int(f.read())

            record_score_text = score_font.render("Best : %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (50, 50))

            name_rect.left,name_rect.top = (width - name_rect.width) // 2, 150
            screen.blit(name_image,name_rect)

            start_rect.left, start_rect.top = (width - start_rect.width) // 2, height // 2 + 100
            screen.blit(start_image, start_rect)

            exit_rect.left, exit_rect.top = (width - exit_rect.width) // 2, start_rect.bottom + 20
            screen.blit(exit_image, exit_rect)

            regular_button_rect.left,regular_button_rect.top = width - regular_button_rect.width - 10,10
            screen.blit(regular_button_image,regular_button_rect)

            if open_regular:
                screen.blit(regular_image,(0,0))
                back_button_rect.left, back_button_rect.top = width - back_button_rect.width - 10, \
                                                                height - back_button_rect.height - 10
                screen.blit(back_button_image, back_button_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if open_regular:
                    if back_button_rect.left < pos[0] < back_button_rect.right and \
                            back_button_rect.top < pos[1] < back_button_rect.bottom:
                        open_regular = False
                else:
                    if regular_button_rect.left < pos[0] < regular_button_rect.right and \
                        regular_button_rect.top < pos[1] < regular_button_rect.bottom:
                        open_regular = True
                    if start_rect.left < pos[0] < start_rect.right and start_rect.top < pos[1] < start_rect.bottom:
                        loading_sign = True
                        loading_sound.play()
                    elif exit_rect.left < pos[0] < exit_rect.right and exit_rect.top < pos[1] < exit_rect.bottom:
                        pygame.quit()
                        sys.exit()

        # 绘制游戏加载界面
        if loading_sign:
            screen.blit(bg_loading_image,(0,0))
            loading.move()
            screen.blit(loading.plane_image,loading.plane_rect)
            if loading.plane_rect.left > width:
                start = True
                pygame.time.set_timer(COUNT_TIME, 1 * 1000)
                pygame.mixer.music.play(-1)
                loading_sign = False

        if life_num != 0 and start:
            # 绘制得分
            score_text = score_font.render("Score : %d" % score, True, WHITE)
            screen.blit(score_text, (10, 5))

            # 绘制暂停按钮
            screen.blit(paused_image,paused_rect)

            # 切换图片
            if not(delay % 5):
                switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        bullet_delay -= 1
        if not bullet_delay:
            bullet_delay = BULLET_DELAY

        pygame.display.flip()

        # 设置帧率
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()