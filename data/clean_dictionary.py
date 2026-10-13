import csv
import os

# Get the data folder path
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Input and output file paths
INPUT_FILE = os.path.join(DATA_DIR, "valid_words_sorted_by_frequency.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "words.csv")


def clean_dictionary():
    total_rows = 0
    valid_rows = 0
    seen_words = set()

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile)

        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as outfile:
            writer = csv.writer(outfile)

            # Write the output column names
            writer.writerow(["word", "frequency"])

            for row in reader:
                total_rows += 1

                word = (row.get("Word") or "").strip().lower()
                frequency_text = (row.get("Frequency count") or "").strip()

                # Skip empty words
                if not word:
                    continue

                # Keep alphabetic English words only
                if not word.isascii() or not word.isalpha():
                    continue

                # Skip invalid frequency values
                try:
                    frequency = int(frequency_text)
                except ValueError:
                    continue

                if frequency < 0:
                    continue

                # Skip duplicate words
                if word in seen_words:
                    continue

                seen_words.add(word)

                writer.writerow([word, frequency])
                valid_rows += 1

    print("Dictionary cleaning completed!")
    print(f"Total rows processed: {total_rows}")
    print(f"Valid unique words saved: {valid_rows}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_dictionary()