
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
let line_points = [];
let triangle_points = [];
let lastMousePos = { x: 0, y: 0 };
const throttleDelay = 16;
let lastUpdate = 0;
let activeTool = null;
let lineToolLocked = false;

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

function toggleLines() {
  if (!lineToolLocked) {
    show_lines = !show_lines;
    if (show_lines) {
      activeTool = 'lines';
      show_triangle = false;
      show_triangle2 = false;
      showBall = false;
    } else {
      activeTool = null;
    }
    socket.emit('toggle_lines');
  }
}

function toggleBall() {
  showBall = !showBall;
  if (showBall) {
    activeTool = 'ball';
    show_triangle = false;
    show_triangle2 = false;
    show_lines = false;
  }
  socket.emit('toggle_ball');
}

function toggleNumbers() {
  socket.emit('toggle_numbers');
}

function toggleTriangle() {
  show_triangle = !show_triangle;
  if (show_triangle) {
    activeTool = 'triangle';
    show_triangle2 = false;
    show_lines = false;
    showBall = false;
  } else {
    activeTool = null;
  }
  socket.emit('toggle_triangle');
}

function toggleTriangle2() {
  show_triangle2 = !show_triangle2;
  if (show_triangle2) {
    activeTool = 'triangle2';
    show_triangle = false;
    show_lines = false;
    showBall = false;
  } else {
    activeTool = null;
  }
  socket.emit('toggle_triangle2');
}

function resetBoard() {
  lineToolLocked = false;
  socket.emit('reset_board');
}

function resetTools() {
  lineToolLocked = false;
  show_lines = false;
  show_triangle = false;
  show_triangle2 = false;
  showBall = false;
  line_points = [];
  activeTool = null;
  socket.emit('reset_triangle');
}

function stopTool() {
  const wasShowingLines = show_lines;
  activeTool = null;
  socket.emit('stop_tool', { preserveLines: wasShowingLines });
}

function toggleShapes() {
  socket.emit('toggle_shapes');
}

function changeFormation(team) {
  const select = document.getElementById(team + 'FormationSelect');
  const formation = select.options[select.selectedIndex].text;
  if (formation !== team + ' Team:') {
    socket.emit('change_formation', { formation: formation, team: team });
    if (team === 'blue') {
      lastBlueFormation = formation;
    } else {
      lastRedFormation = formation;
    }
  }
}

socket.on('formations_list', function(formations) {
  const blueSelect = document.getElementById('blueFormationSelect');
  const redSelect = document.getElementById('redFormationSelect');
  
  blueSelect.innerHTML = '<option value="blue">Blue Team:</option>';
  redSelect.innerHTML = '<option value="red">Red Team:</option>';
  
  formations.forEach(formation => {
    blueSelect.innerHTML += `<option value="${formation}">${formation}</option>`;
    redSelect.innerHTML += `<option value="${formation}">${formation}</option>`;
  });
});

socket.on('board_update', function(data) {
  const img = new Image();
  img.onload = function() {
    ctx.drawImage(img, 0, 0);
  };
  img.src = 'data:image/png;base64,' + data.image;
});

socket.on('player_selected', function(data) {
  if (activeTool === null) {
    dragging = true;
    selectedPlayer = data;
  } else {
    selectedPlayer = data;
    dragging = false;
  }
});

socket.on('tool_stopped', function(data) {
  showBall = false;
  show_triangle = false;
  show_triangle2 = false;
  show_lines = false;
  activeTool = null;
});

document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'l') {
    toggleLines();
  } else if (e.key.toLowerCase() === 's') {
    stopTool();
  } else if (e.key.toLowerCase() === 'u') {
    toggleShapes();
  }
});

// Request formations when page loads
socket.emit('get_formations');
