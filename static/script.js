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
let activeTool = null;
let lineToolLocked = false;

function handleToolSelect(value) {
  switch(value) {
    case 'numbers': toggleNumbers(); break;
    case 'triangle': toggleTriangle(); break;
    case 'triangle2': toggleTriangle2(); break;
    case 'lines': toggleLines(); break;
    case 'reset': resetTools(); break;
  }
  document.getElementById('toolsSelect').selectedIndex = 0;
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

function handleMouseDown(e) {
  const rect = canvas.getBoundingClientRect();
  const x = (e.clientX - rect.left) * (canvas.width / rect.width);
  const y = (e.clientY - rect.top) * (canvas.height / rect.height);
  socket.emit('check_click', {x: x, y: y, isToolActive: show_triangle || show_triangle2 || show_lines});
}

function handleMouseMove(e) {
  if (!dragging || !selectedPlayer) return;
  
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  
  let clientX = e.clientX;
  let clientY = e.clientY;
  
  if (e.touches) {
    clientX = e.touches[0].clientX;
    clientY = e.touches[0].clientY;
  }
  
  const x = Math.max(0, Math.min(canvas.width, (clientX - rect.left) * scaleX));
  const y = Math.max(0, Math.min(canvas.height, (clientY - rect.top) * scaleY));

  window.requestAnimationFrame(() => {
    socket.emit('move_player', {
      x: Math.round(x * 100) / 100,
      y: Math.round(y * 100) / 100,
      team: selectedPlayer.team,
      index: selectedPlayer.index
    });
  });
}

function toggleLines() {
  show_lines = !show_lines;
  activeTool = show_lines ? 'lines' : null;
  if (show_lines) {
    show_triangle = false;
    show_triangle2 = false;
    show_ball = false;
  }
  socket.emit('toggle_lines');
}

function toggleBall() {
  show_ball = !show_ball;
  activeTool = show_ball ? 'ball' : null;
  if (show_ball) {
    show_triangle = false;
    show_triangle2 = false;
    show_lines = false;
  }
  socket.emit('toggle_ball');
}

function toggleNumbers() {
  showNumbers = !showNumbers;
  dragging = false;
  socket.emit('toggle_numbers');
}

function toggleTriangle() {
  show_triangle = !show_triangle;
  activeTool = show_triangle ? 'triangle' : null;
  if (show_triangle) {
    show_triangle2 = false;
    show_lines = false;
    show_ball = false;
  }
  socket.emit('toggle_triangle');
}

function toggleTriangle2() {
  show_triangle2 = !show_triangle2;
  activeTool = show_triangle2 ? 'triangle2' : null;
  if (show_triangle2) {
    show_triangle = false;
    show_lines = false;
    show_ball = false;
  }
  socket.emit('toggle_triangle2');
}

function stopTool() {
  const wasShowingLines = show_lines;
  activeTool = null;
  socket.emit('stop_tool', { preserveLines: wasShowingLines });
}

function toggleShapes() {
  socket.emit('toggle_shapes');
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

function changeFormation(team) {
  const select = document.getElementById(team + 'FormationSelect');
  const formation = select.options[select.selectedIndex].text;
  if (formation !== team + ' Team:') {
    socket.emit('change_formation', { formation: formation, team: team });
  }
}

function resetBoard() {
  lineToolLocked = false;
  const blueSelect = document.getElementById('blueFormationSelect');
  const redSelect = document.getElementById('redFormationSelect');
  socket.emit('reset_board', {
    blueFormation: blueSelect.options[blueSelect.selectedIndex].text === 'Blue Team:' ? '4-3-3' : blueSelect.options[blueSelect.selectedIndex].text,
    redFormation: redSelect.options[redSelect.selectedIndex].text === 'Red Team:' ? '3-4-3' : redSelect.options[redSelect.selectedIndex].text
  });
}

canvas.addEventListener('mousedown', handleMouseDown);
canvas.addEventListener('mousemove', handleMouseMove);
canvas.addEventListener('mouseup', () => {
  dragging = false;
  selectedPlayer = null;
});

// Add touch events for mobile
canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  handleMouseDown({clientX: touch.clientX, clientY: touch.clientY});
});

canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  handleMouseMove({clientX: touch.clientX, clientY: touch.clientY});
});

canvas.addEventListener('touchend', () => {
  dragging = false;
  selectedPlayer = null;
});
canvas.addEventListener('mouseleave', () => {
  dragging = false;
  selectedPlayer = null;
});


socket.on('board_update', function(data) {
  const img = new Image();
  img.onload = function() {
    ctx.drawImage(img, 0, 0);
  };
  img.src = 'data:image/png;base64,' + data.image;
});

socket.on('tool_stopped', function(data) {
  if (activeTool !== 'ball') {
    show_triangle = false;
    show_triangle2 = false;
    show_lines = false;
    activeTool = null;
  }
});

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

socket.emit('get_formations');

socket.on('player_selected', function(data) {
  dragging = true;
  selectedPlayer = data;
});