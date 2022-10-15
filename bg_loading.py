import pygame

class Backgroud_Roll(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("photo/background.png").convert_alpha()
        self.rect1 = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect1.left,self.rect1.top = 0,(0 - self.rect1.height)
        self.rect2.left,self.rect2.top = 0,0
        self.speed = 5

    #移动边界判断
    def move(self):
        if self.rect1.top < self.height:
            self.rect1.top += self.speed
        else:
            self.rect1.top = 0 - self.rect1.height
        if self.rect2.top < self.height:
            self.rect2.top += self.speed
        else:
            self.rect2.top = 0 - self.rect2.height

class Loading(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.plane_image = pygame.image.load("photo/game_loading.png").convert_alpha()
        self.plane_rect = self.plane_image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.plane_rect.left,self.plane_rect.top = 0,self.height - 165
        self.speed = 4

    def move(self):
        self.plane_rect.left += self.speed



