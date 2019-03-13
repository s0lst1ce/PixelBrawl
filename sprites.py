#sprite classes of all the entities of Pixel Brawl

import pygame as pgm
import pygame.freetype as pgm_frtp
import math
import os
import time
from settings import *
from weapons import weapons_firearms as wpn_frm
from weapons import weapons_melee as wpn_mle
from weapons import explosives as expv
from projectiles import projectile_type as pjt
from destructibles import destructibles_types as dstr
import main as main
vec = pgm.math.Vector2

projectiles_list = []


class Player(pgm.sprite.Sprite):
	"""player's sprite class"""
	def __init__(self, x, y, profile):
		pgm.sprite.Sprite.__init__(self)
		self.load_sprites()
		self.image = self.sprt_list[0]
		self.rect = self.image.get_rect()
		self.profile = eval("PLAYER_PROFILE_{}".format(profile))
		self.rect.center = (x, y)

		#creating vectors
		self.pos = vec(x, y)
		self.acc = vec(0, 0)
		self.vel = vec(0, 0)

		#init players attributes
		self.can_jump = True
		self.hp = PLAYER_HP
		self.time_of_jump = time.time()

		#init weapons attributes
		self.has_wpn = False
		self.last_side = 1 #used to determine the way the bullet will be shot -1 = left & 1 = right
		self.last_time = 0
		self.started_to_reload = 0
		self.weapon = None

		#init animation attributes
		self.last_dis = 0 #sets the disposition of the player image: 0 = idle ; 1 = left ; 2 = right ; 3 = up
		self.anim_idxs = [0,2,4,6]


	def load_sprites(self):
		print("Loading {} sprites".format(self))
		self.path = "Sprites/Players/Lizard/"
		self.sprt_list = []
		for sprt_file in os.listdir(self.path):
			self.sprt_list.append(pgm.image.load(str(self.path+sprt_file)).convert_alpha())
		print("Sprite list is:\t{}".format(self.sprt_list))

	def update(self):
		#print("Player Sprite is updating last side is {}".format(self.last_side))
		self.acc = vec(0, 0.5)
		#self.vel = vec(0,0)

		#fetching pressed keys
		pressed_keys = pgm.key.get_pressed()

		#setting player to idle direction
		self.animate()
		
		#accelarating left
		if pressed_keys[eval("pgm."+self.profile[0])]:
			self.acc.x = - PLAYER_ACCELERATION
			self.last_side = -1
			self.animate(dis=1)

		#accelerating right
		if pressed_keys[eval("pgm."+self.profile[1])]:
			self.acc.x = PLAYER_ACCELERATION
			self.last_side = 1
			self.animate(dis=2)

		#jumping
		if not pressed_keys[eval("pgm."+self.profile[2])]:self.can_jump = False #dirty fix

		if pressed_keys[eval("pgm."+self.profile[2])]:
			if self.can_jump:
				self.time_of_jump = time.time()
				self.acc.y = - PLAYER_ACCELERATION * 2
				self.animate(dis=3)
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

		#applying friction
		self.acc += self.vel * PLAYER_FRICTION
		#movement
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		self.rect.center = self.pos

	def animate(self, dis=0):
		if dis == self.last_dis:
			#currently only works for animations made of 2 sprites per disposition
			if self.image == self.sprt_list[self.anim_idxs[dis]]:
				self.image = self.sprt_list[self.anim_idxs[dis]+1]
			else:
				self.image = self.sprt_list[self.anim_idxs[dis]]

		else:
			self.image = self.sprt_list[self.anim_idxs[dis]]

	def pickup(self, coll_dict):
		self.coll_dict = coll_dict
		pressed_keys = pgm.key.get_pressed()
		if pressed_keys[eval("pgm."+self.profile[4])]:
			if self.has_wpn:
				self.weapon.rect.y = self.rect.y + self.rect.height - self.weapon.rect.height
			self.has_wpn = True
			#print("Picking up:\t", self.coll_dict)
			for self in self.coll_dict.keys(): #is using "self" ok for a loop ?
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
		if self.has_wpn:
			self.weapon.rect.y = self.rect.y + self.rect.height - self.weapon.rect.height
		self.kill()


class Platform(pgm.sprite.Sprite):
	"""Platforms sprite function"""
	def __init__(self, x, y, w, h):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((w, h))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
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
	right sign?
	"""
	def __init__(self, x, y, projectile_type, last_side):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((pjt[projectile_type][0], pjt[projectile_type][1]))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.speed = pjt[projectile_type][2] * last_side
		#print("Speed of the Projectile is of {} p/s".format(self.speed))
		#placing the bullet on the beside the weapon
		self.rect.x = x
		self.rect.y = y
		#print("Bullet {} is at ({};{})".format(self, self.rect.x, self.rect.y))
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
	also change the start() function to accept Sprite class with 2 caps
	"""
	def __init__(self, x, y, wpn_name):
		pgm.sprite.Sprite.__init__(self)
		
		self.wield_rate = wpn_mle[wpn_name][2]
		self.damage = wpn_mle[wpn_name][3]

		self.image = pgm.Surface((wpn_mle[wpn_name][0], wpn_mle[wpn_name][1]))
		self.image.fill(YELLOW)
		self.rect =self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Explosive(pgm.sprite.Sprite):
	"""docstring for Explosive"""
	def __init__(self, x, y, expv_name):
		#initializing pgm Sprite		
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((expv[expv_name][0], expv[expv_name][1]))
		self.image.fill(ORANGE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		#deducing attributes from expv_name
		self.hp_max = self.hp = expv[expv_name][2]
		self.pjt_number = expv[expv_name][3]
		self.expl_radius = expv[expv_name][4]
		self.explode_countdown = expv[expv_name][5]
		self.started_to_ignite = False

		self.dmg_ignited_tick = (self.hp_max/4) / (self.explode_countdown * FPS)

	def update(self):
		if self.started_to_ignite:
			print("{} started to ignite -> dealing {} damage. Current hp is of {}".format(self, self.dmg_ignited_tick, self.hp))
			self.damage(self.dmg_ignited_tick)


	def damage(self, dmg_dealt):
		self.hp -= dmg_dealt
		''' add the change of displayed sprite depending on hp %'''
		if self.hp <= self.hp_max / 4 and not self.started_to_ignite:
			self.started_to_ignite = True
			self.image.fill(RED)
		if self.hp <= 0:
			self.explode()

	def middle_2_pts(self, pt1, pt2):
		return ((pt2[0]-pt1[0])/2 ,(pt2[1]-pt1[1])/2)

	def get_pjt_dir(self):
		'''Make algorithm to equally place all projectile in an
		expanding circle trajectory
		see https://forums.futura-sciences.com/mathematiques-superieur/376022-coordonnes-dun-point-de-triangle-isocele.html
		& https://www.maths-forum.com/superieur/trouver-les-coordonnees-point-dans-triangle-isocele-t77086.html
		explains the formula that should be used
		'''
		#creating required data
		o_coo = (self.rect.centerx, self.rect.centery)
		a_coo = (o_coo[0],o_coo[0]+self.expl_radius)
		angle = crt_angle = (math.pi/2)/self.pjt_number
		pts_list = []
		pjts_dirs = []

		#making coords
		for crt_pt in range(self.pjt_number):
			x_coo = o_coo[0] + (a_coo[0]-o_coo[0])*math.cos(crt_angle) - (a_coo[1]-o_coo[1])*math.sin(crt_angle)
			y_coo = o_coo[1] + (a_coo[1]-o_coo[1])*math.cos(crt_angle) + (a_coo[0]-o_coo[0])*math.sin(crt_angle)
			pts_list.append((x_coo, y_coo))
			crt_angle += angle

		for crt_pt in pts_list:
			#reducing the speed to a maximum of 1 by axis; adapt this value
			reduced_pt_div = max(crt_pt)
			crt_dir = (math.ceil(crt_pt[0]/reduced_pt_div), math.ceil(crt_pt[1]/reduced_pt_div))
			pjts_dirs.append(crt_dir)
		i = 0
		for j in pjts_dirs:
			i+=1
			print("\nDirection for the {} projectile is \t{}".format(i,j))
		return pjts_dirs

	def explode(self):
		print("{} is exploding".format(self))
		'''should I first remove the explosive from all groups ?'''
		#self.pjt_list = []
		self.pjts_dirs = self.get_pjt_dir()
		for pt_coo in self.pjts_dirs:
			self.crt_pjt = ExplosiveProjectile(self.rect.centerx, self.rect.centery, pt_coo, self.expl_radius, "normal_bullet")
			projectiles_list.append(self.crt_pjt)
		self.kill()

class ExplosiveProjectile(pgm.sprite.Sprite):
	"""docstring for ExplosiveProjectile"""
	def __init__(self, x, y, speed, radius, pjt_name):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((1, 1))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = self.orig_x = x
		self.rect.y = self.orig_y = y
		self.speed = speed
		self.radius = radius
		self.damage = pjt[pjt_name][3]
		print("Creating {} at N({};{})".format(self, self.rect.x, self.rect.y))

	def update(self):
		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]
		if self.distance_from_orig() >= self.radius:
			print("The distance from O({};{}) and N({};{}) is of {} which is greater than {} :\t killing bullet".format(self.orig_x, self.orig_y, self.rect.x, self.rect.y, self.distance_from_orig(), self.radius))
			self.kill()

	def distance_from_orig(self):
		#print("Will square {}".format(((self.orig_x - self.rect.x)^2) + ((self.orig_y - self.rect.y)^2)))
		return math.sqrt((self.orig_x - self.rect.x)**2 + (self.orig_y - self.rect.y)**2)
		
class TextSurface(pgm.sprite.Sprite):
	"""docstring for Text, is there a way to delete a surface or remove
	a subsurface for a parent surface ?
	fix the false alpha background -> due to colorkey ?
	also add an offset for the size of the text box to make it more readable
	"""
	def __init__(self, x, y, text, fg_color=WHITE, bg_color=None):
		pgm.sprite.Sprite.__init__(self)
		self.text = text
		self.bg_color = bg_color
		self.fg_color = fg_color
		if self.bg_color == None: self.bg_color=ALPHA
		if self.bg_color!=ALPHA: self.on_hover_bg_color = (self.bg_color[0]-math.floor(0.3*self.bg_color[0]), self.bg_color[1]-math.floor(0.3*self.bg_color[1]), self.bg_color[2]-math.floor(0.3*self.bg_color[2]))
		else: self.on_hover_bg_color = self.bg_color
		self.txt_font = pgm_frtp.Font(None, 20)
		self.txt_rect = self.txt_font.get_rect(self.text)
		self.image = pgm.Surface((self.txt_rect.w+TEXT_CORR_W, self.txt_rect.h+TEXT_CORR_H)).convert_alpha()
		self.image.fill(self.bg_color)
		self.rect = self.image.get_rect()
		self.rect.x = x - (self.txt_rect.w /2)
		self.rect.y = y
		self.txt_font.render_to(self.image, (TEXT_CORR_W/2,TEXT_CORR_H	/2), self.text, fgcolor=self.fg_color, bgcolor=None)

	def chg_pos(self, new_pos=(0,0)):
		self.rect.x = new_pos[0]
		self.rect.y = new_pos[1]

	def chg_color(self, state=0, bg_color=ALPHA):
		'''state is 0 if the bgcolor is normal and 1 if highlighted'''
		if state==1:
			self.new_bg_color = self.on_hover_bg_color
		else:
			self.new_bg_color = self.bg_color
		self.image.fill(bg_color)
		self.txt_font.render_to(self.image, (TEXT_CORR_W/2,TEXT_CORR_H	/2), self.text, fgcolor=self.fg_color, bgcolor=self.new_bg_color)

	def chg_txt(self, new_txt, bg_color=ALPHA):
		'''Improve the code in order to rebuild the image surface to fit the
		whole new text perfectly -> really needed ?
		'''
		self.image.fill(bg_color)
		self.text = new_txt
		self.txt_rect = self.txt_font.get_rect(new_txt)
		self.rect.w = self.txt_rect.w
		self.txt_font.render_to(self.image, (TEXT_CORR_W/2,TEXT_CORR_H	/2), new_txt, fgcolor=self.fg_color, bgcolor=None)

class TextButton(pgm.sprite.Sprite):
	"""docstring for Button how could I make it inherit from TextSurface ?"""
	def __init__(self, x, y, text, action=None, bg_color=BLACK, fg_color=GREEN):
		pgm.sprite.Sprite.__init__(self)
		self.text = str(text)
		self.action = action
		self.bg_color = bg_color
		self.fg_color = fg_color
		self.txt_displayer = TextSurface(x, y, self.text, self.fg_color, self.bg_color)
		#self.txt_displayer.image.fill(self.bg_color)
		self.image = self.txt_displayer.image
		self.rect = self.txt_displayer.rect
		self.was_hovered = False
		self.acting = False

	def update(self):
		self.events = pgm.event.get()
		self.mouse_pos = pgm.mouse.get_pos()
		if (self.mouse_pos[0]>= self.rect.x and self.mouse_pos[0]<= self.rect.x + self.rect.w) and (self.mouse_pos[1]>= self.rect.y and self.mouse_pos[1] <=self.rect.y + self.rect.h) :
			self.txt_displayer.chg_color(state=1, bg_color=self.txt_displayer.on_hover_bg_color)
			self.was_hovered = True
			self.mouse_clicks = pgm.mouse.get_pressed()
			if self.mouse_clicks[0]:
				self.acting = True
		elif self.was_hovered:
			self.was_hovered = False
			self.txt_displayer.chg_color(bg_color=self.bg_color)


class ImageButton(pgm.sprite.Sprite):
	"""docstring for ImageButton
	maybe add another surface under the image which would change colors when hovered ?
	or just modify the color of the pixels of the image"""
	def __init__(self, x, y, image, action=None):
		pgm.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = pgm.image.load(str(str(IMG_MISC_FOLDER.iterdir()))).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x - (self.rect.w/2)
		self.rect.y = y - (self.rect.h/2)
		self.action = action
		self.acting = False
		self.was_hovered = False

	def chg_color(self, new_fg_color, new_bg_color):
		self.txt_font.render_to(self.image, (0, 0), self.text, fgcolor=new_fg_color, bgcolor=new_bg_color)

	def update(self):
		self.events = pgm.event.get()
		self.mouse_pos = pgm.mouse.get_pos()
		if (self.mouse_pos[0]>= self.rect.x and self.mouse_pos[0]<= self.rect.x + self.rect.w) and (self.mouse_pos[1]>= self.rect.y and self.mouse_pos[1] <=self.rect.y + self.rect.h) :
			self.was_hovered = True
			self.mouse_clicks = pgm.mouse.get_pressed()
			if self.mouse_clicks[0]:
				self.acting = True
		elif self.was_hovered:
			self.was_hovered = False
			pass


class InputField(pgm.sprite.Sprite):
	"""docstring for InputField, heavily depends on TextSurface. Just a prototype, not very well written
	add a background image/surface to help the user determine the nature of the sprite and its rect"""
	def __init__(self, x, y, hint_text, fg_color=BLUE, bg_color=None, nbr=None):
		pgm.sprite.Sprite.__init__(self)
		self.nbr = nbr
		assert (self.nbr != None), "InputField isn't bound"
		self.hint_text = self.crt_txt = hint_text
		self.fg_color = fg_color
		self.bg_color = bg_color
		self.txt_displayer = TextSurface(x, y, str(self.hint_text), LIGHT_GREY, self.bg_color)
		self.rect = self.txt_displayer.rect
		self.image = self.txt_displayer.image
		self.was_hovered = self.focused = False
		self.returned = False

	def update(self, key=None):
		#if self.returned: self.crt_txt = ""
		self.mouse_pos = pgm.mouse.get_pos()
		self.key = key
		if (self.mouse_pos[0]>= self.rect.x and self.mouse_pos[0]<= self.rect.x + self.rect.w) and (self.mouse_pos[1]>= self.rect.y and self.mouse_pos[1] <=self.rect.y + self.rect.h) :
			self.was_hovered = True #replaces the on_hover function along with the next line
			if self.crt_txt == self.hint_text or "":
				self.txt_displayer.chg_color(state=1)
			self.mouse_clicks = pgm.mouse.get_pressed()
			if self.mouse_clicks[0]:
				self.focused = True

		elif self.was_hovered:
			self.was_hovered = False
			if self.crt_txt == "": self.txt_displayer.chg_txt(str(self.hint_text))
			self.txt_displayer.chg_color()

		if self.focused and self.key!=None:
			if self.crt_txt == self.hint_text:
				self.crt_txt = ""

			self.new_txt = self.crt_txt
			self.str_to_append = ""
			if self.key == "\b":
				if len(self.str_to_append) == 0:
					self.crt_txt = self.crt_txt[:-1]
				else:
					self.str_to_append = self.str_to_append[:-1]

			elif self.key == "\r":
				self.returned = True
				self.focused = False

			else:
				self.str_to_append = self.str_to_append + self.key
			self.crt_txt = self.crt_txt + self.str_to_append

			#if self.txt_displayer.txt_rect.w >= INPUT_MAX_LENGTH:
			drawn_txt = self.crt_txt[-INPUT_MAX_LENGTH:]
			self.txt_displayer.chg_txt(drawn_txt)

class Ladder(pgm.sprite.Sprite):
	"""docstring for Ladder"""
	def __init__(self, x, y, h):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((35, h))
		self.rect= self.image.get_rect()

class Throwables(pgm.sprite.Sprite):
	"""docstring for Throwables Sprite class"""
	def __init__(self, x, y, thrb_name):
		pgm.sprite.Sprite.__init__(self)
		self.image = pgm.Surface((thrb))

		self.x = x
		self.y = y
		self.thrb_name = thrb_name