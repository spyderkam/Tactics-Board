## Main Components:

### `server.py`:
- Flask server handling WebSocket connections and rendering the tactics board
  - Implements socket events for player movement, ball toggling, and triangle drawing
  - Renders HTML template with canvas and control buttons
  - Runs on port 80

### `main.py`:
- Core game logic
  - Sets up 1920x1080 Pygame display
  - Manages player formations, ball position, and triangle drawing
  - Handles keyboard controls (B, N, R, T, Y)
  - Player circles are size 20 with varying font sizes for numbers

### `database.py`:
- Formation configurations
  - Contains formations: 433, 4231, 442, 352
  - Defines colors (BLUE, GREEN, RED, WHITE, BLACK)
  - Stores coordinates for each player position

### `tools.py`:
- Helper functions
  - Contains `draw_triangle` function with semi-transparent orange color
  - Uses `SRCALPHA` for transparency

## Current Features:
- Drag and drop player movement
- Toggle player numbers (single/double digits supported)
- Toggle ball visibility
- Triangle drawing tool
- Formation reset functionality
- Smooth movement handling with throttling
- WebSocket-based real-time updates

## Dependencies:
- Python 3.10+
- Flask
- Flask-SocketIO
- Pygame
- DearPyGui
- Supertools

## Current Issues:
- Pitch not visible until button click (noted in `todolist.md`)
- Formation selection menu not implemented yet

This represents Version 1.0 of the Tactics Board project, with core functionality implemented and room for planned improvements.

