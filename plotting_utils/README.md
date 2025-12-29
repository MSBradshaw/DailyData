# Plotting Utils

A year-agnostic Python package for visualizing daily tracking data. This package provides reusable tools for creating emotion calendars, activity timelines, and processing text for word clouds.

## Modules

### 1. `emotion.py`
Creates split-cell calendar heatmaps showing daily emotion scores for two people.

**Key Functions:**
- `plot_emotion_calendar()` - Complete workflow to generate emotion calendar
- `load_emotion_data()` - Load and process emotion data from CSV
- `create_split_calendar_heatmap()` - Create the visualization

**Example:**
```python
from plotting_utils import plot_emotion_calendar

fig, ax = plot_emotion_calendar(
    csv_path='YearDataDailyCollector.csv',
    year=2024,
    person1_col='Michael - Emotion (5 neutral) ',
    person2_col='Melanie - Emotion (5 neutral)',
    person1_name='Michael',
    person2_name='Melanie',
    output_path='calendar_heatmap.png',
    cache_path='calendar_data.pkl'
)
```

### 2. `activities.py`
Creates pie charts and timeline visualizations for daily activities.

**Key Functions:**
- `plot_activities()` - Complete workflow for activity visualizations
- `create_activity_pie_grid()` - Grid of pie charts showing activity distributions
- `create_task_timeline()` - Timeline scatter plot of activities
- `get_standard_activity_columns()` - Get standard activity column names
- `get_standard_column_mapping()` - Get standard column name mapping

**Example:**
```python
from plotting_utils import plot_activities

pie_fig, timeline_fig, timeline_ax = plot_activities(
    csv_path='YearDataDailyCollector.csv',
    output_pie_path='activity_pies.png',
    output_timeline_path='task_timeline.png',
    timeline_title="Our Year of Daily Data"
)
```

### 3. `wordcloud_processing.py`
NLP processing for extracting meaningful words from free-text responses.

**Key Functions:**
- `process_best_worst_parts()` - Complete workflow for best/worst text processing
- `get_wordcloud_data()` - Extract word frequencies
- `export_wordcloud_words()` - Export processed words to file
- `process_text()` - Core NLP processing (tokenization, lemmatization, n-grams)

**Example:**
```python
from plotting_utils import process_best_worst_parts

best_freq, worst_freq = process_best_worst_parts(
    csv_path='YearDataDailyCollector.csv',
    output_best_words='best_words.txt',
    output_worst_words='worst_words.txt'
)
```

## Installation

This package requires the following dependencies:

```bash
pip install pandas numpy matplotlib seaborn nltk
```

NLTK data will be downloaded automatically on first use.

## Usage for Different Years

The package is designed to be year-agnostic. Simply specify the year parameter:

```python
# For 2024
plot_emotion_calendar(csv_path='2024_data.csv', year=2024, ...)

# For 2025
plot_emotion_calendar(csv_path='2025_data.csv', year=2025, ...)
```

## Expected CSV Format

The package expects CSV files with the following columns:

**Required for all modules:**
- `Timestamp` - Date/time of entry

**For emotion calendar:**
- Person 1 emotion score column (1-10 scale)
- Person 2 emotion score column (1-10 scale)

**For activities:**
- Activity columns (binary Yes/No or numeric values)
- Standard columns: laughter, crying, tender moments, fights, family time, cardio, climbing, strength training, fruit, vegetables, TV, reading, dishes

**For word cloud processing:**
- `Best part of the day` - Free text
- `Worst part of the day` - Free text

## Customization

All functions support customization through parameters:

- **Column names** - Specify your own column names
- **Colors** - Customize color schemes
- **Labels** - Change person names and titles
- **Caching** - Optional pickle caching for faster reloads
- **NLP settings** - Custom stop words and word replacements

## Testing

Run the test script to verify the package works with your data:

```bash
python test_plotting_utils.py
```

This will generate test outputs for all visualization types.
