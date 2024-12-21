
# Tactics Board

A real-time interactive football tactics board built with Python, Flask, and Pygame.

## Features

- Interactive drag-and-drop player movement
- Two formations: 3-5-2 (Blue Team) and 4-3-3 (Red Team)
- Toggle player numbers (supports single and double digits)
- Toggle ball visibility
- Dual triangle drawing tools (Orange and Purple)
- Real-time WebSocket updates
- Formation reset functionality

## Controls

- **B**: Toggle ball visibility
- **N**: Toggle player numbers
- **T**: Toggle first triangle (Orange)
- **G**: Toggle second triangle (Purple)
- **Y**: Reset both triangles
- **R**: Reset entire board

## Requirements

- Python 3.10+
- Flask
- Flask-SocketIO
- Pygame

## Running the Application

1. Click the "Run" button in your Replit workspace
2. The server will start on port 80
3. Use the interface buttons or keyboard shortcuts to control the board

## Implementation Details

The project consists of four main components:

- `server.py`: Flask server handling WebSocket connections
- `main.py`: Core game logic and Pygame display
- `database.py`: Formation configurations and colors
- `tools.py`: Triangle drawing utilities

## Current Status

Version 1.0 - Core functionality implemented with room for future improvements.

## Author

Created by spyderkam
