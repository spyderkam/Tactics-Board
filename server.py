#!/user/bin/env python3

__author__ = "Claude 3.5 Sonnet V2"

from flask import Flask, Response, render_template_string, request
from flask_socketio import SocketIO, emit
from main import SCREEN, main, BLUE_TEAM, RED_TEAM, BALL_POS, WIDTH, HEIGHT, draw_player, WHITE, triangle_points, triangle_points2, Shape
import base64
import io
import os
import pygame
import json

app = Flask(__name__, static_url_path='/static', static_folder='static')
socketio = SocketIO(app)

# Read the HTML file
with open('tactics_board.html', 'r', encoding='utf-8') as file:
  HTML_TEMPLATE = file.read()

show_numbers = False
show_ball = False
show_triangle1 = False
show_triangle2 = False
show_lines = False # Added to track line visibility

@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)

@socketio.on('check_click')
def check_click(data):
  global BLUE_TEAM, RED_TEAM, triangle_points, triangle_points2, BALL_POS, show_ball, show_lines, line_points
  x, y = data['x'], data['y']
  isDoubleClick = data.get('isDoubleClick', False)
    
  # Check if ball is clicked first when visible
  if show_ball and ((x - BALL_POS[0])**2 + (y - BALL_POS[1])**2)**0.5 < 15:  # Matches player click detection radius
    emit('player_selected', {'team': 'ball', 'index': 0})
    return
            
  for i, pos in enumerate(BLUE_TEAM):
    if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
      emit('player_selected', {'team': 'blue', 'index': i})
      if show_lines and isDoubleClick:
        line_points.append([x for x in BLUE_TEAM[i]])
        update_board()
      elif show_triangle2 and isDoubleClick:
        if len(triangle_points2) < 3:
          triangle_points2.append(BLUE_TEAM[i])
          update_board()
      elif isDoubleClick:
        if len(triangle_points) < 3:
          triangle_points.append([x for x in BLUE_TEAM[i]])
          update_board()
      return
            
  for i, pos in enumerate(RED_TEAM):
    if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
      emit('player_selected', {'team': 'red', 'index': i})
      if show_lines and isDoubleClick:
        line_points.append([x for x in RED_TEAM[i]])
        update_board()
      elif show_triangle2 and isDoubleClick:
        if len(triangle_points2) < 3:
          triangle_points2.append(RED_TEAM[i])
          update_board()
      elif isDoubleClick:
        if len(triangle_points) < 3:
          triangle_points.append([x for x in RED_TEAM[i]])
          update_board()
      return

@socketio.on('move_player')
def move_player(data):
  global BLUE_TEAM, RED_TEAM, BALL_POS, line_points
  x, y = data['x'], data['y']
  team = data['team']
  index = data['index']
    
  global triangle_points, triangle_points2
  new_pos = [x, y]
    
  if team == 'ball':
    BALL_POS[0] = x
    BALL_POS[1] = y
  elif team == 'blue':
    old_pos = BLUE_TEAM[index]
    BLUE_TEAM[index] = new_pos
    if old_pos in triangle_points:
      triangle_points[triangle_points.index(old_pos)] = new_pos
    if old_pos in triangle_points2:
      triangle_points2[triangle_points2.index(old_pos)] = new_pos
    for i, point in enumerate(line_points):
      if point[0] == old_pos[0] and point[1] == old_pos[1]:
        line_points[i] = [x for x in new_pos]
  else:
    old_pos = RED_TEAM[index]
    RED_TEAM[index] = new_pos
    if old_pos in triangle_points:
      triangle_points[triangle_points.index(old_pos)] = new_pos
    if old_pos in triangle_points2:
      triangle_points2[triangle_points2.index(old_pos)] = new_pos
    for i, point in enumerate(line_points):
      if point[0] == old_pos[0] and point[1] == old_pos[1]:
        line_points[i] = [x for x in new_pos]
    
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
  global show_triangle1, triangle_points
  if len(triangle_points) == 3:
    show_triangle1 = not show_triangle1
  else:
    triangle_points.clear()
    show_triangle1 = False
  update_board()

@socketio.on('toggle_triangle2')
def toggle_triangle2_handler():
  global show_triangle2, triangle_points2
  if len(triangle_points2) < 3:
    show_triangle2 = True
  elif len(triangle_points2) == 3:
    show_triangle2 = not show_triangle2
  else:
    triangle_points2.clear()
    show_triangle2 = False
  update_board()

@socketio.on('reset_triangle')
def reset_triangle():
  global triangle_points, triangle_points2, show_triangle1, show_triangle2, show_lines, line_points
  triangle_points.clear()
  triangle_points2.clear()
  show_triangle1 = False
  show_triangle2 = False
  show_lines = False
  line_points.clear()
  update_board()

@socketio.on('change_formation')
def handle_formation_change(data):
  global BLUE_TEAM, RED_TEAM
  from database import formation
  formation_data = formation(data['formation'])
  if data['team'] == 'blue':
    BLUE_TEAM[:] = [pos[:] for pos in formation_data["blue"]]
  else:
    RED_TEAM[:] = [pos[:] for pos in formation_data["red"]]
  update_board()

@socketio.on('reset_board')
def handle_reset_board():
  global BLUE_TEAM, RED_TEAM, BALL_POS, triangle_points, triangle_points2, show_triangle1, show_triangle2, show_lines, line_points
  from main import ORIGINAL_BLUE, ORIGINAL_RED
  BLUE_TEAM[:] = [pos[:] for pos in ORIGINAL_BLUE]
  RED_TEAM[:] = [pos[:] for pos in ORIGINAL_RED]
  BALL_POS[:] = [WIDTH//2, HEIGHT//2]
  triangle_points.clear()
  triangle_points2.clear()
  show_triangle1 = False
  show_triangle2 = False
  show_lines = False #Added
  line_points = [] #Added
  update_board()

@socketio.on('toggle_lines') #Added
def toggle_lines():
    global show_lines
    show_lines = not show_lines
    update_board()

def update_board():
  global show_numbers, show_ball, show_triangle1, show_triangle2, show_lines, line_points
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
    pygame.draw.circle(SCREEN, (0, 0, 0), BALL_POS, 15)
        
  if show_triangle1 and len(triangle_points) == 3:
    Shape().draw_triangle1(SCREEN, triangle_points)
  if show_triangle2 and len(triangle_points2) == 3:
    Shape().draw_triangle2(SCREEN, triangle_points2)
  if show_lines and len(line_points) > 1:
    Shape().draw_lines(SCREEN, line_points)

  buffer = io.BytesIO()
  pygame.image.save(SCREEN, buffer, 'PNG')
  buffer.seek(0)
  base64_image = base64.b64encode(buffer.getvalue()).decode()
  emit('board_update', {'image': base64_image}, broadcast=True)

if __name__ == '__main__':
  os.environ['SDL_VIDEODRIVER'] = 'dummy'
  pygame.init()
  socketio.run(app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)