#!/user/bin/env python3

__author__ = "Claude 3.5 Sonnet V2"

from flask import Flask, Response, render_template_string, request
from flask_socketio import SocketIO, emit
from main import SCREEN, main, BLUE_TEAM, RED_TEAM, BALL_POS, WIDTH, HEIGHT, draw_player, WHITE, triangle_points, draw_triangle
import base64
import io
import os
import pygame
import json

app = Flask(__name__)
socketio = SocketIO(app)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <title>Tactics Board</title>
  <style>
    .controls { margin: 20px 0; }
    button { margin: 0 10px; padding: 8px 16px; }
    canvas { border: 1px solid #ccc; }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body style="text-align: center;">
  <h1>Tactics Board</h1>
  <h2>@spyderkam</h2>
  <div class="controls">
    <button onclick="toggleBall()">Toggle Ball (B)</button>
    <button onclick="toggleNumbers()">Toggle Numbers (N)</button>
    <button onclick="toggleTriangle()">Toggle Triangle (T)</button>
    <button onclick="resetTriangle()">Reset Triangle (Y)</button>
    <button onclick="resetBoard()">Reset (R)</button>
  </div>
  <canvas id="board" width="1920" height="1080" style="max-width: 100%; height: auto;"></canvas>
  <script>
    const socket = io();
    const canvas = document.getElementById('board');
    const ctx = canvas.getContext('2d');
    let dragging = false;
    let selectedPlayer = null;
    let showBall = false;
    let showNumbers = false;
    let show_triangle = false;
    let lastMousePos = { x: 0, y: 0 };
    const throttleDelay = 16; // ~60fps
    let lastUpdate = 0;

    canvas.addEventListener('mousedown', (e) => {
      handleMouseDown(e);
      dragging = true;
    });
    canvas.addEventListener('mousemove', throttle(handleMouseMove, 30)); // Throttle mousemove updates
    canvas.addEventListener('mouseup', () => {
      dragging = false;
      selectedPlayer = null;
    });
    canvas.addEventListener('mouseleave', () => {
      dragging = false;
      selectedPlayer = null;
    });

    function throttle(func, limit) {
      let inThrottle;
      return function(...args) {
        if (!inThrottle) {
          func.apply(this, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      }
    }

    function toggleTriangle() {
      socket.emit('toggle_triangle');
    }

    function handleMouseDown(e) {
      const rect = canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left) * (canvas.width / rect.width);
      const y = (e.clientY - rect.top) * (canvas.height / rect.height);
      socket.emit('check_click', {x: x, y: y});
    }

    function handleMouseMove(e) {
      if (!dragging || !selectedPlayer) return;
      
      const now = Date.now();
      if (now - lastUpdate < throttleDelay) return;
      
      const rect = canvas.getBoundingClientRect();
      const x = Math.max(0, Math.min(canvas.width, (e.clientX - rect.left) * (canvas.width / rect.width)));
      const y = Math.max(0, Math.min(canvas.height, (e.clientY - rect.top) * (canvas.height / rect.height)));
      
      if (Math.abs(x - lastMousePos.x) > 1 || Math.abs(y - lastMousePos.y) > 1) {
        socket.emit('move_player', {x: x, y: y, team: selectedPlayer.team, index: selectedPlayer.index});
        lastMousePos = { x, y };
        lastUpdate = now;
      }
    }

    function toggleBall() {
      socket.emit('toggle_ball');
    }

    function toggleNumbers() {
      socket.emit('toggle_numbers');
    }

    function resetBoard() {
      socket.emit('reset_board');
    }

    function resetTriangle() {
      socket.emit('reset_triangle');
    }

    socket.on('board_update', function(data) {
      const img = new Image();
      img.onload = function() {
        ctx.drawImage(img, 0, 0);
      };
      img.src = 'data:image/png;base64,' + data.image;
    });

    socket.on('player_selected', function(data) {
      dragging = true;
      selectedPlayer = data;
    });
  </script>
</body>
</html>
'''

show_numbers = False
show_ball = False
show_triangle = False

@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)

@socketio.on('check_click')
def check_click(data):
  global BLUE_TEAM, RED_TEAM, triangle_points, BALL_POS, show_ball
  x, y = data['x'], data['y']
    
  # Check if ball is clicked first when visible
  if show_ball and ((x - BALL_POS[0])**2 + (y - BALL_POS[1])**2)**0.5 < 15:
    emit('player_selected', {'team': 'ball', 'index': 0})
    return
            
  for i, pos in enumerate(BLUE_TEAM):
    if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
      emit('player_selected', {'team': 'blue', 'index': i})
      if len(triangle_points) < 3:
        triangle_points.append(BLUE_TEAM[i])
        update_board()
      return
            
  for i, pos in enumerate(RED_TEAM):
    if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
      emit('player_selected', {'team': 'red', 'index': i})
      if len(triangle_points) < 3:
        triangle_points.append(RED_TEAM[i])
        update_board()
      return

@socketio.on('move_player')
def move_player(data):
  global BLUE_TEAM, RED_TEAM, BALL_POS
  x, y = data['x'], data['y']
  team = data['team']
  index = data['index']
    
  global triangle_points
  new_pos = [x, y]
    
  if team == 'ball':
    BALL_POS[0] = x
    BALL_POS[1] = y
  elif team == 'blue':
    old_pos = BLUE_TEAM[index]
    BLUE_TEAM[index] = new_pos
    if old_pos in triangle_points:
      triangle_points[triangle_points.index(old_pos)] = new_pos
  else:
    old_pos = RED_TEAM[index]
    RED_TEAM[index] = new_pos
    if old_pos in triangle_points:
      triangle_points[triangle_points.index(old_pos)] = new_pos
    
  update_board()

@socketio.on('toggle_ball')
def toggle_ball():
  global show_ball
  show_ball = not show_ball
  update_board()

@socketio.on('toggle_numbers')
def toggle_numbers():
  global show_numbers
  show_numbers = not show_numbers
  update_board()

@socketio.on('toggle_triangle')
def toggle_triangle_handler():
  global show_triangle, triangle_points
  if len(triangle_points) == 3:
    show_triangle = not show_triangle
  else:
    triangle_points.clear()
    show_triangle = False
  update_board()

@socketio.on('reset_triangle')
def reset_triangle():
  global triangle_points, show_triangle
  triangle_points.clear()
  show_triangle = False
  update_board()

@socketio.on('reset_board')
def reset_board():
  global BLUE_TEAM, RED_TEAM, BALL_POS, triangle_points, show_triangle
  from main import ORIGINAL_BLUE, ORIGINAL_RED
  BLUE_TEAM[:] = [pos[:] for pos in ORIGINAL_BLUE]
  RED_TEAM[:] = [pos[:] for pos in ORIGINAL_RED]
  BALL_POS[:] = [WIDTH//2, HEIGHT//2]
  triangle_points.clear()
  show_triangle = False
  update_board()

def update_board():
  global show_numbers, show_ball, show_triangle
  SCREEN.fill((34, 139, 34))
  pygame.draw.rect(SCREEN, WHITE, (80, 60, WIDTH-160, HEIGHT-120), 2)
  pygame.draw.line(SCREEN, WHITE, (WIDTH//2, 60), (WIDTH//2, HEIGHT-60), 2)
  pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 85, 2)
  pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 6)
  pygame.draw.rect(SCREEN, WHITE, (80, HEIGHT//2-240, 240, 480), 2)          # Left penalty area
  pygame.draw.rect(SCREEN, WHITE, (WIDTH-320, HEIGHT//2-240, 240, 480), 2)   # Right penalty area
  pygame.draw.rect(SCREEN, WHITE, (80, HEIGHT//2-90, 72, 180), 2)            # Left goal area
  pygame.draw.rect(SCREEN, WHITE, (WIDTH-152, HEIGHT//2-90, 72, 180), 2)     # Right goal area

  for i, pos in enumerate(BLUE_TEAM, 1):
    draw_player(SCREEN, pos, (0, 0, 255), i, show_numbers)
  for i, pos in enumerate(RED_TEAM, 1):
    draw_player(SCREEN, pos, (255, 0, 0), i, show_numbers)

  if show_ball:
    pygame.draw.circle(SCREEN, (0, 0, 0), BALL_POS, 12)
        
  if show_triangle and len(triangle_points) == 3:
    draw_triangle(SCREEN, triangle_points, None)

  buffer = io.BytesIO()
  pygame.image.save(SCREEN, buffer, 'PNG')
  buffer.seek(0)
  base64_image = base64.b64encode(buffer.getvalue()).decode()
  emit('board_update', {'image': base64_image}, broadcast=True)

if __name__ == '__main__':
  os.environ['SDL_VIDEODRIVER'] = 'dummy'
  pygame.init()
  socketio.run(app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)
  