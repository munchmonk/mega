import pygame

from const import *


class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pygame.image.load('player.png')
		self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))
		self.x = x
		self.y = y

	def move(self, dx, dy):
		self.x += dx * TILESIZE
		self.y += dy * TILESIZE

	def update(self):
		key = pygame.key.get_pressed()

		if key[pygame.K_w]:
			self.move(0, -1)

		self.rect.x = self.x * TILESIZE
		self.rect.y = self.y * TILESIZE

	def draw(self):
		self.game.screen.blit(self.image, self.rect)
