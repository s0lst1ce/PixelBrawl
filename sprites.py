#sprite classes of all the entities of Pixel Brawl

import pygame as pgm
from settings import *
from weapons import weapons_firearms as wpn_frm
from weapons import weapons_melee as wpn_mle
from projectiles import projectile_type as pjt
from destructibles import destructibles_types as dstr
import time as time
vec = pgm.math.Vector2

projectiles_list = []

class Player(pgm.sprite.Sprite):
	"""player's sprite class"""
	def __init__(self, x, y, profile):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.profile = profile
		self.rect.center = (x, y)

		#creating vectors
		self.pos = vec(x, y)
		self.acc = vec(0, 0)
		self.vel = vec(0, 0)
		self.can_jump = True
		self.hp = PLAYER_HP
		self.time_of_jump = time.time()
		self.has_wpn = False
		self.last_side = 1
		self.last_time = 0
		self.started_to_reload = 0
		print("{} dict is ->".format(self) ,self.__dict__)



	def update(self):
		print("Player Sprite is updating last side is {}".format(self.last_side))
		self.acc = vec(0, 0.5)
		#self.vel = vec(0,0)

		#handling user input
		pressed_keys = pgm.key.get_pressed()
		#accelarating left
		if pressed_keys[eval("pgm."+self.profile[0])]:
			self.acc.x = - PLAYER_ACCELERATION
			self.last_side = -1
			print("Turning left -> Last side is {}".format(self.last_side))
		#accelerating right
		if pressed_keys[eval("pgm."+self.profile[1])]:
			self.acc.x = PLAYER_ACCELERATION
			self.last_side = 1
			print("Turning right -> Last side is {}".format(self.last_side))
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
		print("Player is shooting & last side is {} and player is at ({};{})".format(self.last_side, self.rect.x, self.rect.y))
		self.actual_time = pgm.time.get_ticks()
		self.fire_interval = FPS / self.weapon.fire_rate
		if self.weapon.magazine <= 0:
			self.started_to_reload = pgm.time.get_ticks()
			self.weapon.magazine = self.weapon.magazine_size
		if (self.actual_time - self.last_time) % self.fire_interval == 0 and self.actual_time - self.started_to_reload >= self.weapon.reload_time:
			print("Last side is {}".format(self.last_side))
			if self.last_side == 1:
				self.bullet = Projectile(self.weapon.rect.x + self.weapon.rect.width, self.weapon.rect.y + (self.weapon.rect.height/2), self.weapon.projectile_type, self.last_side)
			elif self.last_side == -1:
				self.bullet = Projectile(self.weapon.rect.x, self.weapon.rect.y + (self.weapon.rect.height/2), self.weapon.projectile_type, self.last_side)
			else:
				print("ERROR -> last side is {}".format(self.last_side))
			projectiles_list.append(self.bullet)
			self.weapon.magazine -= 1
			self.last_time = pgm.time.get_ticks()
			print("Player has shot")
	
	def damage(self, dmg_dealt):
		self.hp -= dmg_dealt
		if self.hp <= 0:
			self.death_animation()

	def death_animation(self):
		self.kill()


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
	def __init__(self, x, y, w, h, dstr_name):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((w,h))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		#placing the destrictible
		self.rect.x = x
		self.rect.y = y
		#how much 
		self.hp = dstr[dstr_name][0]

	def damage(self, dmg_dealt):
		self.hp -= dmg_dealt
		if self.hp <= 0:
			self.kill()

class Projectile(pgm.sprite.Sprite):
	"""class for the projectile sprite
	note: should you have a way and speed arg or only a speed with the
	right sign?"""
	def __init__(self, x, y, projectile_type, last_side):
		pgm.sprite.Sprite.__init__(self)
		


		self.image = pgm.Surface((pjt[projectile_type][0], pjt[projectile_type][1]))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.speed = pjt[projectile_type][2] * last_side
		print("Speed of the Projectile is of {} p/s".format(self.speed))
		#placing the bullet on the beside the weapon
		self.rect.x = x
		self.rect.y = y
		print("Bullet {} is at ({};{})".format(self, self.rect.x, self.rect.y))
		#how much damage does the projectile deals
		self.damage = pjt[projectile_type][3]

	def update(self):
		self.rect.x += self.speed
		if self.rect.x > WIDTH or self.rect.x + self.rect.width < 0:
			self.kill

class Firearm(pgm.sprite.Sprite):
	"""class for firearms sprites"""
	def __init__(self, x, y, wpn_name):
		pgm.sprite.Sprite.__init__(self)

		self.projectile_type = wpn_frm[wpn_name][2]
		self.fire_rate = wpn_frm[wpn_name][3]
		self.magazine_size = self.magazine = wpn_frm[wpn_name][4]
		self.reload_time = wpn_frm[wpn_name][5]

		self.image = pgm.Surface((wpn_frm[wpn_name][0], wpn_frm[wpn_name][1] ))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class MeleeWeapon(pgm.sprite.Sprite):
	"""Class for mellee weapons
	not yet ready to use -> not implemented
	also change the start() function to accept Sprite class with 2 caps"""
	def __init__(self, x, y, wpn_name):
		pgm.sprite.Sprite.__init__(self)
		
		self.wield_rate = wpn_mle[wpn_name][2]
		self.damage = wpn_mle[wpn_name][3]

		self.image = pgm.Surface((wpn_mle[wpn_name][0], wpn_mle[wpn_name][1]))
		self.image.fill(YELLOW)
		self.rect =self.image.get_rect()
		self.rect.x = x
		self.rect.y = y