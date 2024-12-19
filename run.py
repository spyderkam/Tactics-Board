
from flask import Flask, Response, render_template_string, request
from flask_socketio import SocketIO, emit
from main import SCREEN, main, BLUE_TEAM, RED_TEAM, BALL_POS, WIDTH, HEIGHT, draw_player, WHITE
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
    <div class="controls">
        <button onclick="toggleBall()">Toggle Ball (B)</button>
        <button onclick="toggleNumbers()">Toggle Numbers (N)</button>
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

        canvas.addEventListener('mousedown', handleMouseDown);
        canvas.addEventListener('mousemove', handleMouseMove);
        canvas.addEventListener('mouseup', () => {
            dragging = false;
            selectedPlayer = null;
        });

        function handleMouseDown(e) {
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left) * (canvas.width / rect.width);
            const y = (e.clientY - rect.top) * (canvas.height / rect.height);
            socket.emit('check_click', {x: x, y: y});
        }

        function handleMouseMove(e) {
            if (!dragging) return;
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left) * (canvas.width / rect.width);
            const y = (e.clientY - rect.top) * (canvas.height / rect.height);
            socket.emit('move_player', {x: x, y: y, team: selectedPlayer.team, index: selectedPlayer.index});
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

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('check_click')
def check_click(data):
    global BLUE_TEAM, RED_TEAM
    x, y = data['x'], data['y']
    
    for i, pos in enumerate(BLUE_TEAM):
        if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
            emit('player_selected', {'team': 'blue', 'index': i})
            return
            
    for i, pos in enumerate(RED_TEAM):
        if ((x - pos[0])**2 + (y - pos[1])**2)**0.5 < 15:
            emit('player_selected', {'team': 'red', 'index': i})
            return

@socketio.on('move_player')
def move_player(data):
    global BLUE_TEAM, RED_TEAM
    x, y = data['x'], data['y']
    team = data['team']
    index = data['index']
    
    if team == 'blue':
        BLUE_TEAM[index] = [x, y]
    else:
        RED_TEAM[index] = [x, y]
    
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

@socketio.on('reset_board')
def reset_board():
    global BLUE_TEAM, RED_TEAM, BALL_POS
    from main import ORIGINAL_BLUE, ORIGINAL_RED
    BLUE_TEAM[:] = [pos[:] for pos in ORIGINAL_BLUE]
    RED_TEAM[:] = [pos[:] for pos in ORIGINAL_RED]
    BALL_POS[:] = [WIDTH//2, HEIGHT//2]
    update_board()

def update_board():
    global show_numbers, show_ball
    SCREEN.fill((34, 139, 34))
    pygame.draw.rect(SCREEN, WHITE, (80, 60, WIDTH-160, HEIGHT-120), 2)
    pygame.draw.line(SCREEN, WHITE, (WIDTH//2, 60), (WIDTH//2, HEIGHT-60), 2)
    pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 85, 2)
    pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 6)
    pygame.draw.rect(SCREEN, WHITE, (80, 210, 180, 300), 2)
    pygame.draw.rect(SCREEN, WHITE, (WIDTH-260, 210, 180, 300), 2)
    pygame.draw.rect(SCREEN, WHITE, (80, 270, 72, 180), 2)
    pygame.draw.rect(SCREEN, WHITE, (WIDTH-152, 270, 72, 180), 2)

    for i, pos in enumerate(BLUE_TEAM, 1):
        draw_player(SCREEN, pos, (0, 0, 255), i, show_numbers)
    for i, pos in enumerate(RED_TEAM, 1):
        draw_player(SCREEN, pos, (255, 0, 0), i, show_numbers)

    if show_ball:
        pygame.draw.circle(SCREEN, (0, 0, 0), BALL_POS, 12)

    buffer = io.BytesIO()
    pygame.image.save(SCREEN, buffer, 'PNG')
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.getvalue()).decode()
    emit('board_update', {'image': base64_image}, broadcast=True)

if __name__ == '__main__':
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    socketio.run(app, host='0.0.0.0', port=80)
