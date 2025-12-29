"""
Generate 2025 emotion calendar with Z-score normalization.
"""

from plotting_utils import plot_emotion_calendar

if __name__ == "__main__":
    print("Generating 2025 emotion calendar with Z-score normalization...")

    # Generate Z-score version
    fig, ax = plot_emotion_calendar(
        csv_path='2025DataCollection.csv',
        year=2025,
        person1_col='Emotion - Michael',
        person2_col='Emotion - Melanie',
        person1_name='Michael',
        person2_name='Melanie',
        output_path='2025_calendar_heatmap_zscore.png',
        cache_path='2025_calendar_heatmap_data.pkl',
        use_zscore=True,  # Enable Z-score mode
        export_weekday_stats='2025_emotion_by_weekday.csv',  # Export weekday statistics
        plot_weekday_heatmap_path='2025_emotion_weekday_heatmap.png'  # Weekday heatmap
    )

    print("✓ 2025 Z-score emotion calendar created successfully!")
    print("  Saved to: 2025_calendar_heatmap_zscore.png")
    print("\nZ-score mode:")
    print("  - Red = Below average days (negative Z-score / bad days)")
    print("  - Yellow = Average days (Z-score ~ 0 / neutral)")
    print("  - Green = Above average days (positive Z-score / great days)")
    print("  - Calculated separately for each person")
