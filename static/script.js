
const socket = io();
const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');

// State management
const state = {
  dragging: false,
  selectedPlayer: null,
  lastMousePos: { x: 0, y: 0 },
  activeTool: null,
  tools: {
    ball: false,
    numbers: false,
    triangle: false,
    triangle2: false,  
    lines: false,
    locked: false
  },
  teams: {
    blue: true,
    red: true
  }
};

// Tool handlers
function handleToolSelect(value) {
  const actions = {
    numbers: toggleNumbers,
    triangle: toggleTriangle,
    triangle2: toggleTriangle2,
    lines: toggleLines,
    reset: resetTools
  };
  if (actions[value]) actions[value]();
  document.getElementById('toolsSelect').selectedIndex = 0;
}

function resetTools() {
  Object.keys(state.tools).forEach(key => state.tools[key] = false);
  state.activeTool = null;
  socket.emit('reset_triangle');
}

// Mouse/Touch event handlers
function handleMouseDown(e) {
  const rect = canvas.getBoundingClientRect();
  const scale = canvas.width / rect.width;
  const x = (e.clientX - rect.left) * scale;
  const y = (e.clientY - rect.top) * scale;
  socket.emit('check_click', {
    x, y, 
    isToolActive: state.tools.triangle || state.tools.triangle2 || state.tools.lines
  });
}

function handleMouseMove(e) {
  if (!state.dragging || !state.selectedPlayer) return;
  
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

  requestAnimationFrame(() => {
    socket.emit('move_player', {
      x: Math.round(x * 100) / 100,
      y: Math.round(y * 100) / 100,
      team: state.selectedPlayer.team,
      index: state.selectedPlayer.index
    });
  });
  
  state.lastMousePos = { x, y };
}

// Tool toggles
function toggleLines() {
  state.tools.lines = !state.tools.lines;
  state.activeTool = state.tools.lines ? 'lines' : null;
  if (state.tools.lines) {
    state.tools.triangle = state.tools.triangle2 = state.tools.ball = false;
  }
  socket.emit('toggle_lines');
}

function toggleBall() {
  state.tools.ball = !state.tools.ball;
  state.activeTool = state.tools.ball ? 'ball' : null;
  if (state.tools.ball) {
    state.tools.triangle = state.tools.triangle2 = state.tools.lines = false;
  }
  socket.emit('toggle_ball');
}

function toggleNumbers() {
  state.tools.numbers = !state.tools.numbers;
  state.dragging = false;
  socket.emit('toggle_numbers');
}

function toggleTriangle() {
  state.tools.triangle = !state.tools.triangle;
  state.activeTool = state.tools.triangle ? 'triangle' : null;
  if (state.tools.triangle) {
    state.tools.triangle2 = state.tools.lines = state.tools.ball = false;
  }
  socket.emit('toggle_triangle');
}

function toggleTriangle2() {
  state.tools.triangle2 = !state.tools.triangle2;
  state.activeTool = state.tools.triangle2 ? 'triangle2' : null;
  if (state.tools.triangle2) {
    state.tools.triangle = state.tools.lines = state.tools.ball = false;
  }
  socket.emit('toggle_triangle2');
}

function stopTool() {
  const preserveLines = state.tools.lines;
  state.activeTool = null;
  socket.emit('stop_tool', { preserveLines });
}

// Formation management
function changeFormation(team) {
  const select = document.getElementById(`${team}FormationSelect`);
  const formation = select.options[select.selectedIndex].text;
  if (formation !== `${team} Team:`) {
    socket.emit('change_formation', { formation, team });
  }
}

function resetBoard() {
  state.tools.locked = false;
  const blueSelect = document.getElementById('blueFormationSelect');
  const redSelect = document.getElementById('redFormationSelect');
  socket.emit('reset_board', {
    blueFormation: blueSelect.options[blueSelect.selectedIndex].text === 'Blue Team:' ? '4-3-3' : blueSelect.options[blueSelect.selectedIndex].text,
    redFormation: redSelect.options[redSelect.selectedIndex].text === 'Red Team:' ? '3-4-3' : redSelect.options[redSelect.selectedIndex].text
  });
}

// Event listeners
canvas.addEventListener('mousedown', handleMouseDown);
canvas.addEventListener('mousemove', handleMouseMove);
canvas.addEventListener('mouseup', () => {
  state.dragging = false;
  state.selectedPlayer = null;
});
canvas.addEventListener('mouseleave', () => {
  state.dragging = false;
  state.selectedPlayer = null;
});

// Touch events
canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  handleMouseDown({clientX: e.touches[0].clientX, clientY: e.touches[0].clientY});
});

canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  handleMouseMove({clientX: e.touches[0].clientX, clientY: e.touches[0].clientY});
});

canvas.addEventListener('touchend', () => {
  state.dragging = false;
  state.selectedPlayer = null;
});

// Socket events
socket.on('board_update', (data) => {
  const img = new Image();
  img.onload = () => ctx.drawImage(img, 0, 0);
  img.src = 'data:image/png;base64,' + data.image;
});

socket.on('tool_stopped', (data) => {
  if (state.activeTool !== 'ball') {
    state.tools.triangle = false;
    state.tools.triangle2 = false;
    state.tools.lines = false;
    state.activeTool = null;
  }
});

socket.on('formations_list', (formations) => {
  const blueSelect = document.getElementById('blueFormationSelect');
  const redSelect = document.getElementById('redFormationSelect');
  blueSelect.innerHTML = '<option value="blue">Blue Team:</option>';
  redSelect.innerHTML = '<option value="red">Red Team:</option>';
  formations.forEach(formation => {
    const option = `<option value="${formation}">${formation}</option>`;
    blueSelect.innerHTML += option;
    redSelect.innerHTML += option;
  });
});

socket.on('player_selected', (data) => {
  state.dragging = true;
  state.selectedPlayer = data;
});

// Initialize formations
socket.emit('get_formations');
// Team toggle handler
function handleTeamToggle(value) {
  if (value === 'blue' || value === 'red') {
    state.teams[value] = !state.teams[value];
    socket.emit('toggle_team', { team: value, visible: state.teams[value] });
  }
  document.getElementById('teamToggleSelect').selectedIndex = 0;
}
