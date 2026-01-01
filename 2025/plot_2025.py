"""
Consolidated 2025 data visualization script.

This script generates all visualizations for 2025 data:
- Emotion calendars (raw and Z-score)
- Pie charts (shared events and person-specific activities)
- Word clouds (best/worst parts of day)
- Event timeline with emotion trends
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / 'data'
OUTPUT_DIR = SCRIPT_DIR.parent / 'docs' / '2025' / 'outputs'

from plotting_utils.emotion import plot_emotion_calendar
from plotting_utils.activities import (
    plot_did_we_events_2025,
    plot_did_we_events_2025_mobile,
    plot_person_specific_events_2025,
    plot_person_specific_events_2025_mobile,
    create_2025_event_timeline
)
from plotting_utils.wordcloud_processing import export_wordcloud_words
import pandas as pd


def plot_emotion_calendars():
    """Generate emotion calendar visualizations."""
    print("\n" + "="*80)
    print("EMOTION CALENDARS")
    print("="*80)

    # Raw emotion calendar - Desktop
    print("\nGenerating raw emotion calendar (desktop)...")
    plot_emotion_calendar(
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        year=2025,
        person1_col='Emotion - Michael',
        person2_col='Emotion - Melanie',
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
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        year=2025,
        person1_col='Emotion - Michael',
        person2_col='Emotion - Melanie',
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
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        year=2025,
        person1_col='Emotion - Michael',
        person2_col='Emotion - Melanie',
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
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        year=2025,
        person1_col='Emotion - Michael',
        person2_col='Emotion - Melanie',
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


def plot_pie_charts():
    """Generate pie chart visualizations."""
    print("\n" + "="*80)
    print("PIE CHARTS")
    print("="*80)

    # Shared events pie chart - Desktop
    print("\nGenerating shared events pie chart (desktop)...")
    plot_did_we_events_2025(
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        output_path=str(OUTPUT_DIR / 'pie_events_together.png')
    )

    # Shared events pie chart - Mobile
    print("\nGenerating shared events pie chart (mobile)...")
    plot_did_we_events_2025_mobile(
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        output_path=str(OUTPUT_DIR / 'pie_events_together_mobile.png')
    )

    # Person-specific activity pie charts - Desktop
    print("\nGenerating person-specific activity pie charts (desktop)...")
    plot_person_specific_events_2025(
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        output_path_michael=str(OUTPUT_DIR / 'pie_activities_michael.png'),
        output_path_melanie=str(OUTPUT_DIR / 'pie_activities_melanie.png')
    )

    # Person-specific activity pie charts - Mobile
    print("\nGenerating person-specific activity pie charts (mobile)...")
    plot_person_specific_events_2025_mobile(
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        output_path_michael=str(OUTPUT_DIR / 'pie_activities_michael_mobile.png'),
        output_path_melanie=str(OUTPUT_DIR / 'pie_activities_melanie_mobile.png')
    )


def generate_wordcloud_data():
    """Generate word cloud data files."""
    print("\n" + "="*80)
    print("WORD CLOUD DATA")
    print("="*80)

    # Load data
    df = pd.read_csv(str(DATA_DIR / '2025DataCollection.csv'))

    # Custom word replacements
    custom_replacements = {
        r'\bpatch\b': 'patches',
        r'\bflo\b': 'florence',
        r'mel\b': 'melanie',
        r'feeling|felt': 'feel',
        r'cats|cat|kitty|kittens|kitties': 'cat',
        r'cuddles|cuddle|snuggles|snuggle': 'cuddle',
        r'sexy|sex': 'sex',
        r'skiing|ski': 'ski',
        r'swimming|swim': 'swim'
    }

    # Export word cloud data for best parts
    print("\nProcessing 'Best part of the day'...")
    best_texts = df['Best part of the day'].dropna()
    export_wordcloud_words(
        best_texts,
        output_path=str(OUTPUT_DIR / 'wordcloud_best_together.txt'),
        use_tildes=True,
        custom_replacements=custom_replacements
    )

    # Export word cloud data for worst parts
    print("\nProcessing 'Worst part of the day'...")
    worst_texts = df['Worst part of the day'].dropna()
    export_wordcloud_words(
        worst_texts,
        output_path=str(OUTPUT_DIR / 'wordcloud_worst_together.txt'),
        use_tildes=True,
        custom_replacements=custom_replacements
    )


def plot_timeline():
    """Generate event timeline with emotion trends."""
    print("\n" + "="*80)
    print("EVENT TIMELINE")
    print("="*80)

    print("\nGenerating timeline...")
    create_2025_event_timeline(
        csv_path=str(DATA_DIR / '2025DataCollection.csv'),
        output_path=str(OUTPUT_DIR / 'timeline_events_together.png'),
        title="Melanie & Michael's 2025 Events & Activities"
    )
    print("✓ Timeline created")


def main():
    """Run all visualization generation."""
    print("="*80)
    print("2025 DATA VISUALIZATION")
    print("="*80)

    # Generate all visualizations
    plot_emotion_calendars()
    plot_pie_charts()
    generate_wordcloud_data()
    plot_timeline()

    print("\n" + "="*80)
    print("ALL VISUALIZATIONS COMPLETE")
    print("="*80)
    print("\nOutputs saved to: docs/2025/outputs/")
    print("\nGenerated files:")
    print("  Emotion calendars:")
    print("    - calendar_emotion_together.png (desktop)")
    print("    - calendar_emotion_together_mobile.png (mobile)")
    print("    - calendar_emotion_together_zscore.png (desktop)")
    print("    - calendar_emotion_together_zscore_mobile.png (mobile)")
    print("    - weekday_emotion_together.csv")
    print("    - weekday_emotion_heatmap_together.png (desktop)")
    print("    - weekday_emotion_heatmap_together_mobile.png (mobile)")
    print("  Pie charts:")
    print("    - pie_events_together.png (desktop)")
    print("    - pie_events_together_mobile.png (mobile)")
    print("    - pie_activities_michael.png (desktop)")
    print("    - pie_activities_michael_mobile.png (mobile)")
    print("    - pie_activities_melanie.png (desktop)")
    print("    - pie_activities_melanie_mobile.png (mobile)")
    print("  Word clouds:")
    print("    - wordcloud_best_together.txt")
    print("    - wordcloud_worst_together.txt")
    print("  Timeline:")
    print("    - timeline_events_together.png")


if __name__ == "__main__":
    main()
