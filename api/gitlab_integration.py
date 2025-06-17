import requests
import os
from typing import List, Dict, Optional
from datetime import datetime

class GitLabIntegration:
    def __init__(self, access_token: str = None):
        """Initialize with GitLab personal access token"""
        self.base_url = os.getenv('GITLAB_API_URL', 'https://gitlab.com/api/v4')
        self.access_token = access_token or os.environ.get("GITLAB_ACCESS_TOKEN", "")
        if not self.access_token:
            print("Warning: GITLAB_ACCESS_TOKEN not set in environment variables")
        self.headers = {
            "PRIVATE-TOKEN": self.access_token
        }
    
    def get_personal_projects(self) -> List[Dict]:
        """Fetch all personal projects from GitLab"""
        url = f"{self.base_url}/projects"
        params = {
            "membership": "true",
            "owned": "true",
            "per_page": 100
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching projects: {e}")
            return []

    def get_issues(self, project_id: int = None) -> List[Dict]:
        """Fetch issues from GitLab"""
        if project_id:
            url = f"{self.base_url}/projects/{project_id}/issues"
        else:
            url = f"{self.base_url}/issues"
            
        params = {
            "per_page": 100,
            "state": "opened"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues: {e}")
            return []

    def get_merge_requests(self, project_id: int = None) -> List[Dict]:
        """Fetch merge requests from GitLab"""
        if project_id:
            url = f"{self.base_url}/projects/{project_id}/merge_requests"
        else:
            url = f"{self.base_url}/merge_requests"
            
        params = {
            "per_page": 100,
            "state": "opened"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching merge requests: {e}")
            return []

    def get_pipelines(self, project_id: int = None) -> List[Dict]:
        """Fetch pipelines from GitLab"""
        if project_id:
            url = f"{self.base_url}/projects/{project_id}/pipelines"
        else:
            # Get pipelines from all user projects
            projects = self.get_personal_projects()
            all_pipelines = []
            for project in projects[:5]:  # Limit to first 5 projects
                project_pipelines = self._get_project_pipelines(project['id'])
                all_pipelines.extend(project_pipelines)
            return all_pipelines
            
        params = {
            "per_page": 20,
            "order_by": "updated_at",
            "sort": "desc"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching pipelines: {e}")
            return []

    def _get_project_pipelines(self, project_id: int) -> List[Dict]:
        """Get pipelines for a specific project"""
        url = f"{self.base_url}/projects/{project_id}/pipelines"
        params = {
            "per_page": 10,
            "order_by": "updated_at",
            "sort": "desc"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            pipelines = response.json()
            # Add project_id to each pipeline for reference
            for pipeline in pipelines:
                pipeline['project_id'] = project_id
            return pipelines
        except requests.exceptions.RequestException:
            return []

    def get_pipeline_jobs(self, project_id: int, pipeline_id: int) -> List[Dict]:
        """Fetch jobs for a specific pipeline"""
        url = f"{self.base_url}/projects/{project_id}/pipelines/{pipeline_id}/jobs"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching pipeline jobs: {e}")
            return []

    def get_commits(self, project_id: int = None, since: str = None) -> List[Dict]:
        """Fetch recent commits"""
        if project_id:
            url = f"{self.base_url}/projects/{project_id}/repository/commits"
        else:
            # Get commits from all user projects
            projects = self.get_personal_projects()
            all_commits = []
            for project in projects[:5]:  # Limit to first 5 projects
                project_commits = self._get_project_commits(project['id'], since)
                all_commits.extend(project_commits)
            return sorted(all_commits, key=lambda x: x.get('created_at', ''), reverse=True)[:50]
            
        params = {
            "per_page": 50,
            "order": "desc"
        }
        if since:
            params["since"] = since
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching commits: {e}")
            return []

    def _get_project_commits(self, project_id: int, since: str = None) -> List[Dict]:
        """Get commits for a specific project"""
        url = f"{self.base_url}/projects/{project_id}/repository/commits"
        params = {
            "per_page": 20,
            "order": "desc"
        }
        if since:
            params["since"] = since
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            commits = response.json()
            # Add project_id to each commit for reference
            for commit in commits:
                commit['project_id'] = project_id
            return commits
        except requests.exceptions.RequestException:
            return []

    def format_project_info(self, project: Dict) -> Dict:
        """Format project information for display"""
        return {
            "id": project.get("id"),
            "name": project.get("name"),
            "description": project.get("description", "No description"),
            "created_at": self._format_date(project.get("created_at")),
            "last_activity": self._format_date(project.get("last_activity_at")),
            "stars": project.get("star_count", 0),
            "forks": project.get("forks_count", 0),
            "url": project.get("web_url"),
            "default_branch": project.get("default_branch", "main"),
            "visibility": project.get("visibility", "private")
        }

    def format_issue_info(self, issue: Dict) -> Dict:
        """Format issue information for display"""
        return {
            "id": issue.get("iid"),
            "title": issue.get("title"),
            "description": issue.get("description", "No description")[:200],
            "state": issue.get("state"),
            "created_at": self._format_date(issue.get("created_at")),
            "updated_at": self._format_date(issue.get("updated_at")),
            "author": issue.get("author", {}).get("name", "Unknown"),
            "labels": issue.get("labels", []),
            "url": issue.get("web_url")
        }

    def format_mr_info(self, mr: Dict) -> Dict:
        """Format merge request information for display"""
        return {
            "id": mr.get("iid"),
            "title": mr.get("title"),
            "description": mr.get("description", "No description")[:200],
            "state": mr.get("state"),
            "source_branch": mr.get("source_branch"),
            "target_branch": mr.get("target_branch"),
            "author": mr.get("author", {}).get("name", "Unknown"),
            "created_at": self._format_date(mr.get("created_at")),
            "updated_at": self._format_date(mr.get("updated_at")),
            "web_url": mr.get("web_url"),
            "merge_status": mr.get("merge_status"),
            "upvotes": mr.get("upvotes", 0),
            "downvotes": mr.get("downvotes", 0)
        }

    def format_pipeline_info(self, pipeline: Dict) -> Dict:
        """Format pipeline information for display"""
        return {
            "id": pipeline.get("id"),
            "status": pipeline.get("status"),
            "ref": pipeline.get("ref"),
            "source": pipeline.get("source"),
            "created_at": self._format_datetime(pipeline.get("created_at")),
            "updated_at": self._format_datetime(pipeline.get("updated_at")),
            "duration": pipeline.get("duration", 0),
            "web_url": pipeline.get("web_url"),
            "project_id": pipeline.get("project_id")
        }

    def format_commit_info(self, commit: Dict) -> Dict:
        """Format commit information for display"""
        return {
            "id": commit.get("short_id"),
            "title": commit.get("title"),
            "message": commit.get("message", "")[:200],
            "author_name": commit.get("author_name"),
            "author_email": commit.get("author_email"),
            "created_at": self._format_datetime(commit.get("created_at")),
            "web_url": commit.get("web_url"),
            "project_id": commit.get("project_id")
        }

    def _format_date(self, date_str: str) -> str:
        """Format ISO date string to readable format"""
        if not date_str:
            return "Unknown"
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            return date_str

    def _format_datetime(self, date_str: str) -> str:
        """Format ISO datetime string to readable format"""
        if not date_str:
            return "Unknown"
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, AttributeError):
            return date_str

    def get_comprehensive_metrics(self, user_id: str = None) -> Dict:
        """Get comprehensive GitLab metrics for dashboard display"""
        try:
            projects = self.get_personal_projects()
            issues = self.get_issues()
            merge_requests = self.get_merge_requests()
            pipelines = self.get_pipelines()
            commits = self.get_commits()

            # Calculate metrics
            open_issues = len([i for i in issues if i.get('state') == 'opened'])
            open_mrs = len([mr for mr in merge_requests if mr.get('state') == 'opened'])
            successful_pipelines = len([p for p in pipelines if p.get('status') == 'success'])
            failed_pipelines = len([p for p in pipelines if p.get('status') == 'failed'])
            
            return {
                "projects": {
                    "total": len(projects),
                    "list": [self.format_project_info(p) for p in projects[:10]]
                },
                "issues": {
                    "total": len(issues),
                    "open": open_issues,
                    "recent": [self.format_issue_info(i) for i in issues[:10]]
                },
                "merge_requests": {
                    "total": len(merge_requests),
                    "open": open_mrs,
                    "recent": [self.format_mr_info(mr) for mr in merge_requests[:10]]
                },
                "pipelines": {
                    "total": len(pipelines),
                    "successful": successful_pipelines,
                    "failed": failed_pipelines,
                    "recent": [self.format_pipeline_info(p) for p in pipelines[:10]]
                },
                "commits": {
                    "total": len(commits),
                    "recent": [self.format_commit_info(c) for c in commits[:20]]
                },
                "activity_score": self._calculate_activity_score(commits, merge_requests, issues),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error getting comprehensive metrics: {e}")
            return self._get_fallback_metrics()

    def _calculate_activity_score(self, commits: List, merge_requests: List, issues: List) -> int:
        """Calculate activity score based on recent activity"""
        score = 0
        score += len(commits) * 2  # 2 points per commit
        score += len(merge_requests) * 5  # 5 points per MR
        score += len(issues) * 3  # 3 points per issue
        return min(score, 100)  # Cap at 100

    def _get_fallback_metrics(self) -> Dict:
        """Fallback metrics when API is unavailable"""
        return {
            "projects": {"total": 0, "list": []},
            "issues": {"total": 0, "open": 0, "recent": []},
            "merge_requests": {"total": 0, "open": 0, "recent": []},
            "pipelines": {"total": 0, "successful": 0, "failed": 0, "recent": []},
            "commits": {"total": 0, "recent": []},
            "activity_score": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": "Unable to connect to GitLab API"
        }