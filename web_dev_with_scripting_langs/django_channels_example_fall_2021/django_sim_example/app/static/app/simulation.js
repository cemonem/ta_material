//https://stackoverflow.com/questions/17130395/real-mouse-position-in-canvas
function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: (evt.clientX - rect.left) / (rect.right - rect.left) * canvas.width,
        y: (evt.clientY - rect.top) / (rect.bottom - rect.top) * canvas.height
    };
}

socket = new WebSocket('ws://'+window.location.host+'/ws/simulation/');

canvas = document.getElementById('canvas');
debug_span = document.getElementById('debug');
debug_span.textContent = 'test test test';
ctx = canvas.getContext('2d');
rect_pos = null;

canvas.onclick = (evt) => {
  rect_pos = getMousePos(canvas, evt);
  socket.send(JSON.stringify(rect_pos));
};

socket.onmessage = (evt) => {
  rect_pos = JSON.parse(evt.data);
};
//https://developer.mozilla.org/en-US/docs/Games/Anatomy#building_a_main_loop_in_javascript
function simLoop() {
  window.requestAnimationFrame(simLoop);

  debug_span.textContent = JSON.stringify(rect_pos);

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillRect(rect_pos.x, rect_pos.y, 10, 10);

}

simLoop();


//ctx.fillStyle = 'green';
//ctx.fillRect(10, 10, 150, 100);
