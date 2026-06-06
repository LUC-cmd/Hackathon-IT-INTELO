/* Cerveau mémoire animé — réseau de nœuds */

const BrainViz = {
  canvas: null,
  ctx: null,
  nodes: [],
  animId: null,
  t: 0,

  init(id = "brain-canvas") {
    this.canvas = document.getElementById(id);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");
    this.resize();
    window.addEventListener("resize", () => this.resize());
    this.seedNodes(24);
    this.loop();
  },

  resize() {
    if (!this.canvas) return;
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height || 280;
  },

  seedNodes(n) {
    const w = this.canvas?.width || 400;
    const h = this.canvas?.height || 280;
    const types = ["fact", "geo", "media", "msg"];
    this.nodes = Array.from({ length: n }, (_, i) => ({
      x: w * 0.2 + Math.random() * w * 0.6,
      y: h * 0.15 + Math.random() * h * 0.7,
      r: 4 + Math.random() * 5,
      type: types[i % 4],
      phase: Math.random() * Math.PI * 2,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
    }));
  },

  setFromMemory(entries) {
    if (!entries?.length || !this.canvas) return;
    const w = this.canvas.width;
    const h = this.canvas.height;
    const types = { fact: "#2F5242", geo: "#D4922A", media: "#C44F28", msg: "#9E8E7E" };
    this.nodes = entries.slice(0, 30).map((e, i) => {
      const angle = (i / entries.length) * Math.PI * 2;
      const type = e.tags?.includes("fact") ? "fact"
        : e.tags?.includes("geo") ? "geo"
        : e.tags?.some(t => ["audio","video","vision","transcript"].includes(t)) ? "media" : "msg";
      return {
        x: w / 2 + Math.cos(angle) * (60 + i * 3),
        y: h / 2 + Math.sin(angle) * (40 + i * 2),
        r: 5 + (i % 3),
        type,
        color: types[type],
        phase: i * 0.3,
        vx: 0, vy: 0,
        label: `t${e.turn}`,
      };
    });
  },

  loop() {
    if (!this.ctx || !this.canvas) return;
    const { ctx, canvas } = this;
    const w = canvas.width;
    const h = canvas.height;
    this.t += 0.015;
    ctx.clearRect(0, 0, w, h);

    // liens
    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const a = this.nodes[i], b = this.nodes[j];
        const dist = Math.hypot(a.x - b.x, a.y - b.y);
        if (dist < 120) {
          ctx.strokeStyle = `rgba(47,82,66,${0.15 * (1 - dist / 120)})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    const colors = { fact: "#2F5242", geo: "#D4922A", media: "#C44F28", msg: "#9E8E7E" };
    this.nodes.forEach((n, i) => {
      n.x += n.vx + Math.sin(this.t + n.phase) * 0.15;
      n.y += n.vy + Math.cos(this.t + n.phase) * 0.12;
      if (n.x < 20 || n.x > w - 20) n.vx *= -1;
      if (n.y < 20 || n.y > h - 20) n.vy *= -1;
      const pulse = 1 + Math.sin(this.t * 2 + i) * 0.2;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r * pulse, 0, Math.PI * 2);
      ctx.fillStyle = n.color || colors[n.type] || "#9E8E7E";
      ctx.fill();
      ctx.strokeStyle = "#1A1714";
      ctx.lineWidth = 1.5;
      ctx.stroke();
    });

    // centre hub
    ctx.beginPath();
    ctx.arc(w / 2, h / 2, 18 + Math.sin(this.t * 3) * 3, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(196,79,40,0.15)";
    ctx.fill();
    ctx.strokeStyle = "#C44F28";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = "#1A1714";
    ctx.font = "bold 11px IBM Plex Mono, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("MCP", w / 2, h / 2);

    this.animId = requestAnimationFrame(() => this.loop());
  },
};

window.BrainViz = BrainViz;
