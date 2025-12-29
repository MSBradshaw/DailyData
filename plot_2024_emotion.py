"""
Generate 2024 emotion calendar and analysis plots.
"""

from plotting_utils import plot_emotion_calendar

if __name__ == "__main__":
    print("Generating 2024 emotion visualizations...")

    # Generate standard version
    fig, ax = plot_emotion_calendar(
        csv_path='YearDataDailyCollector.csv',
        year=2024,
        person1_col='Michael - Emotion (5 neutral) ',  # Note: trailing space in 2024 data
        person2_col='Melanie - Emotion (5 neutral)',
        person1_name='Michael',
        person2_name='Melanie',
        output_path='2024_calendar_heatmap.png',
        cache_path='2024_calendar_heatmap_data.pkl',
        export_weekday_stats='2024_emotion_by_weekday.csv',
        plot_weekday_heatmap_path='2024_emotion_weekday_heatmap.png'
    )

    print("✓ 2024 emotion calendar created successfully!")
    print("  Saved to: 2024_calendar_heatmap.png")
    print("  Weekday stats: 2024_emotion_by_weekday.csv")
    print("  Weekday heatmap: 2024_emotion_weekday_heatmap.png")
