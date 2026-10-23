from core.dictionary_loader import load_dictionary
from core.spell_corrector import SpellCorrector


def test_dictionary_spell_corrector():
    print("Loading dictionary...")

    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words.")

    print("Preparing spell corrector...")
    corrector = SpellCorrector(dictionary, max_distance=2)

    test_words = ["aple", "bananna", "computr", "helo"]

    for word in test_words:
        print(f"\nInput: {word}")

        suggestions = corrector.correct(word, limit=5)

        print("Suggestions:", suggestions)

        assert isinstance(suggestions, list)
        assert len(suggestions) <= 5

        for suggestion in suggestions:
            assert suggestion.isalpha()
            assert suggestion.islower()

    print("\nFull-dictionary spell correction test passed!")


if __name__ == "__main__":
    test_dictionary_spell_corrector()