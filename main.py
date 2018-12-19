#Main file for the Pixel Brawl game

import pygame as pgm
import random
from settings import *
from sprites import *


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
		global projectiles_list
		#starts a new game
		#making sprites groups
		self.all_sprites = pgm.sprite.Group()
		self.platforms = pgm.sprite.Group()
		self.projectiles = pgm.sprite.Group()
		self.explosives = pgm.sprite.Group()
		self.weapons = pgm.sprite.Group()
		self.players = pgm.sprite.Group()
		self.destructibles = pgm.sprite.Group()
		self.non_crossable = pgm.sprite.Group()
		#creating sprites
		self.player_1 = Player(PLAYER_PROFILE_1)
		self.p1 = Platform(0, HEIGHT-10, WIDTH, 10)
		self.p2 = Platform(30, 0, 10, HEIGHT - 10)
		self.p3 = Platform(WIDTH-10, 0, 10, HEIGHT - 10)
		self.p4 = Platform(WIDTH/2 -25, HEIGHT-100, 100, 10)
		self.test_wpn = Firearm(WIDTH/2, HEIGHT -20, 20, 10)
		self.destr1 = Destructible(40, 0, 10 , HEIGHT)
		#adding sprites to groups
		self.all_sprites.add(self.player_1)
		self.all_sprites.add(self.p1)
		self.all_sprites.add(self.p2)
		self.all_sprites.add(self.p3)
		self.all_sprites.add(self.p4)
		self.all_sprites.add(self.test_wpn)
		self.all_sprites.add(self.destr1)
		self.players.add(self.player_1)
		self.platforms.add(self.p1)
		self.platforms.add(self.p2)
		self.platforms.add(self.p3)
		self.platforms.add(self.p4)
		self.non_crossable.add(self.p1)
		self.non_crossable.add(self.p2)
		self.non_crossable.add(self.p3)
		self.non_crossable.add(self.p4)
		self.non_crossable.add(self.destr1)
		self.weapons.add(self.test_wpn)
		self.destructibles.add(self.destr1)


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
		print("Running UPDATE\n", self.player_1.rect, self.player_1.vel)

		self.all_sprites.update()
		self.projectiles.update()

		for self.projectile in projectiles_list:
			self.projectiles.add(self.projectile)
		projectiles_list.clear()

		self.player_collisions = pgm.sprite.spritecollide(self.player_1, self.non_crossable, False)
		#migth need to change that code to groupcollide() to handle all the players
		self.item_collide = pgm.sprite.groupcollide(self.players, self.weapons, False, False)
		self.destructibles_collide = pgm.sprite.groupcollide(self.destructibles, self.projectiles, False, True)

		if self.player_collisions:
			#print("self.player_1 has collided with", self.player_collisions[0], self.player_1.rect, self.player_1.vel)
			for self.collision in self.player_collisions:
				#Handling of the down collision
				if self.player_1.rect.y + self.player_1.rect.height >= self.collision.rect.y and self.player_1.rect.y + self.player_1.rect.height < self.collision.rect.y + (self.collision.rect.height / 2):
					self.player_1.vel.y = 0
					self.player_1.pos.y = self.collision.rect.top - (self.player_1.rect.height/2)
					print("Down collision")

				#Handling of the up collision
				if (self.player_1.rect.y <= self.collision.rect.y + self.collision.rect.height and self.player_1.rect.y >= (self.collision.rect.y + self.collision.rect.height - 5)) and (self.player_1.rect.x + self.player_1.rect.width >= self.collision.rect.x and self.player_1.rect.x <= self.collision.rect.x + self.collision.rect.width):
					self.player_1.vel.y = 0.5
					self.player_1.pos.y = self.collision.rect.bottom + (self.player_1.rect.height /2) + 1
					print("Up collision")

				#Handling of the left collision
				if (self.player_1.rect.x <= self.collision.rect.x + self.collision.rect.width and self.player_1.rect.x > self.collision.rect.x + (self.collision.rect.width -4.17)):
					self.player_1.vel.x = 0

					#self.player_1.vel.x = self.player_1.vel.x * -0.3
					self.player_1.pos.x = self.collision.rect.right + (self.player_1.rect.width /2)
					print("Left collision")

				#Handling of the right collision
				if (self.player_1.rect.x + self.player_1.rect.width >= self.collision.rect.x and self.player_1.rect.x + self.player_1.rect.width < self.collision.rect.x + 4.17) and (self.player_1.rect.y <= self.collision.rect.y + self.collision.rect.height and self.player_1.rect.y + self.player_1.rect.height >= self.collision.rect.y):
					self.player_1.vel.x = 0
					self.player_1.pos.x = self.collision.rect.left - (self.player_1.rect.width / 2)
					print("Right collision")


		if self.item_collide:
			print("\nItem collide: " ,self.item_collide)
			for self.player_on_item in self.item_collide.keys():
				self.player_on_item.pickup(self.item_collide)

		if self.destructibles_collide:
			print("Bullet collissions", self.destructibles_collide)


	def run(self):
		print("Game is RUNNING")
		frame_count = 0
		self.playing = True
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
		self.projectiles.draw(self.main_window)
		self.all_sprites.draw(self.main_window)
		pgm.display.flip()

	def show_start_screen(self):
		pass
	def show_gameover_screen(self):
		pass
	def load_map(self):
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
'''
