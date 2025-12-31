"""
Generate word cloud data files for 2025 best/worst parts of the day.
"""

from plotting_utils.wordcloud_processing import export_wordcloud_words
import pandas as pd

if __name__ == "__main__":
    print("="*80)
    print("Generating 2025 Word Cloud Data")
    print("="*80)

    # Load data
    df = pd.read_csv('2025DataCollection.csv')

    # Extract columns
    best_col = 'Best part of the day'
    worst_col = 'Worst part of the day'

    # Custom word replacements (cat names and other personal terms)
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
    best_texts = df[best_col].dropna()
    best_count = export_wordcloud_words(
        best_texts,
        output_path='2025_best_part_wordcloud.txt',
        use_tildes=True,
        custom_replacements=custom_replacements
    )

    # Export word cloud data for worst parts
    print("\nProcessing 'Worst part of the day'...")
    worst_texts = df[worst_col].dropna()
    worst_count = export_wordcloud_words(
        worst_texts,
        output_path='2025_worst_part_wordcloud.txt',
        use_tildes=True,
        custom_replacements=custom_replacements
    )

    print("\n" + "="*80)
    print("Word Cloud Summary")
    print("="*80)
    print(f"\nBest part of the day: {best_count} words")
    print(f"  Output: 2025_best_part_wordcloud.txt")
    print(f"\nWorst part of the day: {worst_count} words")
    print(f"  Output: 2025_worst_part_wordcloud.txt")
    print("\nNote: Bigrams use tildes (~) instead of spaces")
    print("      Use these files with wordcloud.com or similar tools")
