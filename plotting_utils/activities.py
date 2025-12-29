"""
Activity visualization utilities.

This module provides functions to create pie charts and timeline visualizations
for daily activity tracking data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta


def create_activity_pie_grid(df, columns, color_map=None, n_cols=7, figsize=(15, 4)):
    """
    Create a grid of pie charts showing the distribution of various activities.

    Args:
        df: DataFrame containing the activity columns
        columns: List of column names to visualize
        color_map: Dictionary mapping categories to colors (default: standard colors)
        n_cols: Number of columns in the grid (default: 7)
        figsize: Figure size tuple (default: (15, 4))

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    # Default color map
    if color_map is None:
        color_map = {
            'Yes': '#287521',    # Green
            'No': '#DF0001',     # Red
            'Other1': '#1f77b4', # Blue
            'Other2': '#ff7f0e', # Orange
            'Other3': '#9467bd', # Purple
            'Other4': '#e377c2'  # Pink
        }

    n_rows = int(np.ceil(len(columns) / n_cols))

    # Create figure
    fig = plt.figure(figsize=figsize)

    # Create pie charts
    for idx, col in enumerate(columns):
        # Normalize values to Yes/No
        df[col] = df[col].replace({
            '0': 'No', '1': 'Yes', '2': 'Yes', '3': 'Yes',
            '4': 'Yes', '9': 'Yes'
        })

        ax = plt.subplot(n_rows, n_cols, idx + 1)

        # Count values
        value_counts = df[col].value_counts()

        # Calculate percentages
        total = value_counts.sum()
        percentages = value_counts / total * 100

        # Create labels with percentages
        labels = [f'{category}: {val:.1f}%' for category, val in percentages.items()]

        # Determine colors
        colors = []
        for category in value_counts.index:
            if category in color_map:
                colors.append(color_map[category])
            else:
                # Use other colors for additional categories
                extra_colors = [color_map['Other1'], color_map['Other2'],
                               color_map['Other3'], color_map['Other4']]
                colors.append(extra_colors[len(colors) % 4])

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            percentages,
            labels=labels,
            autopct='',
            colors=colors,
            textprops={'fontsize': 8}
        )

        # Add title
        ax.set_title(col, fontsize=10, pad=5)

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)

    return fig


def create_task_timeline(df, columns, date_col='Date', title=None, figsize=(15, 8)):
    """
    Create a timeline visualization of binary task completion data.

    Args:
        df: DataFrame with date column and binary task columns
        columns: List of task column names to plot
        date_col: Name of the date column (default: 'Date')
        title: Plot title (optional)
        figsize: Figure size tuple (default: (15, 8))

    Returns:
        tuple: (fig, ax) matplotlib figure and axis objects
    """
    # Invert column order for better visualization
    columns = columns[::-1]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Generate color palette
    colors = sns.color_palette('husl', n_colors=len(columns))

    # Plot each task
    for idx, (task, color) in enumerate(zip(columns, colors)):
        # Normalize responses
        df[task] = df[task].replace({
            'Both No': 'No', 'Both Yes': 'Yes',
            'Mel Yes': 'Yes', 'Michael Yes': 'Yes'
        })

        # Get dates where task was completed
        mask = df[task] == 'Yes'
        completion_dates = df.loc[mask, date_col]

        if len(completion_dates) > 0:
            # Plot points for each completion
            ax.scatter(completion_dates,
                      [idx] * len(completion_dates),
                      color=color,
                      label=task,
                      s=25,
                      marker='s',
                      alpha=1)

            # Draw horizontal lines at each point
            for date in completion_dates:
                ax.hlines(y=idx,
                         xmin=date - pd.Timedelta(days=0.25),
                         xmax=date + pd.Timedelta(days=0.25),
                         color=color,
                         linewidth=1)

    # Customize the plot
    ax.set_ylim(-1, len(columns))
    ax.set_yticks(range(len(columns)))
    ax.set_yticklabels(columns)

    # Format x-axis
    plt.xticks(rotation=45)

    # Add vertical lines for each week
    start_date = df[date_col].min()
    end_date = df[date_col].max()
    date_range = pd.date_range(start_date, end_date, freq='W')
    for date in date_range:
        ax.axvline(date, color='grey', linestyle='--', linewidth=0.8)

    # Remove y-axis label
    ax.set_ylabel('')

    # Add grid
    ax.grid(True, axis='x', color='black')
    ax.set_facecolor('white')

    # Add title if provided
    if title:
        plt.title(title, pad=20, fontsize=32)

    # Adjust layout
    plt.tight_layout()

    return fig, ax


def prepare_activity_data(csv_path, column_mapping=None, hour_offset=6):
    """
    Load and prepare activity data from CSV.

    Args:
        csv_path: Path to CSV file
        column_mapping: Dictionary to rename columns (optional)
        hour_offset: Hours to offset for day assignment (default: 6)

    Returns:
        DataFrame with prepared data
    """
    # Load CSV
    df = pd.read_csv(csv_path)

    # Convert 'Miles of Cardio' to binary
    if 'Miles of Cardio' in df.columns:
        df['Miles of Cardio'] = np.where(df['Miles of Cardio'] == 0, 'No', 'Yes')

    # Rename columns if mapping provided
    if column_mapping:
        # Ensure all columns are in the mapping
        for col in df.columns:
            if col not in column_mapping:
                column_mapping[col] = col
        df = df.rename(columns=column_mapping)

    # Convert timestamp to date
    if 'Timestamp' in df.columns:
        df['Date'] = pd.to_datetime(df['Timestamp'])
        df['Date'] = df['Date'] - pd.Timedelta(hours=hour_offset)

    return df


def get_standard_activity_columns():
    """
    Get the standard list of activity columns used in analysis.

    Returns:
        list: Standard activity column names
    """
    return [
        'Did we laugh?',
        'Did we cry?',
        'Did we have a tender moment?',
        'Did we fight?',
        'Did we spend time with family?',
        'Did we do cardio?',
        'Did we go climbing?',
        'Did we do strength training?',
        'Did we eat fruit?',
        'Did we eat vegetables?',
        'Did we watch TV?',
        'Did we read?',
        'Did we do dishes?'
    ]


def get_standard_column_mapping():
    """
    Get the standard column name mapping.

    Returns:
        dict: Mapping from original names to standardized names
    """
    return {
        'Loud laughter': 'Did we laugh?',
        'Cried': 'Did we cry?',
        'Tender moments': 'Did we have a tender moment?',
        'Fought': 'Did we fight?',
        'Spent time with family?': 'Did we spend time with family?',
        'Miles of Cardio': 'Did we do cardio?',
        'Went climbing?': 'Did we go climbing?',
        'Did strength training?': 'Did we do strength training?',
        'Did you both consume fruit today?': 'Did we eat fruit?',
        'Did you both consume vegetables today?': 'Did we eat vegetables?',
        'Did you watch TV today?': 'Did we watch TV?',
        'Did you read a book today?': 'Did we read?',
        'Did dishes?': 'Did we do dishes?'
    }


def plot_activities(csv_path, output_pie_path=None, output_timeline_path=None,
                   column_mapping=None, timeline_title=None):
    """
    Complete workflow to create activity pie charts and timeline.

    Args:
        csv_path: Path to CSV file
        output_pie_path: Optional path to save pie chart figure
        output_timeline_path: Optional path to save timeline figure
        column_mapping: Optional column name mapping (uses standard if None)
        timeline_title: Optional title for timeline plot

    Returns:
        tuple: (pie_fig, timeline_fig, timeline_ax)
    """
    # Use standard mapping if none provided
    if column_mapping is None:
        column_mapping = get_standard_column_mapping()

    # Prepare data
    df = prepare_activity_data(csv_path, column_mapping)

    # Get activity columns
    activity_columns = get_standard_activity_columns()

    # Create pie charts
    pie_fig = create_activity_pie_grid(df, activity_columns)
    if output_pie_path:
        plt.savefig(output_pie_path, dpi=300, bbox_inches='tight')
        print(f'Saved pie charts to: {output_pie_path}')

    # Create timeline
    timeline_fig, timeline_ax = create_task_timeline(
        df, activity_columns, title=timeline_title
    )
    if output_timeline_path:
        plt.savefig(output_timeline_path, dpi=300, bbox_inches='tight')
        print(f'Saved timeline to: {output_timeline_path}')

    return pie_fig, timeline_fig, timeline_ax
