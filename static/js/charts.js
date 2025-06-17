// Charts.js - Core charting utilities for DevX Tracker
// Provides consistent Chart.js configurations and utilities across the application

// Global chart defaults
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.color = '#f8fafc';
Chart.defaults.plugins.legend.labels.usePointStyle = true;

// Color palette for consistent theming
const CHART_COLORS = {
    primary: '#0ea5e9',
    primaryLight: 'rgba(14, 165, 233, 0.2)',
    secondary: '#64748b',
    secondaryLight: 'rgba(100, 116, 139, 0.2)',
    success: '#10b981',
    successLight: 'rgba(16, 185, 129, 0.2)',
    warning: '#f59e0b',
    warningLight: 'rgba(245, 158, 11, 0.2)',
    danger: '#ef4444',
    dangerLight: 'rgba(239, 68, 68, 0.2)',
    info: '#06b6d4',
    infoLight: 'rgba(6, 182, 212, 0.2)',
    accent: '#f472b6',
    accentLight: 'rgba(244, 114, 182, 0.2)',
    muted: '#94a3b8',
    grid: 'rgba(148, 163, 184, 0.1)',
    text: '#f8fafc'
};

// Common chart options
const DEFAULT_OPTIONS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: CHART_COLORS.text,
                font: {
                    family: "'Inter', sans-serif",
                    size: 11
                },
                usePointStyle: true,
                pointStyle: 'circle'
            }
        },
        tooltip: {
            backgroundColor: '#1e293b',
            titleColor: CHART_COLORS.text,
            bodyColor: CHART_COLORS.text,
            borderColor: CHART_COLORS.grid,
            borderWidth: 1,
            cornerRadius: 6,
            displayColors: true
        }
    },
    scales: {
        x: {
            grid: {
                color: CHART_COLORS.grid,
                borderColor: CHART_COLORS.grid
            },
            ticks: {
                color: CHART_COLORS.muted,
                font: {
                    family: "'Inter', sans-serif",
                    size: 10
                }
            }
        },
        y: {
            grid: {
                color: CHART_COLORS.grid,
                borderColor: CHART_COLORS.grid
            },
            ticks: {
                color: CHART_COLORS.muted,
                font: {
                    family: "'Inter', sans-serif",
                    size: 10
                }
            }
        }
    }
};

// Chart creation utilities
class ChartUtils {
    
    // Create a line chart with gradient fill
    static createLineChart(ctx, data, options = {}) {
        const config = {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: data.datasets.map(dataset => ({
                    ...dataset,
                    borderWidth: dataset.borderWidth || 2,
                    tension: dataset.tension || 0.4,
                    pointRadius: dataset.pointRadius || 4,
                    pointHoverRadius: dataset.pointHoverRadius || 6,
                    fill: dataset.fill !== undefined ? dataset.fill : true
                }))
            },
            options: {
                ...DEFAULT_OPTIONS,
                ...options
            }
        };
        
        return new Chart(ctx, config);
    }
    
    // Create a bar chart
    static createBarChart(ctx, data, options = {}) {
        const config = {
            type: 'bar',
            data: {
                labels: data.labels || [],
                datasets: data.datasets.map(dataset => ({
                    ...dataset,
                    borderWidth: dataset.borderWidth || 1,
                    borderRadius: dataset.borderRadius || 4,
                    borderSkipped: false
                }))
            },
            options: {
                ...DEFAULT_OPTIONS,
                ...options
            }
        };
        
        return new Chart(ctx, config);
    }
    
    // Create a doughnut chart
    static createDoughnutChart(ctx, data, options = {}) {
        const config = {
            type: 'doughnut',
            data: {
                labels: data.labels || [],
                datasets: data.datasets.map(dataset => ({
                    ...dataset,
                    borderWidth: dataset.borderWidth || 0,
                    hoverOffset: dataset.hoverOffset || 4
                }))
            },
            options: {
                ...DEFAULT_OPTIONS,
                plugins: {
                    ...DEFAULT_OPTIONS.plugins,
                    legend: {
                        ...DEFAULT_OPTIONS.plugins.legend,
                        position: options.legendPosition || 'bottom'
                    }
                },
                ...options
            }
        };
        
        return new Chart(ctx, config);
    }
    
    // Create a radar chart
    static createRadarChart(ctx, data, options = {}) {
        const config = {
            type: 'radar',
            data: {
                labels: data.labels || [],
                datasets: data.datasets.map(dataset => ({
                    ...dataset,
                    borderWidth: dataset.borderWidth || 2,
                    pointBackgroundColor: dataset.pointBackgroundColor || dataset.borderColor,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: dataset.borderColor
                }))
            },
            options: {
                ...DEFAULT_OPTIONS,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: options.maxValue || 10,
                        grid: {
                            color: CHART_COLORS.grid
                        },
                        angleLines: {
                            color: CHART_COLORS.grid
                        },
                        pointLabels: {
                            color: CHART_COLORS.muted,
                            font: {
                                family: "'Inter', sans-serif",
                                size: 11
                            }
                        },
                        ticks: {
                            color: CHART_COLORS.muted,
                            font: {
                                family: "'Inter', sans-serif",
                                size: 10
                            },
                            stepSize: options.stepSize || 2
                        }
                    }
                },
                ...options
            }
        };
        
        return new Chart(ctx, config);
    }
    
    // Create gradient background
    static createGradient(ctx, color1, color2, direction = 'vertical') {
        const canvas = ctx.canvas;
        const gradient = direction === 'vertical' 
            ? ctx.createLinearGradient(0, 0, 0, canvas.height)
            : ctx.createLinearGradient(0, 0, canvas.width, 0);
        
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
        
        return gradient;
    }
    
    // Get color palette for multiple datasets
    static getColorPalette(count) {
        const colors = [
            CHART_COLORS.primary,
            CHART_COLORS.success,
            CHART_COLORS.warning,
            CHART_COLORS.danger,
            CHART_COLORS.info,
            CHART_COLORS.accent,
            CHART_COLORS.secondary
        ];
        
        return Array.from({length: count}, (_, i) => colors[i % colors.length]);
    }
    
    // Format numbers for display
    static formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }
    
    // Format percentage
    static formatPercentage(value, decimals = 1) {
        return (value * 100).toFixed(decimals) + '%';
    }
    
    // Format duration
    static formatDuration(hours) {
        if (hours < 1) {
            return Math.round(hours * 60) + 'm';
        } else if (hours >= 24) {
            return Math.round(hours / 24) + 'd';
        } else {
            return hours.toFixed(1) + 'h';
        }
    }
    
    // Destroy chart safely
    static destroyChart(chart) {
        if (chart && typeof chart.destroy === 'function') {
            chart.destroy();
        }
    }
    
    // Animation helpers
    static animateChart(chart, animation = 'fadeIn') {
        if (chart && chart.canvas) {
            chart.canvas.style.animation = `${animation} 0.5s ease-in-out`;
            setTimeout(() => {
                chart.canvas.style.animation = '';
            }, 500);
        }
    }
}

// Specific chart configurations for DevX Tracker

// Productivity metrics chart
function createProductivityChart(ctx, data) {
    return ChartUtils.createLineChart(ctx, {
        labels: data.labels,
        datasets: [{
            label: 'Productivity Score',
            data: data.productivity,
            backgroundColor: ChartUtils.createGradient(ctx, CHART_COLORS.primaryLight, 'transparent'),
            borderColor: CHART_COLORS.primary,
            pointBackgroundColor: CHART_COLORS.primary
        }]
    }, {
        scales: {
            y: {
                ...DEFAULT_OPTIONS.scales.y,
                beginAtZero: true,
                max: 10,
                ticks: {
                    ...DEFAULT_OPTIONS.scales.y.ticks,
                    callback: function(value) {
                        return value + '/10';
                    }
                }
            }
        }
    });
}

// Health metrics chart
function createHealthChart(ctx, data) {
    return ChartUtils.createLineChart(ctx, {
        labels: data.labels,
        datasets: [
            {
                label: 'Sleep Hours',
                data: data.sleep,
                backgroundColor: ChartUtils.createGradient(ctx, CHART_COLORS.primaryLight, 'transparent'),
                borderColor: CHART_COLORS.primary,
                yAxisID: 'y'
            },
            {
                label: 'Stress Level',
                data: data.stress,
                backgroundColor: ChartUtils.createGradient(ctx, CHART_COLORS.dangerLight, 'transparent'),
                borderColor: CHART_COLORS.danger,
                yAxisID: 'y1'
            }
        ]
    }, {
        scales: {
            y: {
                ...DEFAULT_OPTIONS.scales.y,
                type: 'linear',
                display: true,
                position: 'left',
                beginAtZero: true,
                max: 12,
                title: {
                    display: true,
                    text: 'Sleep Hours',
                    color: CHART_COLORS.text
                }
            },
            y1: {
                ...DEFAULT_OPTIONS.scales.y,
                type: 'linear',
                display: true,
                position: 'right',
                beginAtZero: true,
                max: 100,
                grid: {
                    drawOnChartArea: false
                },
                title: {
                    display: true,
                    text: 'Stress Level (%)',
                    color: CHART_COLORS.text
                }
            }
        }
    });
}

// Language breakdown chart
function createLanguageChart(ctx, data) {
    const colors = ChartUtils.getColorPalette(Object.keys(data).length);
    
    return ChartUtils.createDoughnutChart(ctx, {
        labels: Object.keys(data),
        datasets: [{
            data: Object.values(data),
            backgroundColor: colors,
            borderWidth: 0
        }]
    });
}

// Team comparison chart
function createTeamChart(ctx, teamData) {
    const developers = Object.keys(teamData);
    const colors = ChartUtils.getColorPalette(developers.length);
    
    return ChartUtils.createRadarChart(ctx, {
        labels: ['Productivity', 'Collaboration', 'Code Quality', 'Health', 'Innovation'],
        datasets: developers.map((dev, index) => ({
            label: teamData[dev].user_info.name.split(' ')[0],
            data: [
                teamData[dev].gitlab.productivity_score,
                teamData[dev].gitlab.collaboration_score,
                teamData[dev].gitlab.pipeline_success_rate * 10,
                (100 - teamData[dev].telemetry.health_data.stress_level) / 10,
                Math.random() * 3 + 7 // Innovation score (simulated)
            ],
            backgroundColor: colors[index] + '20',
            borderColor: colors[index]
        }))
    });
}

// Sparkline chart
function createSparkline(ctx, data) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: data.length}, (_, i) => i),
            datasets: [{
                data: data,
                borderColor: CHART_COLORS.primary,
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
                },
                tooltip: {
                    enabled: false
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
}

// Export utilities and functions
window.ChartUtils = ChartUtils;
window.CHART_COLORS = CHART_COLORS;
window.createProductivityChart = createProductivityChart;
window.createHealthChart = createHealthChart;
window.createLanguageChart = createLanguageChart;
window.createTeamChart = createTeamChart;
window.createSparkline = createSparkline;

// Initialize chart resize handlers
window.addEventListener('resize', function() {
    Chart.helpers.each(Chart.instances, function(instance) {
        instance.resize();
    });
});

// Theme change handler (if needed)
function updateChartsTheme(isDark = true) {
    const textColor = isDark ? '#f8fafc' : '#1e293b';
    const gridColor = isDark ? 'rgba(148, 163, 184, 0.1)' : 'rgba(100, 116, 139, 0.2)';
    
    Chart.defaults.color = textColor;
    
    Chart.helpers.each(Chart.instances, function(instance) {
        if (instance.options.scales) {
            Object.keys(instance.options.scales).forEach(scaleKey => {
                const scale = instance.options.scales[scaleKey];
                if (scale.ticks) scale.ticks.color = textColor;
                if (scale.grid) scale.grid.color = gridColor;
            });
        }
        instance.update();
    });
}

// Auto-initialize any charts on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Chart utilities loaded and ready');
    
    // Add subtle entrance animation to chart containers
    const chartContainers = document.querySelectorAll('.chart-container, canvas');
    chartContainers.forEach((container, index) => {
        container.style.opacity = '0';
        container.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            container.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
