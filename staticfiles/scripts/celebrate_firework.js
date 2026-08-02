const canvas = document.getElementById('fireworkCanvas');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

const colors = ['#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1', '#ff9ff3', '#f9ca24'];

class Particle {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    this.color = color;
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 4 + 2;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed;
    this.alpha = 1;
    this.gravity = 0.05;
    this.friction = 0.98;
    this.size = Math.random() * 2 + 1.5;
  }
  update() {
    this.vx *= this.friction;
    this.vy *= this.friction;
    this.vy += this.gravity;
    this.x += this.vx;
    this.y += this.vy;
    this.alpha -= 0.015;
  }
  draw() {
    ctx.save();
    ctx.globalAlpha = Math.max(this.alpha, 0);
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
}

let particles = [];
let animating = false;

function createBurst(x, y) {
  const color = colors[Math.floor(Math.random() * colors.length)];
  const count = 40;
  for (let i = 0; i < count; i++) {
    particles.push(new Particle(x, y, color));
  }
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  particles = particles.filter(p => p.alpha > 0);
  particles.forEach(p => {
    p.update();
    p.draw();
  });

  if (particles.length > 0) {
    requestAnimationFrame(animate);
  } else {
    animating = false;
  }
}

let fireworkInterval = null;

function fireOneBurst() {
  const w = canvas.width;
  const h = canvas.height;
  const x = w / 2 + (Math.random() - 0.5) * w * 0.6;
  const y = h * 0.3 + (Math.random() - 0.5) * h * 0.2;
  createBurst(x, y);
  if (!animating) {
    animating = true;
    animate();
  }
}

function startCelebration() {
  if (fireworkInterval) return;
  fireOneBurst();
  fireworkInterval = setInterval(fireOneBurst, 350);
}

function stopCelebration() {
  clearInterval(fireworkInterval);
  fireworkInterval = null;
}