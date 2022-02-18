import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from utils import * 
from random import choice

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        #define sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv')
            }

        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects'),
        }
        print(graphics['objects'])

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')

                        if style == 'grass':
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', choice(graphics['grass']))

                        if style == 'object':
                            obj_surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', obj_surf)


        self.player = Player((2000,1430), [self.visible_sprites], self.obstacle_sprites)



    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #setup
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width =  self.display_surface.get_size()[0]//2
        self.half_height =  self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surface = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))


    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        #Center the player in the middle of the cammera and move with
        #the player change of coordinates
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

