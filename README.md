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

## GitHub Pages Website

A static website showcasing all visualizations is available in the `docs/` directory.

**To enable GitHub Pages:**
1. Go to your repository settings on GitHub
2. Navigate to "Pages" section
3. Set source to "Deploy from a branch"
4. Select branch: `main` and folder: `/docs`
5. Save and wait for deployment

The site will be available at: `https://<username>.github.io/<repository>/`

**Website features:**
- Clean, modern design with responsive layout
- All 2025 and 2024 visualizations displayed
- Organized by year and category (emotion, timeline, activities)
- Placeholder descriptions for each visualization (ready for customization)
- Automatic dark/light theme based on browser preference

### Password Protection with StatiCrypt

The GitHub Pages website is password-protected using [StatiCrypt](https://github.com/robinmoisson/staticrypt) to keep personal data private.

**Installation:**
```bash
npm install -g staticrypt
```

**Encrypting the Website:**

⚠️ **IMPORTANT**: The unencrypted `index.html` should NEVER be committed to the repository. Only commit the encrypted version.

1. Create your unencrypted HTML file as `docs/index_unencrypted.html` (this file is gitignored)
2. Encrypt it with your password:
   ```bash
   staticrypt docs/index_unencrypted.html -o docs/index.html --password YOUR_PASSWORD --remember --short
   ```
3. Only commit the encrypted `docs/index.html` file

**Workflow for updating the website:**
1. Make changes to `docs/index_unencrypted.html`
2. Re-encrypt using the command above
3. Commit only the encrypted `docs/index.html`
4. Push to GitHub - the encrypted version will be deployed

**StatiCrypt options used:**
- `--password`: Sets the password for decryption
- `--remember`: Enables "Remember me" checkbox to save password in browser
- `--short`: Generates more compact output
