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

    '''
        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'stone', 'variant':1, 'pos': (3 + i, 10)}

    '''
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0]) // self.tile_size, int(pos[1] // self.tile_size))

        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        file = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid':self.offgrid_tiles}, file)
        file.close

    def load(self, path):
        file = open(path, 'r')
        map_data = json.load(file)
        file.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size , tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surface, offset = (0,0)):
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

            
        
