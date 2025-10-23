#!/usr/bin/env python3
"""
Issue scoring algorithm for Keep

Scores open issues based on:
- Continuity (30%): Same area as recent work
- Priority (30%): Labels indicating urgency
- Freshness (20%): Recent activity
- Dependencies (20%): Blockers cleared

Usage:
    python score_issues.py --recent-work .claude/state.md [--issues issues.json]
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# Weight distribution for scoring
WEIGHT_CONTINUITY = 0.30
WEIGHT_PRIORITY = 0.30
WEIGHT_FRESHNESS = 0.20
WEIGHT_DEPENDENCY = 0.20


def parse_state_file(state_path: str) -> Dict[str, Any]:
    """
    Parse .claude/state.md to extract recent work context

    Returns dict with:
    - recent_directories: List of directories worked in
    - recent_labels: List of labels from recent issues
    - recent_issues: List of recent issue numbers
    """
    try:
        content = Path(state_path).read_text()
    except FileNotFoundError:
        return {
            'recent_directories': [],
            'recent_labels': [],
            'recent_issues': []
        }

    # Simple parsing - look for key patterns
    directories = set()
    labels = set()
    issues = set()

    for line in content.split('\n'):
        # Extract directories from "Working primarily in src/auth/"
        if 'working primarily in' in line.lower():
            parts = line.split('in')[-1].strip()
            directories.update(d.strip().rstrip('/,') for d in parts.split() if d.strip())

        # Extract issue numbers
        if '#' in line:
            import re
            issue_nums = re.findall(r'#(\d+)', line)
            issues.update(issue_nums)

    return {
        'recent_directories': list(directories),
        'recent_labels': list(labels),
        'recent_issues': list(issues)
    }


def calculate_continuity_score(issue: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, str]:
    """
    Calculate continuity score (0-100)

    Higher score for issues in same area as recent work
    """
    score = 0
    reasons = []

    # Check if issue mentions directories from recent work
    issue_text = f"{issue.get('title', '')} {issue.get('body', '')}".lower()
    for directory in context['recent_directories']:
        if directory.lower() in issue_text:
            score += 50
            reasons.append(f"mentions {directory}")
            break

    # Check for overlapping labels
    issue_labels = {label['name'].lower() for label in issue.get('labels', [])}
    recent_labels = {label.lower() for label in context['recent_labels']}
    overlap = issue_labels & recent_labels

    if overlap:
        score += 30
        reasons.append(f"related: {', '.join(overlap)}")

    # Check if references recent issues
    issue_body = issue.get('body', '')
    for recent_issue in context['recent_issues']:
        if f'#{recent_issue}' in issue_body:
            score += 20
            reasons.append(f"references #{recent_issue}")
            break

    rationale = '; '.join(reasons) if reasons else 'no continuity'
    return min(score, 100), rationale


def calculate_priority_score(issue: Dict[str, Any]) -> Tuple[float, str]:
    """
    Calculate priority score (0-100) from labels
    """
    labels = {label['name'].lower() for label in issue.get('labels', [])}

    if 'urgent' in labels:
        return 100, 'urgent'
    elif 'high-priority' in labels or 'high' in labels:
        return 75, 'high-priority'
    elif 'low-priority' in labels or 'low' in labels:
        return 25, 'low-priority'
    else:
        return 50, 'medium (default)'


def calculate_freshness_score(issue: Dict[str, Any]) -> Tuple[float, str]:
    """
    Calculate freshness score (0-100) based on last update
    """
    updated_at = issue.get('updatedAt')
    if not updated_at:
        return 50, 'unknown update time'

    try:
        # Parse ISO 8601 timestamp
        updated = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        days_ago = (now - updated).days

        if days_ago <= 7:
            return 100, f'updated {days_ago}d ago'
        elif days_ago <= 14:
            return 75, f'updated {days_ago}d ago'
        elif days_ago <= 30:
            return 50, f'updated {days_ago}d ago'
        else:
            return 25, f'updated {days_ago}d ago'

    except (ValueError, AttributeError):
        return 50, 'invalid update time'


def parse_blockers(issue_body: str) -> List[str]:
    """
    Parse blocker references from issue body

    Looks for:
    - "depends on #123"
    - "blocked by #456"
    - "requires #789"
    """
    import re

    if not issue_body:
        return []

    patterns = [
        r'depends?\s+on\s+#(\d+)',
        r'blocked?\s+by\s+#(\d+)',
        r'requires?\s+#(\d+)',
        r'needs?\s+#(\d+)',
    ]

    blockers = set()
    for pattern in patterns:
        matches = re.finditer(pattern, issue_body, re.IGNORECASE)
        blockers.update(match.group(1) for match in matches)

    return list(blockers)


def calculate_dependency_score(
    issue: Dict[str, Any],
    all_issues: List[Dict[str, Any]]
) -> Tuple[float, str]:
    """
    Calculate dependency score (0-100)

    Lower score if has open blockers
    """
    blockers = parse_blockers(issue.get('body', ''))

    if not blockers:
        return 100, 'no dependencies'

    # Check status of blockers
    issue_map = {str(i['number']): i for i in all_issues}
    open_blockers = []
    closed_blockers = []

    for blocker_num in blockers:
        blocker = issue_map.get(blocker_num)
        if blocker:
            if blocker.get('state') == 'OPEN':
                open_blockers.append(blocker_num)
            else:
                closed_blockers.append(blocker_num)
        else:
            # Unknown blocker - assume open (conservative)
            open_blockers.append(blocker_num)

    if not open_blockers:
        return 90, f"dependencies resolved: #{', #'.join(closed_blockers)}"

    # Penalty for each open blocker
    penalty = len(open_blockers) * 25
    score = max(0, 100 - penalty)

    reason = f"blocked by #{', #'.join(open_blockers)}"
    if closed_blockers:
        reason += f" (#{', #'.join(closed_blockers)} done)"

    return score, reason


def score_issue(
    issue: Dict[str, Any],
    context: Dict[str, Any],
    all_issues: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Score a single issue

    Returns dict with:
    - total_score: Weighted total (0-100)
    - continuity_score, continuity_reason
    - priority_score, priority_reason
    - freshness_score, freshness_reason
    - dependency_score, dependency_reason
    """
    continuity_score, continuity_reason = calculate_continuity_score(issue, context)
    priority_score, priority_reason = calculate_priority_score(issue)
    freshness_score, freshness_reason = calculate_freshness_score(issue)
    dependency_score, dependency_reason = calculate_dependency_score(issue, all_issues)

    total_score = (
        continuity_score * WEIGHT_CONTINUITY +
        priority_score * WEIGHT_PRIORITY +
        freshness_score * WEIGHT_FRESHNESS +
        dependency_score * WEIGHT_DEPENDENCY
    )

    return {
        'number': issue['number'],
        'title': issue['title'],
        'total_score': round(total_score, 1),
        'continuity_score': round(continuity_score, 1),
        'continuity_reason': continuity_reason,
        'priority_score': round(priority_score, 1),
        'priority_reason': priority_reason,
        'freshness_score': round(freshness_score, 1),
        'freshness_reason': freshness_reason,
        'dependency_score': round(dependency_score, 1),
        'dependency_reason': dependency_reason,
    }


def score_all_issues(
    issues: List[Dict[str, Any]],
    context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Score all issues and return sorted by score descending
    """
    scored = [score_issue(issue, context, issues) for issue in issues]
    return sorted(scored, key=lambda x: x['total_score'], reverse=True)


def format_recommendations(scored_issues: List[Dict[str, Any]], top_n: int = 5) -> str:
    """
    Format scored issues as recommendations
    """
    if not scored_issues:
        return "No issues to recommend"

    lines = ["🎯 Recommended Next Work\n"]

    # Top recommendation
    top = scored_issues[0]
    lines.append(f"🔥 Hot Recommendation:")
    lines.append(f"#{top['number']} - {top['title']}")
    lines.append(f"├─ Score: {top['total_score']}/100")
    lines.append(f"├─ {top['continuity_reason']}")
    lines.append(f"└─ Priority: {top['priority_reason']}")
    lines.append("")

    # Other options
    if len(scored_issues) > 1:
        lines.append("📋 Other Good Options:\n")
        for i, issue in enumerate(scored_issues[1:top_n], start=2):
            lines.append(f"{i}. #{issue['number']} - {issue['title']}")
            lines.append(f"   └─ Score: {issue['total_score']} | {issue['priority_reason']}")
            if issue['dependency_score'] < 100:
                lines.append(f"      {issue['dependency_reason']}")
            lines.append("")

    return '\n'.join(lines)


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Score GitHub issues')
    parser.add_argument(
        '--recent-work',
        default='.claude/state.md',
        help='Path to state.md file'
    )
    parser.add_argument(
        '--issues',
        help='Path to JSON file with issues (or use stdin)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=5,
        help='Number of recommendations to show'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON instead of formatted text'
    )

    args = parser.parse_args()

    # Load context
    context = parse_state_file(args.recent_work)

    # Load issues
    if args.issues:
        with open(args.issues) as f:
            issues = json.load(f)
    else:
        issues = json.load(sys.stdin)

    # Ensure issues is a list
    if isinstance(issues, dict):
        issues = [issues]

    # Score issues
    scored = score_all_issues(issues, context)

    # Output
    if args.json:
        print(json.dumps(scored, indent=2))
    else:
        print(format_recommendations(scored, args.top))


if __name__ == '__main__':
    main()
