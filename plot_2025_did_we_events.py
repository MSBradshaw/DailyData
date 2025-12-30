"""
Generate all pie charts for 2025 data.
"""

from plotting_utils.activities import plot_did_we_events_2025, plot_person_specific_events_2025

if __name__ == "__main__":
    print("="*80)
    print("Generating 2025 Pie Charts")
    print("="*80)

    # Generate "Did we ..." event pie charts
    print("\n1. Generating 'Did we ...' event pie charts...")
    fig_did_we = plot_did_we_events_2025(
        csv_path='2025DataCollection.csv',
        output_path='2025_did_we_events_pie_charts.png'
    )

    # Generate person-specific activity pie charts
    print("\n2. Generating person-specific activity pie charts...")
    fig_michael, fig_melanie = plot_person_specific_events_2025(
        csv_path='2025DataCollection.csv',
        output_path_michael='2025_michael_activities_pie_charts.png',
        output_path_melanie='2025_melanie_activities_pie_charts.png'
    )

    print("\n" + "="*80)
    print("Pie Chart Summary")
    print("="*80)
    print("\nCombined events (same for both people):")
    print("  - Events: Laugh, Cry, Fight, Tender Moment, Spend Money")
    print("  - Exercise: Any Exercise, Cardio, Strength")
    print("  - Green = Yes, Red = No")
    print("  - Percentages shown (except Cry shows raw counts)")
    print("\nPerson-specific activities:")
    print("  - Activities: Reading, TV, Fruit/Veggie")
    print("  - Green = Yes, Red = No")
    print("  - All activities show percentages")
