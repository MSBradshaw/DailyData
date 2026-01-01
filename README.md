# Year of Data

Personal data tracking and visualization project for daily life metrics.

## Project Structure

```
plotting_utils/          # Year-agnostic plotting library
├── emotion.py          # Emotion calendar heatmaps
├── activities.py       # Activity pie charts and timelines
└── wordcloud_processing.py  # Text processing for word clouds

2024/
├── data/               # 2024 data files
├── outputs/            # Generated visualizations and analysis
└── plot_2024.py        # Consolidated plotting script

2025/
├── data/               # 2025 data files
├── outputs/            # Generated visualizations and analysis
├── plot_2025.py        # Consolidated plotting script
└── analyze_emotion_events_2025.py  # Statistical analysis

docs/
└── index.html          # GitHub Pages website showcasing visualizations
```

## Setup

Install dependencies with uv:

```bash
uv sync
```

## Usage

### Generate All Visualizations

**For 2025 data:**
```bash
cd 2025
uv run python plot_2025.py
```

**For 2024 data:**
```bash
cd 2024
uv run python plot_2024.py
```

### Run Statistical Analysis

**2025 event-emotion associations:**
```bash
cd 2025
uv run python analyze_emotion_events_2025.py
```

All outputs will be saved to the respective `outputs/` directory.

## Visualizations Generated

The consolidated plotting scripts generate the following visualizations:

### File Naming Convention

All outputs follow the pattern: `<type>_<subject>_<person>.<ext>`
- **person**: `together` (both people), `michael`, or `melanie`
- **type**: `calendar`, `pie`, `wordcloud`, `timeline`, `analysis`, `weekday`
- **subject**: `emotion`, `events`, `activities`, `best`, `worst`

### 2025 Outputs

**Emotion Calendars:**
- `calendar_emotion_together.png` - Raw emotion scores
- `calendar_emotion_together_zscore.png` - Z-score normalized emotions
- `weekday_emotion_together.csv` - Weekday statistics
- `weekday_emotion_heatmap_together.png` - Weekday patterns

**Pie Charts:**
- `pie_events_together.png` - Shared events (Laugh, Cry, Fight, etc.)
- `pie_activities_michael.png` - Michael's activities
- `pie_activities_melanie.png` - Melanie's activities

**Timeline:**
- `timeline_events_together.png` - Event timeline with emotion trends
  - Event markers with overplotting visibility
  - 7-day rolling average emotion Z-scores
  - Person-specific activity rows
  - Monthly grid lines

**Word Cloud Data:**
- `wordcloud_best_together.txt` - Best part of day (for wordclouds.com)
- `wordcloud_worst_together.txt` - Worst part of day (for wordclouds.com)

**Statistical Analysis:**
- `analysis_emotion_events_together.csv` - Event-emotion associations

### 2024 Outputs

**Emotion Calendars:**
- `calendar_emotion_together.png` - Raw emotion scores
- `calendar_emotion_together_zscore.png` - Z-score normalized emotions
- `weekday_emotion_together.csv` - Weekday statistics
- `weekday_emotion_heatmap_together.png` - Weekday patterns

## Word Cloud Creation

The word cloud data files can be used with [www.wordclouds.com](https://www.wordclouds.com):

1. Click "Word List" input mode
2. Copy and paste the contents of the word list file
3. Configure colors:
   - **Best part**: Green `#287521`
   - **Worst part**: Red `#DF0001`
4. Generate and download

**Note:** Word lists use tildes (~) for multi-word phrases (e.g., "good~session").

## Statistical Analysis

### Event-Emotion Association Analysis

The `analyze_emotion_events_2025.py` script analyzes associations between daily events and emotion scores using rigorous statistical methods designed to handle real-world data challenges.

#### Statistical Testing Methodology

The analysis uses Welch's t-test to compare emotion scores between days with and without specific events. Key features:

- **Statistical test**: Welch's t-test (handles unequal variances and imbalanced datasets)
- **Effect size**: Cohen's d for standardized comparison across events
- **Multiple comparison correction**: Bonferroni correction (threshold: p < 0.0014 for 36 comparisons)
- **Minimum sample size**: 3 observations per group required for testing

#### Events Analyzed

**Shared Events** (same for both people):
- Emotional: Laugh, Cry, Fight, Tender Moment, Spend Money
- Exercise: Any Exercise, Cardio, Strength Training
- Social: Family or Friends, Family (specific), Friends (specific)
- Activities: Any Activity
- Blood Sugar: Bad (1), Medium (2), Good (3)

**Person-Specific Events**:
- Reading (tracked separately per person)
- TV watching (tracked separately per person)
- Fruit/Vegetable consumption (tracked separately per person)

#### Output

Results are saved to `2025_emotion_event_analysis.csv` with columns:
- `Person`: Michael or Melanie
- `Event`: Event name
- `p_value`: Statistical significance (formatted with scientific notation for very small values)
- `significant_bonferroni`: Boolean indicating significance after Bonferroni correction
- `num_positive`: Number of days with event
- `num_negative`: Number of days without event
- `balance_ratio`: Group balance metric (0-1)
- `avg_emotion_positive`: Average emotion score on days with event
- `avg_emotion_negative`: Average emotion score on days without event
- `difference`: Mean difference (positive - negative)
- `cohens_d`: Effect size (standardized mean difference)

## GitHub Pages Website

The site will be available at: `https://msbradshaw.github.io/DailyData/`

### Password Protection with StatiCrypt

The GitHub Pages website is password-protected using [StatiCrypt](https://github.com/robinmoisson/staticrypt) to keep personal data private.

**Workflow for updating the website:**
1. Make changes to `docs/index_unencrypted.html`
2. Re-encrypt using the command above
3. Commit only the encrypted `docs/index.html`
4. Push to GitHub - the encrypted version will be deployed
