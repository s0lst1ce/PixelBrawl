# ROADMAP

*NB:* This roadmap is subject to change at any moment. If there's any feature you'd like me to add please post a comment before asking for a pull request for the roadmap.

### v0.2-a2 - RELEASED:

- [x] Handle damage
- [x] Add a handler for different types of weapons/items 
- [x] Create a consistent firearms definition
- [x] Add handler to load map data from different files
- [x] Add different types of projectiles & re-write Projectile sprite class

### v0.3-a3 - IN DEVELOPMENT:

- [ ] Add explosives
  - [ ] Write dispersion algorithm
- [ ] Improve general code
  - [x] Re-write the `start()` function with loops to handle different maps
  - [ ] Improve weapons handler & re-write
  - [ ] Improve Groups handler 
- [x] Create a consistent map definition format & filetype
- [ ] Add throwables


### v0.4-a4:

- [ ] Add more types of projectiles such as explosive ones
- [ ] Add melee weapons
- [x] Add spawnpoints
- [x] Add multiplayer support
- [ ] Add perks

### v0.5-a5:

- [ ] Fix various bugs
 - [ ] Reload issues
 - [ ] Bullets which can pass through `non-crossable`
 - [ ] Players who can jump through `non-crossable` if they're too close
 - [ ] Lots of small bugfixes
- [ ] Re-write collision block of the `update()` function to suit multiple players

### v0.6-a6:

- [ ] Add GUI
 - [ ] Add Menus
  - [ ] Start Game
  - [ ] Options
  - [ ] End of Game display
  - [ ] Settings


### v0.7-b1:

- [ ] Replace Pygame rectangles by drawn sprites
 - [ ] Add animations
- [ ] Add sound

### v0.8-b2:

- [ ] Create Map Editor

### v0.9-b3:

- [ ] Add Errors handler
  - [ ] Add debug log