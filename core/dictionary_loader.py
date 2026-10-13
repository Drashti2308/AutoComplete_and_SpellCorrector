import csv
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICTIONARY_FILE = os.path.join(PROJECT_DIR, "data", "words.csv")


def load_dictionary(file_path=DICTIONARY_FILE):
    """
    Load words and their frequencies from words.csv.

    Returns:
        list of tuples: [(word, frequency), ...]
    """
    dictionary = []

    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {"word", "frequency"}

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "Dictionary CSV must contain 'word' and 'frequency' columns."
            )

        for row in reader:
            word = (row.get("word") or "").strip()
            frequency_text = (row.get("frequency") or "").strip()

            if not word:
                continue

            try:
                frequency = int(frequency_text)
            except ValueError:
                continue

            if frequency < 0:
                continue

            dictionary.append((word, frequency))

    return dictionary


if __name__ == "__main__":
    words = load_dictionary()

    print(f"Total words loaded: {len(words)}")
    print("First five entries:")

    for word, frequency in words[:5]:
        print(f"{word}: {frequency}")