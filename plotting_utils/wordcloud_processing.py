"""
Text processing utilities for word cloud generation.

This module provides NLP processing functions to extract meaningful words
and phrases from free-text responses for word cloud visualization.
"""

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from collections import Counter
import re
import string


def ensure_nltk_data():
    """Download required NLTK data if not already present."""
    required_packages = [
        'punkt',
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords',
        'punkt_tab',
        'averaged_perceptron_tagger_eng'
    ]

    for package in required_packages:
        try:
            nltk.download(package, quiet=True)
        except:
            pass


def get_wordnet_pos(treebank_tag):
    """
    Convert Penn Treebank POS tags to WordNet POS tags.

    Args:
        treebank_tag: Penn Treebank POS tag

    Returns:
        str: WordNet POS tag
    """
    if treebank_tag.startswith('J'):
        return 'a'  # adjective
    elif treebank_tag.startswith('V'):
        return 'v'  # verb
    elif treebank_tag.startswith('N'):
        return 'n'  # noun
    elif treebank_tag.startswith('R'):
        return 'r'  # adverb
    else:
        return 'n'  # default to noun


def process_text(texts, custom_replacements=None, custom_stops=None):
    """
    Process a list of texts to extract and clean 1-grams and meaningful 2-grams.

    Args:
        texts: List of strings containing text entries
        custom_replacements: Dictionary of word replacements (optional)
        custom_stops: Set of additional stop words (optional)

    Returns:
        tuple: (Counter of 1-grams, Counter of bigrams, list of all words)
    """
    # Ensure NLTK data is available
    ensure_nltk_data()

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # Default custom stop words
    default_stops = {'day', 'today', 'got', 'went', 'had', 'made', 'really', 'get'}
    if custom_stops:
        stop_words.update(custom_stops)
    else:
        stop_words.update(default_stops)

    # Default custom replacements
    default_replacements = {
        r'mel\b': 'melanie',
        r'feeling|felt': 'feel',
        r'cats|cat|kitty|kittens|kitties': 'cat',
        r'cuddle|snuggle': 'cuddle',
        r'sexy|sex': 'sex',
        r'skiing|ski': 'ski',
        r'swimming|swim': 'swim'
    }

    replacements = custom_replacements if custom_replacements else default_replacements

    unigrams = []
    verb_noun_bigrams = []

    for text in texts:
        if pd.isna(text):
            continue

        # Convert to lowercase and remove possessives
        text = text.lower()
        text = re.sub(r"'s\b", "", text)

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Tokenize
        tokens = word_tokenize(text)

        # Apply custom replacements
        for pattern, replacement in replacements.items():
            tokens = [re.sub(pattern, replacement, token) for token in tokens]

        # POS tagging
        pos_tags = pos_tag(tokens)

        # Process unigrams
        cleaned_tokens = []
        for word, tag in pos_tags:
            # Skip stop words and short words
            if word in stop_words or len(word) < 3:
                continue

            # Lemmatize based on POS tag
            if tag.startswith('V'):
                lemma = lemmatizer.lemmatize(word, pos='v')
            elif tag.startswith('N'):
                lemma = lemmatizer.lemmatize(word, pos='n')
            elif tag.startswith('R'):
                lemma = lemmatizer.lemmatize(word, pos='r')
            else:
                lemma = lemmatizer.lemmatize(word)

            cleaned_tokens.append(lemma)

        unigrams.extend(cleaned_tokens)

        # Extract meaningful bigrams (verb-noun and adjective-noun)
        combos = [('V', 'N'), ('J', 'N')]

        for i in range(len(pos_tags) - 1):
            word1, tag1 = pos_tags[i]
            word2, tag2 = pos_tags[i + 1]

            for pair in combos:
                if tag1.startswith(pair[0]) and tag2.startswith(pair[1]):
                    # Lemmatize both words
                    word1_lemma = lemmatizer.lemmatize(
                        word1.lower(),
                        pos=get_wordnet_pos(pair[0].lower())
                    )
                    word2_lemma = lemmatizer.lemmatize(
                        word2.lower(),
                        pos=get_wordnet_pos(pair[1].lower())
                    )

                    verb_noun_bigrams.append(f"{word1_lemma} {word2_lemma}")

    all_words = unigrams + verb_noun_bigrams
    return Counter(unigrams), Counter(verb_noun_bigrams), all_words


def get_wordcloud_data(texts, min_freq=2, custom_replacements=None, custom_stops=None):
    """
    Process texts and return data suitable for word cloud visualization.

    Args:
        texts: List of text entries
        min_freq: Minimum frequency threshold for words (default: 2)
        custom_replacements: Dictionary of word replacements (optional)
        custom_stops: Set of additional stop words (optional)

    Returns:
        tuple: (word_freq dict, all_words list)
    """
    unigrams, bigrams, all_words = process_text(texts, custom_replacements, custom_stops)

    # Combine and filter by minimum frequency
    word_freq = {
        word: freq
        for word, freq in {**unigrams, **bigrams}.items()
        if freq >= min_freq
    }

    return word_freq, all_words


def export_wordcloud_words(texts, output_path, use_tildes=True,
                          custom_replacements=None, custom_stops=None):
    """
    Process texts and export all words to a file for word cloud generation.

    Args:
        texts: List of text entries
        output_path: Path to output text file
        use_tildes: Replace spaces with tildes in bigrams (default: True)
        custom_replacements: Dictionary of word replacements (optional)
        custom_stops: Set of additional stop words (optional)

    Returns:
        int: Number of words written
    """
    _, all_words = get_wordcloud_data(texts, min_freq=1,
                                      custom_replacements=custom_replacements,
                                      custom_stops=custom_stops)

    with open(output_path, 'w') as f:
        for word in all_words:
            if use_tildes:
                word = word.replace(' ', '~')
            f.write(f"{word}\n")

    print(f'Wrote {len(all_words)} words to: {output_path}')
    return len(all_words)


def process_best_worst_parts(csv_path, best_col='Best part of the day',
                             worst_col='Worst part of the day',
                             output_best_csv=None, output_worst_csv=None,
                             output_best_words=None, output_worst_words=None):
    """
    Complete workflow to process best/worst parts of day from CSV.

    Args:
        csv_path: Path to CSV file
        best_col: Column name for best part of day (default: 'Best part of the day')
        worst_col: Column name for worst part of day (default: 'Worst part of the day')
        output_best_csv: Optional path to save best parts CSV
        output_worst_csv: Optional path to save worst parts CSV
        output_best_words: Optional path to save best words for word cloud
        output_worst_words: Optional path to save worst words for word cloud

    Returns:
        tuple: (best_word_freq, worst_word_freq)
    """
    # Load data
    df = pd.read_csv(csv_path)

    # Export CSVs if requested
    if output_best_csv:
        df[best_col].to_csv(output_best_csv, index=False)
        print(f'Saved best parts to: {output_best_csv}')

    if output_worst_csv:
        df[worst_col].to_csv(output_worst_csv, index=False)
        print(f'Saved worst parts to: {output_worst_csv}')

    # Process texts
    best_freq, best_words = get_wordcloud_data(df[best_col].dropna())
    worst_freq, worst_words = get_wordcloud_data(df[worst_col].dropna())

    # Export word files if requested
    if output_best_words:
        export_wordcloud_words(df[best_col].dropna(), output_best_words)

    if output_worst_words:
        export_wordcloud_words(df[worst_col].dropna(), output_worst_words)

    return best_freq, worst_freq


def print_top_words(word_freq, n=50):
    """
    Print top N words and their frequencies.

    Args:
        word_freq: Dictionary of word frequencies
        n: Number of top words to print (default: 50)
    """
    print(f"\nTop {n} words:")
    for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:n]:
        print(f"{word}: {freq}")
