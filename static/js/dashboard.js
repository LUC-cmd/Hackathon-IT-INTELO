// Dashboard JavaScript - Real-time fraud detection monitoring

let scoreChart = null;
let countryChart = null;
let currentFilter = 'all';
let currentThreshold = 0.5;

// Update timestamp
function updateTimestamp() {
    const now = new Date();
    document.getElementById('timestamp').textContent = now.toLocaleString();
}

// Initialize dashboard
function initDashboard() {
    updateTimestamp();
    setInterval(updateTimestamp, 1000);

    // Event listeners
    document.getElementById('thresholdSlider').addEventListener('change', handleThresholdChange);
    document.getElementById('exportBtn').addEventListener('click', exportCSV);
    document.getElementById('refreshBtn').addEventListener('click', refreshData);

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            loadTransactions();
        });
    });

    // Initial load
    loadData();
}

// Handle threshold change
function handleThresholdChange() {
    const threshold = parseFloat(document.getElementById('thresholdSlider').value);
    document.getElementById('thresholdValue').textContent = threshold.toFixed(2);
    currentThreshold = threshold;
    loadData();
    loadTransactions();
}

// Load data from API
async function loadData() {
    try {
        const response = await fetch(`/api/data?threshold=${currentThreshold}`);
        const data = await response.json();

        // Update KPIs
        document.getElementById('kpiTotal').textContent = data.metrics.total;
        document.getElementById('kpiAlerts').textContent = data.metrics.alerts;
        document.getElementById('kpiAlertRate').textContent = data.metrics.alert_rate;
        document.getElementById('kpiCritical').textContent = data.metrics.critical;
        document.getElementById('kpiAvgScore').textContent = data.metrics.avg_score.toFixed(3);

        // Update charts
        updateScoreChart(data.score_distribution);
        updateCountryChart(data.country_data);

        // Update alerts
        updateAlerts(data.top_alerts);
        document.getElementById('alertCount').textContent = data.top_alerts.length;

        // Update recent transactions
        updateRecentTransactions(data.recent_transactions);
        document.getElementById('txCount').textContent = data.recent_transactions.length;

    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Update score distribution chart
function updateScoreChart(data) {
    const ctx = document.getElementById('scoreChart');

    if (scoreChart) {
        scoreChart.data.labels = Object.keys(data);
        scoreChart.data.datasets[0].data = Object.values(data);
        scoreChart.update();
    } else {
        scoreChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Number of Transactions',
                    data: Object.values(data),
                    backgroundColor: [
                        'rgba(39, 174, 96, 0.8)',
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(241, 196, 15, 0.8)',
                        'rgba(230, 126, 34, 0.8)',
                        'rgba(231, 76, 60, 0.8)'
                    ],
                    borderColor: [
                        '#27ae60',
                        '#3498db',
                        '#f1c40f',
                        '#e67e22',
                        '#e74c3c'
                    ],
                    borderWidth: 2,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#bdc3c7' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#bdc3c7' }
                    }
                }
            }
        });
    }
}

// Update country risk chart
function updateCountryChart(data) {
    const ctx = document.getElementById('countryChart');

    // Sort by avg_score
    data = data.sort((a, b) => b.avg_score - a.avg_score);

    if (countryChart) {
        countryChart.data.labels = data.map(d => d.country);
        countryChart.data.datasets[0].data = data.map(d => (d.avg_score * 100).toFixed(1));
        countryChart.update();
    } else {
        countryChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => `${d.country} (${d.alerts}/${d.total})`),
                datasets: [{
                    data: data.map(d => (d.avg_score * 100).toFixed(1)),
                    backgroundColor: [
                        '#e74c3c',
                        '#e67e22',
                        '#f1c40f',
                        '#3498db',
                        '#27ae60',
                        '#9b59b6',
                        '#1abc9c'
                    ],
                    borderColor: '#1a1a2e',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#bdc3c7', padding: 15 }
                    }
                }
            }
        });
    }
}

// Update alerts display
function updateAlerts(alerts) {
    const alertsList = document.getElementById('alertsList');

    if (alerts.length === 0) {
        alertsList.innerHTML = '<p class="no-data">No alerts at current threshold</p>';
        return;
    }

    alertsList.innerHTML = alerts.map((alert, idx) => `
        <div class="alert-item ${alert.score > 0.7 ? 'critical' : ''}">
            <div class="alert-item-title">
                #{idx + 1} ${alert.id}
                <span class="alert-item-score">${(alert.score * 100).toFixed(0)}%</span>
            </div>
            <div class="alert-item-reason">${alert.reason.substring(0, 150)}</div>
        </div>
    `).join('');
}

// Update recent transactions
function updateRecentTransactions(transactions) {
    const txList = document.getElementById('transactionsList');

    if (transactions.length === 0) {
        txList.innerHTML = '<p class="no-data">No transactions at current filter</p>';
        return;
    }

    txList.innerHTML = transactions.map(tx => `
        <div class="transaction-item ${tx.is_suspicious ? 'alert' : ''}">
            <div class="transaction-item-id">${tx.id}</div>
            <div class="transaction-item-reason">${tx.reason.substring(0, 100)}</div>
            <div style="min-width: 70px; text-align: right;">
                <span style="font-weight: bold; color: ${tx.score > 0.7 ? '#e74c3c' : tx.score > 0.5 ? '#f39c12' : '#27ae60'}">
                    ${(tx.score * 100).toFixed(0)}%
                </span>
            </div>
            <div class="transaction-item-status">${tx.status}</div>
        </div>
    `).join('');
}

// Load transactions with filter
async function loadTransactions() {
    try {
        const response = await fetch(`/api/transactions?filter=${currentFilter}&threshold=${currentThreshold}`);
        const data = await response.json();

        // The transactions will be updated in the main loadData call
        // This is just for loading with filter

    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

// Export to CSV
async function exportCSV() {
    try {
        const response = await fetch('/api/export');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'fraud_results.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error exporting:', error);
        alert('Failed to export CSV');
    }
}

// Refresh data
function refreshData() {
    console.log('Refreshing data...');
    loadData();

    // Show refresh animation
    const btn = document.getElementById('refreshBtn');
    btn.style.transform = 'rotate(180deg)';
    setTimeout(() => {
        btn.style.transform = 'rotate(0deg)';
    }, 500);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initDashboard);

// Auto-refresh every 30 seconds
setInterval(loadData, 30000);
