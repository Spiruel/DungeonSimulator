from pygame.locals import *
import pygame
import sys
import spritesheet, dungeon
import numpy as np
 
class Player:
    def __init__(self, maze):
        self.x = 44
        self.y = 44
        self.speed = .25
        self.maze = maze
        self.counter = 0
        
    def move(self, dx, dy):
        self.x += self.speed*dx
        self.y += self.speed*dy
        # self.collision_detect()
        
    # def collision_detect(self):

        # print self.x, self.y
                    
class Maze:
    def __init__(self):

        self.block_size = 32
        self.walls = []
        cellsX, cellsY, cellsize = 6, 6, 7
        self.maze =  dungeon.generate(cellsX,cellsY,cellsize)
        self.M = cellsX*cellsize
        self.N = cellsY*cellsize
        # self.maze = [ 1,1,1,1,1,1,1,1,1,1,
                     # 1,0,0,0,0,0,0,0,0,1,
                     # 1,0,0,0,0,0,0,0,0,1,
                     # 1,0,1,1,1,1,1,1,0,1,
                     # 1,0,1,0,0,0,0,0,0,1,
                     # 1,0,1,0,1,1,1,1,0,1,
                     # 1,0,0,0,0,0,0,0,0,1,
                     # 1,1,1,1,1,1,1,1,1,1,]
        # print self.maze, len(self.maze)
 
    def draw(self,display_surf,image_surf):
        bx = 0
        by = 0
        for i in range(0,self.M*self.N):
            if self.maze[ bx + (by*self.M) ] == 1:
                block_pos = ( bx * self.block_size , by * self.block_size)
                self.walls.append(block_pos)
                
                if (bx + ((by+1)*self.M)) < len(self.maze):
                    if self.maze[ (bx + (by+1)*self.M) ] == 0:
                        display_surf.blit(image_surf[0][1],( bx * self.block_size , by * self.block_size))
                    else:
                        display_surf.blit(image_surf[0][0],( bx * self.block_size , by * self.block_size))
                else:
                    display_surf.blit(image_surf[0][0],( bx * self.block_size , by * self.block_size))
            else:
                # display_surf.blit(image_surf[1][np.random.randint(0,4)],( bx * self.block_size , by * self.block_size))
                display_surf.blit(image_surf[1][0],( bx * self.block_size , by * self.block_size))

            bx = bx + 1
            if bx > self.M-1:
                bx = 0 
                by = by + 1

class App:
    windowWidth = 1270
    windowHeight = 720
    player = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.maze = Maze()
        self.player = Player(self.maze)
        self.counter = 0
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Dungeon Simulator')
        self._running = True
        
        # pygame.mixer.music.load('assets/cave_theme.ogg')
        # pygame.mixer.music.play()
        pygame.mixer.music.load('assets/ambient_water_drip.ogg')
        pygame.mixer.music.play(loops=-1)
        
        self.no_ammo = pygame.mixer.Sound("assets/player_noammo.ogg")

        ss = spritesheet.spritesheet('assets/tiles_nooffset.png')
        self._block_surf = ss.images_at([(3*32, 6*32+8, 32, 32),(3*32, 7*32, 32, 32)], colorkey=(255,255,255))
        
        self._floor_surf = []
        # Load two images into an array, their transparent bit is (255, 255, 255)
        self._floor_surf = ss.images_at([(32*i, 0, 32, 32) for i in range(4)], colorkey=(255, 255, 255))
    
        self._image_surf = pygame.image.load('assets/sprite_player_0.png').convert()
        self._player_surf_down = ['assets/sprite_player_%i.png' %i for i in range(6)]
        
    def get_player_sprite(self, dir):
        if dir == 'down':
            return ['assets/sprite_player_%i.png' %i for i in range(6)]
        elif dir == 'left':
            return ['assets/sprite_player_%i.png' %i for i in range(12,12+6)]
        elif dir == 'up':
            return ['assets/sprite_player_%i.png' %i for i in range(24,24+6)]
        elif dir == 'right':
            return ['assets/sprite_player_%i.png' %i for i in range(36,36+6)]
        elif dir == 'downleft':
            return ['assets/sprite_player_%i.png' %i for i in range(6,6+6)]
        elif dir == 'downright':
            return ['assets/sprite_player_%i.png' %i for i in range(42,42+6)]
        elif dir == 'upleft':
            return ['assets/sprite_player_%i.png' %i for i in range(18,18+6)]
        elif dir == 'upright':
            return ['assets/sprite_player_%i.png' %i for i in range(30,30+6)]
            
    def on_event(self, event):
        for ev in event:
            if ev.type == QUIT:
                   self._running = False
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    self._running = False
 
    def on_loop(self):
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.maze.draw(self._display_surf, [self._block_surf, self._floor_surf])
        self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
        pygame.display.flip()
        self.on_event(pygame.event.get())
 
    def on_cleanup(self):
        pygame.quit()
        sys.exit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                if keys[K_UP]:
                    images = self.get_player_sprite('upleft')
                    self.player.move(-2, 0); self.player.move(0, -2)
                elif keys[K_DOWN]:
                    images = self.get_player_sprite('downleft')
                    self.player.move(-2, 0); self.player.move(0, 2)
                else:   
                    images = self.get_player_sprite('left')
                    self.player.move(-2, 0)
                self._image_surf = pygame.image.load(images[self.counter])
                self.counter = (self.counter + 1) % len(images)
            elif keys[K_RIGHT]:
                if keys[K_UP]:
                    images = self.get_player_sprite('upright')
                    self.player.move(2, 0); self.player.move(0, -2)
                elif keys[K_DOWN]:
                    images = self.get_player_sprite('downright')
                    self.player.move(2, 0); self.player.move(0, 2)
                else:   
                    images = self.get_player_sprite('right')
                    self.player.move(2, 0)
                self._image_surf = pygame.image.load(images[self.counter])
                self.counter = (self.counter + 1) % len(images)
            elif keys[K_UP]:
                images = self.get_player_sprite('up')
                self._image_surf = pygame.image.load(images[self.counter])
                self.counter = (self.counter + 1) % len(images)
                
                self.player.move(0, -2)
            elif keys[K_DOWN]:
                images = self.get_player_sprite('down') 
                self._image_surf = pygame.image.load(images[self.counter])
                self.counter = (self.counter + 1) % len(images)
                
                self.player.move(0, 2)
 
            if (keys[K_SPACE]):
                self.no_ammo.play()
                
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()  