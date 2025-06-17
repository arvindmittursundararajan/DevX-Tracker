// Telemetry page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('Telemetry page loaded');
    
    // Initialize data tables if present
    initDataTables();
    
    // Add hover effects to health metrics
    document.querySelectorAll('.health-metric').forEach(metric => {
        metric.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        });
        
        metric.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '';
        });
    });
    
    // Simulate device connection status
    updateDeviceStatus();
    setInterval(updateDeviceStatus, 60000); // Update every minute
});

// Initialize focus score chart
function initFocusChart(data, labels) {
    const ctx = document.getElementById('focusChart');
    if (!ctx) return;
    
    // Set explicit canvas dimensions
    ctx.style.width = '100%';
    ctx.style.height = '200px';
    ctx.width = ctx.offsetWidth;
    ctx.height = 200;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.map(date => new Date(date).toLocaleDateString('en-US', { weekday: 'short' })),
            datasets: [{
                label: 'Focus Score',
                data: data,
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderColor: 'rgba(16, 185, 129, 1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: 'rgba(16, 185, 129, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            size: 10
                        },
                        callback: function(value) {
                            return value + '%';
                        }
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

// Initialize screen time chart
function initScreenTimeChart(data, labels) {
    const ctx = document.getElementById('screenTimeChart');
    if (!ctx) return;
    
    // Set explicit canvas dimensions
    ctx.style.width = '100%';
    ctx.style.height = '250px';
    ctx.width = ctx.offsetWidth;
    ctx.height = 250;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.map(date => new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
            datasets: [{
                label: 'Screen Time (hours)',
                data: data,
                backgroundColor: 'rgba(14, 165, 233, 0.8)',
                borderColor: 'rgba(14, 165, 233, 1)',
                borderWidth: 1,
                borderRadius: 4,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#f8fafc',
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            family: "'Inter', sans-serif"
                        },
                        callback: function(value) {
                            return value + 'h';
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    }
                }
            }
        }
    });
}

// Initialize sparklines for app usage
function initAppUsageSparklines() {
    const sparklineElements = document.querySelectorAll('[id^="sparkline-"]');
    
    sparklineElements.forEach((canvas, index) => {
        // Generate sample hourly usage data
        const data = Array.from({length: 24}, () => Math.floor(Math.random() * 10));
        
        new Chart(canvas, {
            type: 'line',
            data: {
                labels: Array.from({length: 24}, (_, i) => i),
                datasets: [{
                    data: data,
                    borderColor: '#0ea5e9',
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0,
                    tension: 0.4
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        display: false
                    },
                    y: {
                        display: false
                    }
                },
                elements: {
                    point: {
                        radius: 0
                    }
                }
            }
        });
    });
}

// Initialize data tables
function initDataTables() {
    if (typeof $ !== 'undefined' && $.fn.DataTable) {
        $('.table').DataTable({
            responsive: true,
            pageLength: 10,
            order: [[2, 'desc']], // Sort by time used
            language: {
                search: "Filter applications:",
                lengthMenu: "Show _MENU_ applications per page",
                info: "Showing _START_ to _END_ of _TOTAL_ applications",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            }
        });
    }
}

// Update device connection status
function updateDeviceStatus() {
    const statusElement = document.querySelector('.badge:contains("Connected")');
    if (statusElement) {
        // Simulate occasional disconnections
        const isConnected = Math.random() > 0.1; // 90% chance of being connected
        
        if (isConnected) {
            statusElement.className = 'badge bg-success';
            statusElement.innerHTML = '<i class="fas fa-bluetooth me-1"></i>Connected';
        } else {
            statusElement.className = 'badge bg-warning';
            statusElement.innerHTML = '<i class="fas fa-bluetooth me-1"></i>Reconnecting...';
            
            // Reconnect after a few seconds
            setTimeout(() => {
                statusElement.className = 'badge bg-success';
                statusElement.innerHTML = '<i class="fas fa-bluetooth me-1"></i>Connected';
            }, 3000);
        }
    }
}

// Health score calculator
function calculateHealthScore(healthData) {
    const sleepScore = Math.min(100, (healthData.sleep_hours / 8) * 100);
    const stressScore = 100 - healthData.stress_level;
    const activityScore = Math.min(100, (healthData.active_minutes / 60) * 100);
    
    return Math.round((sleepScore + stressScore + activityScore) / 3);
}

// Productivity insights updater
function updateProductivityInsights() {
    const insights = document.querySelectorAll('.productivity-stats .stat-item');
    
    insights.forEach(insight => {
        insight.addEventListener('click', function() {
            // Add visual feedback when clicking on insights
            this.style.animation = 'pulse 0.3s ease-in-out';
            setTimeout(() => {
                this.style.animation = '';
            }, 300);
        });
    });
}

// Format time duration
function formatDuration(hours) {
    if (hours < 1) {
        return Math.round(hours * 60) + 'm';
    } else {
        return hours.toFixed(1) + 'h';
    }
}

// Get productivity category color
function getProductivityColor(category) {
    const colors = {
        'Development': '#10b981',
        'Communication': '#f59e0b', 
        'Research': '#06b6d4',
        'Design': '#8b5cf6',
        'Testing': '#ef4444',
        'DevOps': '#f97316'
    };
    return colors[category] || '#64748b';
}

// Initialize productivity insights
document.addEventListener('DOMContentLoaded', updateProductivityInsights);
