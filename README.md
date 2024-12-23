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

### Shape Tools
- Ball placement and movement with realistic physics
- Dual triangle system for tactical analysis
  - Orange triangle for primary movements
  - Purple triangle for secondary patterns
- Dynamic line tool with dashed visualization
- Shape persistence: lines and shapes move with players

### Shape Tool Usage Guide
1. Select the desired shape tool
2. Click on players to create the shape
3. Click the "Stop Tool" button when finished
4. To create additional shapes:
   - Ensure current shapes are toggled off
   - Create new shapes
   - Use the toggle feature to show/hide all shapes as needed
5. To reset all tools, select "Reset Tools" from the Tool dropdown menu

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

### Mouse Controls
- Click and drag players to move them
- Click players when using shape tools
- Click and drag the ball when visible

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
- Team visibility toggle functionality
- Multiple line tools (second and third variants)
- Improved shape tool interaction without requiring toggle-off of current shapes
- Player number display optimization
- Mobile interface refinements

## ⚠️ Beta Version Notice

This is currently a beta version (0.9.0). While fully functional, you may encounter:
- Minor visual glitches during rapid movements
- Performance optimizations in progress
- Additional features being implemented
- Reduced drag performance when player numbers are enabled
- Mobile interface refinements

Please report any issues through Replit's comments section.

## 👨‍💻 Author

Created by spyderkam

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/spyderkam/Tactics-Board/blob/main/LICENSE) file for details.

---
*Last updated: 2024*
