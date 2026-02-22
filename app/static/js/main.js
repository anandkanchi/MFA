/**
 * Mutual Fund Data Analyzer - Main JavaScript
 * Handles all frontend interactivity and API calls
 */

// Global state
const appState = {
    fundData: null,
    currentFundName: '',
    currentDateRange: {}
};

// DOM Elements
const dataForm = document.getElementById('dataForm');
const previewSection = document.getElementById('previewSection');
const exportSection = document.getElementById('exportSection');
const alertContainer = document.getElementById('alertContainer');
const fundNameInput = document.getElementById('fundName');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const btnFetch = document.querySelector('.btn-fetch');
const btnPdf = document.querySelector('.btn-pdf');
const btnExcel = document.querySelector('.btn-excel');
const btnConvert = document.querySelector('.btn-convert');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadFundSuggestions();
    setDefaultDates();
    initializeAuroraEffect();
});

/**
 * Set default dates (last 30 days)
 */
function setDefaultDates() {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);

    endDateInput.value = endDate.toISOString().split('T')[0];
    startDateInput.value = startDate.toISOString().split('T')[0];
}

/**
 * Load fund suggestions (placeholder for now)
 */
function loadFundSuggestions() {
    // In a real scenario, populate from API
    const suggestions = ['HDFC', 'SBI', 'Axis', 'ICICI', 'Aditya Birla'];
    fundNameInput.setAttribute('data-suggestions', JSON.stringify(suggestions));
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertId = 'alert-' + Date.now();
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.id = alertId;
    alertDiv.innerHTML = `
        <span>${message}</span>
        <span class="alert-close" onclick="closeAlert('${alertId}')">&times;</span>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    // Auto close after 5 seconds
    setTimeout(() => closeAlert(alertId), 5000);
}

/**
 * Close alert
 */
function closeAlert(alertId) {
    const alert = document.getElementById(alertId);
    if (alert) {
        alert.style.animation = 'slideOutRight 0.4s ease forwards';
        setTimeout(() => alert.remove(), 400);
    }
}

/**
 * Toggle button loading state
 */
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.querySelector('.btn-text').style.display = 'none';
        button.querySelector('.btn-loader').style.display = 'flex';
    } else {
        button.disabled = false;
        button.querySelector('.btn-text').style.display = 'inline';
        button.querySelector('.btn-loader').style.display = 'none';
    }
}

/**
 * Fetch mutual fund data
 */
dataForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fundName = fundNameInput.value.trim();
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    
    // Validation
    if (!fundName || !startDate || !endDate) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    if (new Date(startDate) > new Date(endDate)) {
        showAlert('Start date cannot be after end date', 'error');
        return;
    }
    
    setButtonLoading(btnFetch, true);
    
    try {
        const response = await fetch('/api/fetch-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fundName: fundName,
                startDate: startDate,
                endDate: endDate
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            appState.fundData = result.data;
            appState.currentFundName = fundName;
            appState.currentDateRange = { start: startDate, end: endDate };
            
            showAlert(`Successfully fetched ${result.record_count} records!`, 'success');
            displayDataPreview(result.data);
            previewSection.style.display = 'block';
            exportSection.style.display = 'block';
            
        } else {
            showAlert(result.message || 'Error fetching data', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Network error: ' + error.message, 'error');
    } finally {
        setButtonLoading(btnFetch, false);
    }
});

/**
 * Display data preview in table
 */
function displayDataPreview(data) {
    if (!data || data.length === 0) {
        showAlert('No data to display', 'error');
        return;
    }
    
    const tableHeader = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');
    const recordCount = document.getElementById('recordCount');
    
    // Clear existing content
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';
    
    // Get column names from first row
    const columns = Object.keys(data[0]);
    
    // Create header
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        tableHeader.appendChild(th);
    });
    
    // Show ALL records (not limited to 10)
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            let value = row[col];
            
            // Format value
            if (typeof value === 'number') {
                value = value.toFixed(2);
            } else if (value === null) {
                value = 'N/A';
            }
            
            td.textContent = value;
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
    
    // Update record count (showing all)
    recordCount.textContent = `Showing all ${data.length} records`;
    
    // Load projections and charts
    loadProjectionsAndCharts();
}

/**
 * Chart instances management
 */
const chartInstances = {
    navChart: null,
    metricsChart: null
};

/**
 * Load projections, analytics, and render charts
 */
async function loadProjectionsAndCharts() {
    try {
        // Get projections data
        const projResponse = await fetch('/api/projections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ projectionDays: 30 })
        });
        
        const projData = await projResponse.json();
        
        // Get analytics/metrics
        const analyticsResponse = await fetch('/api/analytics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const analyticsData = await analyticsResponse.json();
        
        // Get chart data
        const chartResponse = await fetch('/api/chart-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const chartData = await chartResponse.json();
        
        if (projData.success || chartData.success) {
            // Show projections section
            const projectionsSection = document.getElementById('projectionsSection');
            projectionsSection.style.display = 'block';
            
            // Render charts
            if (chartData.success) {
                renderNAVChart(projData, chartData.chartData);
                renderMetricsChart(chartData.chartData);
            }
            
            // Display metrics
            if (analyticsData.success) {
                displayMetrics(analyticsData.metrics);
            }
        }
    } catch (error) {
        console.error('Error loading projections:', error);
        // Don't show alert - charts are optional
    }
}

/**
 * Render NAV Chart with projection
 */
function renderNAVChart(projectionData, chartDataObj) {
    const canvas = document.getElementById('navChart');
    if (!canvas) return;
    
    // Destroy existing chart if any
    if (chartInstances.navChart) {
        chartInstances.navChart.destroy();
    }
    
    // Prepare data
    let labels = [];
    let currentData = [];
    let projectionData_array = [];
    let projectionLabels = [];
    
    if (chartDataObj && chartDataObj.labels) {
        labels = chartDataObj.labels;
        if (chartDataObj.datasets && chartDataObj.datasets.length > 0) {
            currentData = chartDataObj.datasets[0].data || [];
        }
    }
    
    if (projectionData && projectionData.projection) {
        projectionData_array = projectionData.projection.projected_navs || [];
        projectionLabels = projectionData.projection.future_dates || [];
    }
    
    // Combine historical and projection data
    const allLabels = [...labels, ...projectionLabels];
    const historicalPadded = [...currentData, ...Array(projectionLabels.length).fill(null)];
    const projectionPadded = [...Array(labels.length).fill(null), ...projectionData_array];
    
    const ctx = canvas.getContext('2d');
    chartInstances.navChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allLabels,
            datasets: [
                {
                    label: 'Actual NAV',
                    data: historicalPadded,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3,
                    pointBackgroundColor: '#3498db',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 1
                },
                {
                    label: '30-Day Projection',
                    data: projectionPadded,
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3,
                    pointRadius: 3,
                    pointBackgroundColor: '#e74c3c',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { font: { size: 12 }, color: '#7f8c8d' }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#3498db',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: true
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: '#7f8c8d' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#7f8c8d', maxTicksLimit: 8 }
                }
            }
        }
    });
}

/**
 * Render Metrics Bar Chart
 */
function renderMetricsChart(chartDataObj) {
    const canvas = document.getElementById('metricsChart');
    if (!canvas) return;
    
    // Destroy existing chart if any
    if (chartInstances.metricsChart) {
        chartInstances.metricsChart.destroy();
    }
    
    const ctx = canvas.getContext('2d');
    chartInstances.metricsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Return %', 'Volatility', 'Sharpe Ratio'],
            datasets: [
                {
                    label: 'Performance Metrics',
                    data: [12.5, 8.3, 1.5], // Placeholder - will be replaced by actual data
                    backgroundColor: [
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(46, 204, 113, 0.8)',
                        'rgba(155, 89, 182, 0.8)'
                    ],
                    borderColor: [
                        '#3498db',
                        '#27ae60',
                        '#9b59b6'
                    ],
                    borderWidth: 1,
                    borderRadius: 6
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { font: { size: 12 }, color: '#7f8c8d' }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#3498db',
                    borderWidth: 1,
                    padding: 10
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: '#7f8c8d' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#7f8c8d' }
                }
            }
        }
    });
}

/**
 * Display performance metrics
 */
function displayMetrics(metrics) {
    if (!metrics) return;
    
    const metricsDisplay = document.getElementById('metricsDisplay');
    const currentNavEl = document.getElementById('currentNav');
    const totalReturnEl = document.getElementById('totalReturn');
    const volatilityEl = document.getElementById('volatility');
    const sharpeRatioEl = document.getElementById('sharpeRatio');
    
    if (metricsDisplay) {
        metricsDisplay.style.display = 'block';
    }
    
    if (currentNavEl && metrics.current_nav) {
        currentNavEl.textContent = metrics.current_nav.toFixed(2);
    }
    
    if (totalReturnEl && metrics.total_return) {
        const returnValue = parseFloat(metrics.total_return);
        totalReturnEl.textContent = returnValue.toFixed(2) + '%';
        totalReturnEl.className = 'metric-value ' + (returnValue >= 0 ? 'positive' : 'negative');
    }
    
    if (volatilityEl && metrics.volatility) {
        volatilityEl.textContent = (metrics.volatility * 100).toFixed(2) + '%';
    }
    
    if (sharpeRatioEl && metrics.sharpe_ratio) {
        sharpeRatioEl.textContent = metrics.sharpe_ratio.toFixed(3);
    }
}

/**
 * Generate PDF report
 */
btnPdf.addEventListener('click', async function() {
    if (!appState.fundData) {
        showAlert('Please fetch data first', 'error');
        return;
    }
    
    setButtonLoading(btnPdf, true);
    
    try {
        const response = await fetch('/api/generate-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fundName: appState.currentFundName,
                startDate: appState.currentDateRange.start,
                endDate: appState.currentDateRange.end
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('PDF generated successfully! Downloading...', 'success');
            // Trigger download
            setTimeout(() => {
                downloadFile(result.filename, 'pdf');
            }, 500);
        } else {
            showAlert(result.message || 'Error generating PDF', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error generating PDF: ' + error.message, 'error');
    } finally {
        setButtonLoading(btnPdf, false);
    }
});

/**
 * Generate Excel file
 */
btnExcel.addEventListener('click', async function() {
    if (!appState.fundData) {
        showAlert('Please fetch data first', 'error');
        return;
    }
    
    setButtonLoading(btnExcel, true);
    
    try {
        const response = await fetch('/api/generate-excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`Excel file created! Downloading...`, 'success');
            // Trigger download
            setTimeout(() => {
                downloadFile(result.filename, 'excel');
            }, 500);
        } else {
            showAlert(result.message || 'Error generating Excel', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error generating Excel: ' + error.message, 'error');
    } finally {
        setButtonLoading(btnExcel, false);
    }
});

/**
 * Convert PDF to Excel
 */
btnConvert.addEventListener('click', async function() {
    const pdfFilename = prompt('Enter PDF filename to convert:');
    
    if (!pdfFilename) {
        return;
    }
    
    setButtonLoading(btnConvert, true);
    
    try {
        const response = await fetch('/api/convert-pdf-to-excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pdfFilename: pdfFilename
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`PDF converted! Found ${result.tables_found} table(s)`, 'success');
        } else {
            showAlert(result.message || 'Error converting PDF', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error converting PDF: ' + error.message, 'error');
    } finally {
        setButtonLoading(btnConvert, false);
    }
});

/**
 * Download file helper
 */
function downloadFile(filename, type) {
    const url = `/download/${type}/${filename}`;
    console.log(`Downloading ${type} file: ${filename}`);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    document.body.appendChild(link);
    
    try {
        link.click();
        console.log(`Download triggered for: ${filename}`);
    } catch (error) {
        console.error('Download error:', error);
        showAlert(`Download failed: ${error.message}`, 'error');
    } finally {
        document.body.removeChild(link);
    }
}

/**
 * Alternative download using fetch (for modern browsers)
 */
async function downloadFileModern(filename, type) {
    const url = `/download/${type}/${filename}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const blob = await response.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = blobUrl;
        link.download = filename;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
        console.error('Download error:', error);
        showAlert(`Download failed: ${error.message}`, 'error');
    }
}

/**
 * Initialize Aurora Lighting Effect
 * Creates a glow effect that follows the mouse cursor
 */
function initializeAuroraEffect() {
    const style = document.createElement('style');
    style.textContent = `
        /* Aurora glow container */
        .aurora-glow {
            position: fixed;
            width: 400px;
            height: 400px;
            pointer-events: none;
            z-index: 1;
            border-radius: 50%;
            filter: blur(80px);
            mix-blend-mode: screen;
            opacity: 0.3;
            will-change: transform;
        }
        
        .aurora-glow::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(52, 152, 219, 0.8) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        .aurora-glow::after {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(46, 204, 113, 0.6) 0%, transparent 70%);
            border-radius: 50%;
            animation: auroraShift 8s ease-in-out infinite;
        }
        
        @keyframes auroraShift {
            0%, 100% { opacity: 0.6; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.1); }
        }
        
        /* Second aurora layer */
        .aurora-glow-2 {
            position: fixed;
            width: 300px;
            height: 300px;
            pointer-events: none;
            z-index: 0;
            border-radius: 50%;
            filter: blur(100px);
            mix-blend-mode: screen;
            opacity: 0.2;
            will-change: transform;
        }
        
        .aurora-glow-2::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(155, 89, 182, 0.7) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        @keyframes slowShift {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.5; }
        }
        
        .aurora-glow-2::after {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(52, 152, 219, 0.5) 0%, transparent 70%);
            border-radius: 50%;
            animation: slowShift 12s ease-in-out infinite;
        }
    `;
    document.head.appendChild(style);
    
    // Create aurora glow elements
    const aurora1 = document.createElement('div');
    aurora1.className = 'aurora-glow';
    document.body.appendChild(aurora1);
    
    const aurora2 = document.createElement('div');
    aurora2.className = 'aurora-glow-2';
    document.body.appendChild(aurora2);
    
    // Track mouse movement
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        // Update primary aurora glow position
        aurora1.style.transform = `translate(${mouseX - 200}px, ${mouseY - 200}px)`;
        
        // Update secondary aurora glow with delayed movement
        setTimeout(() => {
            aurora2.style.transform = `translate(${mouseX - 150}px, ${mouseY - 150}px)`;
        }, 100);
    });
    
    // Reset glows on mouse leave
    document.addEventListener('mouseleave', () => {
        aurora1.style.transform = `translate(-500px, -500px)`;
        aurora2.style.transform = `translate(-500px, -500px)`;
    });
    
    // Update on mouse enter
    document.addEventListener('mouseenter', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
}

/**
 * Add animation for slide out right (for alerts)
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(30px);
        }
    }
`;
document.head.appendChild(style);

console.log('Mutual Fund Analyzer - Application Ready');
