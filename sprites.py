import pygame

from const import *


class Wall(pygame.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self.groups = game.walls
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.rect = pygame.Rect(x, y, w, h)
		self.x = x / TILESIZE
		self.y = y / TILESIZE

	def update(self):
		pass

	def draw(self):
		pass


class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.allsprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pygame.image.load('player.png')
		self.rect = self.image.get_rect(topleft=(x, y))
		self.x = x / TILESIZE
		self.y = y / TILESIZE

		# Movement
		self.dx = 0
		self.dy = 0
		self.speed = 300
		self.to_next_tile = 0

	def move(self):
		if not (self.dx or self.dy):
			return

		if not self.is_walkable(self.dx, self.dy):
			self.dx = 0
			self.dy = 0
			self.to_next_tile = 0
			return	

		step_x = round(self.dx * self.speed * self.game.dt)
		step_y = round(self.dy * self.speed * self.game.dt)
		
		# Ensure the step is at least one pixel
		if self.dx and not step_x:
			step_x = self.dx
		if self.dy and not step_y:
			step_y = self.dy

		self.rect.x += step_x
		self.rect.y += step_y
		self.to_next_tile -= abs(step_x + step_y)

		# Stop moving
		if self.to_next_tile <= 0:
			self.rect.x += self.to_next_tile * self.dx
			self.rect.y += self.to_next_tile * self.dy
			self.dx = 0
			self.dy = 0
			self.to_next_tile = 0

			self.x = self.rect.x / TILESIZE
			self.y = self.rect.y / TILESIZE

	# def is_walkable(self, dx, dy):
	# 	target_x = self.x + dx
	# 	target_y = self.y + dy
	# 	for wall in self.game.walls:
	# 		if wall.x == target_x and wall.y == target_y:
	# 			return False
	# 	return True

	def is_walkable(self, dx, dy):
		target_x = self.x + dx
		target_y = self.y + dy
		target_rect = pygame.Rect(target_x * TILESIZE, target_y * TILESIZE, TILESIZE, TILESIZE)
		for wall in self.game.walls:
			if pygame.Rect.colliderect(target_rect, wall.rect):
				return False
		return True

	def get_movement_input(self):
		if self.to_next_tile:
			return

		key = pygame.key.get_pressed()

		if key[pygame.K_w]:
			self.dx = 0
			self.dy = -1
			self.to_next_tile = TILESIZE
		if key[pygame.K_a]:
			self.dx = -1
			self.dy = 0
			self.to_next_tile = TILESIZE
		if key[pygame.K_s]:
			self.dx = 0
			self.dy = 1
			self.to_next_tile = TILESIZE
		if key[pygame.K_d]:
			self.dx = 1
			self.dy = 0
			self.to_next_tile = TILESIZE

	def update(self):
		self.get_movement_input()
		self.move()

	def draw(self):
		self.game.screen.blit(self.image, self.rect)










