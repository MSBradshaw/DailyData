import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle, Polygon
from datetime import datetime, timedelta
from matplotlib.colors import LinearSegmentedColormap  # Add this import at the top
import os

# Create custom diverging colormap (red to green)
def create_diverging_cmap():
    # Create colors from red to green (no white)
    colors = [(0.8, 0.1, 0.1),  # Dark red
              (0.95, 0.2, 0.1), # Light red
              (0.2, 0.8, 0.2),  # Light green
              (0.1, 0.6, 0.1)]  # Dark green
    
    # Create colormap with a sharp transition at the midpoint
    return LinearSegmentedColormap.from_list('custom_diverging', colors)

# Function to normalize scores to color range (0-1) with midpoint at 5
def normalize_score(score):
    if score <= 5:
        return (score - 1) / 8  # Map 1-5 to 0-0.5
    else:
        return 0.5 + (score - 5) / 10  # Map 6-10 to 0.5-1

def create_split_calendar_heatmap(data):
    """
    Create a calendar heatmap with split square cells showing two people's emotion scores.
    
    Args:
        data: DataFrame with columns:
            - date: datetime
            - person1_score: int (1-10)
            - person2_score: int (1-10)
    """
    # Ensure data is sorted by date
    data = data.sort_values('date')
    
    # Calculate number of weeks for proper scaling
    weeks = data['date'].dt.isocalendar().week.unique()
    n_weeks = len(weeks)
    
    # Calculate figure size to maintain square cells
    # We want the height of 7 cells to equal the width of 1 cell
    cell_size = 0.8  # Base size for each cell
    fig_width = n_weeks * cell_size + 2  # Add margin for labels
    fig_height = 7 * cell_size + 2  # 7 days + margin
    
    # Create figure with specific aspect ratio to ensure squares
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111)
    
    # Calculate week numbers and weekdays
    data['weekday'] = data['date'].dt.weekday
    data['week_num'] = data['date'].dt.isocalendar().week
    
    # Replace the existing colormap creation with:
    cmap1 = create_diverging_cmap()
    cmap2 = create_diverging_cmap()
    
    # Plot each day as a split square
    for _, row in data.iterrows():
        week_idx = np.where(weeks == row['week_num'])[0][0]
        
        # Calculate position
        x = week_idx
        y = row['weekday']
        
        # Create split squares using triangles
        # Left triangle (Person 1)
        triangle1 = Polygon(
            [[x, y], [x+1, y], [x, y+1]],
            facecolor=cmap1(normalize_score(row['person1_score'])),
            edgecolor='white',
            linewidth=0.5
        )
        
        # Right triangle (Person 2)
        triangle2 = Polygon(
            [[x+1, y], [x+1, y+1], [x, y+1]],
            facecolor=cmap2(normalize_score(row['person2_score'])),
            edgecolor='white',
            linewidth=0.5
        )
        
        ax.add_patch(triangle1)
        ax.add_patch(triangle2)
    
    # Customize the plot
    ax.set_ylim(7, -1)  # Reverse y-axis to match calendar orientation
    ax.set_xlim(-1, len(weeks))
    
    # Set labels
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_yticks(range(7))
    ax.set_yticklabels(weekdays, rotation=0, fontsize=16)
    
    # Add month labels
    months = pd.date_range(data['date'].min(), data['date'].max(), freq='MS')
    month_weeks = [np.where(weeks == week)[0][0] for week in 
                  pd.DataFrame({'date': months})['date'].dt.isocalendar().week]
    
    ax.set_xticks(month_weeks)
    ax.set_xticklabels([d.strftime('%B') for d in months], rotation=0, fontsize=16)
    
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    sm = plt.cm.ScalarMappable(cmap=cmap1, norm=plt.Normalize(1, 10))
    cbar = plt.colorbar(sm, cax=cbar_ax)

    # Remove numerical ticks
    # Set just two ticks at the extremes
    cbar.set_ticks([1, 5, 10])
    cbar.set_ticklabels(['1 - Awful','5 - Neutral', '10 - Amazing'], fontsize=16)

    # extra legend section:
   # Calculate averages (ignoring None values)
    # Calculate averages (ignoring None values)
    michael_avg = data['person1_score'].dropna().mean()
    melanie_avg = data['person2_score'].dropna().mean()

    # Create a split square legend - increased from 0.05 to 0.15 for both width and height
    legend_ax = fig.add_axes([0.855, 0.01, 0.15, 0.15])  # Made it 3x larger
    legend_ax.set_aspect('equal')  # Force square aspect ratio
    legend_ax.set_axis_off()

    # Create the split square for the legend
    triangle1 = Polygon(
        [[0, 0], [1, 1], [0, 1]],  # Changed from [[0, 0], [1, 0], [0, 1]]
        facecolor=cmap1(normalize_score(michael_avg)),
        edgecolor='white',
        linewidth=0.5
    )
    triangle2 = Polygon(
        [[0, 0], [1, 0], [1, 1]],  # Changed from [[1, 0], [1, 1], [0, 1]]
        facecolor=cmap2(normalize_score(melanie_avg)),
        edgecolor='white',
        linewidth=0.5
    )

    legend_ax.add_patch(triangle1)
    legend_ax.add_patch(triangle2)

    # Add labels - adjusted position for larger square
    legend_ax.text(-1.2, .4, f'Michael\nMean={michael_avg:.1f}', ha='left', va='bottom', fontsize=12)
    legend_ax.text(1.2, .4, f'Melanie\nMean={melanie_avg:.1f}', ha='left', va='bottom', fontsize=12)

    # Set the legend axes limits
    legend_ax.set_xlim(-0.2, 1.2)
    legend_ax.set_ylim(-0.2, 1.2)
        
    # Set title
    plt.suptitle('How was your day on a scale of 1-10?', y=0.95, fontsize=32)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    plt.subplots_adjust(right=0.9)
    
    return fig, ax

def load_data():
    # if this file exists, load it data.to_pickle('calendar_heatmap_data.pkl', index=False)
    if os.path.exists('calendar_heatmap_data.pkl'):
        print('Loading data from file')
        return pd.read_pickle('calendar_heatmap_data.pkl')

    michae_emo = 'Michael - Emotion (5 neutral) '
    mel_emo = 'Melanie - Emotion (5 neutral)'
    df = pd.read_csv('YearDataDailyCollector.csv')
    # convert the date column to datetime
    df['Date'] = pd.to_datetime(df['Timestamp'])
    # if the time is from before 6am, then it is the previous day
    df['Date'] = df['Date'] - pd.Timedelta(hours=6)
    # create a "thedate" that is just the date and strip off the time

    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    michael_scores = []
    mel_scores = []
    missing_count = 0
    for date in dates:
        # if the month day year is a match, ignore time
        sub = df[df['Date'].dt.strftime('%m-%d-%Y') == date.strftime('%m-%d-%Y')]
        if len(sub) == 0:
            missing_count += 1
            michael_scores.append(None)
            mel_scores.append(None)
        else:
            michael_score = sub[michae_emo].mean()
            mel_score = sub[mel_emo].mean()
            # if scores or nan or None make None
            if pd.isna(michael_score):
                michael_score = None
            if pd.isna(mel_score):
                mel_score = None
            if mel_score is None:
                mel_score = michael_score
            if michael_score is None:
                michael_score = mel_score
            michael_scores.append(michael_score)
            mel_scores.append(mel_score)
    data = pd.DataFrame({
        'date': dates,
        'person1_score': michael_scores,
        'person2_score': mel_scores
    })
    # save data as csv
    print('Writing data to file')
    data.to_pickle('calendar_heatmap_data.pkl')

    return data

if __name__ == "__main__":
    # Generate sample data
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    sample_data = load_data()
    
    # Create the visualization
    fig, ax = create_split_calendar_heatmap(sample_data)
    # remove all borders, but keep the ticks and labels
    ax.spines['top'].set_visible(False)    # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border
    ax.spines['bottom'].set_visible(False) # Remove bottom border
    ax.spines['left'].set_visible(False)   # Remove left border
    
    # Don't try to remove any colorbars since we only created one
    
    plt.savefig('calendar_heatmap.png', dpi=300)
    # plt.show()