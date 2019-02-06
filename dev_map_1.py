from settings import *

world = {
	"Platform": [[0, HEIGHT-10, WIDTH, 10], [30, 0, 10, HEIGHT - 10], [WIDTH-10, 0, 10, HEIGHT - 10], [WIDTH/2 -25, HEIGHT-100, 100, 10]],
	"Firearm": [[WIDTH/2, HEIGHT -20, "pistol"], [WIDTH/3, HEIGHT -20, "machine_gun"]],
#	"MeleeWeapon": [[WIDTH/2, HEIGHT -20, "axe"]],
	"Destructible": [[40, 0, 10 , HEIGHT, "wood"]],
	"Explosive": [[WIDTH-60, HEIGHT-50, "barril"]],
	"Player": [[WIDTH/2, HEIGHT/2, 1], [WIDTH/2+30, HEIGHT/2, 2]],
}