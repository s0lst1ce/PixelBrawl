from settings import *
settings = {
	"TextSurface": [],
	"TextButton": [],
	"ImageButton": []
}
start = {
	"TextSurface": [[WIDTH/2, HEIGHT/4, "Pixel Brawl", "#fg_color=YELLOW"]],
	"TextButton": [[WIDTH/3, HEIGHT/2, "Start", """#action='starting()'""", '#bg_color=GREEN', '#fg_color=WHITE'], [WIDTH/3*2, HEIGHT/2, "Quit", """#action='''self.stop_game()'''""", '#bg_color=RED', '#fg_color=WHITE']],
	"ImageButton": [[20, HEIGHT-20, "settings_icon.png"]]
}
score = {
	"TextSurface": [],
	"TextButton": [],
	"ImageButton": []
}
'''find a way to improve the handler to be able to pass ratios adpated to text size
improve handler to be able to choose the font
'''