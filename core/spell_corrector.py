
from core.edit_distance import levenshtein_distance


class SpellCorrector:
    def __init__(self, dictionary, max_distance=2):
        self.max_distance = max_distance
        self.words_by_length = {}
        self.word_frequencies = {}

        for word, frequency in dictionary:
            word = word.strip().lower()

            if not word or not word.isascii() or not word.isalpha():
                continue

            self.word_frequencies[word] = max(
                frequency,
                self.word_frequencies.get(word, 0)
            )

        for word, frequency in self.word_frequencies.items():
            self.words_by_length.setdefault(len(word), []).append(
                (word, frequency)
            )

    def correct(self, word, limit=5):
        if not isinstance(word, str):
            return []

        word = word.strip().lower()

        if not word or not word.isascii() or not word.isalpha():
            return []

        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            return []

        if word in self.word_frequencies:
            return [word]

        candidates = []

        min_length = max(1, len(word) - self.max_distance)
        max_length = len(word) + self.max_distance

        for length in range(min_length, max_length + 1):
            for candidate, frequency in self.words_by_length.get(length, []):
                distance = levenshtein_distance(word, candidate)

                if distance > self.max_distance:
                    continue

                common_prefix = 0
                for a, b in zip(word, candidate):
                    if a != b:
                        break
                    common_prefix += 1

                positional_mismatches = sum(
                    1 for a, b in zip(word, candidate) if a != b
                )

                # Prefer candidates whose characters align well
                # with the misspelled input.
                length_difference = abs(len(word) - len(candidate))

                candidates.append(
                    (
                        candidate,
                        distance,
                        common_prefix,
                        positional_mismatches,
                        length_difference,
                        frequency,
                    )
                )

        candidates.sort(
            key=lambda item: (
                 item[1],   # Lowest edit distance
                -item[2],  # Longest common prefix
                item[3],   # Fewest positional mismatches
                item[4],   # Smallest length difference
                -item[5],  # Highest frequency
                item[0]    # Alphabetical tie-breaker
            )
        )

        return [
            item[0] for item in candidates[:limit]
        ]

