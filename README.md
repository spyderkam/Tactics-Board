# Tactics Board Project

## Keybindings

- **B:** Toggle ball
- **N:** Toggle jersey numbers
- **R:** Reset formations and triangle
- **T:** Toggle triangle (first 3 players after reset)
- **Y:** Reset triangle

## Questions Answered

### How would changing `BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE]` in the `# Teams and team formations` section of `main.py` to `BLUE_TEAM = ORIGINAL_BLUE` affect this program?

Changing `BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE]` to `BLUE_TEAM = ORIGINAL_BLUE` would create a direct reference instead of a deep copy of the list. This means that when players are dragged to new positions, both `BLUE_TEAM` and `ORIGINAL_BLUE` would be modified simultaneously. As a result, pressing **R** to reset formations would not work properly since the original positions would have been changed.

The current implementation using `[pos[:] for pos in ORIGINAL_BLUE]` creates a deep copy of the nested lists, ensuring that `ORIGINAL_BLUE` remains unchanged when players are moved, allowing the formation to be properly reset when **R** is pressed.

This change would break the reset functionality of the program since the original positions would no longer be preserved.
