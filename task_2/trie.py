class TrieNode:
    """A node in the trie structure."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.value = None

class Trie:
    """Trie data structure."""
    def __init__(self):
        """Initializes the Trie with a root node."""
        self.root = TrieNode()

    def put(self, key: str, value):
        """
        Inserts a key-value pair into the Trie.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.value = value

    def _find_node(self, prefix: str):
        """
        Finds the node corresponding to a given prefix.
        Returns the node if found, otherwise None.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node