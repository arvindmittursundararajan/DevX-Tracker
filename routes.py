import os
import logging
from flask import render_template, request, session, redirect, url_for, jsonify, flash, send_from_directory
from app import app
from api.gitlab_api import GitLabAPI
from api.gitlab_integration import GitLabIntegration
from api.gitlab_sync import GitLabSync
from ai.recommendations import GeminiRecommendations
from ai.adk_agent import get_adk_insights
from db.models import MongoDBManager
from utils.data_generator import get_telemetry_data, get_hardcoded_users, get_achievements
import traceback
from datetime import datetime, timezone

# Initialize components
gitlab_api = GitLabAPI()
gitlab_sync = GitLabSync()
mongodb = MongoDBManager()
gemini = GeminiRecommendations(os.getenv('GEMINI_API_KEY', ''))

@app.route('/')
def index():
    """Main dashboard route"""
    if 'user_role' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id', 'dev1')
    user_role = session.get('user_role', 'developer')
    
    if user_role == 'admin':
        return redirect(url_for('admin'))
    
    # Get GitLab metrics
    gitlab_metrics = gitlab_api.get_developer_metrics(user_id) or {}
    
    # Get user information
    users = get_hardcoded_users()
    current_user = users.get(user_id, users['dev1'])
    
    # Get developer details for Gemini
    developer_details = {
        'name': current_user.get('name', 'Unknown'),
        'team': current_user.get('team', 'Unknown'),
        'role': current_user.get('role', 'developer'),
        'recent_activity': gitlab_metrics.get('recent_activity', []),
        'skills': gitlab_metrics.get('skills', [])
    }
    
    # Get AI recommendations from Gemini
    recommendations = gemini.get_recommendations(developer_details) or {'recommendations': []}
    
    # Get achievements
    achievements = get_achievements(user_id) or []
    
    # Create productivity insights
    productivity_insights = {
        'productivity_score': gitlab_metrics.get('productivity_score', 7),
        'collaboration_score': gitlab_metrics.get('collaboration_score', 6),
        'strengths': [
            'Active project participation',
            'Multiple project contributions',
            'Regular code commits'
        ],
        'areas_for_improvement': [
            'Issue tracking',
            'Documentation',
            'Code review participation'
        ]
    }
    
    # Create weekly goals
    weekly_goals = [
        {
            'goal': 'Improve Issue Management',
            'metric': 'Number of issues created',
            'target': '5'
        },
        {
            'goal': 'Enhance Documentation',
            'metric': 'Documentation updates',
            'target': '3'
        }
    ]
    
    # Create skill development data
    skill_development = {
        'current_level': 'intermediate',
        'recommended_focus': ['Project Management', 'Documentation'],
        'learning_resources': ['GitLab Documentation', 'Project Management Best Practices']
    }
    
    return render_template('dashboard.html', 
                         gitlab_metrics=gitlab_metrics,
                         achievements=achievements,
                         recommendations=recommendations['recommendations'],
                         current_user=current_user,
                         user_id=user_id,
                         productivity_insights=productivity_insights,
                         weekly_goals=weekly_goals,
                         skill_development=skill_development)

@app.route('/telemetry')
def telemetry():
    """Telemetry and profile page"""
    if 'user_role' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id', 'dev1')
    user_role = session.get('user_role', 'developer')
    
    if user_role == 'admin':
        return redirect(url_for('admin'))
    
    # Get telemetry data
    telemetry_data = get_telemetry_data(user_id)
    users = get_hardcoded_users()
    current_user = users.get(user_id, users['dev1'])
    
    return render_template('telemetry.html', 
                         telemetry_data=telemetry_data,
                         current_user=current_user,
                         user_id=user_id)

@app.route('/admin')
def admin():
    """Admin dashboard"""
    if 'user_role' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    # Get comprehensive team data including GitLab metrics
    team_data = gitlab_api.get_team_metrics()
    users = get_hardcoded_users()
    team_metrics = {}
    
    for user_id in users.keys():
        if user_id != 'admin':
            gitlab_metrics = gitlab_api.get_developer_metrics(user_id)
            team_metrics[user_id] = {
                'gitlab': gitlab_metrics,
                'telemetry': get_telemetry_data(user_id),
                'user_info': users[user_id]
            }
    
    return render_template('admin.html', 
                         team_metrics=team_metrics, 
                         team_data=team_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple hardcoded authentication
        users = get_hardcoded_users()
        
        if username in users and password == 'password':
            session['user_id'] = username
            session['user_role'] = users[username].get('role', 'developer')
            flash(f'Welcome, {users[username]["name"]}!', 'success')
            
            if session['user_role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Try: dev1/password, dev2/password, or admin/password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/api/gitlab_metrics/<user_id>')
def api_gitlab_metrics(user_id):
    """API endpoint for GitLab metrics"""
    metrics = gitlab_api.get_developer_metrics(user_id)
    return jsonify(metrics)

@app.route('/api/telemetry/<user_id>')
def api_telemetry(user_id):
    """API endpoint for telemetry data"""
    data = get_telemetry_data(user_id)
    return jsonify(data)

@app.route('/api/recommendations/<user_id>')
def api_recommendations(user_id):
    """API endpoint for AI recommendations"""
    gitlab_metrics = gitlab_api.get_developer_metrics(user_id)
    developer_details = {
        'user_info': {
            'name': get_hardcoded_users()[user_id]['name'],
            'username': user_id,
            'role': get_hardcoded_users()[user_id]['role']
        },
        'activity': {
            'total_events': gitlab_metrics.get('commits_this_week', 0),
            'total_projects': len(gitlab_metrics.get('gitlab_projects', [])),
            'projects': gitlab_metrics.get('gitlab_projects', [])[:5]
        },
        'contributions': {
            'commits': {'total': gitlab_metrics.get('commits_this_week', 0)},
            'merge_requests': {
                'total': gitlab_metrics.get('merge_requests_open', 0) + gitlab_metrics.get('merge_requests_merged', 0),
                'open': gitlab_metrics.get('merge_requests_open', 0),
                'merged': gitlab_metrics.get('merge_requests_merged', 0)
            },
            'issues': {
                'total': gitlab_metrics.get('issues_assigned', 0),
                'open': gitlab_metrics.get('issues_assigned', 0) - gitlab_metrics.get('issues_closed', 0),
                'closed': gitlab_metrics.get('issues_closed', 0)
            }
        }
    }
    recommendations = gemini.get_recommendations(developer_details)
    return jsonify(recommendations)

@app.route('/api/analyze_image', methods=['POST'])
def api_analyze_image():
    """API endpoint for image analysis with Gemini AI"""
    data = request.get_json()
    image_path = data.get('image_path')
    prompt = data.get('prompt')

    if not image_path or not prompt:
        return jsonify({"success": False, "error": "Image path and prompt are required."}), 400
    
    # Prepend 'static/' to the image_path to make it a valid file system path
    full_image_path = os.path.join(app.root_path, image_path)

    response = gemini.analyze_image_with_gemini(full_image_path, prompt)
    return jsonify(response)

@app.route('/api/adk_insights/<user_id>')
def api_adk_insights(user_id):
    """API endpoint for ADK insights"""
    try:
        app.logger.info(f"Processing ADK insights request for user: {user_id}")
        
        # Get GitLab metrics
        gitlab_metrics = gitlab_api.get_developer_metrics(user_id) or {}
        app.logger.info(f"Retrieved GitLab metrics: {gitlab_metrics}")
        
        # Get user information
        users = get_hardcoded_users()
        current_user = users.get(user_id, users['dev1'])
        app.logger.info(f"Retrieved user info: {current_user}")
        
        # Prepare developer details for ADK
        developer_details = {
            'name': current_user.get('name', 'Unknown'),
            'role': current_user.get('role', 'developer'),
            'recent_activity': gitlab_metrics.get('recent_activity', []),
            'skills': gitlab_metrics.get('skills', [])
        }
        app.logger.info(f"Prepared developer details: {developer_details}")
        
        # Get insights from ADK agent
        insights = get_adk_insights(developer_details)
        app.logger.info("Successfully generated insights")
        
        return jsonify(insights)
        
    except Exception as e:
        app.logger.error(f"Error in ADK insights endpoint: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Failed to generate insights',
            'message': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html'), 500
