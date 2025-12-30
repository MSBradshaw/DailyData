"""
Analyze the association between events (laugh, cry, fight, tender moment, spend money)
and emotion scores for 2025 data.
"""

import pandas as pd
import numpy as np
from scipy import stats

def load_and_parse_2025_data(csv_path='2025DataCollection.csv'):
    """Load 2025 data and parse events."""
    df = pd.read_csv(csv_path)

    # Parse the "Did we ..." column to extract individual events
    # Events are semicolon-separated
    events_col = 'Did we ...'

    # Create binary columns for each event type
    df['had_laugh'] = df[events_col].fillna('').str.contains('laugh', case=False, regex=False)
    df['had_cry'] = df[events_col].fillna('').str.contains('cry', case=False, regex=False)
    df['had_fight'] = df[events_col].fillna('').str.contains('fight', case=False, regex=False)
    df['had_tender'] = df[events_col].fillna('').str.contains('tender', case=False, regex=False)
    df['had_spend_money'] = df[events_col].fillna('').str.contains('spend', case=False, regex=False)

    # Parse the "Exercise " column (note: has trailing space in column name)
    exercise_col = 'Exercise '
    df['exercise_raw'] = df[exercise_col].fillna('')

    # Create exercise binary columns
    df['had_any_exercise'] = df['exercise_raw'].str.strip() != ''
    df['had_cardio'] = df['exercise_raw'].str.contains('Cardio', case=False, regex=False)
    df['had_strength'] = df['exercise_raw'].str.contains('Strength', case=False, regex=False)

    # Parse reading and TV columns (person-specific)
    read_col = 'Did you read a book today?'
    tv_col = 'Did you watch TV today?'
    fruit_veg_col = 'Fruit / Vegetable Consumption'

    df['read_raw'] = df[read_col].fillna('')
    df['tv_raw'] = df[tv_col].fillna('')
    df['fruit_veg_raw'] = df[fruit_veg_col].fillna('')

    # Create person-specific binary columns
    # Reading
    df['michael_read'] = (df['read_raw'].str.contains('Michael', case=False) |
                          df['read_raw'].str.contains('Both Yes', case=False))
    df['melanie_read'] = (df['read_raw'].str.contains('Mel', case=False) |
                          df['read_raw'].str.contains('Both Yes', case=False))

    # TV
    df['michael_tv'] = (df['tv_raw'].str.contains('Michael', case=False) |
                        df['tv_raw'].str.contains('Both Yes', case=False))
    df['melanie_tv'] = (df['tv_raw'].str.contains('Mel', case=False) |
                        df['tv_raw'].str.contains('Both Yes', case=False))

    # Fruit/Vegetables
    df['michael_fruit_veg'] = df['fruit_veg_raw'].str.contains('Michael', case=False)
    df['melanie_fruit_veg'] = df['fruit_veg_raw'].str.contains('Melanie', case=False)

    # Parse Activities column
    activities_col = 'Activities'
    df['activities_raw'] = df[activities_col].fillna('')
    df['had_any_activity'] = df['activities_raw'].str.strip() != ''

    # Parse Social column (Family/Friends)
    social_col = 'Social'
    df['social_raw'] = df[social_col].fillna('')
    df['had_family_or_friends'] = df['social_raw'].str.strip() != ''
    df['had_family'] = df['social_raw'].str.contains('Family', case=False, regex=False)
    df['had_friends'] = df['social_raw'].str.contains('Friends', case=False, regex=False)

    # Parse Blood sugar reflection (1=bad, 2=medium, 3=good)
    blood_sugar_col = 'Blood sugar reflection'
    df['blood_sugar_numeric'] = pd.to_numeric(df[blood_sugar_col], errors='coerce')
    df['had_bad_blood_sugar'] = df['blood_sugar_numeric'] == 1
    df['had_medium_blood_sugar'] = df['blood_sugar_numeric'] == 2
    df['had_good_blood_sugar'] = df['blood_sugar_numeric'] == 3

    # Get emotion scores
    df['michael_emotion'] = pd.to_numeric(df['Emotion - Michael'], errors='coerce')
    df['melanie_emotion'] = pd.to_numeric(df['Emotion - Melanie'], errors='coerce')

    return df


def analyze_event_emotion_association(df, person_name, emotion_col, event_col, event_display_name):
    """
    Analyze association between an event and emotion scores.
    Uses Welch's t-test (doesn't assume equal variances) to handle imbalanced groups.

    Returns dict with: person, event, p_value, num_positive, num_negative,
                       avg_positive, avg_negative, effect_size, balance_ratio
    """
    # Filter to valid emotion scores
    valid_data = df[df[emotion_col].notna()].copy()

    # Split into event present vs absent
    has_event = valid_data[valid_data[event_col] == True][emotion_col]
    no_event = valid_data[valid_data[event_col] == False][emotion_col]

    # Calculate statistics
    num_positive = len(has_event)
    num_negative = len(no_event)
    avg_positive = has_event.mean() if num_positive > 0 else np.nan
    avg_negative = no_event.mean() if num_negative > 0 else np.nan
    std_positive = has_event.std() if num_positive > 0 else np.nan
    std_negative = no_event.std() if num_negative > 0 else np.nan

    # Calculate balance ratio (smaller/larger)
    if num_positive > 0 and num_negative > 0:
        balance_ratio = min(num_positive, num_negative) / max(num_positive, num_negative)
    else:
        balance_ratio = 0

    # Perform Welch's t-test (doesn't assume equal variances, better for imbalanced data)
    # Only if we have sufficient data in both groups (minimum 3 observations each)
    if num_positive >= 3 and num_negative >= 3:
        t_stat, p_value = stats.ttest_ind(has_event, no_event, equal_var=False)  # Welch's t-test
    else:
        p_value = np.nan

    # Calculate Cohen's d effect size (standardized mean difference)
    # Only if we have both groups
    if num_positive > 0 and num_negative > 0 and not (pd.isna(std_positive) or pd.isna(std_negative)):
        # Pooled standard deviation
        pooled_std = np.sqrt(((num_positive - 1) * std_positive**2 +
                              (num_negative - 1) * std_negative**2) /
                             (num_positive + num_negative - 2))
        if pooled_std > 0:
            cohens_d = (avg_positive - avg_negative) / pooled_std
        else:
            cohens_d = np.nan
    else:
        cohens_d = np.nan

    return {
        'Person': person_name,
        'Event': event_display_name,
        'p_value': p_value,
        'num_positive': num_positive,
        'num_negative': num_negative,
        'balance_ratio': balance_ratio,
        'avg_emotion_positive': avg_positive,
        'avg_emotion_negative': avg_negative,
        'difference': avg_positive - avg_negative if not (pd.isna(avg_positive) or pd.isna(avg_negative)) else np.nan,
        'cohens_d': cohens_d
    }


def main():
    print("Loading 2025 data...")
    df = load_and_parse_2025_data()

    print(f"Total entries: {len(df)}")
    print(f"Valid Michael emotions: {df['michael_emotion'].notna().sum()}")
    print(f"Valid Melanie emotions: {df['melanie_emotion'].notna().sum()}")

    # Define shared events (same for both people)
    shared_events = [
        ('had_laugh', 'Laugh'),
        ('had_cry', 'Cry'),
        ('had_fight', 'Fight'),
        ('had_tender', 'Tender Moment'),
        ('had_spend_money', 'Spend Money'),
        ('had_any_exercise', 'Any Exercise'),
        ('had_cardio', 'Cardio'),
        ('had_strength', 'Strength Training'),
        ('had_any_activity', 'Any Activity'),
        ('had_family_or_friends', 'Family or Friends'),
        ('had_family', 'Family'),
        ('had_friends', 'Friends'),
        ('had_bad_blood_sugar', 'Bad Blood Sugar'),
        ('had_medium_blood_sugar', 'Medium Blood Sugar'),
        ('had_good_blood_sugar', 'Good Blood Sugar')
    ]

    # Define person-specific events (different columns for each person)
    person_specific_events = [
        ('Read', 'michael_read', 'melanie_read'),
        ('Watch TV', 'michael_tv', 'melanie_tv'),
        ('Eat Fruit/Veg', 'michael_fruit_veg', 'melanie_fruit_veg')
    ]

    # Analyze for both people
    results = []

    # Analyze shared events
    for event_col, event_name in shared_events:
        # Michael
        result = analyze_event_emotion_association(
            df, 'Michael', 'michael_emotion', event_col, event_name
        )
        results.append(result)

        # Melanie
        result = analyze_event_emotion_association(
            df, 'Melanie', 'melanie_emotion', event_col, event_name
        )
        results.append(result)

    # Analyze person-specific events
    for event_name, michael_col, melanie_col in person_specific_events:
        # Michael
        result = analyze_event_emotion_association(
            df, 'Michael', 'michael_emotion', michael_col, event_name
        )
        results.append(result)

        # Melanie
        result = analyze_event_emotion_association(
            df, 'Melanie', 'melanie_emotion', melanie_col, event_name
        )
        results.append(result)

    # Create DataFrame
    results_df = pd.DataFrame(results)

    # Calculate Bonferroni correction
    # Number of comparisons = number of valid tests (non-null p-values)
    num_comparisons = results_df['p_value'].notna().sum()
    bonferroni_threshold = 0.05 / num_comparisons if num_comparisons > 0 else 0.05

    # Add Bonferroni significance column
    results_df['significant_bonferroni'] = results_df['p_value'] < bonferroni_threshold

    # Format p-values properly
    # Note: p=0.0 means p-value is extremely small (< 0.0001), not null or error
    # We'll keep more precision and use scientific notation for very small values
    def format_pvalue(p):
        if pd.isna(p):
            return 'N/A'  # Null/missing
        elif p < 0.0001:
            return f'{p:.2e}'  # Scientific notation for very small p-values
        else:
            return f'{p:.4f}'

    results_df['p_value_formatted'] = results_df['p_value'].apply(format_pvalue)

    # Round other numeric columns
    results_df['balance_ratio'] = results_df['balance_ratio'].round(2)
    results_df['avg_emotion_positive'] = results_df['avg_emotion_positive'].round(2)
    results_df['avg_emotion_negative'] = results_df['avg_emotion_negative'].round(2)
    results_df['difference'] = results_df['difference'].round(2)
    results_df['cohens_d'] = results_df['cohens_d'].round(2)

    # Sort by event then person
    results_df = results_df.sort_values(['Event', 'Person'])

    # Create output dataframe with formatted p-value and Bonferroni significance
    output_df = results_df[['Person', 'Event', 'p_value_formatted', 'significant_bonferroni',
                            'num_positive', 'num_negative', 'balance_ratio',
                            'avg_emotion_positive', 'avg_emotion_negative',
                            'difference', 'cohens_d']].copy()
    output_df.columns = ['Person', 'Event', 'p_value', 'significant_bonferroni',
                        'num_positive', 'num_negative', 'balance_ratio',
                        'avg_emotion_positive', 'avg_emotion_negative', 'difference', 'cohens_d']

    # Save to CSV
    output_file = '2025_emotion_event_analysis.csv'
    output_df.to_csv(output_file, index=False)
    print(f"✓ Analysis saved to: {output_file}")

    # Print summary statistics
    print(f"\nAnalyzed {len(df)} days of data")
    print(f"Shared events analyzed: {len(shared_events)}")
    print(f"Person-specific events analyzed: {len(person_specific_events)}")
    print(f"Total comparisons: {num_comparisons}")
    print(f"\nUsing Welch's t-test (robust to unequal variances)")
    print(f"Minimum sample size per group: 3")
    print(f"Reporting Cohen's d effect size and balance ratio")
    print(f"Bonferroni correction threshold: p < {bonferroni_threshold:.4f} (= 0.05 / {num_comparisons})")

    # Count significant results (uncorrected)
    sig_count = (results_df['p_value'] < 0.05).sum()
    sig_bonferroni_count = results_df['significant_bonferroni'].sum()

    print(f"\nSignificant associations (uncorrected p < 0.05): {sig_count}")
    print(f"Significant associations (Bonferroni corrected): {sig_bonferroni_count}")

    if sig_bonferroni_count > 0:
        print("\n" + "="*80)
        print("BONFERRONI-CORRECTED SIGNIFICANT FINDINGS:")
        print("="*80)
        sig_results = results_df[results_df['significant_bonferroni']][['Person', 'Event', 'p_value', 'difference', 'cohens_d', 'balance_ratio']]
        for _, row in sig_results.iterrows():
            direction = "higher" if row['difference'] > 0 else "lower"
            effect_size = abs(row['cohens_d']) if not pd.isna(row['cohens_d']) else 0
            effect_desc = "small" if effect_size < 0.5 else ("medium" if effect_size < 0.8 else "large")
            print(f"  {row['Person']}: {row['Event']} → {direction} emotion")
            print(f"    p={row['p_value']:.4f}, Δ={row['difference']:.2f}, Cohen's d={row['cohens_d']:.2f} ({effect_desc}), balance={row['balance_ratio']:.2f}")

    # Also show uncorrected significant results if different
    if sig_count > sig_bonferroni_count:
        print("\n" + "="*80)
        print(f"NOMINALLY SIGNIFICANT (p < 0.05) BUT NOT AFTER BONFERRONI:")
        print("="*80)
        nominal_sig = results_df[(results_df['p_value'] < 0.05) & (~results_df['significant_bonferroni'])]
        for _, row in nominal_sig.iterrows():
            direction = "higher" if row['difference'] > 0 else "lower"
            print(f"  {row['Person']}: {row['Event']} → {direction} emotion (p={row['p_value']:.4f})")

    return results_df


if __name__ == "__main__":
    results = main()
