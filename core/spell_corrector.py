from core.edit_distance import levenshtein_distance


class SpellCorrector:

    def __init__(self, dictionary, max_distance=2, trie=None):

        self.max_distance = max_distance
        self.trie = trie

        self.words_by_length = {}
        self.word_frequencies = {}

        # Load dictionary and retain highest frequency.
        for word, frequency in dictionary:

            word = word.strip().lower()

            if not word or not word.isascii() or not word.isalpha():
                continue

            self.word_frequencies[word] = max(
                frequency,
                self.word_frequencies.get(word, 0)
            )

        # Group words by length for fallback search.
        for word, frequency in self.word_frequencies.items():

            self.words_by_length.setdefault(
                len(word), []
            ).append((word, frequency))

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

        if not word or not candidate:
            return 0.0

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

    def _trie_search(self, word):

        """
        Find words within the maximum edit distance
        using Trie traversal and incremental DP.
        """

        results = []

        initial_row = list(range(len(word) + 1))

        def search(node, current_word, previous_row):

            for character, child in node.children.items():

                current_word += character

                current_row = [previous_row[0] + 1]

                for column in range(1, len(word) + 1):

                    insert_cost = current_row[column - 1] + 1

                    delete_cost = previous_row[column] + 1

                    replace_cost = (
                        previous_row[column - 1]
                        + (word[column - 1] != character)
                    )

                    current_row.append(
                        min(
                            insert_cost,
                            delete_cost,
                            replace_cost
                        )
                    )

                # Prune branches that cannot produce valid words.
                if min(current_row) <= self.max_distance:

                    if (
                        child.is_end_of_word
                        and current_row[-1] <= self.max_distance
                    ):

                        results.append((
                            current_word,
                            current_row[-1],
                            child.frequency
                        ))

                    search(
                        child,
                        current_word,
                        current_row
                    )

                current_word = current_word[:-1]

        search(
            self.trie.root,
            "",
            initial_row
        )

        return results

    def _dictionary_search(self, word):

        """
        Fallback implementation for tests or cases
        where a Trie has not been provided.
        """

        results = []

        min_length = max(
            1,
            len(word) - self.max_distance
        )

        max_length = len(word) + self.max_distance

        for length in range(min_length, max_length + 1):

            for candidate, frequency in self.words_by_length.get(
                length, []
            ):

                distance = levenshtein_distance(
                    word,
                    candidate,
                    max_distance=self.max_distance
                )

                if distance <= self.max_distance:

                    results.append((
                        candidate,
                        distance,
                        frequency
                    ))

        return results

    def correct(self, word, limit=5):

        if not isinstance(word, str):
            return []

        word = word.strip().lower()

        if not word or not word.isascii() or not word.isalpha():
            return []

        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or limit <= 0
        ):
            return []

        # Return an already-correct word immediately.
        if word in self.word_frequencies:
            return [word]

        # Select candidate-search method.
        if self.trie is not None:

            candidates = self._trie_search(word)

        else:

            candidates = self._dictionary_search(word)

        ranked_candidates = []

        for candidate, distance, frequency in candidates:

            common_prefix = self._common_prefix(
                word,
                candidate
            )

            similarity = self._character_similarity(
                word,
                candidate
            )

            length_difference = abs(
                len(word) - len(candidate)
            )

            ranked_candidates.append((
                candidate,
                distance,
                common_prefix,
                similarity,
                length_difference,
                frequency
            ))

        # Preserve the existing ranking strategy.
        ranked_candidates.sort(
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
            in ranked_candidates[:limit]
        ]