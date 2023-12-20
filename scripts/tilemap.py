import pygame
import json

PHYSICS_TILES = {'grass', 'stone'}
NEIGHBOR_OFFSETS = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (0,0), (-1,1), (0,1), (1,1)]


class Tilemap:
    def __init__(self, game, tile_size = 16) -> None:
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'stone', 'variant':1, 'pos': (3 + i, 10)}

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0]) // self.tile_size, int(pos[1] // self.tile_size))

        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size , tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surface):
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0], tile['pos'][1]))

        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

            
        


'''
    
    def render(self,surface, offset = (0,0)):
        for tile in self.offgrid_tiles:
            #blitting this type of tile at a specific location
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            #print(tile)
            #blit each tile by type and variant, at a specfic position
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
            #print(self.game.assets[tile['type']][tile['variant']], ([tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size]) )
    
        

'''