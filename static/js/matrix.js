let matrixInterval;
function startMatrix() {
  const c   = document.getElementById('matrix-canvas'),
        ctx = c.getContext('2d');
  c.width  = innerWidth;
  c.height = innerHeight;

  const letters  = '01',
        fontSize = 16,
        cols     = Math.floor(c.width / fontSize),
        drops    = Array(cols).fill(0);

  function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle = '#e67e68';
    ctx.font = fontSize + 'px monospace';
    drops.forEach((d,i) => {
      const char = letters[Math.floor(Math.random()*letters.length)];
      ctx.fillText(char, i*fontSize, d*fontSize);
      drops[i] = (d*fontSize > c.height || Math.random()>0.975) ? 0 : d+1;
    });
  }

  clearInterval(matrixInterval);
  matrixInterval = setInterval(draw, 50);
  window.onresize = () => {
    c.width  = innerWidth;
    c.height = innerHeight;
  };
}

function stopMatrix() {
  clearInterval(matrixInterval);
  const c = document.getElementById('matrix-canvas');
  c.getContext('2d').clearRect(0,0,c.width,c.height);
}