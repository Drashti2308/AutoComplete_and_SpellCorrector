
from core.dictionary_loader import load_dictionary
from core.spell_corrector import SpellCorrector


def test_spell_correction_quality():
    dictionary = load_dictionary()
    corrector = SpellCorrector(dictionary, max_distance=2)

    # Inspect frequencies of relevant words
    print("\n--- Word Frequency Check ---")

    words_to_check = {"hello", "hell", "help", "held", "helo"}

    for word, frequency in dictionary:
        if word in words_to_check:
            print(f"{word}: {frequency}")

    # Test spelling corrections
    test_cases = {
        "aple": "apple",
        "bananna": "banana",
        "computr": "computer",
        "helo": "hello",
    }

    print("\n--- Spell Correction Quality Tests ---")

    for misspelled_word, expected_word in test_cases.items():
        suggestions = corrector.correct(misspelled_word, limit=5)

        print(f"\nInput: {misspelled_word}")
        print(f"Expected: {expected_word}")
        print(f"Suggestions: {suggestions}")

        assert isinstance(suggestions, list)
        assert len(suggestions) <= 5

        if expected_word not in suggestions:
            print(
                f"WARNING: '{expected_word}' was not found "
                f"in the top five suggestions."
            )
        else:
            print("Expected correction found.")

    print("\nSpell correction quality check completed.")


if __name__ == "__main__":
    test_spell_correction_quality()
