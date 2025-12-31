"""
Generate 2025 events and activities timeline.
"""

from plotting_utils.activities import create_2025_event_timeline

if __name__ == "__main__":
    print("="*80)
    print("Generating 2025 Timeline")
    print("="*80)

    fig, ax = create_2025_event_timeline(
        csv_path='2025DataCollection.csv',
        output_path='2025_events_timeline.png',
        title="Melanie & Michael's 2025 Events & Activities"
    )

    print("\n" + "="*80)
    print("Timeline Summary")
    print("="*80)
    print("\nVisualization shows when events occurred throughout 2025")
    print("\nEvent categories:")
    print("  - Emotional: Laugh, Cry, Fight, Tender Moment, Spend Money")
    print("  - Exercise: Any Exercise, Cardio, Strength")
    print("  - Social: Family, Friends")
    print("  - Activities: Any Activity")
    print("  - Person-specific: Reading, TV, Fruit/Veg (divided by Michael/Melanie)")
    print("\nTimeline features:")
    print("  - Each row = one event type")
    print("  - Colored dots/bars = days when event occurred")
    print("  - Vertical lines = month boundaries")
