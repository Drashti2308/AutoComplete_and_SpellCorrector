from core.trie_node import TrieNode


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=0):
        if not isinstance(word, str):
            raise TypeError("Word must be a string.")

        word = word.strip().lower()

        if not word or not word.isascii() or not word.isalpha():
            return

        current = self.root

        for character in word:
            if character not in current.children:
                current.children[character] = TrieNode()

            current = current.children[character]

        current.is_end_of_word = True
        current.frequency = frequency

    def search(self, word):
        if not isinstance(word, str):
            return False

        word = word.strip().lower()

        if not word or not word.isascii() or not word.isalpha():
            return False

        current = self.root

        for character in word:
            if character not in current.children:
                return False

            current = current.children[character]

        return current.is_end_of_word

    def starts_with(self, prefix):
        if not isinstance(prefix, str):
            return False

        prefix = prefix.strip().lower()

        if not prefix or not prefix.isascii() or not prefix.isalpha():
            return False

        current = self.root

        for character in prefix:
            if character not in current.children:
                return False

            current = current.children[character]

        return True