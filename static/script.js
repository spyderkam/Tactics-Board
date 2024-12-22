function handleToolSelect(value) {
  switch(value) {
    case 'numbers':
      toggleNumbers();
      break;
    case 'triangle':
      toggleTriangle();
      break;
    case 'triangle2':
      toggleTriangle2();
      break;
    case 'lines':
      toggleLines();
      break;
    case 'reset':
      resetTools();
      break;
  }
  // Reset dropdown to default option
  document.getElementById('toolsSelect').selectedIndex = 0;
}

const socket = io();
const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
let dragging = false;
let selectedPlayer = null;
let show_ball = false;
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

function resetTools() {
  lineToolLocked = false;
  show_lines = false;
  show_triangle = false;
  show_triangle2 = false;
  show_ball = false;
  line_points = [];
  activeTool = null;
  socket.emit('reset_triangle');
}

socket.on('player_selected', function(data) {
  selectedPlayer = data;
  if (showNumbers) {
    handleNumberEdit(null, data);
  } else {
    dragging = true;
    lastMousePos = { x: 0, y: 0 };
  }
});

canvas.addEventListener('mousedown', (e) => {
  handleMouseDown(e, false);
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

  socket.emit('move_player', {x: x, y: y, team: selectedPlayer.team, index: selectedPlayer.index});
  lastMousePos = { x, y };
  lastUpdate = now;
}

function toggleLines() {
  if (!lineToolLocked) {
    show_lines = !show_lines;
    if (show_lines) {
      activeTool = 'lines';
      show_triangle = false;
      show_triangle2 = false;
      show_ball = false;
    } else {
      activeTool = null;
    }
    socket.emit('toggle_lines');
  }
}

function toggleBall() {
  show_ball = !show_ball;
  if (show_ball) {
    activeTool = 'ball';
    show_triangle = false;
    show_triangle2 = false;
    show_lines = false;
  } else {
    activeTool = null;
  }
  socket.emit('toggle_ball');
}

function toggleNumbers() {
  showNumbers = !showNumbers;
  dragging = false;  // Prevent dragging when numbers are shown
  socket.emit('toggle_numbers');
}

function handleNumberEdit(e, playerData) {
  const newNumber = prompt('Enter new number:', '');
  if (newNumber !== null && !isNaN(newNumber) && newNumber.trim() !== '') {
    socket.emit('update_player_number', {
      team: playerData.team,
      index: playerData.index,
      number: parseInt(newNumber)
    });
  }
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
  const blueSelect = document.getElementById('blueFormationSelect');
  const redSelect = document.getElementById('redFormationSelect');
  const blueFormation = blueSelect.options[blueSelect.selectedIndex].text;
  const redFormation = redSelect.options[redSelect.selectedIndex].text;
  socket.emit('reset_board', {
    blueFormation: blueFormation === 'Blue Team:' ? '4-3-3' : blueFormation,
    redFormation: redFormation === 'Red Team:' ? '3-4-3' : redFormation
  });
}

function resetTools() {
  lineToolLocked = false;
  show_lines = false;
  show_triangle = false;
  show_triangle2 = false;
  show_ball = false;
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
  selectedPlayer = data;
  if (showNumbers) {
    handleNumberEdit(null, data);
  } else {
    dragging = true;
    lastMousePos = { x: 0, y: 0 };
  }
});

socket.on('tool_stopped', function(data) {
  if (activeTool !== 'ball') {
    show_triangle = false;
    show_triangle2 = false;
    show_lines = false;
    activeTool = null;
  }
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