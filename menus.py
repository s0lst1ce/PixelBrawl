from settings import *
'''this kind of loading method requires a to move a lot of data around, is it worth it ? Also causes issues and difficulties
concerning variable values, how ot improve it ?
also think to improve the loader to make settings independant or the map deisgner won't work correctly across multiple configs
also it's far from being pythonic

NB: change the nested strings + "#" which is a flag for keyword argument (see main.py: screen_loader()) '''
settings = {
	"TextSurface": [[WIDTH/2, HEIGHT/10, "Settings", "#fg_color=BLACK"],[WIDTH/4, HEIGHT/10*2, "Resolution:", "#fg_color=BLACK"],[WIDTH/2, HEIGHT/8*3, "Keymaps", "#fg_color=BLACK"]],
	"TextButton": [[WIDTH/2, HEIGHT/8*7, "Main Menu", """#action='''show_start_screen'''""", '#bg_color=ORANGE', '#fg_color=WHITE'],
	[WIDTH/3*2.5, HEIGHT/10*2, "Apply", """#action='''change_resolution'''""", '#bg_color=GREEN', '#fg_color=WHITE'],
	[WIDTH/3*1.8, HEIGHT/8*3, "1", """#action='''select_profile_1'''""", '#bg_color=BLUE', '#fg_color=WHITE'],
	[WIDTH/3*2, HEIGHT/8*3, "2", """#action='''select_profile_2'''""", '#bg_color=CYAN', '#fg_color=WHITE']],
	"ImageButton": [],
	"InputField": [[WIDTH/3*1.5, HEIGHT/10*2, "854", "#nbr=0"],[WIDTH/3*2, HEIGHT/10*2, "480", "#nbr=1"]],
}
pause = {
	"TextSurface": [[WIDTH/2, HEIGHT/6, "Game has been paused", "#fg_color=YELLOW"]],
	"TextButton": [[WIDTH/2, HEIGHT/8*3.5, "Main Menu", """#action='''show_start_screen'''""", '#bg_color=ORANGE', '#fg_color=WHITE'], [WIDTH/2, HEIGHT/8*2.5, "Resume", """#action='''resume_game'''""", '#bg_color=BLUE', '#fg_color=WHITE'], [WIDTH/2, HEIGHT/8*4, "QUIT", """#action='''stop_game'''""", '#bg_color=RED', '#fg_color=WHITE']],
	"ImageButton": []
}
start = {
	"TextSurface": [[WIDTH/2, HEIGHT/4, "Pixel Brawl", "#fg_color=DARK_YELLOW"]],
	"TextButton": [[WIDTH/3, HEIGHT/2, "Start", """#action='start_game'""", '#bg_color=GREEN', '#fg_color=WHITE'], [WIDTH/3*2, HEIGHT/2, "Quit", """#action='''stop_game'''""", '#bg_color=RED', '#fg_color=WHITE']],
	#"InputField": [[WIDTH/2, HEIGHT/3*2, "Type here..."]],
	"ImageButton": [[20, HEIGHT-20, "settings-32.png", """#action='show_settings_screen'"""]]
}
newgame = {
	"TextSurface": [],
	"TextButton": [],
	"ImageButton": []
}
score = {
	"TextSurface": [[WIDTH/2, HEIGHT/4, "Game has ended !", "#fg_color=YELLOW"]],
	"TextButton": [[WIDTH/2, HEIGHT/2, "Main Menu", """#action='''show_start_screen'''""", '#bg_color=ORANGE', '#fg_color=WHITE']],
	"ImageButton": []
}
loading = {
	"TextSurface": [[WIDTH/2, HEIGHT/2, "LOADING...", "#fg_color=YELLOW"]],
}
'''find a way to improve the handler to be able to pass ratios adapted to text size
improve handler to be able to choose the font
'''