// Admin dashboard JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin dashboard loaded');
    
    // Add real-time updates simulation
    setInterval(updateTeamMetrics, 45000); // Update every 45 seconds
    
    // Initialize sortable tables
    initSortableTables();
    
    // Add hover effects to developer cards
    initDeveloperCardEffects();
});

// Initialize team charts
function initTeamCharts(teamData) {
    initTeamProductivityChart(teamData);
    initTeamHealthChart(teamData);
}

// Team productivity comparison chart
function initTeamProductivityChart(teamData) {
    const ctx = document.getElementById('teamProductivityChart');
    if (!ctx) return;
    
    const developers = Object.keys(teamData);
    const productivityScores = developers.map(dev => teamData[dev].gitlab.productivity_score);
    const collaborationScores = developers.map(dev => teamData[dev].gitlab.collaboration_score);
    const developerNames = developers.map(dev => teamData[dev].user_info.name.split(' ')[0]);
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: developerNames,
            datasets: [
                {
                    label: 'Productivity Score',
                    data: productivityScores,
                    backgroundColor: 'rgba(14, 165, 233, 0.2)',
                    borderColor: 'rgba(14, 165, 233, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(14, 165, 233, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(14, 165, 233, 1)'
                },
                {
                    label: 'Collaboration Score',
                    data: collaborationScores,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(16, 185, 129, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(16, 185, 129, 1)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
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
                r: {
                    beginAtZero: true,
                    max: 10,
                    grid: {
                        color: 'rgba(148, 163, 184, 0.2)'
                    },
                    angleLines: {
                        color: 'rgba(148, 163, 184, 0.2)'
                    },
                    pointLabels: {
                        color: '#94a3b8',
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11
                        }
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            family: "'Inter', sans-serif",
                            size: 10
                        },
                        stepSize: 2
                    }
                }
            }
        }
    });
}

// Team health overview chart
function initTeamHealthChart(teamData) {
    const ctx = document.getElementById('teamHealthChart');
    if (!ctx) return;
    
    const developers = Object.keys(teamData);
    const sleepData = developers.map(dev => teamData[dev].telemetry.health_data.sleep_hours);
    const stressData = developers.map(dev => teamData[dev].telemetry.health_data.stress_level);
    const focusData = developers.map(dev => {
        const dailyData = teamData[dev].telemetry.daily_data;
        return dailyData && dailyData[0] ? dailyData[0].focus_score : 85;
    });
    const developerNames = developers.map(dev => teamData[dev].user_info.name.split(' ')[0]);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: developerNames,
            datasets: [
                {
                    label: 'Sleep Hours',
                    data: sleepData,
                    backgroundColor: 'rgba(14, 165, 233, 0.8)',
                    borderColor: 'rgba(14, 165, 233, 1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Focus Score',
                    data: focusData,
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                },
                {
                    label: 'Stress Level',
                    data: stressData,
                    backgroundColor: 'rgba(239, 68, 68, 0.8)',
                    borderColor: 'rgba(239, 68, 68, 1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
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
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    max: 12,
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    },
                    title: {
                        display: true,
                        text: 'Sleep Hours',
                        color: '#f8fafc'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    },
                    title: {
                        display: true,
                        text: 'Score/Stress %',
                        color: '#f8fafc'
                    }
                }
            }
        }
    });
}

// Update team metrics (simulation)
function updateTeamMetrics() {
    console.log('Updating team metrics...');
    
    // Add subtle animation to indicate update
    const metricCards = document.querySelectorAll('.card-body h3');
    metricCards.forEach(card => {
        card.style.animation = 'pulse 0.5s ease-in-out';
        setTimeout(() => {
            card.style.animation = '';
        }, 500);
    });
    
    // Update last updated timestamp
    updateLastSyncTime();
}

// Initialize sortable tables
function initSortableTables() {
    if (typeof $ !== 'undefined' && $.fn.DataTable) {
        $('.table').DataTable({
            responsive: true,
            pageLength: 10,
            order: [[1, 'desc']], // Sort by productivity by default
            language: {
                search: "Filter developers:",
                lengthMenu: "Show _MENU_ developers per page",
                info: "Showing _START_ to _END_ of _TOTAL_ developers"
            }
        });
    }
}

// Initialize developer card effects
function initDeveloperCardEffects() {
    document.querySelectorAll('.card').forEach(card => {
        // Add hover effect
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
        
        // Add click effect for developer cards
        card.addEventListener('click', function(e) {
            if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A') {
                this.style.animation = 'pulse 0.3s ease-in-out';
                setTimeout(() => {
                    this.style.animation = '';
                }, 300);
            }
        });
    });
}

// Calculate team statistics
function calculateTeamStats(teamData) {
    const developers = Object.keys(teamData);
    const stats = {
        totalDevelopers: developers.length,
        averageProductivity: 0,
        averageCollaboration: 0,
        averageHealth: 0,
        totalCommits: 0,
        totalMRs: 0,
        highPerformers: 0,
        needsSupport: 0
    };
    
    developers.forEach(dev => {
        const data = teamData[dev];
        stats.averageProductivity += data.gitlab.productivity_score;
        stats.averageCollaboration += data.gitlab.collaboration_score;
        stats.totalCommits += data.gitlab.commits_this_week;
        stats.totalMRs += data.gitlab.merge_requests_merged;
        
        // Calculate health score
        const healthScore = calculateDeveloperHealthScore(data.telemetry.health_data);
        stats.averageHealth += healthScore;
        
        // Categorize developers
        if (data.gitlab.productivity_score >= 8.0 && healthScore >= 80) {
            stats.highPerformers++;
        } else if (data.gitlab.productivity_score < 6.0 || healthScore < 60) {
            stats.needsSupport++;
        }
    });
    
    // Calculate averages
    stats.averageProductivity = (stats.averageProductivity / developers.length).toFixed(1);
    stats.averageCollaboration = (stats.averageCollaboration / developers.length).toFixed(1);
    stats.averageHealth = Math.round(stats.averageHealth / developers.length);
    
    return stats;
}

// Calculate individual developer health score
function calculateDeveloperHealthScore(healthData) {
    const sleepScore = Math.min(100, (healthData.sleep_hours / 8) * 100);
    const stressScore = 100 - healthData.stress_level;
    const activityScore = Math.min(100, (healthData.active_minutes / 60) * 100);
    
    return Math.round((sleepScore + stressScore + activityScore) / 3);
}

// Generate team insights
function generateTeamInsights(teamData) {
    const insights = [];
    const stats = calculateTeamStats(teamData);
    
    if (stats.averageProductivity >= 8.0) {
        insights.push({
            type: 'success',
            message: 'Team productivity is excellent! Average score: ' + stats.averageProductivity
        });
    } else if (stats.averageProductivity < 6.0) {
        insights.push({
            type: 'warning',
            message: 'Team productivity needs attention. Consider workload review.'
        });
    }
    
    if (stats.needsSupport > 0) {
        insights.push({
            type: 'info',
            message: `${stats.needsSupport} developer(s) may need additional support or reduced workload.`
        });
    }
    
    if (stats.highPerformers > stats.totalDevelopers / 2) {
        insights.push({
            type: 'success',
            message: 'More than half the team are high performers! Great job!'
        });
    }
    
    return insights;
}

// Update last sync time
function updateLastSyncTime() {
    const syncElements = document.querySelectorAll('[data-last-sync]');
    const now = new Date().toLocaleString();
    
    syncElements.forEach(element => {
        element.textContent = `Last updated: ${now}`;
    });
}

// Export team report (placeholder function)
function exportTeamReport() {
    // This would generate and download a team report
    console.log('Exporting team report...');
    alert('Team report export functionality would be implemented here.');
}

// Send team notification (placeholder function)
function sendTeamNotification(message, type = 'info') {
    // This would send notifications to team members
    console.log(`Sending ${type} notification: ${message}`);
    
    // Show toast notification
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toast);
    });
}

// Filter developers by criteria
function filterDevelopers(criteria) {
    const rows = document.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const shouldShow = evaluateFilterCriteria(row, criteria);
        row.style.display = shouldShow ? '' : 'none';
    });
}

// Evaluate filter criteria for a developer row
function evaluateFilterCriteria(row, criteria) {
    // This would implement complex filtering logic
    // For now, just show all rows
    return true;
}

// Initialize admin dashboard features
document.addEventListener('DOMContentLoaded', function() {
    // Add any additional admin-specific initialization here
    console.log('Admin dashboard features initialized');
});
