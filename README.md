
# ⚽ Football Tactics Board (Beta)

An interactive real-time football tactics board built with Python, Flask, and Pygame. Perfect for coaches, analysts, and football enthusiasts to create and visualize game strategies.

## 🎯 Features

### Team Management
- Interactive drag-and-drop player movement
- Jersey number customization (single and double digits)
- Multiple formation presets:
  - 4-3-3
  - 4-4-2
  - 4-4-2 Diamond
  - 4-2-3-1
  - 3-5-2
  - 3-4-3
- Independent formation control for each team

### Drawing Tools
- Ball placement and movement
- Triangle drawing tool (supports two independent triangles)
- Line drawing tool with dashed lines
- Auto-adjusting lines and shapes that move with players

### Real-time Features
- WebSocket-based real-time updates
- Smooth player movement
- Instant formation changes

## ⌨️ Controls

### Keyboard Shortcuts
- `B` - Toggle ball visibility
- `N` - Toggle player numbers
- `T` - Toggle first triangle tool
- `G` - Toggle second triangle tool
- `L` - Toggle line drawing tool
- `Y` - Reset triangles
- `R` - Reset entire board
- `S` - Stop active tool
- `U` - Toggle all active shapes

### Mouse Controls
- Click and drag players to move them
- Double-click players when using triangle/line tools
- Click the ball to move it (when visible)

## 🔧 Technical Requirements

- Python 3.10+
- Required Python packages:
  - Flask
  - Flask-SocketIO
  - Pygame
  - beautifulsoup4

## 🚀 Getting Started

1. Click the "Run" button in your Replit workspace
2. Wait for all dependencies to install
3. The server will start automatically
4. The tactics board will be accessible through your Repl's URL

## 🏗️ Project Structure

```
├── server.py      # WebSocket server & main application logic
├── main.py        # Core game engine & Pygame display
├── database.py    # Formation configurations & colors
├── tools.py       # Drawing tools implementation
└── static/        # Frontend assets
    └── script.js  # Client-side JavaScript
```

## ⚠️ Beta Version Notice

This is currently a beta version (0.9.0). While fully functional, you may encounter:
- Minor visual glitches
- Performance optimizations in progress
- Additional features being implemented

Please report any issues or suggestions through Replit's comments.

## 👨‍💻 Author

Created by spyderkam

## 📝 License

All rights reserved. For educational purposes only.

---
*Last updated: 2024*
