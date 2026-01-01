"""
Emotion calendar heatmap plotting utilities.

This module provides functions to create split-cell calendar heatmaps
showing daily emotion scores for two people throughout a year.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
import os


def create_diverging_cmap():
    """
    Create a custom diverging colormap from red to green.

    Returns:
        LinearSegmentedColormap: Custom colormap with sharp transition
    """
    colors = [
        (0.8, 0.1, 0.1),   # Dark red
        (0.95, 0.2, 0.1),  # Light red
        (0.2, 0.8, 0.2),   # Light green
        (0.1, 0.6, 0.1)    # Dark green
    ]
    return LinearSegmentedColormap.from_list('custom_diverging', colors)


def create_zscore_cmap():
    """
    Create a diverging colormap for Z-scores: red (low) -> yellow (0) -> green (high).

    Returns:
        LinearSegmentedColormap: Red-yellow-green colormap
    """
    colors = [
        (0.8, 0.1, 0.1),   # Dark red (low Z-score / bad day)
        (0.95, 0.4, 0.2),  # Orange-red
        (1.0, 1.0, 0.3),   # Yellow (Z=0 / neutral)
        (0.6, 0.9, 0.3),   # Yellow-green
        (0.1, 0.6, 0.1)    # Dark green (high Z-score / great day)
    ]
    return LinearSegmentedColormap.from_list('zscore_diverging', colors)


def normalize_score(score, neutral=5, min_score=1, max_score=10):
    """
    Normalize scores to color range (0-1) with midpoint at neutral value.

    Args:
        score: The score to normalize
        neutral: The neutral point (default: 5)
        min_score: Minimum possible score (default: 1)
        max_score: Maximum possible score (default: 10)

    Returns:
        float: Normalized score between 0 and 1
    """
    if score <= neutral:
        return (score - min_score) / (2 * (neutral - min_score))
    else:
        return 0.5 + (score - neutral) / (2 * (max_score - neutral))


def calculate_zscore(scores):
    """
    Calculate Z-scores for a series of values.

    Args:
        scores: pandas Series or array-like of scores

    Returns:
        pandas Series: Z-scores (standardized values)
    """
    scores_clean = pd.Series(scores).dropna()
    if len(scores_clean) == 0:
        return pd.Series(scores)

    mean = scores_clean.mean()
    std = scores_clean.std()

    if std == 0:
        return pd.Series([0] * len(scores))

    return (pd.Series(scores) - mean) / std


def normalize_zscore(zscore, z_range=3.0):
    """
    Normalize Z-score to color range (0-1) with midpoint at 0.

    Args:
        zscore: The Z-score to normalize
        z_range: Range of Z-scores to map to color extremes (default: 3.0)
                 Z-scores beyond ±z_range will be clipped

    Returns:
        float: Normalized value between 0 and 1
    """
    # Clip to range
    clipped = np.clip(zscore, -z_range, z_range)
    # Map [-z_range, z_range] to [0, 1] with 0 at center
    return (clipped + z_range) / (2 * z_range)


def create_split_calendar_heatmap(data, person1_name='Person 1', person2_name='Person 2',
                                   title='How was your day on a scale of 1-10?',
                                   use_zscore=False):
    """
    Create a calendar heatmap with split square cells showing two people's emotion scores.

    Args:
        data: DataFrame with columns:
            - date: datetime
            - person1_score: int (1-10) or float (Z-score)
            - person2_score: int (1-10) or float (Z-score)
        person1_name: Name of first person (default: 'Person 1')
        person2_name: Name of second person (default: 'Person 2')
        title: Plot title (default: 'How was your day on a scale of 1-10?')
        use_zscore: Use Z-score normalization instead of raw scores (default: False)

    Returns:
        tuple: (fig, ax) matplotlib figure and axis objects
    """
    # Ensure data is sorted by date
    data = data.copy().sort_values('date')

    # Calculate Z-scores if requested
    if use_zscore:
        data['person1_zscore'] = calculate_zscore(data['person1_score'])
        data['person2_zscore'] = calculate_zscore(data['person2_score'])
        score1_col = 'person1_zscore'
        score2_col = 'person2_zscore'
    else:
        score1_col = 'person1_score'
        score2_col = 'person2_score'

    # Calculate number of weeks for proper scaling
    weeks = data['date'].dt.isocalendar().week.unique()
    n_weeks = len(weeks)

    # Calculate figure size to maintain square cells
    cell_size = 0.8
    fig_width = n_weeks * cell_size + 2
    fig_height = 7 * cell_size + 2

    # Create figure
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111)

    # Calculate week numbers and weekdays
    data['weekday'] = data['date'].dt.weekday
    data['week_num'] = data['date'].dt.isocalendar().week

    # Create colormaps based on mode
    if use_zscore:
        cmap1 = create_zscore_cmap()
        cmap2 = create_zscore_cmap()
    else:
        cmap1 = create_diverging_cmap()
        cmap2 = create_diverging_cmap()

    # Plot each day as a split square
    for _, row in data.iterrows():
        week_idx = np.where(weeks == row['week_num'])[0][0]

        x = week_idx
        y = row['weekday']

        # Determine normalization function based on mode
        if use_zscore:
            norm_func = normalize_zscore
        else:
            norm_func = normalize_score

        # Left triangle (Person 1)
        triangle1 = Polygon(
            [[x, y], [x+1, y], [x, y+1]],
            facecolor=cmap1(norm_func(row[score1_col])),
            edgecolor='white',
            linewidth=0.5
        )

        # Right triangle (Person 2)
        triangle2 = Polygon(
            [[x+1, y], [x+1, y+1], [x, y+1]],
            facecolor=cmap2(norm_func(row[score2_col])),
            edgecolor='white',
            linewidth=0.5
        )

        ax.add_patch(triangle1)
        ax.add_patch(triangle2)

    # Customize the plot
    ax.set_ylim(7, -1)
    ax.set_xlim(-1, len(weeks))

    # Set weekday labels
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_yticks(range(7))
    ax.set_yticklabels(weekdays, rotation=0, fontsize=16)

    # Add month labels
    months = pd.date_range(data['date'].min(), data['date'].max(), freq='MS')
    month_weeks = [np.where(weeks == week)[0][0] for week in
                   pd.DataFrame({'date': months})['date'].dt.isocalendar().week]

    ax.set_xticks(month_weeks)
    ax.set_xticklabels([d.strftime('%B') for d in months], rotation=0, fontsize=16)

    # Add colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    if use_zscore:
        sm = plt.cm.ScalarMappable(cmap=cmap1, norm=plt.Normalize(-3, 3))
        cbar = plt.colorbar(sm, cax=cbar_ax)
        cbar.set_ticks([-3, 0, 3])
        cbar.set_ticklabels(['-3σ (Bad)', '0σ (Average)', '+3σ (Great)'], fontsize=16)
    else:
        sm = plt.cm.ScalarMappable(cmap=cmap1, norm=plt.Normalize(1, 10))
        cbar = plt.colorbar(sm, cax=cbar_ax)
        cbar.set_ticks([1, 5, 10])
        cbar.set_ticklabels(['1 - Awful', '5 - Neutral', '10 - Amazing'], fontsize=16)

    # Calculate averages for display
    person1_raw_avg = data['person1_score'].dropna().mean()
    person2_raw_avg = data['person2_score'].dropna().mean()

    if use_zscore:
        # For Z-scores, the mean should be ~0, but we'll calculate actual mean
        person1_avg = data[score1_col].dropna().mean()
        person2_avg = data[score2_col].dropna().mean()
        avg_label1 = f'{person1_name}\nAvg={person1_raw_avg:.1f}'
        avg_label2 = f'{person2_name}\nAvg={person2_raw_avg:.1f}'
    else:
        person1_avg = person1_raw_avg
        person2_avg = person2_raw_avg
        avg_label1 = f'{person1_name}\nMean={person1_avg:.1f}'
        avg_label2 = f'{person2_name}\nMean={person2_avg:.1f}'

    # Create legend with split square
    legend_ax = fig.add_axes([0.855, 0.01, 0.15, 0.15])
    legend_ax.set_aspect('equal')
    legend_ax.set_axis_off()

    # Use appropriate normalization for legend colors
    if use_zscore:
        legend_norm = normalize_zscore
    else:
        legend_norm = normalize_score

    triangle1 = Polygon(
        [[0, 0], [1, 1], [0, 1]],
        facecolor=cmap1(legend_norm(person1_avg)),
        edgecolor='white',
        linewidth=0.5
    )
    triangle2 = Polygon(
        [[0, 0], [1, 0], [1, 1]],
        facecolor=cmap2(legend_norm(person2_avg)),
        edgecolor='white',
        linewidth=0.5
    )

    legend_ax.add_patch(triangle1)
    legend_ax.add_patch(triangle2)

    # Add labels
    legend_ax.text(-1.2, .4, avg_label1, ha='left', va='bottom', fontsize=12)
    legend_ax.text(1.2, .4, avg_label2, ha='left', va='bottom', fontsize=12)

    legend_ax.set_xlim(-0.2, 1.2)
    legend_ax.set_ylim(-0.2, 1.2)

    # Set title
    plt.suptitle(title, y=0.95, fontsize=32)

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(right=0.9)

    return fig, ax


def create_split_calendar_heatmap_mobile(data, person1_name='Person 1', person2_name='Person 2',
                                          title='How was your day on a scale of 1-10?',
                                          use_zscore=False):
    """
    Create a mobile-friendly calendar heatmap with day-of-week columns and weeks as rows.

    Args:
        data: DataFrame with columns:
            - date: datetime
            - person1_score: int (1-10) or float (Z-score)
            - person2_score: int (1-10) or float (Z-score)
        person1_name: Name of first person (default: 'Person 1')
        person2_name: Name of second person (default: 'Person 2')
        title: Plot title (default: 'How was your day on a scale of 1-10?')
        use_zscore: Use Z-score normalization instead of raw scores (default: False)

    Returns:
        tuple: (fig, ax) matplotlib figure and axis objects
    """
    # Ensure data is sorted by date
    data = data.copy().sort_values('date')

    # Calculate Z-scores if requested
    if use_zscore:
        data['person1_zscore'] = calculate_zscore(data['person1_score'])
        data['person2_zscore'] = calculate_zscore(data['person2_score'])
        score1_col = 'person1_zscore'
        score2_col = 'person2_zscore'
    else:
        score1_col = 'person1_score'
        score2_col = 'person2_score'

    # Calculate week numbers and weekdays
    data['weekday'] = data['date'].dt.weekday
    data['week_num'] = data['date'].dt.isocalendar().week

    # Get unique weeks in order
    weeks = data['week_num'].unique()
    n_weeks = len(weeks)

    # Calculate figure size - mobile friendly (narrow width, tall height)
    cell_size = 0.6
    fig_width = 7 * cell_size + 2  # 7 days of week
    fig_height = n_weeks * cell_size + 4  # Extra space for legend at bottom

    # Create figure
    fig = plt.figure(figsize=(fig_width, fig_height))

    # Main plot takes most of the space, leave room at bottom for legend
    ax = fig.add_axes([0.1, 0.14, 0.8, 0.80])

    # Create colormaps based on mode
    if use_zscore:
        cmap1 = create_zscore_cmap()
        cmap2 = create_zscore_cmap()
    else:
        cmap1 = create_diverging_cmap()
        cmap2 = create_diverging_cmap()

    # Plot each day as a split square
    for _, row in data.iterrows():
        week_idx = np.where(weeks == row['week_num'])[0][0]

        # Swapped: weekday is now x, week is y
        x = row['weekday']
        y = week_idx

        # Determine normalization function based on mode
        if use_zscore:
            norm_func = normalize_zscore
        else:
            norm_func = normalize_score

        # Left triangle (Person 1)
        triangle1 = Polygon(
            [[x, y], [x+1, y], [x, y+1]],
            facecolor=cmap1(norm_func(row[score1_col])),
            edgecolor='white',
            linewidth=0.5
        )

        # Right triangle (Person 2)
        triangle2 = Polygon(
            [[x+1, y], [x+1, y+1], [x, y+1]],
            facecolor=cmap2(norm_func(row[score2_col])),
            edgecolor='white',
            linewidth=0.5
        )

        ax.add_patch(triangle1)
        ax.add_patch(triangle2)

    # Customize the plot
    ax.set_xlim(0, 7)
    ax.set_ylim(-0.1, n_weeks + 0.1)

    # Set weekday labels on x-axis
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax.set_xticks(range(7))
    ax.set_xticklabels(weekdays, rotation=0, fontsize=14)
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()

    # Add week/month labels on y-axis
    # Group weeks by month for cleaner labels
    week_to_month = {}
    for _, row in data.iterrows():
        week_num = row['week_num']
        month = row['date'].strftime('%b')
        if week_num not in week_to_month:
            week_to_month[week_num] = month

    # Create y-tick labels showing month for first week of each month
    y_labels = []
    prev_month = None
    for week in weeks:
        month = week_to_month[week]
        if month != prev_month:
            y_labels.append(f"{month}")
            prev_month = month
        else:
            y_labels.append('')

    ax.set_yticks(range(n_weeks))
    ax.set_yticklabels(y_labels, fontsize=12)

    # Invert y-axis so earliest weeks are at top
    ax.invert_yaxis()

    # Remove right and bottom borders
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Add horizontal colorbar at bottom
    cbar_ax = fig.add_axes([0.15, 0.10, 0.7, 0.03])
    if use_zscore:
        sm = plt.cm.ScalarMappable(cmap=cmap1, norm=plt.Normalize(-3, 3))
        cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal')
        cbar.set_ticks([-3, 0, 3])
        cbar.set_ticklabels(['-3σ (Bad)', '0σ (Avg)', '+3σ (Great)'], fontsize=12)
    else:
        sm = plt.cm.ScalarMappable(cmap=cmap1, norm=plt.Normalize(1, 10))
        cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal')
        cbar.set_ticks([1, 5, 10])
        cbar.set_ticklabels(['1 - Awful', '5 - Neutral', '10 - Amazing'], fontsize=12)

    # Calculate averages for display
    person1_raw_avg = data['person1_score'].dropna().mean()
    person2_raw_avg = data['person2_score'].dropna().mean()

    if use_zscore:
        avg_label1 = f'{person1_name}: Avg={person1_raw_avg:.1f}'
        avg_label2 = f'{person2_name}: Avg={person2_raw_avg:.1f}'
    else:
        person1_avg = person1_raw_avg
        person2_avg = person2_raw_avg
        avg_label1 = f'{person1_name}: Mean={person1_avg:.1f}'
        avg_label2 = f'{person2_name}: Mean={person2_avg:.1f}'

    # Create legend with split square at bottom
    legend_ax = fig.add_axes([0.35, 0.02, 0.3, 0.08])
    legend_ax.set_aspect('equal')
    legend_ax.set_axis_off()

    # Use appropriate normalization for legend colors
    if use_zscore:
        legend_norm = normalize_zscore
        legend_val1 = 0  # Use neutral for Z-score
        legend_val2 = 0
    else:
        legend_norm = normalize_score
        legend_val1 = person1_raw_avg
        legend_val2 = person2_raw_avg

    triangle1 = Polygon(
        [[0, 0], [1, 1], [0, 1]],
        facecolor=cmap1(legend_norm(legend_val1)),
        edgecolor='black',
        linewidth=1
    )
    triangle2 = Polygon(
        [[0, 0], [1, 0], [1, 1]],
        facecolor=cmap2(legend_norm(legend_val2)),
        edgecolor='black',
        linewidth=1
    )

    legend_ax.add_patch(triangle1)
    legend_ax.add_patch(triangle2)

    # Add labels below the split square
    legend_ax.text(0, -0.5, avg_label1, ha='center', va='top', fontsize=10)
    legend_ax.text(1, -0.5, avg_label2, ha='center', va='top', fontsize=10)

    legend_ax.set_xlim(-0.2, 1.2)
    legend_ax.set_ylim(-0.8, 1.2)

    # Set title
    plt.suptitle(title, y=0.98, fontsize=18)

    return fig, ax


def plot_emotion_weekday_heatmap(data, person1_name='Person 1', person2_name='Person 2',
                                 output_path='emotion_weekday_heatmap.png'):
    """
    Create a heatmap showing average emotion scores by day of week for each person.
    Uses Z-score coloring (relative to each person's average) but displays raw values.

    Args:
        data: DataFrame with columns: date, person1_score, person2_score
        person1_name: Name of first person (default: 'Person 1')
        person2_name: Name of second person (default: 'Person 2')
        output_path: Path to save heatmap (default: 'emotion_weekday_heatmap.png')

    Returns:
        tuple: (fig, ax) matplotlib figure and axis objects
    """
    # Get the statistics
    stats_df = export_emotion_by_weekday(data, person1_name, person2_name, output_path=None)

    # Pivot to get person as rows, day as columns
    pivot_df = stats_df.pivot(index='Person', columns='Day', values='Avg')

    # Reorder to put Melanie first, then Michael
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    person_order = [person2_name, person1_name]  # Melanie first, then Michael

    pivot_df = pivot_df.reindex(index=person_order, columns=day_order)

    # Calculate Z-scores for each person (row-wise)
    pivot_zscore = pivot_df.copy()
    for person in person_order:
        person_values = pivot_df.loc[person]
        mean = person_values.mean()
        std = person_values.std()
        if std > 0:
            pivot_zscore.loc[person] = (person_values - mean) / std
        else:
            pivot_zscore.loc[person] = 0

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 3))

    # Get the red-yellow-green colormap (same as Z-score)
    cmap = create_zscore_cmap()

    # Normalize Z-scores to color range
    vmin, vmax = -2, 2  # Z-score range for coloring

    # Create the heatmap using Z-scores for color
    im = ax.imshow(pivot_zscore.values, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)

    # Set ticks and labels
    ax.set_xticks(np.arange(len(day_order)))
    ax.set_yticks(np.arange(len(person_order)))
    ax.set_xticklabels(day_order, fontsize=12)
    ax.set_yticklabels(person_order, fontsize=14)

    # Rotate x labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

    # Add text annotations with values
    for i in range(len(person_order)):
        for j in range(len(day_order)):
            value = pivot_df.iloc[i, j]
            if not pd.isna(value):
                text = ax.text(j, i, f'{value:.1f}',
                             ha='center', va='center', color='black', fontsize=14, fontweight='bold')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Emotion Z-Score', rotation=270, labelpad=20, fontsize=12)

    # Set title
    ax.set_title('Average Emotion by Day of Week', fontsize=16, pad=15)

    # Remove ticks
    ax.tick_params(which='both', length=0)

    # Add grid
    ax.set_xticks(np.arange(len(day_order)) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(person_order)) - 0.5, minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=2)

    plt.tight_layout()

    # Save if requested
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f'Saved weekday heatmap to: {output_path}')

    return fig, ax


def plot_emotion_weekday_heatmap_mobile(data, person1_name='Person 1', person2_name='Person 2',
                                        output_path='emotion_weekday_heatmap_mobile.png'):
    """
    Create a mobile-friendly heatmap showing average emotion scores by day of week.
    Uses Z-score coloring (relative to each person's average) but displays raw values.
    Days are rows, people are columns.

    Args:
        data: DataFrame with columns: date, person1_score, person2_score
        person1_name: Name of first person (default: 'Person 1')
        person2_name: Name of second person (default: 'Person 2')
        output_path: Path to save heatmap (default: 'emotion_weekday_heatmap_mobile.png')

    Returns:
        tuple: (fig, ax) matplotlib figure and axis objects
    """
    # Get the statistics
    stats_df = export_emotion_by_weekday(data, person1_name, person2_name, output_path=None)

    # Pivot to get person as rows, day as columns
    pivot_df = stats_df.pivot(index='Person', columns='Day', values='Avg')

    # Reorder to put Melanie first, then Michael
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_abbrev = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    person_order = [person2_name, person1_name]  # Melanie first, then Michael

    pivot_df = pivot_df.reindex(index=person_order, columns=day_order)

    # Transpose for mobile (days as rows, people as columns)
    pivot_df_t = pivot_df.T

    # Calculate Z-scores for each person (column-wise after transpose)
    pivot_zscore_t = pivot_df_t.copy()
    for person in person_order:
        person_values = pivot_df_t[person]
        mean = person_values.mean()
        std = person_values.std()
        if std > 0:
            pivot_zscore_t[person] = (person_values - mean) / std
        else:
            pivot_zscore_t[person] = 0

    # Create figure - mobile dimensions (narrow and tall)
    fig, ax = plt.subplots(figsize=(4, 8))

    # Get the red-yellow-green colormap (same as Z-score)
    cmap = create_zscore_cmap()

    # Normalize Z-scores to color range
    vmin, vmax = -2, 2  # Z-score range for coloring

    # Create the heatmap using Z-scores for color
    im = ax.imshow(pivot_zscore_t.values, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)

    # Set ticks and labels
    ax.set_yticks(np.arange(len(day_abbrev)))
    ax.set_xticks(np.arange(len(person_order)))
    ax.set_yticklabels(day_abbrev, fontsize=12)
    ax.set_xticklabels(person_order, fontsize=12)

    # Put x labels on top
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()

    # Add text annotations with values
    for i in range(len(day_abbrev)):
        for j in range(len(person_order)):
            value = pivot_df_t.iloc[i, j]
            if not pd.isna(value):
                text = ax.text(j, i, f'{value:.1f}',
                             ha='center', va='center', color='black', fontsize=14, fontweight='bold')

    # Add horizontal colorbar at bottom
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.1)
    cbar.set_label('Emotion Z-Score', fontsize=11)

    # Set title
    ax.set_title('Average Emotion by Day of Week', fontsize=14, pad=15)

    # Remove ticks
    ax.tick_params(which='both', length=0)

    # Add grid
    ax.set_xticks(np.arange(len(person_order)) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(day_abbrev)) - 0.5, minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=2)

    # Remove right and bottom borders
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.tight_layout()

    # Save if requested
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f'Saved weekday heatmap (mobile) to: {output_path}')

    return fig, ax


def export_emotion_by_weekday(data, person1_name='Person 1', person2_name='Person 2',
                              output_path='emotion_by_weekday.csv'):
    """
    Export average emotion scores by day of week for each person to CSV.

    Args:
        data: DataFrame with columns: date, person1_score, person2_score
        person1_name: Name of first person (default: 'Person 1')
        person2_name: Name of second person (default: 'Person 2')
        output_path: Path to save CSV file (default: 'emotion_by_weekday.csv')
                     If None, does not save to file

    Returns:
        DataFrame: The statistics that were exported
    """
    # Add day of week to data
    data = data.copy()
    data['day_of_week'] = data['date'].dt.day_name()

    # Day order for sorting
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Calculate stats for person 1
    person1_stats = data.groupby('day_of_week')['person1_score'].agg(['mean', 'std']).reset_index()
    person1_stats['Person'] = person1_name
    person1_stats.columns = ['Day', 'Avg', 'STD', 'Person']

    # Calculate stats for person 2
    person2_stats = data.groupby('day_of_week')['person2_score'].agg(['mean', 'std']).reset_index()
    person2_stats['Person'] = person2_name
    person2_stats.columns = ['Day', 'Avg', 'STD', 'Person']

    # Combine and reorder
    combined = pd.concat([person1_stats, person2_stats], ignore_index=True)
    combined['Day'] = pd.Categorical(combined['Day'], categories=day_order, ordered=True)
    combined = combined.sort_values(['Day', 'Person'])

    # Reorder columns and round to 1 decimal place
    combined = combined[['Person', 'Day', 'Avg', 'STD']]
    combined['Avg'] = combined['Avg'].round(1)
    combined['STD'] = combined['STD'].round(1)

    # Export to CSV if path provided
    if output_path:
        combined.to_csv(output_path, index=False)
        print(f'Exported day-of-week statistics to: {output_path}')

    return combined


def load_emotion_data(csv_path, year, person1_col, person2_col,
                      timestamp_col='Timestamp', hour_offset=6,
                      cache_path=None):
    """
    Load and process emotion data from CSV file.

    Args:
        csv_path: Path to CSV file containing daily data
        year: Year to process (e.g., 2024)
        person1_col: Column name for person 1's emotion score
        person2_col: Column name for person 2's emotion score
        timestamp_col: Column name for timestamp (default: 'Timestamp')
        hour_offset: Hours to offset for day assignment (default: 6)
        cache_path: Optional path to cache processed data as pickle

    Returns:
        DataFrame with columns: date, person1_score, person2_score
    """
    # Check cache first
    if cache_path and os.path.exists(cache_path):
        print(f'Loading data from cache: {cache_path}')
        return pd.read_pickle(cache_path)

    # Load CSV
    df = pd.read_csv(csv_path)

    # Drop rows with missing timestamps
    df = df.dropna(subset=[timestamp_col])
    df = df[df[timestamp_col].astype(str).str.strip() != '']

    # Convert timestamp to datetime, ignoring timezone to avoid parsing issues
    # Remove timezone suffix before parsing
    df['Date'] = df[timestamp_col].astype(str).str.replace(r'\s+[A-Z]{3,4}$', '', regex=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop any rows that failed to parse
    df = df.dropna(subset=['Date'])

    # Apply hour offset (entries before offset hour count as previous day)
    df['Date'] = df['Date'] - pd.Timedelta(hours=hour_offset)

    # Generate all dates for the year
    start_date = datetime(year, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365 + (1 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 0))]

    person1_scores = []
    person2_scores = []

    for date in dates:
        # Match by date only (ignore time)
        sub = df[df['Date'].dt.strftime('%m-%d-%Y') == date.strftime('%m-%d-%Y')]

        if len(sub) == 0:
            person1_scores.append(None)
            person2_scores.append(None)
        else:
            person1_score = sub[person1_col].mean()
            person2_score = sub[person2_col].mean()

            # Handle missing values
            if pd.isna(person1_score):
                person1_score = None
            if pd.isna(person2_score):
                person2_score = None

            # Cross-fill if one is missing
            if person2_score is None:
                person2_score = person1_score
            if person1_score is None:
                person1_score = person2_score

            person1_scores.append(person1_score)
            person2_scores.append(person2_score)

    # Create DataFrame
    data = pd.DataFrame({
        'date': dates,
        'person1_score': person1_scores,
        'person2_score': person2_scores
    })

    # Cache if requested
    if cache_path:
        print(f'Caching data to: {cache_path}')
        data.to_pickle(cache_path)

    return data


def plot_emotion_calendar(csv_path, year, person1_col, person2_col,
                          person1_name='Person 1', person2_name='Person 2',
                          output_path=None, cache_path=None, use_zscore=False,
                          export_weekday_stats=None, plot_weekday_heatmap_path=None,
                          mobile=False):
    """
    Complete workflow to load data and create emotion calendar heatmap.

    Args:
        csv_path: Path to CSV file
        year: Year to process
        person1_col: Column name for person 1 emotion scores
        person2_col: Column name for person 2 emotion scores
        person1_name: Display name for person 1 (default: 'Person 1')
        person2_name: Display name for person 2 (default: 'Person 2')
        output_path: Optional path to save figure
        cache_path: Optional path to cache processed data
        use_zscore: Use Z-score normalization instead of raw scores (default: False)
        export_weekday_stats: Optional path to export weekday statistics CSV (default: None)
        plot_weekday_heatmap_path: Optional path to save weekday heatmap plot (default: None)
        mobile: Use mobile layout (day-of-week columns, weeks as rows) (default: False)

    Returns:
        tuple: (fig, ax) matplotlib figure and axis objects
    """
    # Load data
    data = load_emotion_data(csv_path, year, person1_col, person2_col, cache_path=cache_path)

    # Export weekday statistics if requested
    if export_weekday_stats:
        export_emotion_by_weekday(data, person1_name, person2_name, export_weekday_stats)

    # Plot weekday heatmap if requested
    if plot_weekday_heatmap_path:
        if mobile:
            plot_emotion_weekday_heatmap_mobile(data, person1_name, person2_name, plot_weekday_heatmap_path)
        else:
            plot_emotion_weekday_heatmap(data, person1_name, person2_name, plot_weekday_heatmap_path)

    # Determine title based on mode
    if use_zscore:
        title = 'Daily Emotion Z-Scores (Standardized by Person)'
    else:
        title = 'How was your day on a scale of 1-10?'

    # Create plot using mobile or desktop layout
    if mobile:
        fig, ax = create_split_calendar_heatmap_mobile(data, person1_name, person2_name,
                                                       title=title, use_zscore=use_zscore)
    else:
        fig, ax = create_split_calendar_heatmap(data, person1_name, person2_name,
                                               title=title, use_zscore=use_zscore)

        # Remove borders (only for desktop version)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

    # Save if requested
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f'Saved plot to: {output_path}')

    return fig, ax
