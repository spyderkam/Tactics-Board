
from flask import Flask, Response, render_template_string, request
from main import SCREEN, main
import base64
import io
import os
import pygame
import json

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tactics Board</title>
    <style>
        .controls { margin: 20px 0; }
        button { margin: 0 10px; padding: 8px 16px; }
    </style>
</head>
<body style="text-align: center;">
    <h1>Tactics Board</h1>
    <div class="controls">
        <button onclick="sendCommand('toggle_ball')">Toggle Ball (B)</button>
        <button onclick="sendCommand('toggle_numbers')">Toggle Numbers (N)</button>
        <button onclick="sendCommand('reset')">Reset (R)</button>
    </div>
    <img id="board" src="/board" style="max-width: 100%; height: auto;">
    <script>
        function sendCommand(cmd) {
            fetch('/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: cmd})
            }).then(() => {
                document.getElementById('board').src = '/board?' + new Date().getTime();
            });
        }
        
        setInterval(() => {
            document.getElementById('board').src = '/board?' + new Date().getTime();
        }, 1000);
    </script>
</body>
</html>
'''

# Global state
show_numbers = False
show_ball = False

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/command', methods=['POST'])
def command():
    global show_numbers, show_ball
    cmd = request.json.get('command')
    if cmd == 'toggle_ball':
        show_ball = not show_ball
    elif cmd == 'toggle_numbers':
        show_numbers = not show_numbers
    elif cmd == 'reset':
        show_ball = False
        show_numbers = False
    return 'OK'

@app.route('/board')
def board():
    global show_numbers, show_ball
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    
    SCREEN.fill((34, 139, 34))
    
    # Draw the board state using main.py drawing functions
    # This is a simplified version - you'll need to adapt the main.py drawing code
    pygame.draw.rect(SCREEN, (255, 255, 255), (80, 60, 1920-160, 1080-120), 2)
    
    # Convert surface to response
    buffer = io.BytesIO()
    pygame.image.save(SCREEN, buffer, 'PNG')
    buffer.seek(0)
    
    return Response(buffer.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
