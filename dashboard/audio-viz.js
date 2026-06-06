/* Visualisation audio légère — palette chaude MemBridge */

const AudioViz = {
  ctx: null,
  animId: null,
  active: false,

  init() {
    const canvas = document.getElementById("audio-viz");
    if (!canvas) return;
    this.ctx = canvas.getContext("2d");
    canvas.width = canvas.offsetWidth || 300;
  },

  start() {
    this.init();
    if (!this.ctx) return;
    this.active = true;
    const draw = () => {
      if (!this.active) return;
      const { ctx } = this;
      const w = ctx.canvas.width;
      const h = ctx.canvas.height;
      ctx.fillStyle = "#F0E8DC";
      ctx.fillRect(0, 0, w, h);
      const t = Date.now() / 200;
      ctx.strokeStyle = "#C44F28";
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let x = 0; x < w; x++) {
        const y = h / 2 + Math.sin(x * 0.05 + t) * 12 + Math.sin(x * 0.12 + t * 1.3) * 6;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      this.animId = requestAnimationFrame(draw);
    };
    draw();
  },

  stop() {
    this.active = false;
    if (this.animId) cancelAnimationFrame(this.animId);
    if (this.ctx) {
      this.ctx.fillStyle = "#F0E8DC";
      this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
    }
  },
};

window.AudioViz = AudioViz;
