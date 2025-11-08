class PiezoelectricDashboard {
    constructor() {
        this.websocket = null;
        this.chart = null;
        this.sparklines = {};
        this.isConnected = false;
        this.isLogging = false;
        this.voltageData = [];
        this.sparklineData = {
            voltage: [],
            energy: [],
            steps: [],
            power: []
        };
        this.maxDataPoints = 120; // 60 seconds at 2Hz
        this.maxSparklinePoints = 30; // 30 points for sparklines
        this.totalEnergy = 0;
        
        this.init();
    }

    init() {
        console.log('🔧 Initializing dashboard components...');
        this.setupChart();
        console.log('📈 Chart setup complete');
        this.setupSparklines();
        console.log('✨ Sparklines setup complete');
        this.setupEventListeners();
        console.log('🎯 Event listeners setup complete');
        this.loadAvailablePorts();
        console.log('🔌 Loading ports...');
        this.connectWebSocket();
        console.log('📡 WebSocket connection initiated');
        this.updateStatus();
        
        // Start periodic status updates
        setInterval(() => this.updateStatus(), 5000);
    }

    setupChart() {
        const ctx = document.getElementById('voltageChart').getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Voltage (V)',
                    data: [],
                    borderColor: '#d69e2e',
                    backgroundColor: 'rgba(214, 158, 46, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 0
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#2d3748',
                            font: {
                                size: 14,
                                weight: '600'
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: '#e2e8f0'
                        },
                        ticks: {
                            color: '#718096',
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#e2e8f0'
                        },
                        ticks: {
                            color: '#718096'
                        },
                        title: {
                            display: true,
                            text: 'Voltage (V)',
                            color: '#2d3748',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    }
                }
            }
        });
    }

    setupSparklines() {
        const sparklineConfig = {
            voltage: { canvas: 'voltageSparkline', color: '#d69e2e', bgColor: 'rgba(214, 158, 46, 0.1)' },
            energy: { canvas: 'energySparkline', color: '#2b6cb0', bgColor: 'rgba(43, 108, 176, 0.1)' },
            steps: { canvas: 'stepsSparkline', color: '#319795', bgColor: 'rgba(49, 151, 149, 0.1)' },
            power: { canvas: 'powerSparkline', color: '#dd6b20', bgColor: 'rgba(221, 107, 32, 0.1)' }
        };

        for (const [key, config] of Object.entries(sparklineConfig)) {
            const ctx = document.getElementById(config.canvas).getContext('2d');
            this.sparklines[key] = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        data: [],
                        borderColor: config.color,
                        backgroundColor: config.bgColor,
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: false }
                    },
                    scales: {
                        x: { display: false },
                        y: { display: false }
                    }
                }
            });
        }
    }

    setupEventListeners() {
        // Toggle controls button
        const toggleControlsBtn = document.getElementById('toggleControls');
        if (toggleControlsBtn) {
            toggleControlsBtn.addEventListener('click', () => {
                const controlsSection = document.getElementById('controlsSection');
                if (controlsSection.style.display === 'none' || !controlsSection.style.display) {
                    controlsSection.style.display = 'block';
                } else {
                    controlsSection.style.display = 'none';
                }
            });
        }

        // Close controls button
        const closeControlsBtn = document.getElementById('closeControls');
        if (closeControlsBtn) {
            closeControlsBtn.addEventListener('click', () => {
                document.getElementById('controlsSection').style.display = 'none';
            });
        }

        // Port refresh button
        document.getElementById('refreshPorts').addEventListener('click', () => {
            this.loadAvailablePorts();
        });

        // Connect button
        document.getElementById('connectBtn').addEventListener('click', () => {
            this.connectSerial();
        });

        // Disconnect button
        document.getElementById('disconnectBtn').addEventListener('click', () => {
            this.disconnectSerial();
        });

        // Clear graph button
        const clearGraphBtn = document.getElementById('clearGraph');
        if (clearGraphBtn) {
            clearGraphBtn.addEventListener('click', () => {
                this.clearGraph();
            });
        }

        // Logging toggle button
        const toggleLoggingBtn = document.getElementById('toggleLogging');
        if (toggleLoggingBtn) {
            toggleLoggingBtn.addEventListener('click', () => {
                this.toggleLogging();
            });
        }
    }

    async loadAvailablePorts() {
        try {
            const response = await fetch('/api/ports');
            const data = await response.json();
            
            const portSelect = document.getElementById('portSelect');
            portSelect.innerHTML = '<option value="">Select Port...</option>';
            
            data.ports.forEach(port => {
                const option = document.createElement('option');
                option.value = port.device;
                option.textContent = `${port.device} - ${port.description}`;
                portSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading ports:', error);
            this.showNotification('Error loading serial ports', 'error');
        }
    }

    async connectSerial() {
        const port = document.getElementById('portSelect').value;
        const baudrate = parseInt(document.getElementById('baudrate').value);

        if (!port) {
            this.showNotification('Please select a serial port', 'error');
            return;
        }

        try {
            const response = await fetch('/api/connect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ port, baudrate })
            });

            if (response.ok) {
                this.isConnected = true;
                this.updateConnectionUI();
                this.showNotification(`Connected to ${port}`, 'success');
            } else {
                const error = await response.json();
                this.showNotification(`Connection failed: ${error.detail}`, 'error');
            }
        } catch (error) {
            console.error('Connection error:', error);
            this.showNotification('Connection failed', 'error');
        }
    }

    async disconnectSerial() {
        try {
            const response = await fetch('/api/disconnect', {
                method: 'POST'
            });

            if (response.ok) {
                this.isConnected = false;
                this.updateConnectionUI();
                this.showNotification('Disconnected from serial port', 'info');
            }
        } catch (error) {
            console.error('Disconnect error:', error);
            this.showNotification('Disconnect failed', 'error');
        }
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.hostname}:8889`;
        
        console.log('🔌 Attempting to connect WebSocket to:', wsUrl);
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            console.log('✅ WebSocket connected successfully!');
        };
        
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('📊 Received data:', data);
            this.updateMetrics(data);
            this.updateGraph(data);
            this.updateLastUpdate();
        };
        
        this.websocket.onclose = () => {
            console.log('❌ WebSocket disconnected');
            // Attempt to reconnect after 3 seconds
            setTimeout(() => this.connectWebSocket(), 3000);
        };
        
        this.websocket.onerror = (error) => {
            console.error('🚨 WebSocket error:', error);
        };
    }

    updateMetrics(data) {
        // Convert to millijoules and milliwatts for display
        const energyMJ = data.energy * 1000; // J to mJ
        const powerMW = data.power * 1000; // W to mW
        
        // Update total energy
        this.totalEnergy += energyMJ;
        this.updateMetricValue('totalEnergyValue', this.totalEnergy, '0.00');
        
        // Update metric values with animation
        this.updateMetricValue('voltageValue', data.voltage, '0.00');
        this.updateMetricValue('energyValue', energyMJ, '0.00');
        this.updateMetricValue('stepsValue', data.steps, '0');
        this.updateMetricValue('powerValue', powerMW, '0.00');
        
        // Update sparklines
        this.updateSparkline('voltage', data.voltage);
        this.updateSparkline('energy', energyMJ);
        this.updateSparkline('steps', data.steps);
        this.updateSparkline('power', powerMW);
        
        // Update LED status
        const ledIndicator = document.getElementById('ledIndicator');
        const ledStatus = document.getElementById('ledStatus');
        
        if (ledIndicator && ledStatus) {
            if (data.led === 'ON') {
                ledIndicator.classList.add('on');
                ledStatus.textContent = 'ON';
                ledStatus.style.color = '#48bb78';
            } else {
                ledIndicator.classList.remove('on');
                ledStatus.textContent = 'OFF';
                ledStatus.style.color = '#fc8181';
            }
        }
    }

    updateSparkline(type, value) {
        // Add new data point
        this.sparklineData[type].push(value);
        
        // Keep only the last maxSparklinePoints
        if (this.sparklineData[type].length > this.maxSparklinePoints) {
            this.sparklineData[type].shift();
        }
        
        // Update the sparkline chart
        const chart = this.sparklines[type];
        chart.data.labels = Array(this.sparklineData[type].length).fill('');
        chart.data.datasets[0].data = this.sparklineData[type];
        chart.update('none');
    }

    updateMetricValue(elementId, value, format) {
        const element = document.getElementById(elementId);
        if (!element) {
            console.warn(`⚠️ Element not found: ${elementId}`);
            return;
        }
        
        const card = element.closest('.metric-card');
        
        // Format the value based on the format string
        let formattedValue;
        if (format.includes('.')) {
            const decimals = format.split('.')[1].length;
            formattedValue = parseFloat(value).toFixed(decimals);
        } else {
            formattedValue = Math.round(value).toString();
        }
        
        // Add updating animation
        element.classList.add('updating');
        if (card) {
            card.classList.add('updating');
        }
        
        element.textContent = formattedValue;
        
        // Remove animation classes after animation completes
        setTimeout(() => {
            element.classList.remove('updating');
            if (card) {
                card.classList.remove('updating');
            }
        }, 500);
    }

    updateGraph(data) {
        const now = new Date().toLocaleTimeString();
        
        // Add new data point
        this.chart.data.labels.push(now);
        this.chart.data.datasets[0].data.push(data.voltage);

        // Keep only the last maxDataPoints
        if (this.chart.data.labels.length > this.maxDataPoints) {
            this.chart.data.labels.shift();
            this.chart.data.datasets[0].data.shift();
        }

        // Update chart
        this.chart.update('none');
    }

    clearGraph() {
        this.chart.data.datasets[0].data = [];
        this.chart.update();
        this.showNotification('Graph cleared', 'info');
    }

    async toggleLogging() {
        try {
            const endpoint = this.isLogging ? '/api/logging/stop' : '/api/logging/start';
            const response = await fetch(endpoint, { method: 'POST' });
            
            if (response.ok) {
                const result = await response.json();
                this.isLogging = !this.isLogging;
                this.updateLoggingUI();
                
                const message = this.isLogging ? 
                    `Logging started: ${result.file}` : 
                    'Logging stopped';
                this.showNotification(message, 'info');
            }
        } catch (error) {
            console.error('Logging toggle error:', error);
            this.showNotification('Logging toggle failed', 'error');
        }
    }

    async updateStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            this.isConnected = status.serial_connected;
            this.isLogging = status.logging;
            
            this.updateConnectionUI();
            this.updateLoggingUI();
            
            // Update client count
            document.getElementById('clientCount').textContent = status.websocket_connections;
            
        } catch (error) {
            console.error('Status update error:', error);
        }
    }

    updateConnectionUI() {
        const connectBtn = document.getElementById('connectBtn');
        const disconnectBtn = document.getElementById('disconnectBtn');
        const statusDot = document.getElementById('connectionStatus');
        const statusText = document.getElementById('connectionText');
        
        if (this.isConnected) {
            connectBtn.disabled = true;
            disconnectBtn.disabled = false;
            statusDot.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            connectBtn.disabled = false;
            disconnectBtn.disabled = true;
            statusDot.classList.remove('connected');
            statusText.textContent = 'Disconnected';
        }
    }

    updateLoggingUI() {
        const toggleBtn = document.getElementById('toggleLogging');
        const loggingIndicator = document.getElementById('loggingIndicator');
        const loggingStatus = document.getElementById('loggingStatus');
        
        if (this.isLogging) {
            toggleBtn.textContent = 'Stop Logging';
            toggleBtn.className = 'btn btn-danger';
            loggingIndicator.classList.add('active');
            loggingStatus.textContent = 'Logging: Active';
        } else {
            toggleBtn.textContent = 'Start Logging';
            toggleBtn.className = 'btn btn-success';
            loggingIndicator.classList.remove('active');
            loggingStatus.textContent = 'Logging: Stopped';
        }
    }

    updateLastUpdate() {
        const lastUpdate = document.getElementById('lastUpdate');
        const now = new Date();
        lastUpdate.textContent = now.toLocaleTimeString();
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        
        // Set background color based on type
        switch (type) {
            case 'success':
                notification.style.background = 'linear-gradient(45deg, #2ed573, #17d8ac)';
                break;
            case 'error':
                notification.style.background = 'linear-gradient(45deg, #ff4757, #ff3838)';
                break;
            case 'info':
                notification.style.background = 'linear-gradient(45deg, #4a90e2, #357abd)';
                break;
            default:
                notification.style.background = 'rgba(255, 255, 255, 0.1)';
        }
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 4 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM loaded, initializing dashboard...');
    console.log('📦 Chart.js available:', typeof Chart !== 'undefined');
    try {
        const dashboard = new PiezoelectricDashboard();
        console.log('✅ Dashboard initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing dashboard:', error);
    }
});
