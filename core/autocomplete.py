from core.trie import Trie
from core.trie_node import TrieNode


class Autocomplete:
    def __init__(self, trie):
        self.trie = trie

    def get_suggestions(self, prefix, limit=5):
        if not isinstance(prefix, str):
            return []

        prefix = prefix.strip().lower()

        if not prefix or not prefix.isascii() or not prefix.isalpha():
            return []

        if limit <= 0:
            return []

        current = self.trie.root

        # Find the node representing the prefix
        for character in prefix:
            if character not in current.children:
                return []

            current = current.children[character]

        # Collect complete words from this subtree
        matches = []
        self._collect_words(current, prefix, matches)

        # Rank by frequency (highest first), then alphabetically
        matches.sort(key=lambda item: (-item[1], item[0]))

        return [word for word, frequency in matches[:limit]]

    def _collect_words(self, node, current_word, matches):
        if node.is_end_of_word:
            matches.append((current_word, node.frequency))

        for character, child_node in node.children.items():
            self._collect_words(
                child_node,
                current_word + character,
                matches
            )