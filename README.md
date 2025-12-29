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
