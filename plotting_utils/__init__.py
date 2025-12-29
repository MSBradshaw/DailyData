"""
Plotting utilities for year-of-data analysis.

This package provides reusable modules for visualizing daily tracking data,
including emotion calendars, activity timelines, and word cloud processing.
"""

from . import emotion
from . import activities
from . import wordcloud_processing

# Convenience imports for most common functions
from .emotion import (
    plot_emotion_calendar,
    load_emotion_data,
    create_split_calendar_heatmap
)

from .activities import (
    plot_activities,
    create_activity_pie_grid,
    create_task_timeline,
    get_standard_activity_columns,
    get_standard_column_mapping
)

from .wordcloud_processing import (
    process_best_worst_parts,
    get_wordcloud_data,
    export_wordcloud_words,
    process_text
)

__version__ = '1.0.0'

__all__ = [
    # Modules
    'emotion',
    'activities',
    'wordcloud_processing',

    # Emotion functions
    'plot_emotion_calendar',
    'load_emotion_data',
    'create_split_calendar_heatmap',

    # Activity functions
    'plot_activities',
    'create_activity_pie_grid',
    'create_task_timeline',
    'get_standard_activity_columns',
    'get_standard_column_mapping',

    # Word cloud functions
    'process_best_worst_parts',
    'get_wordcloud_data',
    'export_wordcloud_words',
    'process_text'
]
