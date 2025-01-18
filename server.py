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
team_visibility = {'blue': True, 'red': True}
player_numbers = {'blue': [i for i in range(1, 12)], 'red': [i for i in range(1, 12)]}
line_points = []

@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)

@socketio.on('get_formations')
def get_formations():
  from database import formation
  # Get all case statements from the formation function
  import inspect
  source = inspect.getsource(formation)
  formations = [line.split('"')[1] for line in source.split('\n') if 'case "' in line]
  emit('formations_list', formations)

@socketio.on('check_click')
def check_click(data):
  global BLUE_TEAM, RED_TEAM, triangle_points, triangle_points2, BALL_POS, show_ball, show_lines, line_points
  x, y = data['x'], data['y']
  isToolClick = data.get('isToolActive', False)  # Check if a shape tool is active
    
  # Check if ball is clicked first when visible
  if show_ball and ((x - BALL_POS[0])**2 + (y - BALL_POS[1])**2)**0.5 < 15:  # Matches player click detection radius
    emit('player_selected', {'team': 'ball', 'index': 0})
    return
            
  for i, pos in enumerate(BLUE_TEAM):
    if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
      emit('player_selected', {'team': 'blue', 'index': i})
      if show_lines and isToolClick:
        line_points.append([x for x in BLUE_TEAM[i]])
        update_board()
      elif show_triangle2 and isToolClick:
        if len(triangle_points2) < 3:
          triangle_points2.append(BLUE_TEAM[i])
          update_board()
      elif isToolClick:
        if len(triangle_points) < 3:
          triangle_points.append([x for x in BLUE_TEAM[i]])
          update_board()
      return
            
  for i, pos in enumerate(RED_TEAM):
    if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
      emit('player_selected', {'team': 'red', 'index': i})
      if show_lines and isToolClick:
        line_points.append([x for x in RED_TEAM[i]])
        update_board()
      elif show_triangle2 and isToolClick:
        if len(triangle_points2) < 3:
          triangle_points2.append(RED_TEAM[i])
          update_board()
      elif isToolClick:
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
    
  # Allow movement regardless of numbers being shown

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
  if len(triangle_points) < 3:
    show_triangle1 = True
  elif len(triangle_points) == 3:
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
def handle_reset_board(data=None):
  global BLUE_TEAM, RED_TEAM, BALL_POS, triangle_points, triangle_points2, show_triangle1, show_triangle2, show_lines, line_points, player_numbers
  from database import formation
  
  blue_formation = data['blueFormation'] if data and 'blueFormation' in data else "4-3-3"
  red_formation = data['redFormation'] if data and 'redFormation' in data else "3-4-3"
  
  BLUE_TEAM[:] = [pos[:] for pos in formation(blue_formation)["blue"]]
  RED_TEAM[:] = [pos[:] for pos in formation(red_formation)["red"]]
  BALL_POS[:] = [WIDTH//2, HEIGHT//2]
  triangle_points.clear()
  triangle_points2.clear()
  show_triangle1 = False
  show_triangle2 = False
  show_lines = False
  line_points = []
  player_numbers = {'blue': [i for i in range(1, 12)], 'red': [i for i in range(1, 12)]} #reset player numbers
  update_board()

@socketio.on('toggle_lines') #Added
def toggle_lines():
    global show_lines
    show_lines = not show_lines
    update_board()

@socketio.on('stop_tool')
def stop_tool(data):
    global show_triangle1, show_triangle2, show_lines
    preserve_lines = data.get('preserveLines', False)
    show_triangle1 = False
    show_triangle2 = False
    if not preserve_lines:
        show_lines = False
    emit('tool_stopped', {'preserveLines': preserve_lines})
    update_board()

@socketio.on('update_player_number')
def update_player_number(data):
    global player_numbers
    team = data['team']
    index = data['index']
    new_number = data['number']
    if team in player_numbers and 0 <= index < len(player_numbers[team]):
        player_numbers[team][index] = new_number
    update_board()

@socketio.on('toggle_blue_team')
def toggle_blue_team():
    global team_visibility
    team_visibility['blue'] = not team_visibility['blue']
    update_board()

@socketio.on('toggle_red_team')
def toggle_red_team():
    global team_visibility
    team_visibility['red'] = not team_visibility['red']
    update_board()


def update_board():
  global show_numbers, show_ball, show_triangle1, show_triangle2, show_lines, line_points, player_numbers, team_visibility
  SCREEN.fill((34, 139, 34))
  pygame.draw.rect(SCREEN, WHITE, (80, 60, WIDTH-160, HEIGHT-120), 2)
  pygame.draw.line(SCREEN, WHITE, (WIDTH//2, 60), (WIDTH//2, HEIGHT-60), 2)
  pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 85, 2)
  pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 6)
  # Draw penalty areas
  pygame.draw.rect(SCREEN, WHITE, (80, HEIGHT//2-220, 220, 440), 2)          # Left penalty area
  pygame.draw.rect(SCREEN, WHITE, (WIDTH-300, HEIGHT//2-220, 220, 440), 2)   # Right penalty area
  
  # Draw penalty arcs
  pygame.draw.arc(SCREEN, WHITE, (220, HEIGHT//2-85, 170, 170), 4.71, 1.57, 2)  # Left arc
  pygame.draw.arc(SCREEN, WHITE, (WIDTH-390, HEIGHT//2-85, 170, 170), 1.57, 4.71, 2)  # Right arc
  
  # Draw goal areas
  pygame.draw.rect(SCREEN, WHITE, (80, HEIGHT//2-90, 60, 180), 2)            # Left goal area
  pygame.draw.rect(SCREEN, WHITE, (WIDTH-140, HEIGHT//2-90, 60, 180), 2)     # Right goal area

  if team_visibility['blue']:
    for i, pos in enumerate(BLUE_TEAM, 1):
      draw_player(SCREEN, pos, (0, 0, 255), player_numbers['blue'][i-1], show_numbers) #Use player_numbers
  if team_visibility['red']:
    for i, pos in enumerate(RED_TEAM, 1):
      draw_player(SCREEN, pos, (255, 0, 0), player_numbers['red'][i-1], show_numbers) #Use player_numbers

  if show_ball:
    pygame.draw.circle(SCREEN, (0, 0, 0), BALL_POS, 20)     # Increased ball size from 15 to 20
        
  if show_triangle1 and len(triangle_points) == 3:
    Shape().draw_triangle1(SCREEN, triangle_points)
  if show_triangle2 and len(triangle_points2) == 3:
    Shape().draw_triangle2(SCREEN, triangle_points2)
  if show_lines and len(line_points) > 1:
    Shape().draw_lines(SCREEN, line_points)

  # Add watermark with white background
  watermark_font = pygame.font.SysFont('Arial Black', 75, italic=True)
  watermark_spyder = watermark_font.render('spyder', True, (0, 0, 0))
  watermark_kam = watermark_font.render('kam', True, (255, 0, 0))
  
  watermark_width = watermark_spyder.get_width() + watermark_kam.get_width() - 11  # For more white space on the right
  watermark_height = watermark_font.get_height() + 7                               # For more white space on the bottom
  watermark_bg_surface = pygame.Surface((watermark_width, watermark_height), pygame.SRCALPHA)
  watermark_bg_surface.fill((255, 255, 255))

  SCREEN.blit(watermark_bg_surface, (100, HEIGHT - 135))
  SCREEN.blit(watermark_spyder, (100, HEIGHT - 135))
  SCREEN.blit(watermark_kam, (100 + watermark_spyder.get_width() - 7, HEIGHT - 135))
  
  # Save the screen with watermark
  buffer = io.BytesIO()
  pygame.image.save(SCREEN, buffer, 'PNG')
  buffer.seek(0)
  base64_image = base64.b64encode(buffer.getvalue()).decode()
  emit('board_update', {'image': base64_image}, broadcast=True)

@socketio.on('toggle_shapes')
def toggle_shapes():
    global show_triangle1, show_triangle2, show_lines
    if show_triangle1 or show_triangle2 or show_lines:
        show_triangle1 = False
        show_triangle2 = False
        show_lines = False
    else:
        show_triangle1 = True
        show_triangle2 = True
        show_lines = True
    update_board()

if __name__ == '__main__':
  os.environ['SDL_VIDEODRIVER'] = 'dummy'
  pygame.init()
  socketio.run(app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)