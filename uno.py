#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

import pygame
import sys

from sprites import *
from const import *


class Game:
	def __init__(self):	
		pygame.init()

		self.screen = pygame.display.set_mode((TILEWIDTH * TILESIZE, TILEHEIGHT * TILESIZE))
		self.clock = pygame.time.Clock()
		pygame.display.flip()

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()

	def quit(self):
		pygame.quit()
		sys.exit()

	def setup(self):
		self.player = Player(self, 1, 3)

	def run(self):
		while True:
			self.dt = self.clock.tick(FPS) / 1000
			self.check_events()
			self.update()
			self.draw()

	def update(self):
		self.player.update()

	def draw(self):
		self.screen.fill((255, 255, 255))
		self.player.draw()
		pygame.display.flip()


if __name__ == '__main__':
	g = Game()
	g.setup()
	g.run()