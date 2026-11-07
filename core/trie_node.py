"""This file defines the basic building block of the Trie data structure. 
Each node stores its child characters, indicates whether a complete word ends at that node, 
and maintains the frequency of the word."""
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0