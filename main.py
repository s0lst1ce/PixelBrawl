#Main file for the Pixel Brawl game
#Available under the GPL3 LISCENCE
#See https://www.github.com/NotaSmartDev/PixelBrawl/ for more information
#Art is from both Kenney (https://www.kenney.com) and myself :)
'''NOTE:
the left and right collision checkers aren't perfect.
They are set to detect a collision even if you're 4.17 pixels inside a
platform (= on a platform). The number was set to 4.17 pixels because
it's > to the maximum x velocity of players, making the player unable to get
into the sprite too much.
Now the same thing is true for the up collision but with a different value because of 
the jump speed being much higher.

Fix bug where you can stick the player head to a roof

Change Surface definitions which are given as args to automatic resolution
through sprite image dimensions -> work in progress

delete about 90% of the "self" which are utterly useless and degrading performance while adding complexity

rethink game_paused var, really useful ?
'''

import time
started_loading_time = time.time()
import pygame as pgm
import pygame.freetype as pgm_frtp
import random
import math
import os
from settings import *
from sprites import *
from dev_map_1 import world as world
from menus import start as startmenu
from menus import score as scoremenu
from menus import pause as pausemenu
from menus import loading as loadingmenu


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
		self.FIRST_TIME = pgm.time.get_ticks()
		#Sprite group
		self.running = True
		self.game_started = False
		self.game_paused = False
		print("[{}:{}]: Game has been initalised".format(0,0))
		self.make_groups()

	def get_current_time(self, sec_or_min):
		now_time = (pgm.time.get_ticks() - self.FIRST_TIME) /1000
		print(now_time)
		now_time_min = math.floor(now_time / 60) 
		now_time_sec = math.floor(now_time % 60)
		if sec_or_min == 0:
			return now_time_min
		else:
			return now_time_sec

	def screen_loader(self, data_dict):
		print("\nLOADING SCREEN {}\n\n".format(data_dict))
		for self.sprite_type in data_dict.keys():
			self.sprite_number = 0
			for self.sprite in data_dict[self.sprite_type]:
				self.sprite_generic_name = self.sprite_type.lower()

				self.sprite_args = data_dict[self.sprite_type][self.sprite_number]
				self.current_sprite_full_name = str(self.sprite_generic_name+str(self.sprite_number))
				self.current_sprite_str = ""
				#print(self.current_sprite_full_name, self.sprite)
				for self.arg in self.sprite_args:
					try:
						self.arg = math.floor(int(self.arg))
						self.current_sprite_str = str(self.current_sprite_str + str(self.arg) + ",")

					except ValueError as e:
						if self.arg[0] == "#":
							#print("{} -> self.arg is a Keyword argument".format(e))
							self.current_sprite_str = str(self.current_sprite_str + str("{},".format(self.arg.replace("#", ""))))
							#print(self.current_sprite_str)
						else:
							#print(e, " -> self.arg is a String")
							self.current_sprite_str = str(self.current_sprite_str + str('''"{}"'''.format(self.arg)) + ",")
							self.current_sprite_str.replace("#", "")
							#print(self.current_sprite_str)

				self.current_sprite_str_len = len(self.current_sprite_str)
				self.current_sprite_str = self.current_sprite_str[:self.current_sprite_str_len-1]
				#print("Current sprite string is {}".format(self.current_sprite_str))
				self.current_sprite = eval(self.sprite_type+"""({})""".format(self.current_sprite_str))
				self.__dict__[self.current_sprite_full_name] = self.current_sprite

				#adding sprite to groups
				#print(self.current_sprite)
				self.all_sprites_group.add(self.current_sprite)
				self.sprite_generic_name_group = str(self.sprite_generic_name)
				eval("self."+self.sprite_generic_name_group+"_group"+".add(self.current_sprite)")
				self.sprite_number +=1
				#print("{} dict is ->".format(self) ,self.__dict__)
		#adding subgroups to main groups
		self.refresh_groups()
		   
	def make_groups(self):
		self.all_sprites_group		= pgm.sprite.Group()
		self.platform_group 		= pgm.sprite.Group()
		self.projectile_group 		= pgm.sprite.Group()
		self.explosive_group 		= pgm.sprite.Group()
		self.weapon_group 			= pgm.sprite.Group()
		self.firearm_group 			= pgm.sprite.Group()
		self.meleeweapon_group 		= pgm.sprite.Group()
		self.player_group 			= pgm.sprite.Group()
		self.destructible_group 	= pgm.sprite.Group()
		self.non_crossable_group 	= pgm.sprite.Group()
		self.damageable_group 		= pgm.sprite.Group()
		self.gravityboud_group 		= pgm.sprite.Group()
		self.throwable_group 		= pgm.sprite.Group()
		self.item_group 			= pgm.sprite.Group()
		self.gui_group 				= pgm.sprite.Group()
		self.textsurface_group 		= pgm.sprite.Group()
		self.textbutton_group 		= pgm.sprite.Group()
		self.imagebutton_group 		= pgm.sprite.Group()
		self.button_group 			= pgm.sprite.Group()
		self.inputfield_group 		= pgm.sprite.Group()

	def refresh_groups(self):
		print("REFRESHING GROUPS")
		#adding subgroups to main groups
		self.weapon_group.add(self.firearm_group, self.meleeweapon_group, self.throwable_group)
		self.item_group.add(self.weapon_group)
		self.non_crossable_group.add(self.destructible_group, self.platform_group, self.explosive_group)
		self.damageable_group.add(self.destructible_group, self.explosive_group, self.player_group)
		self.gravityboud_group.add(self.player_group, self.item_group)
		self.button_group.add(self.textbutton_group, self.imagebutton_group)
		self.gui_group.add(self.textsurface_group, self.button_group, self.inputfield_group)
		self.all_sprites_group.add(self.item_group, self.non_crossable_group, self.damageable_group, self.gravityboud_group, self.gui_group, self.projectile_group)
		print(self.gui_group)

	def start(self):
		''' Starts a bew game by creating all Pygame Sprites and Sprites
		Groups
		'''
		global projectiles_list
		#creating sprites
		self.screen_loader(world)
		#displaying new state
		print("[{}:{}] Game has been STARTED".format(self.get_current_time(0), self.get_current_time(1)))
		self.run()

	def events(self):
		print("[{}:{}] Running EVENTS\n".format(self.get_current_time(0), self.get_current_time(1)))
		for event in pgm.event.get():
			#print("Processing {} event of {} type".format(event, event.type))
			if event.type == pgm.QUIT:
				if self.playing:
					self.playing = False
				playing = False

			if event.type == pgm.KEYDOWN:
				for inputfield in self.inputfield_group: inputfield.update(key=event.unicode) #maybe add focused here ?

			pressed_keys = pgm.key.get_pressed()
			if (pressed_keys[eval("pgm.K_ESCAPE")] or pressed_keys[eval("pgm.K_{}".format(PAUSE_KEY))]) and self.game_started:
				if self.game_paused: self.resume_game()
				else: self.show_pause_screen()



		if len(self.player_group) == 1: #what if both player die at the same time ?
			self.show_score_screen()

	def update(self):
		self.gui_update()
		if self.game_started and not self.game_paused:
			self.game_update()

	def gui_update(self):
		self.gui_group.update()
		print("Text surfaces are {}".format(self.textsurface_group))
		for self.crt_button in iter(self.button_group):
			if self.crt_button.acting:
				print("Executing {} from {} button".format(self.crt_button.action, self.crt_button))
				self.button_runner(self.crt_button.action)

	def game_update(self):
		print("Running UPDATE\n")

		#updating sprites
		self.player_group.update()
		self.explosive_group.update()
		self.projectile_group.update()
		self.gui_group.update()

		for self.projectile in projectiles_list:
			self.projectile_group.add(self.projectile)
		projectiles_list.clear()

		self.player_collisions = pgm.sprite.groupcollide(self.player_group, self.non_crossable_group, False, False)
		#migth need to change that code to groupcollide() to handle all the players
		self.item_collide = pgm.sprite.groupcollide(self.player_group, self.weapon_group, False, False)
		self.damageable_collisions = pgm.sprite.groupcollide(self.damageable_group, self.projectile_group, False, False)
		self.pjt_non_crossable_coll = pgm.sprite.groupcollide(self.projectile_group, self.non_crossable_group, True, False)

		if self.player_collisions:
			print("Player collisions dict is: {}".format(self.player_collisions))
			for self.player in self.player_collisions.keys():
				print("{} ({};{}), with a velocity of: {} has collided with {}".format(self.player, self.player.rect.x, self.player.rect.y, self.player.vel, self.player_collisions[self.player]))
				for self.collision in self.player_collisions[self.player]:
					#Handling of the down collision
					if self.player.rect.y + self.player.rect.height >= self.collision.rect.y and self.player.rect.y + self.player.rect.height < self.collision.rect.y + (self.collision.rect.height / 2):
						self.player.vel.y = 0
						self.player.pos.y = self.collision.rect.top - (self.player.rect.height/2)
						print("Down collision")

					#Handling of the up collision
					if (self.player.rect.y <= self.collision.rect.y + self.collision.rect.height and self.player.rect.y >= (self.collision.rect.y + self.collision.rect.height - 5)) and (self.player.rect.x + self.player.rect.width >= self.collision.rect.x and self.player.rect.x <= self.collision.rect.x + self.collision.rect.width):
						self.player.vel.y = 0.5
						self.player.pos.y = self.collision.rect.bottom + (self.player.rect.height /2) + 1
						print("Up collision")

					#Handling of the left collision
					if (self.player.rect.x <= self.collision.rect.x + self.collision.rect.width and self.player.rect.x > self.collision.rect.x + (self.collision.rect.width -4.17)):
						self.player.vel.x = 0

						#self.player.vel.x = self.player.vel.x * -0.3
						self.player.pos.x = self.collision.rect.right + (self.player.rect.width /2)
						print("Left collision")
   
					#Handling of the right collision
					if (self.player.rect.x + self.player.rect.width >= self.collision.rect.x and self.player.rect.x + self.player.rect.width < self.collision.rect.x + 4.17) and (self.player.rect.y <= self.collision.rect.y + self.collision.rect.height and self.player.rect.y + self.player.rect.height >= self.collision.rect.y):
						self.player.vel.x = 0
						self.player.pos.x = self.collision.rect.left - (self.player.rect.width / 2)
						print("Right collision")

		#item pickup
		if self.item_collide:
			#print("\nItem collide: " ,self.item_collide)
			for self.player_on_item in self.item_collide.keys():
				if self.player_on_item.weapon != self.item_collide[self.player_on_item][0]:
					self.player_on_item.pickup(self.item_collide)

		#damage handler
		if self.damageable_collisions:
			#print("Bullet collissions", self.damageable_collisions)
			for self.dmg_collision in self.damageable_collisions.keys():
				self.dmg_to_deal = 0
				print("DMG", self.dmg_collision)
				for self.hitting_projectile in self.damageable_collisions[self.dmg_collision]:
					print("The projectile {} hit {} at a speed of {}".format(self.hitting_projectile,self.dmg_collision ,self.hitting_projectile.speed))
					self.dmg_to_deal += self.hitting_projectile.damage
					self.hitting_projectile.kill()

				print("Sprite will be dealt {} damage points".format(self.dmg_collision,self.dmg_to_deal))
				self.dmg_collision.damage(self.dmg_to_deal)

		#handling explosions
		



	def run(self):
		print("Game took {} seconds to load".format(time.time() - started_loading_time))
		print("Game is RUNNING")
		frame_count = 0
		self.playing = True
		self.show_start_screen()
		while self.playing:
			frame_count += 1
			print("\n\nFRAME", frame_count, "\n")
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.render()
		self.show_score_screen()

	def render(self):
		print("Running RENDER")
		self.main_window.fill(BACKGROUND)
		if not self.game_paused:
			self.projectile_group.draw(self.main_window)
			self.non_crossable_group.draw(self.main_window)
			self.player_group.draw(self.main_window)
			self.weapon_group.draw(self.main_window)
			self.projectile_group.draw(self.main_window)
		self.gui_group.draw(self.main_window)
		#self.gui_group.draw(self.main_window)
		pgm.display.flip()

	def stop_game(self):
		self.running = False
	def starting(self):
		self.start()

	def show_start_screen(self):
		print("\n\n--DISPLAYING START MENU--\n\n")
		global BACKGROUND
		if self.all_sprites_group:
			for sprite in iter(self.all_sprites_group): sprite.kill()
		BACKGROUND = WHITE
		self.screen_loader(startmenu)
		self.render()

	def button_runner(self, action=None):
		if action==None:
			return None
		eval("self."+action+"()")

	def stop_game(self):
		self.playing = False
	def start_game(self):
		global BACKGROUND
		self.game_started = True
		for gui_element in iter(self.gui_group): gui_element.kill()
		BACKGROUND = BLACK
		self.screen_loader(world)


	def show_score_screen(self):
		global BACKGROUND
		self.game_started = False
		for sprite in iter(self.all_sprites_group): sprite.kill()
		BACKGROUND = WHITE
		self.main_window.fill(BACKGROUND)
		self.screen_loader(scoremenu)

	def show_loading_screen(self):
		'''a screen which, I hope will never be needed for this game.
		Still I've laways wished to make up my own loading screen ^^'''
		global BACKGROUND
		BACKGROUND = BLACK
		self.show_loading_screen(loadingmenu)

	def show_settings_screen(self):
		pass
	def show_pause_screen(self):
		global BACKGROUND
		self.game_paused = True
		BACKGROUND = WHITE
		self.screen_loader(pausemenu)

	def resume_game(self):
		'''meant to make the game sprites drawn and updated again.'''
		global BACKGROUND
		BACKGROUND = BLACK
		for gui_element in iter(self.gui_group): gui_element.kill()
		self.game_paused = False


print("LOADING...")

g = Game()
print()

def passing(command):
	eval("g."+command)

if __name__ == '__main__':
	g.run()