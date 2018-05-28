#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
import pytmx
from pytmx.util_pygame import load_pygame

from sprites import *
from const import *


class TiledMap:
	def __init__(self, filename):
		self.mapdata = load_pygame(filename, pixelalpha=True)
		self.width = self.mapdata.width * self.mapdata.tilewidth
		self.height = self.mapdata.height * self.mapdata.tileheight

	def render(self, surf):
		for layer in self.mapdata.visible_layers:
			if isinstance(layer, pytmx.TiledTileLayer):
				for(x, y, gid) in layer:
					tile = self.mapdata.get_tile_image_by_gid(gid)
					if tile:
						surf.blit(tile, (x * self.mapdata.tilewidth, y * self.mapdata.tileheight))

	def make_map(self):
		surf = pygame.Surface((self.width, self.height))
		self.render(surf)
		return surf


class Game:
	def __init__(self):	
		pygame.init()

		self.screen = pygame.display.set_mode((TILEWIDTH * TILESIZE, TILEHEIGHT * TILESIZE))
		self.clock = pygame.time.Clock()

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()

	def quit(self):
		pygame.quit()
		sys.exit()

	def make_sprites(self):
		for layer in self.tiledmap.mapdata.layers:
			if isinstance(layer, pytmx.TiledTileLayer):
				for(x, y, gid) in layer:
					tile = self.tiledmap.mapdata.get_tile_image_by_gid(gid)
					if tile:
						if layer.name == '4locked':
							Wall(self, x, y)
						if layer.name == 'p':
							Player(self, x, y)

	def setup(self):
		# Map
		self.tiledmap = TiledMap('map_test.tmx')
		self.map_image = self.tiledmap.make_map()
		self.map_rect = self.map_image.get_rect()

		# Sprite groups
		self.allsprites = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()

		self.make_sprites()

	def run(self):
		while True:
			self.dt = self.clock.tick(FPS) / 1000.0
			self.check_events()
			self.update()
			self.draw()

	def update(self):
		self.allsprites.update()

	def draw(self):
		self.screen.blit(self.map_image, self.map_rect)
		self.allsprites.draw(self.screen)
		pygame.display.flip()


if __name__ == '__main__':
	g = Game()
	g.setup()
	g.run()











