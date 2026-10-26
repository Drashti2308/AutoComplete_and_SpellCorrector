
from core.dictionary_loader import load_dictionary
from core.spell_corrector import SpellCorrector
from core.edit_distance import levenshtein_distance


def main():
    dictionary = load_dictionary()
    corrector = SpellCorrector(dictionary, max_distance=1)

    word = "helo"
    candidates_to_check = [
        "hello",
        "helot",
        "held",
        "help",
        "hell",
        "helm",
    ]

    print("Input:", word)
    print("\nCandidate comparison:")

    for candidate in candidates_to_check:
        frequency = corrector.word_frequencies.get(candidate, 0)
        distance = levenshtein_distance(word, candidate)

        print(
            f"{candidate:8} "
            f"distance={distance} "
            f"frequency={frequency}"
        )

    print("\nTop 5 suggestions:", corrector.correct(word, 5))


if __name__ == "__main__":
    main()
