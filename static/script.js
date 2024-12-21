
const socket = io();
const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
let dragging = false;
let selectedPlayer = null;
let showBall = false;
let showNumbers = false;
let show_triangle = false;
let show_lines = false;
let show_triangle2 = false;
let lastMousePos = { x: 0, y: 0 };
const throttleDelay = 16; // ~60fps
let lastUpdate = 0;
canvas.addEventListener('mousedown', (e) => {
  const toolActive = showBall || show_triangle || show_triangle2 || show_lines;
  if (toolActive) {
    handleMouseDown(e, true);
  } else {
    handleMouseDown(e, false);
  }
});
canvas.addEventListener('mousemove', throttle(handleMouseMove, 30));
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

function toggleTriangle2() {
  socket.emit('toggle_triangle2');
}

function handleMouseDown(e, isDoubleClick) {
  const rect = canvas.getBoundingClientRect();
  const x = (e.clientX - rect.left) * (canvas.width / rect.width);
  const y = (e.clientY - rect.top) * (canvas.height / rect.height);
  socket.emit('check_click', {x: x, y: y, isDoubleClick: isDoubleClick});
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
  if (!showBall && !show_triangle && !show_triangle2 && !show_lines) {
    dragging = true;
    selectedPlayer = data;
  } else {
    selectedPlayer = null;
    dragging = false;
  }
});

function changeFormation(team) {
  const formation = document.getElementById(team + 'FormationSelect').value;
  if (formation !== team) {
    socket.emit('change_formation', { formation: formation, team: team });
  }
}
function toggleLines() {
  show_lines = !show_lines;
  socket.emit('toggle_lines');
}

function toggleBall() {
  showBall = !showBall;
  socket.emit('toggle_ball');
}

function toggleTriangle() {
  show_triangle = !show_triangle;
  socket.emit('toggle_triangle');
}

function toggleTriangle2() {
  show_triangle2 = !show_triangle2;
  socket.emit('toggle_triangle2');
}

function stopTool() {
  socket.emit('stop_tool');
}

socket.on('tool_stopped', function(data) {
  showBall = data.show_ball;
  show_triangle = data.show_triangle1;
  show_triangle2 = data.show_triangle2;
  show_lines = data.show_lines;
});

document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'l') {
    toggleLines();
  } else if (e.key.toLowerCase() === 's') {
    stopTool();
  }
});
