"""
Test script to verify plotting_utils package works with 2024 data.
"""

from plotting_utils import (
    plot_emotion_calendar,
    plot_activities,
    process_best_worst_parts
)

def test_emotion_plot():
    """Test emotion calendar generation."""
    print("Testing emotion calendar plot...")

    fig, ax = plot_emotion_calendar(
        csv_path='YearDataDailyCollector.csv',
        year=2024,
        person1_col='Michael - Emotion (5 neutral) ',
        person2_col='Melanie - Emotion (5 neutral)',
        person1_name='Michael',
        person2_name='Melanie',
        output_path='test_calendar_heatmap.png',
        cache_path='test_calendar_heatmap_data.pkl'
    )

    print("✓ Emotion calendar created successfully")
    return fig, ax


def test_activity_plots():
    """Test activity pie charts and timeline."""
    print("\nTesting activity plots...")

    pie_fig, timeline_fig, timeline_ax = plot_activities(
        csv_path='YearDataDailyCollector.csv',
        output_pie_path='test_activity_pies.png',
        output_timeline_path='test_task_timeline.png',
        timeline_title="Melanie & Michael's Year of Daily Data"
    )

    print("✓ Activity plots created successfully")
    return pie_fig, timeline_fig


def test_wordcloud_processing():
    """Test word cloud data processing."""
    print("\nTesting word cloud processing...")

    best_freq, worst_freq = process_best_worst_parts(
        csv_path='YearDataDailyCollector.csv',
        output_best_csv='test_best_part_of_day.csv',
        output_worst_csv='test_worst_part_of_day.csv',
        output_best_words='test_all_words_best.txt',
        output_worst_words='test_all_words_worst.txt'
    )

    print(f"✓ Processed {len(best_freq)} unique words from best parts")
    print(f"✓ Processed {len(worst_freq)} unique words from worst parts")

    # Print top 10 words from each
    print("\nTop 10 'best' words:")
    for word, freq in sorted(best_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {word}: {freq}")

    print("\nTop 10 'worst' words:")
    for word, freq in sorted(worst_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {word}: {freq}")

    return best_freq, worst_freq


if __name__ == "__main__":
    print("=" * 60)
    print("Testing plotting_utils package with 2024 data")
    print("=" * 60)

    try:
        # Test emotion plot
        emotion_fig, emotion_ax = test_emotion_plot()

        # Test activity plots
        pie_fig, timeline_fig = test_activity_plots()

        # Test word cloud processing
        best_freq, worst_freq = test_wordcloud_processing()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print("\nGenerated test files:")
        print("  - test_calendar_heatmap.png")
        print("  - test_activity_pies.png")
        print("  - test_task_timeline.png")
        print("  - test_best_part_of_day.csv")
        print("  - test_worst_part_of_day.csv")
        print("  - test_all_words_best.txt")
        print("  - test_all_words_worst.txt")
        print("  - test_calendar_heatmap_data.pkl")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
