// Live Dashboard JavaScript Controller (Pure Matplotlib Image Refresh - No JS Charting Libraries)
let pollingInterval = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
    
    // Auto refresh live data every 10 seconds
    pollingInterval = setInterval(fetchDashboardData, 10000);
    
    const refreshBtn = document.getElementById('btn-manual-refresh');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', triggerManualFetch);
    }
});

async function fetchDashboardData() {
    try {
        // Fetch current live temperature reading
        const resCurrent = await fetch('/api/current');
        const dataCurrent = await resCurrent.json();
        
        if (dataCurrent.status === 'success' && dataCurrent.data) {
            updateCurrentDisplay(dataCurrent.data);
        }

        // Refresh Matplotlib Time Series Chart Image
        refreshMatplotlibChartImage();

        // Fetch historical readings table
        const resHist = await fetch('/api/history?limit=15');
        const dataHist = await resHist.json();

        if (dataHist.status === 'success' && dataHist.data) {
            updateHistoryTable(dataHist.data);
        }
        
        updateLastRefreshedTime();
    } catch (err) {
        console.error('Error fetching dashboard data:', err);
    }
}

function updateCurrentDisplay(reading) {
    const tempElem = document.getElementById('current-temp-val');
    const apparentElem = document.getElementById('current-apparent-val');
    const humidityElem = document.getElementById('current-humidity-val');
    const windElem = document.getElementById('current-wind-val');
    const timestampElem = document.getElementById('current-timestamp');

    if (tempElem && reading.temperature !== null) {
        tempElem.textContent = reading.temperature;
    }
    if (apparentElem && reading.apparent_temperature !== null) {
        apparentElem.textContent = reading.apparent_temperature;
    }
    if (humidityElem && reading.humidity !== null) {
        humidityElem.textContent = reading.humidity;
    }
    if (windElem && reading.wind_speed !== null) {
        windElem.textContent = reading.wind_speed;
    }
    if (timestampElem && reading.formatted_time) {
        timestampElem.textContent = reading.formatted_time;
    }
}

function refreshMatplotlibChartImage() {
    const img = document.getElementById('matplotlib-temp-chart');
    if (img) {
        // Append unique timestamp to force browser image cache refresh
        const basePath = img.src.split('?')[0];
        img.src = basePath + '?t=' + new Date().getTime();
    }
}

function updateHistoryTable(readings) {
    const tbody = document.getElementById('history-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    readings.slice().reverse().forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="fw-medium">${r.formatted_time}</td>
            <td class="text-info fw-bold">${r.temperature} °C</td>
            <td>${r.apparent_temperature !== null ? r.apparent_temperature + ' °C' : 'N/A'}</td>
            <td>${r.humidity !== null ? r.humidity + ' %' : 'N/A'}</td>
            <td>${r.wind_speed !== null ? r.wind_speed + ' km/h' : 'N/A'}</td>
            <td><span class="badge bg-secondary opacity-75">${r.location}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

async function triggerManualFetch() {
    const btn = document.getElementById('btn-manual-refresh');
    const icon = btn ? btn.querySelector('i') : null;
    
    if (btn) btn.disabled = true;
    if (icon) icon.classList.add('fa-spin');

    try {
        const res = await fetch('/api/trigger-fetch', { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
            await fetchDashboardData();
        }
    } catch (e) {
        console.error('Error triggering manual fetch:', e);
    } finally {
        if (btn) btn.disabled = false;
        if (icon) icon.classList.remove('fa-spin');
    }
}

function updateLastRefreshedTime() {
    const elem = document.getElementById('last-refreshed');
    if (elem) {
        const now = new Date();
        elem.textContent = now.toLocaleTimeString();
    }
}
