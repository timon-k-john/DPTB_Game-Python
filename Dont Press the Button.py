#Dont Touch the Button

import pygame
from pygame.locals import *
import time

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 500
screen_height = 500

chr_x = 220
chr_y = 335

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dont Press the Button')

screen.fill([0,0,0])

#define game variables
tile_size = 25
game_over = 0
main_menu = True
unlock = False
win = False

restart_img = pygame.image.load('images/restart_btn.png')
start_img = pygame.image.load('images/start_btn.png')
exit_img = pygame.image.load('images/exit_btn.png')
win_img = pygame.image.load('images/win.png')


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



class ex_Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        
        #mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over ex_button and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x,y)
        
    def update(self, game_over, unlock, win):
        dx = 0
        dy = 0

        if game_over == 0:
            #get keypress
            key = pygame.key.get_pressed()
            
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -11
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 3
            if key[pygame.K_RIGHT]:
                dx += 3

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
                
            dy += self.vel_y
                    
            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    
                    #check if below the ground ie jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

                    #check if above the ground ie falling
                    elif self.vel_y > 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check if button pressed
            if pygame.sprite.spritecollide(self, Button_gp, False):
                game_over = -1

            
            if pygame.sprite.spritecollide(self, key_gp, False):
                unlock = True

            if unlock == True:
                if pygame.sprite.spritecollide(self, door_gp, False):
                    win = True
                    #print("WINNER")
                
                

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        #draw player onto screen
        screen.blit(self.image, self.rect)

        #pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        return game_over, unlock, win

    def reset(self, x, y):
        img = pygame.image.load('images/pacman.png')
        self.image = pygame.transform.scale(img, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()        
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
        #unlock = False

        #return unlock


class World():
    def __init__(self, data):
        self.tile_list = []
        
        #load images
        floor = pygame.image.load('images/B_bg2.jpg')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(floor, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count*tile_size
                    img_rect.y = row_count*tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    bt = Button(col_count*tile_size, row_count*tile_size + 7)
                    Button_gp.add(bt)

                if tile == 3:
                    k = End_Key(col_count*tile_size, row_count*tile_size + 7)
                    key_gp.add(k)

                if tile == 4:
                    d = Door(col_count*tile_size, row_count*tile_size + 18)
                    door_gp.add(d)
                    
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255,255,255), tile[1], 2)

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/red-button2.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class End_Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/key.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/door.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 2, 1, 1, 1], 
[1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 0, 0, 0, 1, 1, 1, 0, 0, 1], 
[1, 0, 0, 0, 0, 1, 1, 0, 5, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 1, 1, 1, 1, 1], 
[1, 2, 0, 0, 0, 0, 1, 7, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1], 
[1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 0, 1, 1, 1], 
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1], 
[1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 7, 0, 7, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 6, 2, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


player = Player(50, screen_height - 100)

Button_gp = pygame.sprite.Group()

key_gp = pygame.sprite.Group()

door_gp = pygame.sprite.Group()

world = World(world_data)

restart_button = ex_Button(190,230, restart_img)
start_button = ex_Button(screen_width//2 - 150, 100, start_img)
exit_button = ex_Button(screen_width//2 - 130, screen_height// 2, exit_img)
win_button = ex_Button(210,0, win_img)

a = 0
#MAIN
run = True
while run:

    clock.tick(fps)
    screen.fill((255,60,60))

    if main_menu == True:
        if win == True:
            win_button.draw()
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
            unlock = False
            win = False
    else:
        world.draw()

        Button_gp.draw(screen)

        door_gp.draw(screen)

        if unlock == False:
            key_gp.draw(screen)
        
        game_over, unlock, win = player.update(game_over, unlock, win)

        if win == True:
            main_menu = True

        #player died
        if game_over == -1:
            if restart_button.draw():
                player.reset(50, screen_height - 100)
                game_over = 0
                win = False
                unlock = False
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
            
    


