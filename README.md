# Year of Data

Personal data tracking and visualization project for daily life metrics.

## Project Structure

- `plotting_utils/` - Year-agnostic plotting library
  - `emotion.py` - Emotion calendar heatmaps
  - `activities.py` - Activity pie charts and timelines
  - `wordcloud_processing.py` - Text processing for word clouds

- `2024/` - 2024 data and analysis
- `2025/` - 2025 data and analysis

## Setup

Install dependencies with uv:

```bash
uv sync
```

## Usage

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Generate visualizations:

```bash
python plot_2025_emotion.py
```

## Word Cloud Generation

### Creating Word Clouds from Exported Data

1. **Generate word lists:**
   ```bash
   uv run python plot_2025_wordclouds.py
   ```
   This creates processed word lists:
   - `2025_best_part_wordcloud.txt` - Best part of the day
   - `2025_worst_part_wordcloud.txt` - Worst part of the day

2. **Create word clouds using wordclouds.com:**
   - Go to [www.wordclouds.com](https://www.wordclouds.com)
   - Click "Word List" input mode
   - Copy and paste the contents of the word list file
   - Configure colors:
     - **Best part of the day**: Green `#287521`
     - **Worst part of the day**: Red `#DF0001`
   - Adjust other settings as desired (shape, font, etc.)
   - Generate and download the word cloud

**Note:** The exported word lists use tildes (~) instead of spaces for multi-word phrases (e.g., "good~session"). This ensures phrases stay together in the word cloud.

## Statistical Analysis

### Event-Emotion Association Analysis

The `analyze_emotion_events_2025.py` script analyzes associations between daily events and emotion scores using rigorous statistical methods designed to handle real-world data challenges.

#### Statistical Testing Methodology

**Test Selection: Welch's t-test**
- Uses Welch's t-test (two-sample t-test with unequal variances)
- Does not assume equal variances between groups
- Robust to imbalanced datasets (e.g., 4 "cry" events vs. 200 "no cry" events)
- Implemented via `scipy.stats.ttest_ind(equal_var=False)`

**Sample Size Requirements**
- Minimum 3 observations per group required for statistical testing
- Tests with insufficient data return `NaN` for p-values
- Prevents unreliable results from very small samples

**Effect Size: Cohen's d**
- Reports standardized mean difference (Cohen's d)
- Independent of sample size, allows comparison across different events
- Interpretation: small (0.2), medium (0.5), large (0.8)
- Calculated using pooled standard deviation

**Multiple Comparison Correction: Bonferroni**
- Corrects for multiple hypothesis testing to control family-wise error rate
- Threshold: p < 0.05 / n_comparisons
- Currently analyzing 36 comparisons (15 shared events × 2 people + 3 person-specific events × 2 people)
- Bonferroni threshold: p < 0.0014

**Balance Ratio**
- Reports min(n_positive, n_negative) / max(n_positive, n_negative)
- Indicates how balanced the groups are (1.0 = perfectly balanced, 0.0 = highly imbalanced)
- Helps interpret results in context of data distribution

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
