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
through sprite image dimensions

rethink game_paused var, really useful ?
clean up var namespace

maybe replace running by playing -> would make more sense
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
from menus import settings as settingsmenu

class Game:

	def __init__(self):
		#Inits pygame and the sound handler
		pgm.init()
		#uninit mixer in order to free an entire CPU core
		pgm.mixer.quit()
		#Create window
		self.main_window = pgm.display.set_mode((WIDTH, HEIGHT)) #removed pgm.RESIZABLE due to issues in scaling, see events()
		self.screen = pgm.Surface((WIDTH, HEIGHT))
		#Setting the name of the window
		pgm.display.set_caption(TITLE)
		#Clock
		self.clock = pgm.time.Clock()
		self.FIRST_TIME = pgm.time.get_ticks()
		#Sprite group
		self.running = True
		self.game_started = False
		self.game_paused = False
		self.on_settings_menu = False
		print("[{}:{}]: Game has been initalised".format(0,0))
		self.make_groups()

	def get_elapsed_time(self, sec_or_min):
		now_time = (pgm.time.get_ticks() - self.FIRST_TIME) /1000
		if sec_or_min == 0:
			return math.floor(now_time / 60)
		else:
			return math.floor(now_time % 60)

	def load_screen(self, data_dict):
		print("\nLOADING SCREEN {}\n\n".format(data_dict))
		for sprite_type in data_dict.keys():
			sprite_number = 0
			for sprite in data_dict[sprite_type]:
				sprite_generic_name = sprite_type.lower()

				current_sprite_str = ""
				for arg in data_dict[sprite_type][sprite_number]:
					try:
						arg = math.floor(int(arg))
						current_sprite_str = str(current_sprite_str + str(arg) + ",")

					except ValueError as e:
						if arg[0] == "#":
							current_sprite_str = str(current_sprite_str + str("{},".format(arg.replace("#", ""))))
						else:
							current_sprite_str = str(current_sprite_str + str('''"{}"'''.format(arg)) + ",")
							current_sprite_str.replace("#", "")

				current_sprite_str = current_sprite_str[:len(current_sprite_str)-1]
				current_sprite = eval(sprite_type+"""({})""".format(current_sprite_str))
				self.__dict__[str(sprite_generic_name+str(sprite_number))] = current_sprite

				self.all_sprites_group.add(current_sprite)
				eval("self."+str(sprite_generic_name)+"_group"+".add(current_sprite)")
				sprite_number +=1
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
		self.load_screen(world)
		#displaying new state
		print("[{}:{}] Game has been STARTED".format(self.get_elapsed_time(0), self.get_elapsed_time(1)))
		self.run()

	def events(self):
		print("[{}:{}] Running EVENTS\n".format(self.get_elapsed_time(0), self.get_elapsed_time(1)))
		for event in pgm.event.get():
			print("Processing {} event of {} type".format(event, event.type))
			if event.type == pgm.QUIT:
				if self.playing:
					self.playing = False
				playing = False

			if event.type == pgm.KEYDOWN:
				print("Currently displaying {} texts".format(self.textsurface_group))
				for inputfield in self.inputfield_group: inputfield.update(key=event.unicode)

			pressed_keys = pgm.key.get_pressed()
			if (pressed_keys[eval("pgm.K_ESCAPE")] or pressed_keys[eval("pgm.K_{}".format(PAUSE_KEY))]) and self.game_started:
				if self.game_paused: self.resume_game()
				else: self.show_pause_screen()

		if len(self.player_group) == 1: #what if both players die at the same time ? too improbable ?
			self.show_score_screen()

	def update(self):
		self.gui_update()
		if self.game_started and not self.game_paused:
			#self.fps_counter.chg_txt(str(int(self.clock.get_fps()))+"FPS")
			self.game_update()

	def gui_update(self):
		self.refresh_groups()
		self.gui_group.update()
		for crt_button in iter(self.button_group):
			if crt_button.acting:
				crt_button.acting = False
				self.button_runner(crt_button.action)

	def game_update(self):
		print("Running UPDATE\n")

		#updating sprites
		self.player_group.update()
		self.explosive_group.update()
		self.projectile_group.update()
		self.gui_group.update()

		for projectile in projectiles_list:
			self.projectile_group.add(projectile)
		projectiles_list.clear()

		player_collisions = pgm.sprite.groupcollide(self.player_group, self.non_crossable_group, False, False)
		item_collide = pgm.sprite.groupcollide(self.player_group, self.weapon_group, False, False)
		damageable_collisions = pgm.sprite.groupcollide(self.damageable_group, self.projectile_group, False, False)
		self.pjt_non_crossable_coll = pgm.sprite.groupcollide(self.projectile_group, self.non_crossable_group, True, False)

		if player_collisions:
			print("Player collisions dict is: {}".format(player_collisions))
			for player in player_collisions.keys():
				print("{} ({};{}), with a velocity of: {} has collided with {}".format(player, player.rect.x, player.rect.y, player.vel, player_collisions[player]))
				for collision in player_collisions[player]:
					#Handling of the down collision
					if player.rect.y + player.rect.height >= collision.rect.y and player.rect.y + player.rect.height < collision.rect.y + (collision.rect.height / 2):
						player.vel.y = 0
						player.pos.y = collision.rect.top - (player.rect.height/2)
						print("Down collision")

					#Handling of the up collision
					if (player.rect.y <= collision.rect.y + collision.rect.height and player.rect.y >= (collision.rect.y + collision.rect.height - 5)) and (player.rect.x + player.rect.width >= collision.rect.x and player.rect.x <= collision.rect.x + collision.rect.width):
						player.vel.y = 0.5
						player.pos.y = collision.rect.bottom + (player.rect.height /2) + 1
						print("Up collision")

					#Handling of the right collision
					if (player.rect.x <= collision.rect.x + collision.rect.width and player.rect.x > collision.rect.x + (collision.rect.width -4.17)):
						player.vel.x = 0

						player.pos.x = collision.rect.right + (player.rect.width /2)
						print("Right collision")
   
					#Handling of the left collision
					if (player.rect.x + player.rect.width >= collision.rect.x and player.rect.x + player.rect.width < collision.rect.x + 4.17) and (player.rect.y <= collision.rect.y + collision.rect.height and player.rect.y + player.rect.height >= collision.rect.y):
						player.vel.x = 0
						player.pos.x = collision.rect.left - (player.rect.width / 2)
						print("Left collision")

		#item pickup
		if item_collide:
			#print("\nItem collide: " ,item_collide)
			for player_on_item in item_collide.keys():
				if player_on_item.weapon != item_collide[player_on_item][0]:
					player_on_item.pickup(item_collide)

		#damage handler
		if damageable_collisions:
			#print("Bullet collissions", damageable_collisions)
			for dmg_collision in damageable_collisions.keys():
				dmg_to_deal = 0
				for hitting_projectile in damageable_collisions[dmg_collision]:
					dmg_to_deal += hitting_projectile.damage
					hitting_projectile.kill()
				dmg_collision.damage(dmg_to_deal)

		#handling explosions
		

	def run(self):
		print("Game is RUNNING")
		frame_count = 0
		self.playing = True
		self.show_start_screen()
		print("Game took {} seconds to load".format(time.time() - started_loading_time))
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
		self.screen.fill(BACKGROUND)
		if not self.game_paused:
			self.projectile_group.draw(self.screen)
			self.non_crossable_group.draw(self.screen)
			self.player_group.draw(self.screen)
			self.weapon_group.draw(self.screen)
			self.projectile_group.draw(self.screen)
		self.gui_group.draw(self.screen)
		self.main_window.blit(self.screen, (0,0))
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
		self.game_paused = False
		self.on_settings_menu = False
		BACKGROUND = WHITE
		self.load_screen(startmenu)
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
		self.load_screen(world)
		self.fps_counter = TextSurface(WIDTH-40, 0, str(int(self.clock.get_fps()))+"FPS")
		self.textsurface_group.add(self.fps_counter)

	def show_score_screen(self):
		global BACKGROUND
		self.game_started = False
		for sprite in iter(self.all_sprites_group): sprite.kill()
		BACKGROUND = WHITE
		self.main_window.fill(BACKGROUND)
		self.load_screen(scoremenu)

	def show_loading_screen(self):
		'''a s0creen which, I hope will never be needed for this game.
		Still I've always wished to make up my own loading screen ^^'''
		global BACKGROUND
		BACKGROUND = BLACK
		self.load_screen(loadingmenu)

	def show_pause_screen(self):
		global BACKGROUND
		#doesn't seems to prevent ser from invoking pause menu while in main menu...
		if self.game_started == False:return None
		self.game_paused = True
		BACKGROUND = WHITE
		self.load_screen(pausemenu)

	def resume_game(self):
		'''meant to make the game sprites drawn and updated again.'''
		global BACKGROUND
		BACKGROUND = BLACK
		for gui_element in iter(self.gui_group): gui_element.kill()
		self.game_paused = False

#settings screen handler functions

	def get_settings_file(self):
		with open("settings.py", "r") as file:
			settings_txt = file.readlines()
		return settings_txt




	def show_settings_screen(self):
		global BACKGROUND
		BACKGROUND = WHITE
		for sprite in iter(self.all_sprites_group): sprite.kill()
		self.on_settings_menu = True
		self.select_profile_1()
		self.load_screen(settingsmenu)


	def change_resolution(self):
		print("Calling change resolution")
		for field in iter(self.inputfield_group):
			if field.nbr == 0:
				w = int(field.crt_txt)
			elif field.nbr == 1:
				h = int(field.crt_txt)
		assert w and h, ("Either width or height isn't defined")
		assert w/16==h/9, "can't change resolution to a ratio different than 16:9"

		old_w = WIDTH
		old_h = HEIGHT
		ratio = h/576
		settings_txt = self.get_settings_file()

		mattering_lines = [None, None, None]
		i = 0
		for line in settings_txt:
			if line[:5] == "WIDTH":
				mattering_lines[0] = i
			elif line[:6] == "HEIGHT":
				mattering_lines[1] = i
			elif line[:9] == "FONT_SIZE":
				mattering_lines[2] = i
			i+=1

		for line in mattering_lines:
			assert line!=None, "One of the settings line couldn't be find"
		settings_txt[mattering_lines[0]] = "WIDTH = {}\n".format(w)
		settings_txt[mattering_lines[1]] = "HEIGHT = {}\n".format(h)
		#had to set 20 as hard coded value for the player can change the value in settings.py
		settings_txt[mattering_lines[2]] = "FONT_SIZE = {}\n".format(25*ratio)

		with open("./settings.py", "w") as file:
			for line in settings_txt:
				file.write(line)

		#quits the game as changes only occur after reboot
		self.playing = False


	def select_profile_1(self):
		self.selected_profile = 1
	def select_profile_2(self):
		self.selected_profile = 2
	def show_crt_keymap(self):
		pass

	def change_keymap(self):
		pass




print("LOADING...")

g = Game()
print()


if __name__ == '__main__':
	g.run()