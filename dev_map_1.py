from settings import *

world = {
	"Platform": [[0, HEIGHT-10, WIDTH, 10], [30, 0, 10, HEIGHT - 10], [WIDTH-10, 0, 10, HEIGHT - 10], [WIDTH/2 -25, HEIGHT-100, 100, 10]],
	"Firearm": [[WIDTH/2, HEIGHT -20, "pistol"]],
	"MeleeWeapon": [],
	"Destructible": [[40, 0, 10 , HEIGHT, "wood"]],
	"Player": [[WIDTH/2, HEIGHT/2, ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_f", "K_SPACE"]]]
}