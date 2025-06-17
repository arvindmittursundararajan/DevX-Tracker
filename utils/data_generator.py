import random
from datetime import datetime, timedelta

def get_hardcoded_users():
    """Return hardcoded user data"""
    return {
        'dev1': {
            'name': 'Alex Thompson',
            'role': 'developer',
            'title': 'Senior Full-Stack Developer',
            'team': 'Platform Team',
            'email': 'alex.thompson@company.com',
            'join_date': '2022-03-15',
            'photo': '1.png'
        },
        'dev2': {
            'name': 'Sarah Chen',
            'role': 'developer', 
            'title': 'Frontend Lead Developer',
            'team': 'UI/UX Team',
            'email': 'sarah.chen@company.com',
            'join_date': '2021-09-01',
            'photo': '2.png'
        },
        'dev3': {
            'name': 'Marcus Rodriguez',
            'role': 'developer',
            'title': 'Backend Developer',
            'team': 'API Team',
            'email': 'marcus.rodriguez@company.com',
            'join_date': '2023-01-10',
            'photo': '3.png'
        },
        'dev4': {
            'name': 'Emily Zhang',
            'role': 'developer',
            'title': 'DevOps Engineer',
            'team': 'Infrastructure Team',
            'email': 'emily.zhang@company.com',
            'join_date': '2022-11-20',
            'photo': '3.png'
        },
        'admin': {
            'name': 'David Kim',
            'role': 'admin',
            'title': 'Engineering Manager',
            'team': 'Leadership',
            'email': 'david.kim@company.com',
            'join_date': '2020-05-01',
            'photo': '1.png'
        }
    }

def get_telemetry_data(user_id):
    """Generate hardcoded telemetry data for desktop apps and smartwatch"""
    
    # Base patterns per user
    if user_id == 'dev1':
        screen_time_base = 9.2
        focus_score_base = 85
    elif user_id == 'dev2':
        screen_time_base = 8.7
        focus_score_base = 92
    elif user_id == 'dev3':
        screen_time_base = 10.1
        focus_score_base = 78
    else:
        screen_time_base = 8.5
        focus_score_base = 88
    
    # Generate realistic daily data for the past week
    daily_data = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        daily_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'screen_time_hours': round(screen_time_base + random.uniform(-1.5, 2.0), 1),
            'focus_score': max(0, min(100, focus_score_base + random.randint(-15, 15))),
            'break_count': random.randint(8, 15),
            'deep_work_hours': round(random.uniform(3.0, 6.5), 1)
        })
    
    # Desktop application usage
    app_usage = [
        {'app': 'VS Code', 'hours': round(random.uniform(4.5, 7.2), 1), 'category': 'Development'},
        {'app': 'GitLab', 'hours': round(random.uniform(1.2, 2.8), 1), 'category': 'Development'},
        {'app': 'Terminal', 'hours': round(random.uniform(2.0, 4.5), 1), 'category': 'Development'},
        {'app': 'Chrome', 'hours': round(random.uniform(2.5, 4.0), 1), 'category': 'Research'},
        {'app': 'Slack', 'hours': round(random.uniform(1.0, 2.5), 1), 'category': 'Communication'},
        {'app': 'Figma', 'hours': round(random.uniform(0.5, 2.0), 1), 'category': 'Design'},
        {'app': 'Postman', 'hours': round(random.uniform(0.8, 1.5), 1), 'category': 'Testing'},
        {'app': 'Docker Desktop', 'hours': round(random.uniform(0.3, 1.0), 1), 'category': 'DevOps'}
    ]
    
    # Smartwatch health data
    health_data = {
        'heart_rate': {
            'avg': random.randint(65, 85),
            'max': random.randint(120, 150),
            'min': random.randint(55, 70)
        },
        'stress_level': random.randint(20, 80),
        'sleep_hours': round(random.uniform(6.5, 8.5), 1),
        'sleep_quality': random.randint(70, 95),
        'steps': random.randint(4000, 12000),
        'calories': random.randint(1800, 2500),
        'active_minutes': random.randint(45, 120)
    }
    
    # Productivity insights
    productivity_insights = {
        'most_productive_hours': ['09:00-11:00', '14:00-16:00'],
        'distraction_score': random.randint(15, 45),
        'multitasking_frequency': random.randint(20, 60),
        'meeting_time_percentage': random.randint(15, 35),
        'deep_work_percentage': random.randint(40, 70)
    }
    
    return {
        'daily_data': daily_data,
        'app_usage': app_usage,
        'health_data': health_data,
        'productivity_insights': productivity_insights,
        'last_sync': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def get_achievements(user_id):
    """Generate achievement data for gamification"""
    all_achievements = [
        {'name': 'Code Warrior', 'description': '100+ commits this month', 'points': 500, 'icon': 'fas fa-code', 'earned': True},
        {'name': 'Review Master', 'description': 'Reviewed 50+ merge requests', 'points': 300, 'icon': 'fas fa-search', 'earned': True},
        {'name': 'Bug Hunter', 'description': 'Closed 25+ issues', 'points': 400, 'icon': 'fas fa-bug', 'earned': True},
        {'name': 'Team Player', 'description': 'High collaboration score', 'points': 200, 'icon': 'fas fa-users', 'earned': True},
        {'name': 'Pipeline Pro', 'description': '95%+ pipeline success rate', 'points': 350, 'icon': 'fas fa-rocket', 'earned': random.choice([True, False])},
        {'name': 'Speed Demon', 'description': 'Fast merge times', 'points': 250, 'icon': 'fas fa-tachometer-alt', 'earned': random.choice([True, False])},
        {'name': 'Documentation Hero', 'description': 'Excellent documentation', 'points': 150, 'icon': 'fas fa-book', 'earned': random.choice([True, False])},
        {'name': 'Quality Guardian', 'description': 'Zero critical bugs', 'points': 600, 'icon': 'fas fa-shield-alt', 'earned': False}
    ]
    
    # Randomize achievements per user
    user_achievements = []
    for achievement in all_achievements:
        if achievement['earned'] or random.random() > 0.3:
            user_achievements.append(achievement)
    
    total_points = sum(a['points'] for a in user_achievements if a['earned'])
    level = min(10, total_points // 500 + 1)
    
    return {
        'achievements': user_achievements,
        'total_points': total_points,
        'level': level,
        'next_level_points': (level * 500) if level < 10 else 5000,
        'weekly_points': random.randint(50, 200)
    }

def get_recommendations(user_id, gitlab_metrics):
    """Generate AI-powered recommendations based on metrics"""
    recommendations = []
    
    # Analyze productivity score
    if gitlab_metrics.get('productivity_score', 0) < 7.0:
        recommendations.append({
            'type': 'productivity',
            'priority': 'high',
            'title': 'Boost Your Productivity',
            'description': 'Your productivity score is below average. Consider breaking down large tasks into smaller chunks and using time-blocking techniques.',
            'action': 'Try the Pomodoro Technique for better focus',
            'icon': 'fas fa-chart-line'
        })
    
    # Analyze collaboration
    if gitlab_metrics.get('collaboration_score', 0) < 7.5:
        recommendations.append({
            'type': 'collaboration',
            'priority': 'medium',
            'title': 'Enhance Team Collaboration',
            'description': 'Increase your code review participation and engage more in team discussions.',
            'action': 'Review 2-3 more merge requests this week',
            'icon': 'fas fa-users'
        })
    
    # Analyze pipeline success rate
    if gitlab_metrics.get('pipeline_success_rate', 0) < 0.85:
        recommendations.append({
            'type': 'quality',
            'priority': 'high',
            'title': 'Improve Code Quality',
            'description': 'Your pipeline success rate could be improved with better testing practices.',
            'action': 'Add more unit tests before committing',
            'icon': 'fas fa-check-circle'
        })
    
    # Analyze commit frequency
    if gitlab_metrics.get('commits_this_week', 0) > 40:
        recommendations.append({
            'type': 'workflow',
            'priority': 'low',
            'title': 'Consider Larger Commits',
            'description': 'You have many small commits. Consider grouping related changes together.',
            'action': 'Use feature branches for related changes',
            'icon': 'fas fa-code-branch'
        })
    
    # Always include some general wellness recommendations
    wellness_tips = [
        {
            'type': 'wellness',
            'priority': 'medium',
            'title': 'Take Regular Breaks',
            'description': 'Regular breaks improve focus and prevent burnout. Try the 20-20-20 rule.',
            'action': 'Set a break reminder every 90 minutes',
            'icon': 'fas fa-coffee'
        },
        {
            'type': 'wellness',
            'priority': 'low',
            'title': 'Stay Hydrated',
            'description': 'Proper hydration improves cognitive function and energy levels.',
            'action': 'Keep a water bottle at your desk',
            'icon': 'fas fa-tint'
        }
    ]
    
    recommendations.extend(random.sample(wellness_tips, 1))
    
    return recommendations[:4]  # Return max 4 recommendations
