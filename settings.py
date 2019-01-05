import os

#all settings and global functions of Pixcel Brawl

#Window definitions
WIDTH = 854
HEIGHT = 480
FPS = 60
TITLE = "Pixel Brawl - v0.2-a2"

#Color definition
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#Player physics properties definition
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = - 0.12

#player properties
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
JUMPING_COUNTDOWN = 0.5 #in s
PLAYER_HP = 100

#players key profiles
#PLAYER_PROFILE_N = ["left_key", "right_key", "up_key",
#"down_key", "pickup_key", "shoot_key"]
PLAYER_PROFILE_1 = ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_f", "K_SPACE"]
PLAYER_PROFILE_2 = None
PLAYER_PROFILE_3 = None

#projectiles properties
PROJECTILE_SPEED = 10 #this must always be < PLAYER_WIDTH

#paths
#img = os.path("curdir")