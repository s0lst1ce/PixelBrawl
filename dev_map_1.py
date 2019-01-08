from settings import *

world = {
	"Platform": [[0, HEIGHT-10, WIDTH, 10], [30, 0, 10, HEIGHT - 10], [WIDTH-10, 0, 10, HEIGHT - 10], [WIDTH/2 -25, HEIGHT-100, 100, 10]],
	"Firearm": [[WIDTH/2, HEIGHT -20, "pistol"], [WIDTH/3, HEIGHT -20, "machine_gun"]],
	"MeleeWeapon": [],
	"Destructible": [[40, 0, 10 , HEIGHT, "wood"]],
	"Explosive": [[WIDTH-60, HEIGHT-50, "barril"]],
	"Player": [[WIDTH/2, HEIGHT/2, ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_f", "K_SPACE"]], [WIDTH/2+40, HEIGHT/2, ["K_a", "K_d", "K_w", "K_s", "K_e", "K_c"]]]
}