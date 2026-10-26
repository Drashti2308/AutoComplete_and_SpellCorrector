
from core.edit_distance import levenshtein_distance


class SpellCorrector:
    def __init__(self, dictionary, max_distance=2):
        self.max_distance = max_distance
        self.words_by_length = {}
        self.word_frequencies = {}

        # Load words and retain the highest frequency for duplicates
        for word, frequency in dictionary:
            word = word.strip().lower()

            if not word or not word.isascii() or not word.isalpha():
                continue

            self.word_frequencies[word] = max(
                frequency,
                self.word_frequencies.get(word, 0)
            )

        # Group words by length to reduce candidate searches
        for word, frequency in self.word_frequencies.items():
            self.words_by_length.setdefault(len(word), []).append(
                (word, frequency)
            )

    @staticmethod
    def _common_prefix(word, candidate):
        count = 0

        for char1, char2 in zip(word, candidate):
            if char1 != char2:
                break
            count += 1

        return count

    @staticmethod
    def _character_similarity(word, candidate):
        """
        Measure how well the input's characters align with a candidate.
        Returns a value between 0 and 1.
        """
        if not word or not candidate:
            return 0.0

        # Longest common subsequence using dynamic programming
        previous = [0] * (len(candidate) + 1)

        for char1 in word:
            current = [0] * (len(candidate) + 1)

            for j, char2 in enumerate(candidate, start=1):
                if char1 == char2:
                    current[j] = previous[j - 1] + 1
                else:
                    current[j] = max(
                        previous[j],
                        current[j - 1]
                    )

            previous = current

        common_length = previous[-1]

        return common_length / max(len(word), len(candidate))

    def correct(self, word, limit=5):
        if not isinstance(word, str):
            return []

        word = word.strip().lower()

        if not word or not word.isascii() or not word.isalpha():
            return []

        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            return []

        # Return an already-correct word immediately
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

                common_prefix = self._common_prefix(word, candidate)

                similarity = self._character_similarity(word, candidate)

                length_difference = abs(len(word) - len(candidate))

                candidates.append(
                    (
                        candidate,
                        distance,
                        common_prefix,
                        similarity,
                        length_difference,
                        frequency
                    )
                )

        # Rank by edit distance first, then character similarity,
        # common prefix, length difference, frequency, and alphabetically.
        candidates.sort(
            key=lambda item: (
                item[1],
                -item[3],
                -item[2],
                item[4],
                -item[5],
                item[0]
            )
        )

        return [
            candidate
            for candidate, distance, common_prefix,
            similarity, length_difference, frequency
            in candidates[:limit]
        ]

