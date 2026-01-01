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
OUTPUT_DIR = SCRIPT_DIR.parent / 'docs' / '2024' / 'outputs'

from plotting_utils.emotion import plot_emotion_calendar


def plot_emotion_calendars():
    """Generate emotion calendar visualizations."""
    print("\n" + "="*80)
    print("EMOTION CALENDARS")
    print("="*80)

    # Raw emotion calendar - Desktop
    print("\nGenerating raw emotion calendar (desktop)...")
    plot_emotion_calendar(
        csv_path=str(DATA_DIR / 'YearDataDailyCollector.csv'),
        year=2024,
        person1_col='Michael - Emotion (5 neutral) ',  # Note: trailing space in 2024 data
        person2_col='Melanie - Emotion (5 neutral)',
        person1_name='Michael',
        person2_name='Melanie',
        output_path=str(OUTPUT_DIR / 'calendar_emotion_together.png'),
        cache_path=str(OUTPUT_DIR / 'calendar_emotion_together.pkl'),
        use_zscore=False,
        mobile=False
    )
    print("✓ Raw emotion calendar (desktop) created")

    # Raw emotion calendar - Mobile
    print("\nGenerating raw emotion calendar (mobile)...")
    plot_emotion_calendar(
        csv_path=str(DATA_DIR / 'YearDataDailyCollector.csv'),
        year=2024,
        person1_col='Michael - Emotion (5 neutral) ',  # Note: trailing space in 2024 data
        person2_col='Melanie - Emotion (5 neutral)',
        person1_name='Michael',
        person2_name='Melanie',
        output_path=str(OUTPUT_DIR / 'calendar_emotion_together_mobile.png'),
        cache_path=str(OUTPUT_DIR / 'calendar_emotion_together.pkl'),
        use_zscore=False,
        mobile=True
    )
    print("✓ Raw emotion calendar (mobile) created")

    # Z-score emotion calendar - Desktop
    print("\nGenerating Z-score emotion calendar (desktop)...")
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
        plot_weekday_heatmap_path=str(OUTPUT_DIR / 'weekday_emotion_heatmap_together.png'),
        mobile=False
    )
    print("✓ Z-score emotion calendar (desktop) created")
    print("✓ Weekday statistics exported")
    print("✓ Weekday heatmap created")

    # Z-score emotion calendar - Mobile
    print("\nGenerating Z-score emotion calendar (mobile)...")
    plot_emotion_calendar(
        csv_path=str(DATA_DIR / 'YearDataDailyCollector.csv'),
        year=2024,
        person1_col='Michael - Emotion (5 neutral) ',  # Note: trailing space in 2024 data
        person2_col='Melanie - Emotion (5 neutral)',
        person1_name='Michael',
        person2_name='Melanie',
        output_path=str(OUTPUT_DIR / 'calendar_emotion_together_zscore_mobile.png'),
        cache_path=str(OUTPUT_DIR / 'calendar_emotion_together.pkl'),
        use_zscore=True,
        plot_weekday_heatmap_path=str(OUTPUT_DIR / 'weekday_emotion_heatmap_together_mobile.png'),
        mobile=True
    )
    print("✓ Z-score emotion calendar (mobile) created")
    print("✓ Weekday heatmap (mobile) created")


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
    print("\nOutputs saved to: docs/2024/outputs/")
    print("\nGenerated files:")
    print("  Emotion calendars:")
    print("    - calendar_emotion_together.png (desktop)")
    print("    - calendar_emotion_together_mobile.png (mobile)")
    print("    - calendar_emotion_together_zscore.png (desktop)")
    print("    - calendar_emotion_together_zscore_mobile.png (mobile)")
    print("    - weekday_emotion_together.csv")
    print("    - weekday_emotion_heatmap_together.png (desktop)")
    print("    - weekday_emotion_heatmap_together_mobile.png (mobile)")


if __name__ == "__main__":
    main()
