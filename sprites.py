#sprite classes of all the entities of Pixel Brawl

import pygame as pgm
from settings import *
import time as time
vec = pgm.math.Vector2

projectiles_list = []

class Player(pgm.sprite.Sprite):
	"""player's sprite class"""
	def __init__(self, profile):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.profile = profile
		self.rect.center = (WIDTH / 2, HEIGHT / 2)

		#creating vectors
		self.pos = vec(WIDTH/2, HEIGHT/2)
		self.acc = vec(0, 0)
		self.vel = vec(0, 0)
		self.can_jump = True
		self.hp = PLAYER_HP
		self.time_of_jump = time.time()
		self.has_wpn = False
		self.last_side = 1



	def update(self):
		self.acc = vec(0, 0.5)
		#self.vel = vec(0,0)

		#handling user input
		pressed_keys = pgm.key.get_pressed()
		#accelarating left
		if pressed_keys[eval("pgm."+self.profile[0])]:
			self.acc.x = - PLAYER_ACCELERATION
			self.last_side = -1
		#accelerating right
		if pressed_keys[eval("pgm."+self.profile[1])]:
			self.acc.x = PLAYER_ACCELERATION
			self.last_side = 1
		#jumping
		if not pressed_keys[eval("pgm."+self.profile[2])]:
			self.can_jump = False
			#dirty fix

		if pressed_keys[eval("pgm."+self.profile[2])]:
			if self.can_jump:
				self.time_of_jump = time.time()
				self.acc.y = - PLAYER_ACCELERATION * 2
				if self.vel.y <= -7:
					self.can_jump = False
			
			elif not self.can_jump and self.vel.y == 0:
					self.current_time = time.time()
					if self.current_time - self.time_of_jump >= JUMPING_COUNTDOWN:
						#print("\n",self.current_time - self.time_of_jump, "since last jump !")
						self.can_jump = True

		if self.has_wpn:
			#print("Player is updating pos of wpn")
			if self.last_side == 1:
				self.weapon.rect.x = self.rect.x + (self.rect.width/2)
				self.weapon.rect.y = self.rect.y + (self.rect.height/2)
			if self.last_side == -1:
				self.weapon.rect.x = self.rect.x + (self.rect.width/2) - self.weapon.rect.width
				self.weapon.rect.y = self.rect.y + (self.rect.height/2)


			if pressed_keys[eval("pgm."+self.profile[5])]:
				print("Player is shooting")
				self.shoot()

		#pickup item -> find a way to use the groups in the sprites section

		#applying friction
		self.acc += self.vel * PLAYER_FRICTION
		#movement
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		self.rect.center = self.pos

	def pickup(self, coll_dict):
		self.coll_dict = coll_dict
		pressed_keys = pgm.key.get_pressed()
		if pressed_keys[eval("pgm."+self.profile[3])]:
			self.has_wpn = True
			print("Picking up:    ", self.coll_dict)
			for self in self.coll_dict.keys():
				print(self)
				self.weapon = self.coll_dict[self][0]
				self.weapon.rect.x = self.rect.x + (self.rect.width/2)
				self.weapon.rect.y = self.rect.y + (self.rect.height/2)

	def shoot(self):
		print("Player is shooting")
		self.bullet = Projectile(self.weapon.rect.x + self.weapon.rect.width, self.weapon.rect.y + (self.weapon.rect.height/2), 5, 3, PROJECTILE_SPEED * self.last_side)
		projectiles_list.append(self.bullet)
		print(projectiles_list)



class Platform(pgm.sprite.Sprite):
	"""Platforms sprite function"""
	def __init__(self, x, y, w, h):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((w, h))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		#placing the platform
		self.rect.x = x
		self.rect.y = y

class Destructible(pgm.sprite.Sprite):
	"""class for the destructible sprites"""
	def __init__(self, x, y, w, h):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((w,h))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		#placing the destrictible
		self.rect.x = x
		self.rect.y = y
		#how much 
		self.hp = 50

	def damage(self, dmg_dealt):
		self.hp -= dmg_dealt

class Projectile(pgm.sprite.Sprite):
	"""class for the projectile sprite
	note: should you have a way and speed arg or only a speed with the
	right sign?"""
	def __init__(self, x, y, w, h, speed):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((w, h))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.speed = speed
		#placing the bullet on the beside the weapon
		self.rect.x = x
		self.rect.y = y
		#how much damage does the projectile deals
		self.damage = 5

	def update(self):
		self.rect.x += self.speed
		if self.rect.x > WIDTH or self.rect.x + self.rect.width < 0:
			self.kill

class Firearm(pgm.sprite.Sprite):
	"""class for firearms sprites"""
	def __init__(self, x, y, w, h):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((w, h))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y