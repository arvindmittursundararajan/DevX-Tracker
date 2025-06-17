// Dashboard JavaScript functionality
console.log('dashboard.js file initiated!'); // Added for debugging

// --- Function Definitions ---

// Initialize weekly contribution chart
function initWeeklyChart(data) {
    const ctx = document.getElementById('weeklyChart');
    if (!ctx) {
        console.warn('Canvas element for weeklyChart not found.');
        return;
    }
    
    // Set explicit canvas dimensions
    ctx.style.width = '100%';
    ctx.style.height = '200px';
    ctx.width = ctx.offsetWidth;
    ctx.height = 200;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Commits',
                data: data,
                backgroundColor: 'rgba(14, 165, 233, 0.2)',
                borderColor: 'rgba(14, 165, 233, 1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: false,
            interaction: {
                intersect: false
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: Math.max(...data) + 2,
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            size: 10
                        },
                        stepSize: 1
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    });
}

// Initialize language breakdown chart
function initLanguageChart(data) {
    const ctx = document.getElementById('languageChart');
    if (!ctx) {
        console.warn('Canvas element for languageChart not found.');
        return;
    }
    
    // Set explicit canvas dimensions
    ctx.style.width = '100%';
    ctx.style.height = '300px';
    ctx.width = ctx.offsetWidth;
    ctx.height = 300;
    
    const languages = Object.keys(data);
    const percentages = Object.values(data);
    const colors = [
        '#0ea5e9', // Blue
        '#10b981', // Green
        '#f59e0b', // Yellow
        '#ef4444', // Red
        '#8b5cf6'  // Purple
    ];
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: languages,
            datasets: [{
                data: percentages,
                backgroundColor: colors.slice(0, languages.length),
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#f8fafc',
                        font: {
                            size: 10
                        },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 10
                    }
                }
            }
        }
    });
}

// Utility function to format numbers
function formatNumber(num) {
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
}

// Utility function to get color based on score
function getScoreColor(score, max = 10) {
    const percentage = (score / max) * 100;
    if (percentage >= 80) return '#10b981'; // Green
    if (percentage >= 60) return '#f59e0b'; // Yellow
    if (percentage >= 40) return '#f97316'; // Orange
    return '#ef4444'; // Red
}

// Add tooltips to elements
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(element => {
        new bootstrap.Tooltip(element);
    });
}

function updateLiveMetrics() {
    // Simulate real-time metric updates
    const commitElement = document.querySelector('.metric-value');
    if (commitElement) {
        // Add subtle animation to indicate update
        commitElement.style.animation = 'fadeIn 0.5s ease-in';
        setTimeout(() => {
            commitElement.style.animation = '';
        }, 500);
    }
}

// --- DOMContentLoaded Listener ---
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded');
    
    // Chart Initialization
    initWeeklyChart(window.weeklyContributionData);
    initLanguageChart(window.languageBreakdownData);

    // Webcam Modal Logic
    const analyzeImageBtn = document.getElementById('analyzeImageBtn');
    console.log('analyzeImageBtn element:', analyzeImageBtn); // Added log to check if button is found
    const loadingIndicator = document.getElementById('loadingIndicator');
    const geminiResponseDiv = document.getElementById('geminiResponse');
    const geminiResponsePre = geminiResponseDiv.querySelector('pre');
    const webcamModal = document.getElementById('webcamModal');

    if (analyzeImageBtn) {
        analyzeImageBtn.addEventListener('click', async () => {
            console.log('Analyze Image button clicked!'); // Added log
            analyzeImageBtn.style.display = 'none';
            loadingIndicator.style.display = 'block';
            geminiResponsePre.textContent = ''; // Clear previous response

            try {
                console.log('Sending request to /api/analyze_image...'); // Added log
                const response = await fetch('/api/analyze_image', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        image_path: 'static/img/6.jpg', // Path to the image
                        prompt: 'Caption this image.'
                    })
                });

                console.log('Received response from API:', response); // Added log
                const data = await response.json();

                if (response.ok) {
                    console.log('API call successful. Data:', data); // Added log
                    geminiResponsePre.textContent = JSON.stringify(data, null, 2);
                } else {
                    console.error('API Error:', data); // Added log
                    geminiResponsePre.textContent = 'Error: ' + (data.error || 'Unknown error');
                }
            } catch (error) {
                console.error('Fetch Error:', error); // Added log
                geminiResponsePre.textContent = 'Error: Could not connect to API.';
            } finally {
                loadingIndicator.style.display = 'none';
                analyzeImageBtn.style.display = 'block';
            }
        });
    }

    // Reset modal content when it's hidden
    if (webcamModal) {
        webcamModal.addEventListener('hidden.bs.modal', () => {
            geminiResponsePre.textContent = '';
            if (analyzeImageBtn) analyzeImageBtn.style.display = 'block';
            loadingIndicator.style.display = 'none';
        });
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add hover effects to metric cards
    document.querySelectorAll('.metric-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Add click animation to achievement items
    document.querySelectorAll('.achievement-item').forEach(item => {
        item.addEventListener('click', function() {
            this.style.animation = 'pulse 0.3s ease-in-out';
            setTimeout(() => {
                this.style.animation = '';
            }, 300);
        });
    });
    
    // Real-time updates simulation (for demo purposes)
    setInterval(updateLiveMetrics, 30000); // Update every 30 seconds
    
    document.querySelectorAll('.main-content, .dashboard-panel, .dashboard-grid, .telemetry-section, .admin-section')
        .forEach(el => el.classList.add('loaded'));
});
