"""
Date utilities for Project Aura.
Handles multi-format date parsing and timeline calculations across the application.
"""

from datetime import datetime, timedelta, date
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def parse_date(date_val: Any) -> Optional[date]:
    """
    Parse a date from string, datetime, date, or float/int timestamp into a datetime.date object.
    Supports a wide variety of date formats.
    """
    if date_val is None or date_val == '':
        return None
    if isinstance(date_val, datetime):
        return date_val.date()
    if isinstance(date_val, date):
        return date_val

    date_str = str(date_val).strip()
    if not date_str or date_str.lower() in ('tbd', 'none', 'null', 'nan'):
        return None

    # Handle ISO timestamp format (e.g., 2026-07-28T00:00:00Z or 2026-07-28 00:00:00)
    if 'T' in date_str:
        date_str = date_str.split('T')[0]
    elif ' ' in date_str:
        parts = date_str.split(' ')
        if len(parts) == 2 and (':' in parts[1] or '-' in parts[0] or '/' in parts[0]):
            date_str = parts[0]

    formats = [
        '%Y-%m-%d',
        '%m-%d-%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%B %d, %Y',
        '%b %d, %Y',
        '%B %d %Y',
        '%b %d %Y',
        '%d %B %Y',
        '%d %b %Y'
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    logger.warning(f"Could not parse date string: {date_val}")
    return None


def parse_datetime(date_val: Any) -> Optional[datetime]:
    """Parse any date input into a datetime object."""
    d = parse_date(date_val)
    if d:
        return datetime(d.year, d.month, d.day)
    return None


def calculate_timeline(start_date_val: Any, duration_weeks_val: Any = None) -> Dict[str, Any]:
    """
    Calculate timeline fields based on start_date and duration_weeks.

    Returns:
        dict containing:
        - start_date: ISO format (YYYY-MM-DD) or 'TBD'
        - start_date_display: Full display format (e.g. July 28, 2026) or 'TBD'
        - end_date: ISO format (YYYY-MM-DD) or 'TBD'
        - end_date_display: Full display format (e.g. October 20, 2026) or 'TBD'
        - duration_weeks: integer duration in weeks
        - duration_text: string duration (e.g. "12 Weeks")
    """
    # Parse duration
    try:
        if duration_weeks_val is not None and str(duration_weeks_val).strip() != '':
            duration_weeks = int(float(duration_weeks_val))
        else:
            duration_weeks = 12
    except (ValueError, TypeError):
        duration_weeks = 12

    if duration_weeks <= 0:
        duration_weeks = 12

    parsed_start = parse_date(start_date_val)
    if not parsed_start:
        return {
            'start_date': str(start_date_val) if start_date_val else 'TBD',
            'start_date_display': str(start_date_val) if start_date_val else 'TBD',
            'end_date': 'TBD',
            'end_date_display': 'TBD',
            'duration_weeks': duration_weeks,
            'duration_text': f"{duration_weeks} Weeks"
        }

    parsed_end = parsed_start + timedelta(weeks=duration_weeks)

    return {
        'start_date': parsed_start.strftime('%Y-%m-%d'),
        'start_date_display': parsed_start.strftime('%B %d, %Y'),
        'end_date': parsed_end.strftime('%Y-%m-%d'),
        'end_date_display': parsed_end.strftime('%B %d, %Y'),
        'duration_weeks': duration_weeks,
        'duration_text': f"{duration_weeks} Weeks"
    }
