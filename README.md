# PixelBrawl
A little and simple yet (hopefully ! ) fun game. The game is made with python 3.7+ and Pygame 1.9.4 (should work with following versions).

## Development History:
I got the idea of coding a game in python a few months ago when I couldn't think of anything else new and entertaining to write. Moreover I thought I'd be a good way to play a simple game with some members of my family & friends. Hopefully you will have fun with it too ! I do not spend a lot of time coding it though so don't expect any regular update. To code this game I first had to get some knowledge on the [Pygame](https://pygame.org/) module. I mostly read the official documentation to learn how to use pygame. I also used [this template](https://github.com/kidscancode/pygame_tutorials/blob/master/pygame%20template.py) to begin my game. I want to thank [KidsCanCode](https://github.com/kidscancode/) [(LISCENCE)](https://github.com/kidscancode/pygame_tutorials/LICENSE) for this much apreciated time saving help ! 
If you are intersted in helping in the development please write to me. Also please feel free to send advices and recomendations. They will all be taken into consideration.

*NOTICE: If you are an artist and are interested in making custom sprites for this game you will be welcome !*

## The Game:
The game is a multiplayer shared screen. The players all compete in a small arena and must be the last one standing in order to win. Teammatches are planned although I have not started working on them yet.

**BEWARE** The game is in early development and currently barely functionnal. Use at your own risk.
![v0.3-a3-DEV Main menu screenshot](https://raw.githubusercontent.com/NotaSmartDev/assets/master/menu.png)

![v0.1-a1 Test map screenshot](https://raw.githubusercontent.com/NotaSmartDev/assets/master/game.png)







## Instructions:

### Installation:

##### Without python:

If you'r under Linux you can just download the version you want by following this [link](https://mega.nz/#F!YOwFhSbL!fjnwdNnDcOq_z7YAiVQ-BA). The Mega folder contains all versions compiled for Linux. I haven't compiled any version for windows so you'll probably have to wait until the full release to get it unless anyone ask for it before that. Meanwhile refer to the next section to get the game.

Once you have the compiled version downloaded simply extract its contents (if compressed) and run onto the binary file (the one called `PixelBrawl-ALPHA`). That's it ! I hope you enjoy. Don't hesitate to give me your feedback !

##### With python:

If you have the python interpreter installed the first thing you should do is to install pygame by running:

- UNIX: `pip3 install pygame`
- Windows: `pip install pygame --user` . The user option can be omitted if you installed python only for your user.

Then download the source code of the latest stable (`v0.3-a3`) or experimental (`master-branch`) version. Extract the source code into a directory then open a terminal (or command prompt under windows) in the directory and type:

- UNIX: `python3 main.py`
- Windows: `py main.py`

That's it ! I hope you enjoy. Don't hesitate to give me your feedback !



### How to play:

##### Controls

The goal of the game is to kill your opponent(s). To do this your first task is to pick up a weapon. For this you need first to move to it using:

- Player1: The arrow keys

- Player2: `w`, `a` and `d`

Then you're going to need to pickup the said weapon. For this use the pickup key:

- Player1: The `m` 
- Player2: `s`

Once that's done you can shoot at whatever seemd best to kill you enemy by pressing:
- Player1: `n`
- Player2: `c`

##### Configuration



Although the game doesn't yet (see #12 ) allow you to change the controls you can still do it with some manual configurations ! To do this open the `settings.py` file into your favorite text editor and change the PLAYER PROFILEs. The file is documented so it tells you which key refers to what. However it doesn't come with a list of all the pygame keys names. To find them head over to their [website](https://www.pygame.org/docs/ref/key.html). If you have trouble with this and can't wait for me to implement the settings in the game, post a comment on issue #12 .