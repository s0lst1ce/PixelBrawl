import os
import pathlib as path

#all settings and global functions of Pixcel Brawl

#Window definitions
#WIDTH must come before HEIGTH or unexpected errors could occur
WIDTH = 1024
HEIGHT = 576
FPS = 60
TITLE = "Pixel Brawl - v0.4-b1"

#Color definition
ALPHA = (255,255,255,255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
DARK_YELLOW	 = (246,246,67, 255)
CYAN = (0, 255, 255, 255)
MAGENTA = (255, 0, 255, 255)
ORANGE = (255, 165, 0, 255)
LIGHT_GREY = (178, 178, 178, 255)
DARK_GREY = (78, 78, 78, 255)

#Game settings
BACKGROUND = BLACK
PAUSE_KEY = "p"
TEXT_CORR_W = 20
TEXT_CORR_H = 5
INPUT_MAX_LENGTH = 10
FONT_SIZE = 25.0
#1 is (1024*876)
SCALE = 1.0

#Player physics properties definition
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12

#player properties
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
JUMPING_COUNTDOWN = 0.5 #in seconds
PLAYER_HP = 100
ANIM_DELAY = FPS/3

#players key profiles
#PLAYER_PROFILE_N = ["left_key", "right_key", "up_key",
#"down_key", "pickup_key", "shoot_key"]
PLAYER_PROFILE_1 = ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_m", "K_n"]
PLAYER_PROFILE_2 = ["K_a", "K_d", "K_w", "K_s", "K_e", "K_SPACE"]
PLAYER_PROFILE_3 = None

#projectiles properties
PROJECTILE_SPEED = 10 #this must always be < PLAYER_WIDTH

#paths
#IMG_SPRITES_FOLDER = os.path.join("Sprites")
IMG_PLAYER_FOLDER = os.path.join("Sprites", "Players")
IMG_MISC_FOLDER = os.path.join("Sprites", "Misc")

'''if os.name == posix:
	IMG_MISC_FOLDER = IMG_MISC_FOLDER.as_posix()
	IMG_PLAYER_FOLDER = IMG_PLAYER_FOLDER.as_posix()
elif os.name == nt:
	IMG_MISC_FOLDER = IMG_MISC_FOLDER.as_'''
