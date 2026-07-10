document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const latestValueEl = document.getElementById("latest-value");
    const latestTimeEl = document.getElementById("latest-time");
    const avgValueEl = document.getElementById("avg-value");
    const avgCountEl = document.getElementById("avg-count");
    const minValueEl = document.getElementById("min-value");
    const minTimeEl = document.getElementById("min-time");
    const maxValueEl = document.getElementById("max-value");
    const maxTimeEl = document.getElementById("max-time");
    
    const filterForm = document.getElementById("filter-form");
    const startDateInput = document.getElementById("start-date");
    const endDateInput = document.getElementById("end-date");
    const resetBtn = document.getElementById("reset-btn");
    const exportBtn = document.getElementById("export-btn");
    
    const refreshToggle = document.getElementById("auto-refresh");
    const reloadBtn = document.getElementById("reload-btn");
    const loader = document.getElementById("loader");
    
    const tableBody = document.querySelector("#readings-table tbody");
    const prevPageBtn = document.getElementById("prev-page");
    const nextPageBtn = document.getElementById("next-page");
    const pageNumEl = document.getElementById("page-num");
    const pageTotalEl = document.getElementById("page-total");
    
    // Application State
    let chartInstance = null;
    let autoRefreshInterval = null;
    let allReadings = [];
    let currentPage = 1;
    const itemsPerPage = 10;
    
    // Initialize Chart.js
    function initChart(labels = [], dataPoints = []) {
        const ctx = document.getElementById("temperatureChart").getContext("2d");
        
        // Create custom gradient for area under the line
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, "rgba(88, 166, 255, 0.3)");
        gradient.addColorStop(1, "rgba(88, 166, 255, 0.0)");
        
        const chartConfig = {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Temperature (°C)",
                    data: dataPoints,
                    borderColor: "#58a6ff",
                    borderWidth: 3,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: "#58a6ff",
                    pointBorderColor: "#0d1117",
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: "#00f2fe",
                    pointHoverBorderColor: "#ffffff",
                    pointHoverBorderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: "rgba(22, 27, 34, 0.95)",
                        titleColor: "#f0f6fc",
                        bodyColor: "#58a6ff",
                        borderColor: "rgba(48, 54, 61, 0.8)",
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8,
                        titleFont: {
                            family: "Inter",
                            weight: "bold"
                        },
                        bodyFont: {
                            family: "Inter"
                        },
                        callbacks: {
                            label: function(context) {
                                return ` Temp: ${context.parsed.y} °C`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: "rgba(48, 54, 61, 0.3)",
                            borderColor: "rgba(48, 54, 61, 0.5)"
                        },
                        ticks: {
                            color: "#8b949e",
                            font: {
                                family: "Inter",
                                size: 10
                            },
                            maxRotation: 45,
                            minRotation: 0,
                            // Show fewer ticks on mobile screens
                            maxTicksLimit: window.innerWidth < 600 ? 6 : 12
                        }
                    },
                    y: {
                        grid: {
                            color: "rgba(48, 54, 61, 0.3)",
                            borderColor: "rgba(48, 54, 61, 0.5)"
                        },
                        ticks: {
                            color: "#8b949e",
                            font: {
                                family: "Inter",
                                size: 11
                            },
                            callback: function(value) {
                                return value + " °C";
                            }
                        },
                        suggestedMin: 15,
                        suggestedMax: 45
                    }
                }
            }
        };
        
        if (chartInstance) {
            chartInstance.destroy();
        }
        
        chartInstance = new Chart(ctx, chartConfig);
    }
    
    // Fetch Data from Django REST Endpoint
    async function fetchDashboardData(showLoader = false) {
        if (showLoader) {
            loader.classList.add("active");
        }
        
        const params = new URLSearchParams();
        if (startDateInput.value) params.append("start_date", startDateInput.value);
        if (endDateInput.value) params.append("end_date", endDateInput.value);
        
        try {
            const response = await fetch(`/api/readings/?${params.toString()}`);
            if (!response.ok) throw new Error("HTTP error " + response.status);
            
            const data = await response.json();
            
            if (data.status === "success") {
                updateStats(data.stats, data.readings);
                allReadings = data.readings;
                
                // Chronological sorting for chart (data comes back DESC, we need ASC for timeline)
                const chronological = [...data.readings].reverse();
                
                const labels = chronological.map(r => `${r.time}`);
                const dataPoints = chronological.map(r => r.temperature);
                
                initChart(labels, dataPoints);
                renderTable();
            }
        } catch (error) {
            console.error("Error fetching readings:", error);
        } finally {
            if (showLoader) {
                loader.classList.remove("active");
            }
        }
    }
    
    // Update Stats Displayed on Cards
    function updateStats(stats, readings) {
        // Latest Reading
        if (stats.latest !== null) {
            latestValueEl.innerHTML = `${stats.latest.toFixed(1)}<span class="metric-unit">°C</span>`;
            latestTimeEl.innerHTML = `At <span>${stats.latest_time}</span>`;
            // Color based on temperature ranges
            if (stats.latest >= 35.0) {
                latestValueEl.style.color = "var(--danger-color)";
            } else if (stats.latest <= 23.0) {
                latestValueEl.style.color = "var(--accent-color)";
            } else {
                latestValueEl.style.color = "var(--success-color)";
            }
        } else {
            latestValueEl.innerHTML = `--<span class="metric-unit">°C</span>`;
            latestTimeEl.innerHTML = "No readings available";
            latestValueEl.style.color = "var(--text-primary)";
        }
        
        // Average Reading
        if (stats.avg !== null) {
            avgValueEl.innerHTML = `${stats.avg.toFixed(1)}<span class="metric-unit">°C</span>`;
            avgCountEl.innerHTML = `Based on <span>${stats.count}</span> records`;
        } else {
            avgValueEl.innerHTML = `--<span class="metric-unit">°C</span>`;
            avgCountEl.innerHTML = "No records";
        }
        
        // Min / Max Readings
        if (stats.min !== null) {
            minValueEl.innerHTML = `${stats.min.toFixed(1)}<span class="metric-unit">°C</span>`;
            
            // Find the reading for min to get its time
            const minReading = readings.find(r => r.temperature === stats.min);
            if (minReading) {
                minTimeEl.innerHTML = `At <span>${minReading.time}</span>`;
            } else {
                minTimeEl.innerHTML = "N/A";
            }
        } else {
            minValueEl.innerHTML = `--<span class="metric-unit">°C</span>`;
            minTimeEl.innerHTML = "N/A";
        }
        
        if (stats.max !== null) {
            maxValueEl.innerHTML = `${stats.max.toFixed(1)}<span class="metric-unit">°C</span>`;
            
            // Find the reading for max to get its time
            const maxReading = readings.find(r => r.temperature === stats.max);
            if (maxReading) {
                maxTimeEl.innerHTML = `At <span>${maxReading.time}</span>`;
            } else {
                maxTimeEl.innerHTML = "N/A";
            }
        } else {
            maxValueEl.innerHTML = `--<span class="metric-unit">°C</span>`;
            maxTimeEl.innerHTML = "N/A";
        }
    }
    
    // Render Paginated Data Table
    function renderTable() {
        tableBody.innerHTML = "";
        
        if (allReadings.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="3" style="text-align: center; color: var(--text-secondary);">No temperature records found for current filters.</td></tr>`;
            pageNumEl.innerText = 0;
            pageTotalEl.innerText = 0;
            prevPageBtn.disabled = true;
            nextPageBtn.disabled = true;
            return;
        }
        
        const totalPages = Math.ceil(allReadings.length / itemsPerPage);
        
        // Bound current page
        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;
        
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const pageItems = allReadings.slice(startIndex, endIndex);
        
        pageItems.forEach((reading) => {
            const row = document.createElement("tr");
            
            // Highlight row color slightly for extreme temperatures
            let badgeClass = "";
            let textStyle = "";
            if (reading.temperature >= 35.0) {
                textStyle = "color: #ff7b72; font-weight: 600;";
            } else if (reading.temperature <= 23.0) {
                textStyle = "color: #58a6ff; font-weight: 600;";
            }
            
            row.innerHTML = `
                <td>${reading.date}</td>
                <td>${reading.time}</td>
                <td style="${textStyle}">${reading.temperature.toFixed(1)} °C</td>
            `;
            tableBody.appendChild(row);
        });
        
        // Update pagination UI
        pageNumEl.innerText = currentPage;
        pageTotalEl.innerText = totalPages;
        
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
    }
    
    // Setup Auto Refresh Timer
    function toggleAutoRefresh() {
        if (refreshToggle.checked) {
            console.log("Auto refresh started (5 seconds interval)");
            autoRefreshInterval = setInterval(() => {
                // Fetch silently in the background (no loader spinner to avoid flashing)
                fetchDashboardData(false);
            }, 5000);
        } else {
            console.log("Auto refresh stopped");
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
                autoRefreshInterval = null;
            }
        }
    }
    
    // Event Listeners
    filterForm.addEventListener("submit", (e) => {
        e.preventDefault();
        currentPage = 1;
        fetchDashboardData(true);
    });
    
    resetBtn.addEventListener("click", () => {
        startDateInput.value = "";
        endDateInput.value = "";
        currentPage = 1;
        fetchDashboardData(true);
    });
    
    reloadBtn.addEventListener("click", () => {
        fetchDashboardData(true);
    });
    
    refreshToggle.addEventListener("change", toggleAutoRefresh);
    
    exportBtn.addEventListener("click", () => {
        const params = new URLSearchParams();
        if (startDateInput.value) params.append("start_date", startDateInput.value);
        if (endDateInput.value) params.append("end_date", endDateInput.value);
        
        // Navigate window to CSV download endpoint
        window.location.href = `/api/export/?${params.toString()}`;
    });
    
    prevPageBtn.addEventListener("click", () => {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    });
    
    nextPageBtn.addEventListener("click", () => {
        const totalPages = Math.ceil(allReadings.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    });
    
    // Auto-update max and min rules in date inputs
    // Enforces start_date <= end_date
    startDateInput.addEventListener("change", () => {
        if (startDateInput.value) {
            endDateInput.min = startDateInput.value;
        } else {
            endDateInput.removeAttribute("min");
        }
    });
    
    endDateInput.addEventListener("change", () => {
        if (endDateInput.value) {
            startDateInput.max = endDateInput.value;
        } else {
            startDateInput.removeAttribute("max");
        }
    });
    
    // Initial Load
    fetchDashboardData(true);
    toggleAutoRefresh(); // Starts auto-refresh if checkbox is checked by default
});
