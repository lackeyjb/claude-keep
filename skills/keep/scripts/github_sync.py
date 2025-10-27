#!/usr/bin/env python3
"""
GitHub sync helper for Keep

Provides functions for GitHub API operations with:
- Authentication handling
- Rate limit management
- Retry logic
- Error handling

Use when `gh` CLI insufficient or for programmatic access.
"""

import json
import os
import subprocess
import sys
import time
from typing import Dict, List, Optional, Any


class GitHubError(Exception):
    """Base exception for GitHub operations"""
    pass


class RateLimitError(GitHubError):
    """Raised when GitHub rate limit exceeded"""
    pass


class NotFoundError(GitHubError):
    """Raised when resource not found"""
    pass


def gh_command(args: List[str], retries: int = 3) -> Dict[str, Any]:
    """
    Execute gh CLI command with retry logic

    Args:
        args: Command arguments (e.g., ['issue', 'view', '123'])
        retries: Number of retry attempts

    Returns:
        Parsed JSON response

    Raises:
        GitHubError: If command fails after retries
        RateLimitError: If rate limit exceeded
        NotFoundError: If resource not found
    """
    cmd = ['gh'] + args

    for attempt in range(retries):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Parse JSON if output present
            if result.stdout.strip():
                return json.loads(result.stdout)
            return {}

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip()

            # Check for rate limit
            if 'rate limit' in error_msg.lower():
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limit hit, waiting {wait_time}s...", file=sys.stderr)
                    time.sleep(wait_time)
                    continue
                raise RateLimitError(f"GitHub rate limit exceeded: {error_msg}")

            # Check for not found
            if '404' in error_msg or 'not found' in error_msg.lower():
                raise NotFoundError(f"Resource not found: {error_msg}")

            # Check for authentication
            if 'authentication' in error_msg.lower():
                raise GitHubError(f"Authentication failed: {error_msg}")

            # Other errors - retry
            if attempt < retries - 1:
                wait_time = 2 ** attempt
                print(f"Command failed, retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
                continue

            raise GitHubError(f"GitHub command failed: {error_msg}")

        except json.JSONDecodeError as e:
            raise GitHubError(f"Invalid JSON response: {e}")

    raise GitHubError(f"Command failed after {retries} retries")


def fetch_issue(issue_number: str) -> Dict[str, Any]:
    """
    Fetch issue details from GitHub

    Args:
        issue_number: Issue number (without #)

    Returns:
        Issue data with keys: title, body, labels, state, etc.
    """
    return gh_command([
        'issue', 'view', str(issue_number),
        '--json', 'number,title,body,labels,state,createdAt,updatedAt,url'
    ])


def list_issues(state: str = 'open', limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    List issues from repository

    Args:
        state: Issue state ('open', 'closed', 'all')
        limit: Maximum number of issues to return

    Returns:
        List of issue data
    """
    args = [
        'issue', 'list',
        '--state', state,
        '--json', 'number,title,body,labels,state,createdAt,updatedAt'
    ]

    if limit:
        args.extend(['--limit', str(limit)])

    result = gh_command(args)
    return result if isinstance(result, list) else []


def post_comment(issue_number: str, body: str) -> Dict[str, Any]:
    """
    Post comment to issue

    Args:
        issue_number: Issue number (without #)
        body: Comment body (markdown)

    Returns:
        Comment data
    """
    return gh_command([
        'issue', 'comment', str(issue_number),
        '--body', body
    ])


def close_issue(issue_number: str, reason: Optional[str] = None) -> Dict[str, Any]:
    """
    Close an issue

    Args:
        issue_number: Issue number (without #)
        reason: Optional closing reason

    Returns:
        Updated issue data
    """
    args = ['issue', 'close', str(issue_number)]
    if reason:
        args.extend(['--comment', reason])

    return gh_command(args)


def create_issue(
    title: str,
    body: str,
    labels: Optional[List[str]] = None,
    milestone: Optional[str] = None,
    assignees: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new GitHub issue

    Args:
        title: Issue title
        body: Issue body (markdown)
        labels: List of label names
        milestone: Milestone name or number
        assignees: List of GitHub usernames

    Returns:
        Created issue data

    Raises:
        GitHubError: If creation fails
    """
    args = ['issue', 'create', '--title', title, '--body', body]

    if labels:
        for label in labels:
            args.extend(['--label', label])

    if milestone:
        args.extend(['--milestone', milestone])

    if assignees:
        for assignee in assignees:
            args.extend(['--assignee', assignee])

    return gh_command(args)


def list_labels() -> List[Dict[str, Any]]:
    """
    List repository labels

    Returns:
        List of label data with name, description, color
    """
    return gh_command([
        'label', 'list',
        '--json', 'name,description,color'
    ])


def list_milestones(state: str = 'open') -> List[Dict[str, Any]]:
    """
    List repository milestones

    Args:
        state: Milestone state ('open', 'closed', 'all')

    Returns:
        List of milestone data
    """
    return gh_command([
        'api', 'repos/{owner}/{repo}/milestones',
        '-f', f'state={state}'
    ])


def parse_dependencies(issue_body: str) -> List[str]:
    """
    Parse dependency references from issue body

    Looks for patterns like:
    - "depends on #123"
    - "blocked by #456"
    - "requires #789"

    Args:
        issue_body: Issue body text

    Returns:
        List of issue numbers (as strings)
    """
    import re

    patterns = [
        r'depends?\s+on\s+#(\d+)',
        r'blocked?\s+by\s+#(\d+)',
        r'requires?\s+#(\d+)',
        r'needs?\s+#(\d+)',
    ]

    dependencies = set()
    for pattern in patterns:
        matches = re.finditer(pattern, issue_body, re.IGNORECASE)
        dependencies.update(match.group(1) for match in matches)

    return sorted(dependencies)


def check_gh_available() -> bool:
    """
    Check if gh CLI is available

    Returns:
        True if gh CLI available, False otherwise
    """
    try:
        subprocess.run(
            ['gh', '--version'],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_repo_info() -> Dict[str, Any]:
    """
    Get current repository information

    Returns:
        Repository data with keys: owner, name, url, etc.
    """
    return gh_command([
        'repo', 'view',
        '--json', 'owner,name,url,description'
    ])


def main():
    """CLI interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='GitHub sync helper')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # fetch-issue command
    fetch_parser = subparsers.add_parser('fetch-issue', help='Fetch issue details')
    fetch_parser.add_argument('number', help='Issue number')

    # list-issues command
    list_parser = subparsers.add_parser('list-issues', help='List issues')
    list_parser.add_argument('--state', default='open', choices=['open', 'closed', 'all'])
    list_parser.add_argument('--limit', type=int, help='Max issues to return')

    # post-comment command
    comment_parser = subparsers.add_parser('post-comment', help='Post comment')
    comment_parser.add_argument('number', help='Issue number')
    comment_parser.add_argument('body', help='Comment body')

    # close-issue command
    close_parser = subparsers.add_parser('close-issue', help='Close issue')
    close_parser.add_argument('number', help='Issue number')
    close_parser.add_argument('--reason', help='Closing reason')

    # create-issue command
    create_parser = subparsers.add_parser('create-issue', help='Create issue')
    create_parser.add_argument('title', help='Issue title')
    create_parser.add_argument('body', help='Issue body')
    create_parser.add_argument('--label', action='append', help='Label to add (can be repeated)')
    create_parser.add_argument('--milestone', help='Milestone')
    create_parser.add_argument('--assignee', action='append', help='Assignee (can be repeated)')

    # list-labels command
    subparsers.add_parser('list-labels', help='List repository labels')

    # list-milestones command
    milestones_parser = subparsers.add_parser('list-milestones', help='List milestones')
    milestones_parser.add_argument('--state', default='open', choices=['open', 'closed', 'all'])

    # check command
    subparsers.add_parser('check', help='Check gh CLI availability')

    args = parser.parse_args()

    try:
        if args.command == 'fetch-issue':
            result = fetch_issue(args.number)
            print(json.dumps(result, indent=2))

        elif args.command == 'list-issues':
            result = list_issues(args.state, args.limit)
            print(json.dumps(result, indent=2))

        elif args.command == 'post-comment':
            result = post_comment(args.number, args.body)
            print(json.dumps(result, indent=2))

        elif args.command == 'close-issue':
            result = close_issue(args.number, args.reason)
            print(json.dumps(result, indent=2))

        elif args.command == 'create-issue':
            result = create_issue(
                title=args.title,
                body=args.body,
                labels=args.label,
                milestone=args.milestone,
                assignees=args.assignee
            )
            print(json.dumps(result, indent=2))

        elif args.command == 'list-labels':
            result = list_labels()
            print(json.dumps(result, indent=2))

        elif args.command == 'list-milestones':
            result = list_milestones(args.state)
            print(json.dumps(result, indent=2))

        elif args.command == 'check':
            available = check_gh_available()
            print(json.dumps({'available': available}))
            sys.exit(0 if available else 1)

        else:
            parser.print_help()
            sys.exit(1)

    except GitHubError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
