#Main file for the Pixel Brawl game

import pygame as pgm
import random
from settings import *
from sprites import *
from dev_map_1 import world as world

class Game:

	def __init__(self):
		#Inits pygame and the sound handler
		pgm.init()
		pgm.mixer.init()
		#Create window
		self.main_window = pgm.display.set_mode((WIDTH, HEIGHT))
		#Setting the name of the window
		pgm.display.set_caption(TITLE)
		#Clock
		self.clock = pgm.time.Clock()
		#Sprite group
		self.running = True
		print("Game has been initalised")

	def start(self):
		''' Starts a bew game by creating all Pygame Sprites and Sprites
		Groups '''
		global projectiles_list
		self.all_sprites_group = pgm.sprite.Group()
		self.platform_group = pgm.sprite.Group()
		self.projectile_group = pgm.sprite.Group()
		self.explosive_group = pgm.sprite.Group()
		self.weapon_group = pgm.sprite.Group()
		self.firearm_group = pgm.sprite.Group()
		self.meleeweapon_group = pgm.sprite.Group()
		self.player_group = pgm.sprite.Group()
		self.destructible_group = pgm.sprite.Group()
		self.non_crossable_group = pgm.sprite.Group()
		self.damageable_group = pgm.sprite.Group()
		
		#creating sprites
		for self.sprite_type in world.keys():
			self.sprite_number = 0
			for self.sprite in world[self.sprite_type]:
				self.sprite_generic_name = self.sprite_type.lower()

				self.sprite_args = world[self.sprite_generic_name.title()][self.sprite_number]
				self.current_sprite_full_name = str(self.sprite_generic_name+str(self.sprite_number))
				self.current_sprite_str = ""
				print(self.current_sprite_full_name, self.sprite)
				for self.arg in self.sprite_args:
					try:
						self.arg = int(self.arg)
						self.current_sprite_str = str(self.current_sprite_str + str(self.arg) + ",")

					except ValueError as e:
						print(e, " -> self.arg is a string")
						self.current_sprite_str = str(self.current_sprite_str + str('''"{}"'''.format(self.arg)) + ",")
					except TypeError as e:
						print(e, "-> self.arg is a list")
						self.current_sprite_str = str(self.current_sprite_str + str(self.arg)+ ",")

				self.current_sprite_str_len = len(self.current_sprite_str)
				self.current_sprite_str = self.current_sprite_str[:self.current_sprite_str_len-1]
				self.current_sprite = eval(self.sprite_type+"({})".format(self.current_sprite_str))
				self.__dict__[self.current_sprite_full_name] = self.current_sprite

				#adding sprite to groups
				self.all_sprites_group.add(self.current_sprite)
				self.sprite_generic_name_group = str(self.sprite_generic_name)
				eval("self."+self.sprite_generic_name_group+"_group"+".add(self.current_sprite)")
				self.sprite_number +=1
				print("{} dict is ->".format(self) ,self.__dict__)

		#adding subgroups to main groups
		self.weapon_group.add(self.firearm_group)
		self.weapon_group.add(self.meleeweapon_group)
		self.non_crossable_group.add(self.platform_group)
		self.non_crossable_group.add(self.destructible_group)
		self.damageable_group.add(self.destructible_group)
		self.damageable_group.add(self.player_group)
		self.damageable_group.add(self.explosive_group)

		print("Game has been STARTED")
		self.run()

	def events(self):
		print("Running EVENTS")
		for event in pgm.event.get():
			if event.type == pgm.QUIT:
				if self.playing:
					self.playing = False
				playing = False

	def update(self):
		print("Running UPDATE\n", self.player0.rect, self.player0.vel)

		#updating sprites
		self.player_group.update()
		self.projectile_group.update()


		for self.projectile in projectiles_list:
			self.projectile_group.add(self.projectile)
			print("Projectile Group: " ,self.projectile_group)
			print("Damageable Group: ", self.damageable_group)
		projectiles_list.clear()

		self.player_collisions = pgm.sprite.spritecollide(self.player0, self.non_crossable_group, False)
		#migth need to change that code to groupcollide() to handle all the players
		self.item_collide = pgm.sprite.groupcollide(self.player_group, self.weapon_group, False, False)
		self.damageable_collisions = pgm.sprite.groupcollide(self.damageable_group, self.projectile_group, False, False)

		if self.player_collisions:
			#print("self.player0 has collided with", self.player_collisions[0], self.player0.rect, self.player0.vel)
			for self.collision in self.player_collisions:
				#Handling of the down collision
				if self.player0.rect.y + self.player0.rect.height >= self.collision.rect.y and self.player0.rect.y + self.player0.rect.height < self.collision.rect.y + (self.collision.rect.height / 2):
					self.player0.vel.y = 0
					self.player0.pos.y = self.collision.rect.top - (self.player0.rect.height/2)
					print("Down collision")

				#Handling of the up collision
				if (self.player0.rect.y <= self.collision.rect.y + self.collision.rect.height and self.player0.rect.y >= (self.collision.rect.y + self.collision.rect.height - 5)) and (self.player0.rect.x + self.player0.rect.width >= self.collision.rect.x and self.player0.rect.x <= self.collision.rect.x + self.collision.rect.width):
					self.player0.vel.y = 0.5
					self.player0.pos.y = self.collision.rect.bottom + (self.player0.rect.height /2) + 1
					print("Up collision")

				#Handling of the left collision
				if (self.player0.rect.x <= self.collision.rect.x + self.collision.rect.width and self.player0.rect.x > self.collision.rect.x + (self.collision.rect.width -4.17)):
					self.player0.vel.x = 0

					#self.player0.vel.x = self.player0.vel.x * -0.3
					self.player0.pos.x = self.collision.rect.right + (self.player0.rect.width /2)
					print("Left collision")
   
				#Handling of the right collision
				if (self.player0.rect.x + self.player0.rect.width >= self.collision.rect.x and self.player0.rect.x + self.player0.rect.width < self.collision.rect.x + 4.17) and (self.player0.rect.y <= self.collision.rect.y + self.collision.rect.height and self.player0.rect.y + self.player0.rect.height >= self.collision.rect.y):
					self.player0.vel.x = 0
					self.player0.pos.x = self.collision.rect.left - (self.player0.rect.width / 2)
					print("Right collision")

		#item pickup
		if self.item_collide:
			print("\nItem collide: " ,self.item_collide)
			for self.player_on_item in self.item_collide.keys():
				self.player_on_item.pickup(self.item_collide)

		#damage handler
		if self.damageable_collisions:
			print("Bullet collissions", self.damageable_collisions)
			for self.dmg_collision in self.damageable_collisions.keys():
				self.dmg_to_deal = 0
				print("DMG", self.dmg_collision)
				for self.hitting_projectile in self.damageable_collisions[self.dmg_collision]:
					self.dmg_to_deal += self.hitting_projectile.damage
					self.hitting_projectile.kill()

				print("Sprite will be dealt {} damage points".format(self.dmg_to_deal))
				self.dmg_collision.damage(self.dmg_to_deal)



	def run(self):
		print("Game is RUNNING")
		frame_count = 0
		self.playing = True
		self.show_start_screen()
		while self.playing:
			frame_count += 1
			print("\nFrame", frame_count)
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.render()
		self.show_gameover_screen()

	def render(self):
		print("Running RENDER")
		self.main_window.fill(BLACK)
		self.projectile_group.draw(self.main_window)
		self.all_sprites_group.draw(self.main_window)
		pgm.display.flip()

	def show_start_screen(self):
		pass
	def show_gameover_screen(self):
		pass

g = Game()
g.start()



'''NOTE:
the left and right collision checkers aren't perfect.
They are set to detect a collision even if you're 4.17 pixels inside a
platform (= on a platform). The number was set to 4.17 pixels because
it's > to the x velocity of players, making the player unable to get
into the sprite too much.
Same thing for the up collision but with a different value because of 
the jump speed being much higher.

The Player Sprite section of the maps now directly contains the key
bindings instead of the PLAYER_PROFILE_n string.
'''
