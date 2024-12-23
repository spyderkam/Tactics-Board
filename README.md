
# ⚽ Football Tactics Board (Beta v0.9.0)

An interactive real-time football tactics board built with Python, Flask, and Pygame. Perfect for coaches, analysts, and football enthusiasts to create and visualize game strategies.

## 🎯 Features

### Team Management
- Interactive drag-and-drop player movement with smooth animations
- Jersey number customization (supports both single and double digits)
- Multiple formation presets:
  - 4-3-3 (Default attacking formation)
  - 4-4-2 (Classic formation)
  - 4-4-2 Diamond (Midfield-focused variant)
  - 4-2-3-1 (Modern defensive formation)
  - 3-5-2 (Wing-back system)
  - 3-4-3 (Attacking formation)
- Independent formation control for each team (blue/red)

### Drawing Tools
- Ball placement and movement with realistic physics
- Dual triangle system for tactical analysis
  - Orange triangle for primary movements
  - Purple triangle for secondary patterns
- Dynamic line tool with dashed visualization
- Shape persistence: lines and shapes move with players

### Real-time Features
- WebSocket-based instantaneous updates
- Smooth player transitions
- Immediate formation changes
- Multi-device synchronization

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

### Mouse/Touch Controls
- Click/tap and drag players to move them
- Double-click/tap players when using shape tools
- Click/tap and drag the ball when visible
- Intuitive touch controls for mobile devices

## 🔧 Technical Requirements

- Python 3.10+
- Required Python packages:
  - Flask
  - Flask-SocketIO
  - Pygame
  - beautifulsoup4

## 🚀 Quick Start

1. Click the "Run" button in your Replit workspace
2. Wait for all dependencies to install automatically
3. The server will start on port 80
4. Access the tactics board through your workspace URL

## 🤝 Contributing

Currently in beta (v0.9.0). Known areas for improvement:
- Additional formation presets
- Enhanced mobile responsiveness
- Custom color schemes
- Formation save/load functionality
- Animation smoothness optimizations

## ⚠️ Beta Version Notice

This is currently a beta version (0.9.0). While fully functional, you may encounter:
- Minor visual glitches during rapid movements
- Performance optimizations in progress
- Additional features being implemented
- Mobile interface refinements

Please report any issues through Replit's comments section.

## 👨‍💻 Author

Created by spyderkam

## 📝 License

All rights reserved. For educational purposes only.

---
*Last updated: 2024*
