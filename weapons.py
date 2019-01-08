weapons_firearms = {
	"Name_of_the_weapon": ["width -> int", "height -> int", "projectile -> str", "fire rate in shots per second -> float", "magazine size -> int", "reload time in seconds -> float", ["sprite1", "sprite2", "spriten"]],
	"pistol": [20, 10, "normal_bullet", 5, 50, 5, []],
	"machine_gun": [40, 12, "normal_bullet", 12, 250, 3, []],
	"sniper": [42, 10, "sniper_bullet", 1, 15, 5, []]

}


weapons_melee = {
	"Name of the weapon": ["width -> int", "height -> int", "numbers of wields per second -> float", "damage to deal -> float", ["sprite1", "spriten"]],
	"axe": [20, 30, 3, 20, []],
	"katana": [10, 30, 10, 5, []]
}

explosives = {
	"Name of the explosive": ["width -> int", "height -> int", "hp -> int", "numbers of shot projectiles -> int", "radius of explosion -> int", "ignite to explode time in seconds -> float"],
	"barril": [30, 40, 50, 20, 104, 5]

}