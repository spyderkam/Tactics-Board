
# Tactics Board

A real-time interactive football tactics board built with Python, Flask, and Pygame.

## Features

- Interactive drag-and-drop player movement
- Multiple formations for both teams:
  - 4-3-3
  - 4-4-2
  - 4-4-2 Diamond
  - 4-2-3-1
  - 3-5-2
- Separate formation controls for each team
- Toggle player numbers (supports single and double digits)
- Toggle ball visibility
- Triangle drawing tools
- Real-time WebSocket updates
- Formation reset functionality

## Controls

- **B**: Toggle ball visibility
- **N**: Toggle player numbers
- **T**: Toggle triangle
  - Click on three players to create a triangle
- **Y**: Reset triangle
- **R**: Reset entire board

## Requirements

- Python 3.10+
- Flask
- Flask-SocketIO
- Pygame

## Running the Application

1. Click the "Run" button in your Replit workspace
2. The server will start automatically
3. Use the interface buttons or keyboard shortcuts to control the board

## Implementation Details

The project consists of four main components:

- `server.py`: Flask server handling WebSocket connections
- `main.py`: Core game logic and Pygame display
- `database.py`: Formation configurations
- `tools.py`: Triangle drawing utilities

## Current Status

Version 1.0 - Base version

## Author

Created by spyderkam
