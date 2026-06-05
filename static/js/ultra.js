// ShieldAI ULTRA - Advanced Fraud Detection Dashboard
// With multiple advanced charts, real-time updates, and AI insights

let charts = {};
let currentFilter = 'all';
let currentThreshold = 0.5;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('[ULTRA] Initializing dashboard...');
    initializeDashboard();
});

function initializeDashboard() {
    // Update time
    updateTime();
    setInterval(updateTime, 1000);

    // Load data
    loadAllData();

    // Event listeners
    document.getElementById('sensitivitySlider').addEventListener('change', handleThresholdChange);
    document.getElementById('fullScanBtn').addEventListener('click', () => loadAllData());
    document.getElementById('alertOnlyBtn').addEventListener('click', () => {
        currentFilter = 'alert';
        loadTransactions();
    });
    document.getElementById('exportBtn').addEventListener('click', exportCSV);
    document.getElementById('refreshBtn').addEventListener('click', () => {
        document.getElementById('refreshBtn').style.transform = 'rotate(180deg)';
        loadAllData();
        setTimeout(() => {
            document.getElementById('refreshBtn').style.transform = 'rotate(0deg)';
        }, 500);
    });

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            loadTransactions();
        });
    });

    // Auto-refresh every 30 seconds
    setInterval(loadAllData, 30000);
}

function updateTime() {
    const now = new Date();
    document.getElementById('liveTime').textContent = now.toLocaleTimeString();
}

function handleThresholdChange() {
    const val = parseFloat(document.getElementById('sensitivitySlider').value);
    document.getElementById('sensitivityValue').textContent = val.toFixed(2);
    currentThreshold = val;
    loadAllData();
}

async function loadAllData() {
    try {
        console.log('[ULTRA] Loading data...');
        const response = await fetch(`/api/data?threshold=${currentThreshold}`);
        const data = await response.json();
        console.log('[ULTRA] Data received:', data);

        updateKPIs(data.metrics);
        updateCharts(data);
        updateAlerts(data.top_alerts);
        loadTransactions();
        generateInsights(data);
        updateThreatLevel(data.metrics);

    } catch (error) {
        console.error('[ERROR]', error);
    }
}

function updateKPIs(metrics) {
    document.getElementById('kpi1').textContent = metrics.total;
    document.getElementById('kpi2').textContent = metrics.alerts;
    document.getElementById('kpiPercent').textContent = metrics.alert_rate;
    document.getElementById('kpi3').textContent = metrics.critical;
    document.getElementById('kpi4').textContent = metrics.avg_score.toFixed(3);

    // Update sidebar metrics
    document.getElementById('metricTotal').textContent = metrics.total;
    document.getElementById('metricAlerts').textContent = metrics.alerts;
    document.getElementById('metricCritical').textContent = metrics.critical;
    document.getElementById('metricAvg').textContent = metrics.avg_score.toFixed(2);

    // Update progress
    const progress = Math.min((metrics.critical / metrics.total) * 100, 100);
    document.getElementById('progFill').style.width = progress + '%';
}

function updateCharts(data) {
    // Chart 1: Risk Timeline (Line Chart)
    const labels = Object.keys(data.score_distribution);
    const values = Object.values(data.score_distribution);

    const timelineCtx = document.getElementById('riskTimeline');
    if (charts.timeline) {
        charts.timeline.data.labels = labels;
        charts.timeline.data.datasets[0].data = values;
        charts.timeline.update();
    } else {
        charts.timeline = new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Risk Distribution',
                    data: values,
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: '#ff006e',
                    pointBorderColor: '#00d4ff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0, 212, 255, 0.1)' },
                        ticks: { color: '#00d4ff' }
                    },
                    x: {
                        grid: { color: 'rgba(0, 212, 255, 0.05)' },
                        ticks: { color: '#00d4ff' }
                    }
                }
            }
        });
    }

    // Chart 2: Country Heatmap (Radar)
    const countryData = data.country_data.sort((a, b) => b.avg_score - a.avg_score);
    const countryLabels = countryData.map(d => d.country);
    const countryScores = countryData.map(d => (d.avg_score * 100).toFixed(0));

    const heatmapCtx = document.getElementById('heatmapChart');
    if (charts.heatmap) {
        charts.heatmap.data.labels = countryLabels;
        charts.heatmap.data.datasets[0].data = countryScores;
        charts.heatmap.update();
    } else {
        charts.heatmap = new Chart(heatmapCtx, {
            type: 'radar',
            data: {
                labels: countryLabels,
                datasets: [{
                    label: 'Risk Score %',
                    data: countryScores,
                    borderColor: '#ff006e',
                    backgroundColor: 'rgba(255, 0, 110, 0.2)',
                    borderWidth: 2,
                    pointRadius: 6,
                    pointBackgroundColor: '#ff006e',
                    pointBorderColor: '#00d4ff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#00d4ff' } } },
                scales: {
                    r: {
                        grid: { color: 'rgba(0, 212, 255, 0.1)' },
                        ticks: { color: '#00d4ff', backdropColor: 'transparent' }
                    }
                }
            }
        });
    }

    // Chart 3: Score Distribution (Bar)
    const scoreCtx = document.getElementById('scoreChart');
    if (charts.score) {
        charts.score.data.datasets[0].data = values;
        charts.score.update();
    } else {
        charts.score = new Chart(scoreCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Transactions',
                    data: values,
                    backgroundColor: ['#06a77d', '#ffb703', '#ff9500', '#ff6b35', '#fb5607'],
                    borderColor: ['#00d4ff', '#00d4ff', '#00d4ff', '#ff006e', '#ff006e'],
                    borderWidth: 2,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0, 212, 255, 0.1)' },
                        ticks: { color: '#00d4ff' }
                    }
                }
            }
        });
    }

    // Chart 4: Alert Breakdown (Doughnut)
    const breakdownCtx = document.getElementById('breakdownChart');
    const breakdown = {
        normal: data.recent_transactions.filter(t => t.score < 0.5).length,
        warning: data.recent_transactions.filter(t => t.score >= 0.5 && t.score < 0.7).length,
        critical: data.recent_transactions.filter(t => t.score >= 0.7).length
    };

    if (charts.breakdown) {
        charts.breakdown.data.datasets[0].data = [breakdown.normal, breakdown.warning, breakdown.critical];
        charts.breakdown.update();
    } else {
        charts.breakdown = new Chart(breakdownCtx, {
            type: 'doughnut',
            data: {
                labels: ['Safe', 'Warning', 'Critical'],
                datasets: [{
                    data: [breakdown.normal, breakdown.warning, breakdown.critical],
                    backgroundColor: ['#06a77d', '#ffb703', '#fb5607'],
                    borderColor: '#00d4ff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#00d4ff' } } }
            }
        });
    }
}

function updateAlerts(alerts) {
    const list = document.getElementById('threatsList');
    document.getElementById('alertCount').textContent = alerts.length + ' Active';

    if (alerts.length === 0) {
        list.innerHTML = '<p class="loading">No threats detected</p>';
        return;
    }

    list.innerHTML = alerts.map((a, i) => `
        <div class="threat-item ${a.score > 0.7 ? 'critical' : ''}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="threat-id">#${i + 1} ${a.id}</span>
                <span class="threat-score ${a.score > 0.7 ? 'critical' : ''}">${(a.score * 100).toFixed(0)}%</span>
            </div>
            <div class="threat-reason">${a.reason.substring(0, 120)}...</div>
        </div>
    `).join('');
}

async function loadTransactions() {
    try {
        const response = await fetch(`/api/transactions?filter=${currentFilter}&threshold=${currentThreshold}`);
        const data = await response.json();

        const list = document.getElementById('transactionsList');
        if (data.transactions.length === 0) {
            list.innerHTML = '<p class="loading">No transactions</p>';
            return;
        }

        list.innerHTML = data.transactions.map(tx => {
            const scorePercent = (tx.score * 100).toFixed(0);
            let statusClass = 'success';
            if (tx.score >= 0.7) statusClass = 'critical';
            else if (tx.score >= 0.5) statusClass = 'alert';

            return `
                <div class="tx-row ${statusClass}">
                    <span class="tx-id">${tx.id}</span>
                    <div class="tx-info">
                        <div class="tx-reason">${tx.reason.substring(0, 80)}</div>
                    </div>
                    <div class="tx-score-box" style="color: ${tx.score > 0.7 ? '#fb5607' : tx.score > 0.5 ? '#ffb703' : '#06a77d'}">
                        ${scorePercent}%
                    </div>
                    <span class="tx-status-badge ${statusClass}">${tx.status}</span>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('[ERROR]', error);
    }
}

function generateInsights(data) {
    const insights = [];
    const metrics = data.metrics;

    // Generate AI insights
    if (metrics.alerts > 0) {
        insights.push(`[ALERT] ${metrics.alerts} fraudulent transactions detected (${metrics.alert_rate})`);
    }
    if (metrics.critical > 0) {
        insights.push(`[CRITICAL] ${metrics.critical} critical-level threats identified`);
    }
    if (metrics.avg_score < 0.3) {
        insights.push('[GOOD] Overall risk level is LOW');
    } else if (metrics.avg_score < 0.6) {
        insights.push('[INFO] Average risk level is MODERATE');
    } else {
        insights.push('[WARNING] Average risk level is HIGH');
    }

    // Patterns
    const patterns = [];
    if (data.country_data.length > 1) {
        const highestRiskCountry = data.country_data.sort((a, b) => b.avg_score - a.avg_score)[0];
        patterns.push(`Highest Risk: ${highestRiskCountry.country} (${(highestRiskCountry.avg_score * 100).toFixed(0)}%)`);
    }
    if (data.score_distribution['0.8-1.0'] > 0) {
        patterns.push(`Detected ${data.score_distribution['0.8-1.0']} critical anomalies`);
    }
    if (data.recent_transactions.filter(t => t.score >= 0.5).length > 2) {
        patterns.push('Cluster of suspicious activities');
    }

    // Update insights
    const insightsList = document.getElementById('insightsList');
    insightsList.innerHTML = insights.map(i => `<div class="insight-item">${i}</div>`).join('');

    // Update patterns
    const patternsList = document.getElementById('patternsList');
    patternsList.innerHTML = patterns.map(p => `<div class="insight-item">${p}</div>`).join('');

    // Update quick stats
    document.getElementById('stat1').textContent = metrics.critical;
    document.getElementById('stat2').textContent = data.country_data.length;
    document.getElementById('stat3').textContent = new Set(data.recent_transactions.map(t => t.id)).size;
    document.getElementById('stat4').textContent = '€' + (metrics.avg_score * 5000).toFixed(0);
}

function updateThreatLevel(metrics) {
    const threatLevel = document.getElementById('threatLevel');
    if (metrics.critical > 0) {
        threatLevel.textContent = 'CRITICAL';
        threatLevel.style.color = '#fb5607';
    } else if (metrics.alerts > 2) {
        threatLevel.textContent = 'HIGH';
        threatLevel.style.color = '#ffb703';
    } else if (metrics.alerts > 0) {
        threatLevel.textContent = 'MEDIUM';
        threatLevel.style.color = '#8338ec';
    } else {
        threatLevel.textContent = 'LOW';
        threatLevel.style.color = '#06a77d';
    }
}

async function exportCSV() {
    try {
        const response = await fetch('/api/export');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'shieldai_ultra_results.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('[ERROR]', error);
        alert('Export failed');
    }
}
