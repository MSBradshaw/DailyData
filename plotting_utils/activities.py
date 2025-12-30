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


def plot_did_we_events_2025(csv_path='2025DataCollection.csv', output_path=None, figsize=(15, 6)):
    """
    Create pie charts for "Did we ..." events from 2025 data format.

    Shows proportion of days with vs without each event.
    Uses percentages for all events except crying (shows raw counts).
    Includes exercise events since they're tracked the same for both people.
    Displays in 2 rows for better layout.

    Args:
        csv_path: Path to 2025 data CSV file
        output_path: Optional path to save figure
        figsize: Figure size tuple (default: (15, 6))

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    # Load data
    df = pd.read_csv(csv_path)

    # Parse the "Did we ..." column to extract individual events
    events_col = 'Did we ...'

    # Parse exercise column
    exercise_col = 'Exercise '
    df['exercise_raw'] = df[exercise_col].fillna('')
    df['had_any_exercise'] = df['exercise_raw'].str.strip() != ''
    df['had_cardio'] = df['exercise_raw'].str.contains('Cardio', case=False, regex=False)
    df['had_strength'] = df['exercise_raw'].str.contains('Strength', case=False, regex=False)

    # Create binary columns for each event type
    events = [
        ('laugh', 'Laugh'),
        ('cry', 'Cry'),
        ('fight', 'Fight'),
        ('tender', 'Tender Moment'),
        ('spend', 'Spend Money'),
        ('had_any_exercise', 'Any Exercise'),
        ('had_cardio', 'Cardio'),
        ('had_strength', 'Strength')
    ]

    event_data = {}
    for keyword, display_name in events:
        # For exercise events, use the already-created boolean columns
        if keyword.startswith('had_'):
            had_event = df[keyword]
        else:
            # For "Did we ..." events, parse from the text column
            had_event = df[events_col].fillna('').str.contains(keyword, case=False, regex=False)

        yes_count = had_event.sum()
        no_count = (~had_event).sum()
        event_data[display_name] = {
            'yes': yes_count,
            'no': no_count,
            'keyword': keyword
        }

    # Create figure with 2 rows
    n_cols = 4  # 4 charts per row
    n_rows = 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Color scheme
    yes_color = '#287521'  # Green
    no_color = '#DF0001'   # Red

    for idx, (display_name, data) in enumerate(event_data.items()):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]

        yes_count = data['yes']
        no_count = data['no']
        total = yes_count + no_count

        # For crying, use raw counts; for others use percentages
        if data['keyword'] == 'cry':
            # Show raw counts for crying
            labels = [f'Yes: {yes_count}', f'No: {no_count}']
            autopct = ''
        else:
            # Show percentages for other events
            yes_pct = (yes_count / total * 100) if total > 0 else 0
            no_pct = (no_count / total * 100) if total > 0 else 0
            labels = [f'Yes: {yes_pct:.1f}%', f'No: {no_pct:.1f}%']
            autopct = ''

        # Create pie chart
        wedges, texts = ax.pie(
            [yes_count, no_count],
            labels=labels,
            colors=[yes_color, no_color],
            startangle=90,
            textprops={'fontsize': 9}
        )

        # Add title
        ax.set_title(display_name, fontsize=11, pad=10, fontweight='bold')

    # Adjust layout
    plt.tight_layout()

    # Save if output path provided
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f'✓ Saved pie charts to: {output_path}')

    return fig


def plot_person_specific_events_2025(csv_path='2025DataCollection.csv',
                                      output_path_michael=None,
                                      output_path_melanie=None,
                                      figsize=(9, 4)):
    """
    Create person-specific pie charts for individual activities from 2025 data.

    Creates two separate figures: one for Michael, one for Melanie.
    Shows proportion of days with vs without each activity.
    Exercise events are in the combined chart since they're tracked the same for both.

    Args:
        csv_path: Path to 2025 data CSV file
        output_path_michael: Optional path to save Michael's figure
        output_path_melanie: Optional path to save Melanie's figure
        figsize: Figure size tuple (default: (9, 4))

    Returns:
        tuple: (michael_fig, melanie_fig)
    """
    # Load data
    df = pd.read_csv(csv_path)

    # Parse exercise column
    exercise_col = 'Exercise '
    df['exercise_raw'] = df[exercise_col].fillna('')
    df['had_any_exercise'] = df['exercise_raw'].str.strip() != ''
    df['had_cardio'] = df['exercise_raw'].str.contains('Cardio', case=False, regex=False)
    df['had_strength'] = df['exercise_raw'].str.contains('Strength', case=False, regex=False)

    # Parse reading and TV columns
    read_col = 'Did you read a book today?'
    tv_col = 'Did you watch TV today?'
    fruit_veg_col = 'Fruit / Vegetable Consumption'

    df['read_raw'] = df[read_col].fillna('')
    df['tv_raw'] = df[tv_col].fillna('')
    df['fruit_veg_raw'] = df[fruit_veg_col].fillna('')

    # Create person-specific binary columns
    df['michael_read'] = (df['read_raw'].str.contains('Michael', case=False) |
                          df['read_raw'].str.contains('Both Yes', case=False))
    df['melanie_read'] = (df['read_raw'].str.contains('Mel', case=False) |
                          df['read_raw'].str.contains('Both Yes', case=False))

    df['michael_tv'] = (df['tv_raw'].str.contains('Michael', case=False) |
                        df['tv_raw'].str.contains('Both Yes', case=False))
    df['melanie_tv'] = (df['tv_raw'].str.contains('Mel', case=False) |
                        df['tv_raw'].str.contains('Both Yes', case=False))

    df['michael_fruit_veg'] = df['fruit_veg_raw'].str.contains('Michael', case=False)
    df['melanie_fruit_veg'] = df['fruit_veg_raw'].str.contains('Melanie', case=False)

    # Define events to plot (column_name, display_name)
    michael_events = [
        ('michael_read', 'Reading'),
        ('michael_tv', 'TV'),
        ('michael_fruit_veg', 'Fruit/Veggie')
    ]

    melanie_events = [
        ('melanie_read', 'Reading'),
        ('melanie_tv', 'TV'),
        ('melanie_fruit_veg', 'Fruit/Veggie')
    ]

    # Color scheme
    yes_color = '#287521'  # Green
    no_color = '#DF0001'   # Red

    # Create Michael's figure
    fig_michael, axes_michael = plt.subplots(1, len(michael_events), figsize=figsize)

    for idx, (col_name, display_name) in enumerate(michael_events):
        ax = axes_michael[idx]

        yes_count = df[col_name].sum()
        no_count = (~df[col_name]).sum()
        total = yes_count + no_count

        yes_pct = (yes_count / total * 100) if total > 0 else 0
        no_pct = (no_count / total * 100) if total > 0 else 0

        labels = [f'Yes: {yes_pct:.1f}%', f'No: {no_pct:.1f}%']

        # Create pie chart
        wedges, texts = ax.pie(
            [yes_count, no_count],
            labels=labels,
            colors=[yes_color, no_color],
            startangle=90,
            textprops={'fontsize': 9}
        )

        # Add title
        ax.set_title(display_name, fontsize=11, pad=10, fontweight='bold')

    # Add overall title for Michael
    fig_michael.suptitle('Michael - Activity Summary', fontsize=14, fontweight='bold', y=1.05)
    plt.tight_layout()

    if output_path_michael:
        fig_michael.savefig(output_path_michael, dpi=300, bbox_inches='tight')
        print(f'✓ Saved Michael\'s pie charts to: {output_path_michael}')

    # Create Melanie's figure
    fig_melanie, axes_melanie = plt.subplots(1, len(melanie_events), figsize=figsize)

    for idx, (col_name, display_name) in enumerate(melanie_events):
        ax = axes_melanie[idx]

        yes_count = df[col_name].sum()
        no_count = (~df[col_name]).sum()
        total = yes_count + no_count

        yes_pct = (yes_count / total * 100) if total > 0 else 0
        no_pct = (no_count / total * 100) if total > 0 else 0

        labels = [f'Yes: {yes_pct:.1f}%', f'No: {no_pct:.1f}%']

        # Create pie chart
        wedges, texts = ax.pie(
            [yes_count, no_count],
            labels=labels,
            colors=[yes_color, no_color],
            startangle=90,
            textprops={'fontsize': 9}
        )

        # Add title
        ax.set_title(display_name, fontsize=11, pad=10, fontweight='bold')

    # Add overall title for Melanie
    fig_melanie.suptitle('Melanie - Activity Summary', fontsize=14, fontweight='bold', y=1.05)
    plt.tight_layout()

    if output_path_melanie:
        fig_melanie.savefig(output_path_melanie, dpi=300, bbox_inches='tight')
        print(f'✓ Saved Melanie\'s pie charts to: {output_path_melanie}')

    return fig_michael, fig_melanie
