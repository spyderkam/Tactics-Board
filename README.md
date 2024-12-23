
# Tactics Board

A real-time interactive soccer tactics board built with Python and JavaScript.

## Features

- Interactive soccer field with draggable players
- Multiple formation presets (4-3-3, 4-4-2, 4-2-3-1, etc.)
- Team management (toggle visibility, change formations)
- Drawing tools:
  - Two triangle tools with different colors
  - Line tool for movement paths
  - Player numbers toggle
- Movable ball object
- Real-time updates for collaborative use

## Getting Started

1. Click "Run" to start the application
2. Select formations for both teams using the dropdown menus
3. Use the Tools menu to access drawing features
4. Use the Objects menu to toggle ball and team visibility

## Controls

### Team Management
- Use formation dropdowns to change team layouts
- Toggle team visibility in the Objects menu
- Reset button returns teams to default positions

### Drawing Tools
1. Select a tool from the Tools dropdown:
   - Numbers: Toggle player numbers
   - Triangle 1: Orange semi-transparent triangle
   - Triangle 2: Purple semi-transparent triangle
   - Lines: Create movement paths
2. Click on players to create shapes
3. Use "Stop Tool" to finish drawing
4. "Toggle Shapes" shows/hides all shapes
5. Reset Tool clears all shapes

### Player Movement
- Click and drag players to move them
- When numbers are displayed, ensure clean clicks on players

## Technical Details

- Backend: Python (Flask, Pygame, SocketIO)
- Frontend: JavaScript, HTML5 Canvas
- Real-time updates via WebSocket
- Canvas resolution: 1920x1080

## Known Issues

- Dragging performance may decrease with player numbers enabled
- Mobile experience needs optimization
- Some shape tool interactions require refinement

## Future Updates

- Additional formation options
- Multiple line tools
- Team color customization
- Shape tool improvements
- Mobile optimization

## Version

Current version: 0.9.0 (Beta)

## Author

Created by spyderkam

## License

This project is licensed under the MIT License - see the LICENSE file for details.
