from trie import Trie, TrieNode

class Homework(Trie):
    def __init__(self):
        super().__init__()
        # Additional trie for reversed words
        self.rev_root = TrieNode()

    def put(self, key, value):
        # Add word to the normal trie
        super().put(key, value)

        # And now add the reversed word to our second trie
        if not isinstance(key, str):
            return # Base class will raise the error itself

        node = self.rev_root
        for char in reversed(key):
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def has_prefix(self, prefix):
        # Check if words with this prefix exist
        if not isinstance(prefix, str):
            print(f"Error: prefix must be a string, not {type(prefix)}")
            return False

        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    # Helper function to count words
    def _count_sub_words(self, node):
        if not node:
            return 0
        
        # Count the current word if it ends here
        count = 1 if node.is_end_of_word else 0
        
        # and add all words from child nodes
        for child in node.children.values():
            count += self._count_sub_words(child)
            
        return count

    def count_words_with_suffix(self, suffix):
        # Count words with a specific suffix
        if not isinstance(suffix, str):
            print(f"Error: suffix must be a string, not {type(suffix)}")
            return 0
        
        if not suffix:
            return 0

        # Search for the reversed suffix in the reversed trie
        node = self.rev_root
        for char in reversed(suffix):
            if char not in node.children:
                return 0 # No such path
            node = node.children[char]
        
        # If found, count all words starting from this node
        return self._count_sub_words(node)

# --- Tests --- 
if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Check the number of words ending with a given suffix
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat
    assert trie.count_words_with_suffix("n") == 1 # application
    assert trie.count_words_with_suffix("xyz") == 0

    # Check for prefix existence
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat

    print("All tests passed successfully!")

    # Check error handling
    print("\nChecking error handling:")
    trie.count_words_with_suffix(123)
    trie.has_prefix(None)
