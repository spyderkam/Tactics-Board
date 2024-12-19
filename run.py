#!/user/bin/env python3

__author__ = "spyderkam"

from flask import Flask, Response, render_template_string
from main import SCREEN, main
import base64
import io
import os
import pygame

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <title>Tactics Board</title>
</head>
<body style="text-align: center;">
  <h1>Tactics Board</h1>
  <img src="/board" style="max-width: 100%; height: auto;">
  <p>For interactive features like dragging players and using keyboard shortcuts (B, N, R, T, Y), please use this project directly in the Replit workspace editor.</p>
</body>
</html>
'''

@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)

@app.route('/board')
def board():
  # Initialize Pygame headlessly
  os.environ['SDL_VIDEODRIVER'] = 'dummy'
  pygame.init()
    
  # Run one frame of the game
  SCREEN.fill((34, 139, 34))  # Green background
    
  # Convert the surface to a response
  data = pygame.image.tostring(SCREEN, 'RGB')
  buffer = io.BytesIO()
  pygame.image.save(buffer, data, 'PNG')
  buffer.seek(0)
    
  return Response(buffer.getvalue(), mimetype='image/png')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
