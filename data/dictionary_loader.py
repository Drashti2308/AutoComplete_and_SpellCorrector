import csv
import os

WORDS_CSV_PATH = "words.csv"

_DICTIONARY = {}
_IS_LOADED = False


def load_dictionary(csv_path=WORDS_CSV_PATH):
    global _DICTIONARY, _IS_LOADED
    if _IS_LOADED:
        return _DICTIONARY

    _DICTIONARY = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = row.get("word")
            fq = row.get("frequency")
            if w and fq:
                try:
                    _DICTIONARY[w.strip().lower()] = int(fq)
                except ValueError:
                    continue

    _IS_LOADED = True
    return _DICTIONARY


def contains_word(word: str) -> bool:
    if not _IS_LOADED:
        load_dictionary()
    return word.strip().lower() in _DICTIONARY


def get_frequency(word: str) -> int:
    if not _IS_LOADED:
        load_dictionary()
    return _DICTIONARY.get(word.strip().lower(), 0)


def get_all_words():
    if not _IS_LOADED:
        load_dictionary()
    return _DICTIONARY.keys()


# Now call the functions:
data = load_dictionary()
print(f"Loaded {len(data):,} words.")

sample_tests = ["the", "apple", "hello", "aple", "xyzabc123"]
for w in sample_tests:
    print(
        f"word='{w:<10}' -> contains={contains_word(w)!s:<5} | frequency={get_frequency(w):,}"
    )