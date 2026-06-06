let naiveChart, memoryChart;
const TOKEN_COST = 0.15 / 1_000_000;

function initCharts() {
    const opts = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { ticks: { color: "#94a3b8" }, grid: { display: false } }, y: { ticks: { color: "#94a3b8" } } },
    };

    naiveChart = new Chart(document.getElementById("naive-chart"), {
        type: "line",
        data: { labels: [], datasets: [{ label: "Naive", data: [], borderColor: "#ef4444", borderWidth: 2, fill: false, tension: 0.3, pointRadius: 0 }] },
        options: opts,
    });

    memoryChart = new Chart(document.getElementById("memory-chart"), {
        type: "line",
        data: { labels: [], datasets: [{ label: "Memory", data: [], borderColor: "#10b981", borderWidth: 2, fill: false, tension: 0.3, pointRadius: 0 }] },
        options: opts,
    });
}

async function startBattle() {
    initCharts();
    document.querySelector(".btn:first-child").disabled = true;
    document.getElementById("status").textContent = "Bataille en cours...";

    const response = await fetch("/api/benchmark/live");
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    const naiveData = [], memoryData = [];

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines[lines.length - 1];

        for (const line of lines.slice(0, -1)) {
            if (line.startsWith("data: ")) {
                const data = JSON.parse(line.substring(6));

                if (data.phase === "naive" && data.turn) {
                    naiveData.push(data.tokens);
                    naiveChart.data.labels.push(`T${data.turn}`);
                    naiveChart.data.datasets[0].data.push(data.tokens);
                    naiveChart.update("none");
                    document.getElementById("n-tokens").textContent = naiveData.reduce((a, b) => a + b, 0).toLocaleString();
                    document.getElementById("n-turn").textContent = `${data.turn}/50`;
                    document.getElementById("status").textContent = `Naive: Tour ${data.turn}/50`;
                }

                if (data.phase === "memory" && data.turn) {
                    memoryData.push(data.tokens);
                    if (memoryChart.data.labels.length < data.turn) {
                        memoryChart.data.labels.push(`T${data.turn}`);
                    }
                    memoryChart.data.datasets[0].data.push(data.tokens);
                    memoryChart.update("none");
                    document.getElementById("m-tokens").textContent = memoryData.reduce((a, b) => a + b, 0).toLocaleString();
                    document.getElementById("m-turn").textContent = `${data.turn}/50`;
                    document.getElementById("status").textContent = `MemBridge: Tour ${data.turn}/50`;
                }

                if (data.phase === "quality_done") {
                    const qual = data.quality || { passed: 0, total: 10 };
                    document.getElementById("n-qual").textContent = `${qual.passed}/10`;
                    document.getElementById("m-qual").textContent = `${qual.passed}/10`;
                }

                if (data.phase === "complete") {
                    const r = data.report;
                    const naiveCost = (r.naive.total_tokens * TOKEN_COST).toFixed(4);
                    const memoryCost = (r.memory.total_tokens * TOKEN_COST).toFixed(4);
                    document.getElementById("n-cost").textContent = naiveCost;
                    document.getElementById("m-cost").textContent = memoryCost;
                    document.getElementById("status").textContent = "Bataille terminee!";

                    const verdict = document.getElementById("verdict");
                    verdict.style.display = "block";
                    if (r.savings_pct >= 70) {
                        verdict.textContent = `VICTOIRE! -${r.savings_pct}% d'economie`;
                        verdict.className = "verdict winner";
                    } else {
                        verdict.textContent = `Dommage: -${r.savings_pct}%`;
                        verdict.className = "verdict";
                    }
                }
            }
        }
    }
}

window.addEventListener("load", () => {
    document.querySelector(".btn:first-child").onclick = startBattle;
});
