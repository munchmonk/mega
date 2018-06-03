#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys
import pytmx
from pytmx.util_pygame import load_pygame

from sprites import *
from const import *


class Camera:
	def __init__(self,width, height):
		self.rect = pygame.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.rect.topleft)

	def apply_rect(self, rect):
		return rect.move(self.rect.topleft)

	def update(self, target):
		x = -target.rect.x + int(SCREENWIDTH / 2) - TILESIZE / 2
		y = -target.rect.y + int(SCREENHEIGHT / 2) - TILESIZE / 2

		x = min(0, x)
		y = min(0, y)
		x = max(x, -(self.width - SCREENWIDTH))
		y = max(y, -(self.height - SCREENHEIGHT))
		self.rect = pygame.Rect(x, y, self.width, self.height)


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

		self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
		self.clock = pygame.time.Clock()

	def check_quit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()

	def quit(self):
		pygame.quit()
		sys.exit()

	def make_sprites(self):
		for tile_object in self.tiledmap.mapdata.objects:
			if tile_object.name == 'wall':
				Wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
			if tile_object.name == 'player':
				self.player = Player(self, tile_object.x, tile_object.y)

	def setup(self):
		# Map
		self.tiledmap = TiledMap('map_test.tmx')
		self.map_image = self.tiledmap.make_map()
		self.map_rect = self.map_image.get_rect()

		# Camera
		self.camera = Camera(self.tiledmap.width, self.tiledmap.height)

		# Sprite groups
		self.allsprites = pygame.sprite.Group()
		self.player = None
		self.walls = pygame.sprite.Group()

		self.make_sprites()

	def run(self):
		while True:
			self.dt = self.clock.tick(FPS) / 1000.0
			self.check_quit()
			self.update()
			self.draw()

	def update(self):
		self.allsprites.update()
		self.camera.update(self.player)

	def draw(self):
		self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
		for sprite in self.allsprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		# self.allsprites.draw(self.screen)
		pygame.display.flip()


if __name__ == '__main__':
	g = Game()
	g.setup()
	g.run()











