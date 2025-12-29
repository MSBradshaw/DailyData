"""
Generate 2025 emotion calendar using plotting_utils package.
"""

from plotting_utils import plot_emotion_calendar

if __name__ == "__main__":
    print("Generating 2025 emotion calendar...")

    fig, ax = plot_emotion_calendar(
        csv_path='2025DataCollection.csv',
        year=2025,
        person1_col='Emotion - Michael',  # Note: column name changed from 2024
        person2_col='Emotion - Melanie',  # Note: column name changed from 2024
        person1_name='Michael',
        person2_name='Melanie',
        output_path='2025_calendar_heatmap.png',
        cache_path='2025_calendar_heatmap_data.pkl',
        export_weekday_stats='2025_emotion_by_weekday.csv',
        plot_weekday_heatmap_path='2025_emotion_weekday_heatmap.png'
    )

    print("✓ 2025 emotion calendar created successfully!")
    print("  Saved to: 2025_calendar_heatmap.png")
