### v0.3-a3:
~ button action handler
~ transparency handler to suit per pixel alpha channel
~ improved `load_screen` method code
~ improved `gui_update` method code
~ improved `game_update` method code
~ improved `load_sprites` function code
~ improved readibility of GUI widgets containing fonts
~ changed TextSurface functions modifying drawn pixels -> smoother UIX
~ cleaned TextButton widget
\+ added InputField GUI widget
\+ significant performance improvment
~ changed scope of several variables to make the code cleaner & more performant
~ simplified InputField `update` section
~ cleaned player animation section
\+ documented player sprite class
~ cleaned player sprite class
~ re-wrote InputField class in order to more effeciently get its data
\+ added settings menu
\+ added possibility to change resolution (though `change_resolution()`)
~ fixed bug where button's function was called every frames

### v0.4-b1:
\+ fixed incorrect path given in some cases (for both posix and nt filesystems)
\+ added rule where screen resolutions must be 16:9
\+  added GUI scaler

