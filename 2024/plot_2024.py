"""
Consolidated 2024 data visualization script.

This script generates all visualizations for 2024 data:
- Emotion calendars (raw and Z-score)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / 'data'
OUTPUT_DIR = SCRIPT_DIR / 'outputs'

from plotting_utils.emotion import plot_emotion_calendar


def plot_emotion_calendars():
    """Generate emotion calendar visualizations."""
    print("\n" + "="*80)
    print("EMOTION CALENDARS")
    print("="*80)

    # Raw emotion calendar
    print("\nGenerating raw emotion calendar...")
    plot_emotion_calendar(
        csv_path=str(DATA_DIR / 'YearDataDailyCollector.csv'),
        year=2024,
        person1_col='Michael - Emotion (5 neutral) ',  # Note: trailing space in 2024 data
        person2_col='Melanie - Emotion (5 neutral)',
        person1_name='Michael',
        person2_name='Melanie',
        output_path=str(OUTPUT_DIR / 'calendar_emotion_together.png'),
        cache_path=str(OUTPUT_DIR / 'calendar_emotion_together.pkl'),
        use_zscore=False
    )
    print("✓ Raw emotion calendar created")

    # Z-score emotion calendar
    print("\nGenerating Z-score emotion calendar...")
    plot_emotion_calendar(
        csv_path=str(DATA_DIR / 'YearDataDailyCollector.csv'),
        year=2024,
        person1_col='Michael - Emotion (5 neutral) ',  # Note: trailing space in 2024 data
        person2_col='Melanie - Emotion (5 neutral)',
        person1_name='Michael',
        person2_name='Melanie',
        output_path=str(OUTPUT_DIR / 'calendar_emotion_together_zscore.png'),
        cache_path=str(OUTPUT_DIR / 'calendar_emotion_together.pkl'),
        use_zscore=True,
        export_weekday_stats=str(OUTPUT_DIR / 'weekday_emotion_together.csv'),
        plot_weekday_heatmap_path=str(OUTPUT_DIR / 'weekday_emotion_heatmap_together.png')
    )
    print("✓ Z-score emotion calendar created")
    print("✓ Weekday statistics exported")
    print("✓ Weekday heatmap created")


def main():
    """Run all visualization generation."""
    print("="*80)
    print("2024 DATA VISUALIZATION")
    print("="*80)

    # Generate all visualizations
    plot_emotion_calendars()

    print("\n" + "="*80)
    print("ALL VISUALIZATIONS COMPLETE")
    print("="*80)
    print("\nOutputs saved to: 2024/outputs/")
    print("\nGenerated files:")
    print("  Emotion calendars:")
    print("    - calendar_emotion_together.png")
    print("    - calendar_emotion_together_zscore.png")
    print("    - weekday_emotion_together.csv")
    print("    - weekday_emotion_heatmap_together.png")


if __name__ == "__main__":
    main()
