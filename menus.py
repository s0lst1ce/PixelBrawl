from settings import *
#this kind of loading method requires a to move a lot of data around, is it worth it ? Also causes issues and difficulties
#concerning variable values, how ot improve it ?
settings = {
	"TextSurface": [],
	"TextButton": [],
	"ImageButton": []
}
start = {
	"TextSurface": [[WIDTH/2, HEIGHT/4, "Pixel Brawl", "#fg_color=YELLOW"]],
	"TextButton": [[WIDTH/3, HEIGHT/2, "Start", """#action='start_game'""", '#bg_color=GREEN', '#fg_color=WHITE'], [WIDTH/3*2, HEIGHT/2, "Quit", """#action='''stop_game'''""", '#bg_color=RED', '#fg_color=WHITE']],
	#"ImageButton": [[20, HEIGHT-20, "settings_icon.png"]]
}
score = {
	"TextSurface": [[WIDTH/2, HEIGHT/4, "Game has ended !", "#fg_color=YELLOW"]],
	"TextButton": [[WIDTH/2, HEIGHT/2, "Main Menu", """#action='''show_start_screen'''""", '#bg_color=BLUE', '#fg_color=WHITE']],
	"ImageButton": []
}
'''find a way to improve the handler to be able to pass ratios adpated to text size
improve handler to be able to choose the font
'''