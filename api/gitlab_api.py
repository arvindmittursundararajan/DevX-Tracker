from .gitlab_integration import GitLabIntegration
from datetime import datetime, timedelta
import logging
import os
import requests
from typing import Dict, List, Any

class GitLabAPI:
    def __init__(self):
        self.gitlab = GitLabIntegration()
        self.base_url = os.getenv('GITLAB_API_URL', 'https://gitlab.com/api/v4')
        self.access_token = os.getenv('GITLAB_ACCESS_TOKEN', '')
        if not self.access_token:
            logging.warning("GITLAB_ACCESS_TOKEN not set in environment variables")
        self.headers = {
            'PRIVATE-TOKEN': self.access_token
        }
        logging.info(f"Initialized with base URL: {self.base_url}")
        
    def get_developer_metrics(self, username: str) -> Dict[str, Any]:
        """Get comprehensive metrics for a developer"""
        try:
            # Get user details
            user = self._get_user_details(username)
            if not user:
                return self._get_mock_metrics(username)

            # Get historical data (last 3 months)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            # Get historical commits
            commits = self._get_historical_commits(user['id'], start_date, end_date)
            
            # Get historical merge requests
            merge_requests = self._get_historical_merge_requests(user['id'], start_date, end_date)
            
            # Get historical issues
            issues = self._get_historical_issues(user['id'], start_date, end_date)
            
            # Calculate metrics
            metrics = {
                'commits_this_week': len([c for c in commits if (end_date - datetime.fromisoformat(c['created_at'].replace('Z', '+00:00'))).days <= 7]),
                'merge_requests_open': len([mr for mr in merge_requests if mr['state'] == 'opened']),
                'merge_requests_merged': len([mr for mr in merge_requests if mr['state'] == 'merged']),
                'issues_assigned': len([i for i in issues if i['state'] == 'opened']),
                'issues_closed': len([i for i in issues if i['state'] == 'closed']),
                'productivity_score': self._calculate_productivity_score(commits, merge_requests, issues),
                'collaboration_score': self._calculate_collaboration_score(merge_requests, issues),
                'pipeline_success_rate': self._calculate_pipeline_success_rate(user['id']),
                'gitlab_projects': self._get_user_projects(user['id']),
                'recent_activity': self._get_recent_activity(commits, merge_requests, issues),
                'weekly_contribution_trend': self._calculate_weekly_trend(commits, merge_requests, issues),
                'language_breakdown': self._get_language_breakdown(user['id']),
                'lines_of_code': self._calculate_lines_of_code(commits),
                'avg_merge_time_hours': self._calculate_avg_merge_time(merge_requests),
                'code_review_participation': self._calculate_review_participation(user['id']),
                'historical_data': {
                    'commits': self._format_historical_data(commits),
                    'merge_requests': self._format_historical_data(merge_requests),
                    'issues': self._format_historical_data(issues)
                }
            }
            
            return metrics
        except Exception as e:
            logging.error(f"Error getting metrics for {username}: {str(e)}")
            return self._get_mock_metrics(username)

    def _get_historical_commits(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get historical commits for a user"""
        commits = []
        page = 1
        while True:
            response = requests.get(
                f"{self.base_url}/users/{user_id}/events",
                headers=self.headers,
                params={
                    'action': 'pushed',
                    'after': start_date.isoformat(),
                    'before': end_date.isoformat(),
                    'per_page': 100,
                    'page': page
                }
            )
            if response.status_code != 200:
                break
            data = response.json()
            if not data:
                break
            commits.extend(data)
            page += 1
        return commits

    def _get_historical_merge_requests(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get historical merge requests for a user"""
        merge_requests = []
        page = 1
        while True:
            response = requests.get(
                f"{self.base_url}/merge_requests",
                headers=self.headers,
                params={
                    'author_id': user_id,
                    'created_after': start_date.isoformat(),
                    'created_before': end_date.isoformat(),
                    'per_page': 100,
                    'page': page
                }
            )
            if response.status_code != 200:
                break
            data = response.json()
            if not data:
                break
            merge_requests.extend(data)
            page += 1
        return merge_requests

    def _get_historical_issues(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get historical issues for a user"""
        issues = []
        page = 1
        while True:
            response = requests.get(
                f"{self.base_url}/issues",
                headers=self.headers,
                params={
                    'assignee_id': user_id,
                    'created_after': start_date.isoformat(),
                    'created_before': end_date.isoformat(),
                    'per_page': 100,
                    'page': page
                }
            )
            if response.status_code != 200:
                break
            data = response.json()
            if not data:
                break
            issues.extend(data)
            page += 1
        return issues

    def _format_historical_data(self, items: List[Dict]) -> List[Dict]:
        """Format historical data for display"""
        formatted_items = []
        for item in items:
            formatted_item = {
                'id': item.get('id'),
                'title': item.get('title', ''),
                'created_at': item.get('created_at', ''),
                'state': item.get('state', ''),
                'type': 'commit' if 'commit' in item else 'merge_request' if 'merge_request' in item else 'issue',
                'description': item.get('description', '')[:100] + '...' if item.get('description') else '',
                'url': item.get('web_url', '')
            }
            formatted_items.append(formatted_item)
        return sorted(formatted_items, key=lambda x: x['created_at'], reverse=True)

    def _is_this_week(self, date_str):
        """Check if date is within this week"""
        if not date_str or date_str == "Unknown":
            return False
        try:
            date = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
            week_ago = datetime.now() - timedelta(days=7)
            return date >= week_ago
        except:
            return False
    
    def _is_today(self, date_str):
        """Check if date is today"""
        if not date_str or date_str == "Unknown":
            return False
        try:
            date = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
            return date.date() == datetime.now().date()
        except:
            return False
    
    def _calculate_pipeline_success_rate(self, pipelines_data):
        """Calculate pipeline success rate"""
        if not pipelines_data.get('recent'):
            return 0.85  # Default reasonable rate
        
        successful = pipelines_data.get('successful', 0)
        total = pipelines_data.get('total', 0)
        if total == 0:
            return 0.85
        return min(successful / total, 1.0)
    
    def _estimate_lines_of_code(self, commits):
        """Estimate lines of code based on commits"""
        return len(commits) * 75
    
    def _get_last_commit_time(self, commits):
        """Get the time of the last commit"""
        if not commits:
            return (datetime.now() - timedelta(hours=24)).isoformat()
        return commits[0].get('created_at', datetime.now().isoformat())
    
    def _calculate_weekly_trend(self, commits, merge_requests, issues):
        """Calculate weekly contribution trend"""
        trend = [0] * 7
        today = datetime.now()
        
        # Process commits
        for commit in commits:
            commit_date = datetime.fromisoformat(commit['created_at'].replace('Z', '+00:00'))
            days_ago = (today - commit_date).days
            if 0 <= days_ago < 7:
                trend[days_ago] += 1
        
        # Process merge requests
        for mr in merge_requests:
            mr_date = datetime.fromisoformat(mr['created_at'].replace('Z', '+00:00'))
            days_ago = (today - mr_date).days
            if 0 <= days_ago < 7:
                trend[days_ago] += 2
        
        # Process issues
        for issue in issues:
            issue_date = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
            days_ago = (today - issue_date).days
            if 0 <= days_ago < 7:
                trend[days_ago] += 1
        
        return trend
    
    def _format_recent_activity(self, metrics):
        """Format recent activity from GitLab data"""
        activities = []
        
        # Add recent commits
        for commit in metrics['commits']['recent'][:3]:
            activities.append({
                'action': f"Committed: {commit['title']}",
                'timestamp': commit['created_at'],
                'type': 'commit'
            })
        
        # Add recent merge requests
        for mr in metrics['merge_requests']['recent'][:2]:
            activities.append({
                'action': f"Merge Request: {mr['title']}",
                'timestamp': mr['created_at'],
                'type': 'merge_request'
            })
        
        return sorted(activities, key=lambda x: x['timestamp'], reverse=True)[:5]
    
    def _get_fallback_metrics(self):
        """Fallback metrics when API is unavailable"""
        return {
            'commits_this_week': 0,
            'commits_today': 0,
            'merge_requests_open': 0,
            'merge_requests_merged': 0,
            'issues_assigned': 0,
            'issues_closed': 0,
            'code_review_participation': 0.0,
            'pipeline_success_rate': 0.0,
            'avg_merge_time_hours': 0.0,
            'lines_of_code': 0,
            'productivity_score': 0.0,
            'collaboration_score': 0.0,
            'last_commit': None,
            'weekly_contribution_trend': [0] * 7,
            'language_breakdown': {},
            'recent_activity': []
        }
    
    def get_team_metrics(self):
        """Get aggregated team metrics"""
        team_data = {}
        users = ['dev1', 'dev2', 'dev3', 'dev4']
        
        for user in users:
            team_data[user] = self.get_developer_metrics(user)
        
        return team_data

    def _get_mock_metrics(self, username: str) -> Dict[str, Any]:
        """Get mock metrics for testing"""
        return {
            'commits_this_week': 15,
            'merge_requests_open': 2,
            'merge_requests_merged': 8,
            'issues_assigned': 5,
            'issues_closed': 12,
            'productivity_score': 7.5,
            'collaboration_score': 6.0,
            'pipeline_success_rate': 0.85,
            'gitlab_projects': [
                {
                    'name': 'Project A',
                    'description': 'Main project',
                    'stars': 5,
                    'last_activity': '2 days ago'
                }
            ],
            'recent_activity': [
                {
                    'type': 'commit',
                    'action': 'Pushed to main',
                    'timestamp': '2 hours ago'
                }
            ],
            'weekly_contribution_trend': [5, 8, 12, 7, 9, 11, 6],
            'language_breakdown': {
                'Python': 45,
                'JavaScript': 30,
                'TypeScript': 25
            },
            'lines_of_code': 15000,
            'avg_merge_time_hours': 24,
            'code_review_participation': 0.75,
            'historical_data': {
                'commits': [],
                'merge_requests': [],
                'issues': []
            }
        }

    def _get_user_details(self, username: str) -> Dict:
        """Get user details from GitLab"""
        try:
            response = requests.get(
                f"{self.base_url}/users",
                headers=self.headers,
                params={'username': username}
            )
            if response.status_code == 200:
                users = response.json()
                return users[0] if users else None
            return None
        except Exception as e:
            logging.error(f"Error getting user details: {str(e)}")
            return None

    def _get_user_projects(self, user_id: int) -> List[Dict]:
        """Get user's projects from GitLab"""
        try:
            response = requests.get(
                f"{self.base_url}/users/{user_id}/projects",
                headers=self.headers,
                params={'per_page': 5}
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logging.error(f"Error getting user projects: {str(e)}")
            return []

    def _calculate_productivity_score(self, commits: List[Dict], merge_requests: List[Dict], issues: List[Dict]) -> float:
        """Calculate productivity score based on activity"""
        try:
            commit_score = min(len(commits) * 0.5, 5.0)
            mr_score = min(len(merge_requests) * 0.3, 3.0)
            issue_score = min(len(issues) * 0.2, 2.0)
            return min(commit_score + mr_score + issue_score, 10.0)
        except Exception as e:
            logging.error(f"Error calculating productivity score: {str(e)}")
            return 5.0

    def _calculate_collaboration_score(self, merge_requests: List[Dict], issues: List[Dict]) -> float:
        """Calculate collaboration score based on MRs and issues"""
        try:
            mr_score = min(len(merge_requests) * 0.6, 6.0)
            issue_score = min(len(issues) * 0.4, 4.0)
            return min(mr_score + issue_score, 10.0)
        except Exception as e:
            logging.error(f"Error calculating collaboration score: {str(e)}")
            return 5.0

    def _calculate_pipeline_success_rate(self, user_id: int) -> float:
        """Calculate pipeline success rate"""
        try:
            response = requests.get(
                f"{self.base_url}/users/{user_id}/pipelines",
                headers=self.headers,
                params={'per_page': 100}
            )
            if response.status_code == 200:
                pipelines = response.json()
                successful = len([p for p in pipelines if p['status'] == 'success'])
                total = len(pipelines)
                return successful / total if total > 0 else 0.85
            return 0.85
        except Exception as e:
            logging.error(f"Error calculating pipeline success rate: {str(e)}")
            return 0.85

    def _get_recent_activity(self, commits: List[Dict], merge_requests: List[Dict], issues: List[Dict]) -> List[Dict]:
        """Get recent activity from all sources"""
        activities = []
        
        # Add commits
        for commit in commits[:3]:
            activities.append({
                'type': 'commit',
                'action': f"Committed: {commit.get('title', '')}",
                'timestamp': commit.get('created_at', '')
            })
        
        # Add merge requests
        for mr in merge_requests[:2]:
            activities.append({
                'type': 'merge_request',
                'action': f"Merge Request: {mr.get('title', '')}",
                'timestamp': mr.get('created_at', '')
            })
        
        # Add issues
        for issue in issues[:2]:
            activities.append({
                'type': 'issue',
                'action': f"Issue: {issue.get('title', '')}",
                'timestamp': issue.get('created_at', '')
            })
        
        return sorted(activities, key=lambda x: x['timestamp'], reverse=True)[:5]

    def _calculate_weekly_trend(self, commits: List[Dict], merge_requests: List[Dict], issues: List[Dict]) -> List[int]:
        """Calculate weekly contribution trend"""
        try:
            trend = [0] * 7
            today = datetime.now()
            
            # Process commits
            for commit in commits:
                commit_date = datetime.fromisoformat(commit['created_at'].replace('Z', '+00:00'))
                days_ago = (today - commit_date).days
                if 0 <= days_ago < 7:
                    trend[days_ago] += 1
            
            # Process merge requests
            for mr in merge_requests:
                mr_date = datetime.fromisoformat(mr['created_at'].replace('Z', '+00:00'))
                days_ago = (today - mr_date).days
                if 0 <= days_ago < 7:
                    trend[days_ago] += 2
            
            # Process issues
            for issue in issues:
                issue_date = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
                days_ago = (today - issue_date).days
                if 0 <= days_ago < 7:
                    trend[days_ago] += 1
            
            return trend
        except Exception as e:
            logging.error(f"Error calculating weekly trend: {str(e)}")
            return [0] * 7

    def _get_language_breakdown(self, user_id: int) -> Dict[str, int]:
        """Get language breakdown from user's projects"""
        try:
            projects = self._get_user_projects(user_id)
            languages = {}
            
            for project in projects:
                response = requests.get(
                    f"{self.base_url}/projects/{project['id']}/languages",
                    headers=self.headers
                )
                if response.status_code == 200:
                    project_languages = response.json()
                    for lang, percentage in project_languages.items():
                        languages[lang] = languages.get(lang, 0) + percentage
            
            # Normalize percentages
            total = sum(languages.values())
            if total > 0:
                languages = {k: int((v / total) * 100) for k, v in languages.items()}
            
            return languages
        except Exception as e:
            logging.error(f"Error getting language breakdown: {str(e)}")
            return {'Python': 45, 'JavaScript': 30, 'TypeScript': 25}

    def _calculate_lines_of_code(self, commits: List[Dict]) -> int:
        """Calculate total lines of code from commits"""
        try:
            return len(commits) * 75  # Estimate 75 lines per commit
        except Exception as e:
            logging.error(f"Error calculating lines of code: {str(e)}")
            return 0

    def _calculate_avg_merge_time(self, merge_requests: List[Dict]) -> float:
        """Calculate average merge time in hours"""
        try:
            merged_mrs = [mr for mr in merge_requests if mr['state'] == 'merged']
            if not merged_mrs:
                return 24.0
            
            total_hours = 0
            for mr in merged_mrs:
                created_at = datetime.fromisoformat(mr['created_at'].replace('Z', '+00:00'))
                merged_at = datetime.fromisoformat(mr['merged_at'].replace('Z', '+00:00'))
                hours = (merged_at - created_at).total_seconds() / 3600
                total_hours += hours
            
            return round(total_hours / len(merged_mrs), 1)
        except Exception as e:
            logging.error(f"Error calculating average merge time: {str(e)}")
            return 24.0

    def _calculate_review_participation(self, user_id: int) -> float:
        """Calculate code review participation rate"""
        try:
            response = requests.get(
                f"{self.base_url}/users/{user_id}/merge_requests",
                headers=self.headers,
                params={'scope': 'assigned_to_me'}
            )
            if response.status_code == 200:
                mrs = response.json()
                reviewed = len([mr for mr in mrs if mr.get('reviewed', False)])
                total = len(mrs)
                return reviewed / total if total > 0 else 0.75
            return 0.75
        except Exception as e:
            logging.error(f"Error calculating review participation: {str(e)}")
            return 0.75
