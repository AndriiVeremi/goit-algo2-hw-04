# Homework #4: Algorithms on Graphs and Data Structures

This repository contains solutions for two assignments from the 'Algorithms and Data Structures' course.

---

## How to Run

All tasks are run via the main script `main.py`, which provides an interactive menu.

**To run the program, execute the command:**
```bash
python3 main.py
```
Then, enter the task number (`1` or `2`) you want to check and press Enter.

---

## Task 1: Applying the Maximum Flow Algorithm for Logistics

### Task Description

A program was developed to model a logistics network consisting of terminals, warehouses, and shops. The goal was to find the maximum flow of goods from the starting points (terminals) to the endpoints (shops) using the Edmonds-Karp algorithm.

### Implementation

- **Graph:** The network is modeled as a directed graph. For the algorithm to work, which requires a single source and a single sink, a 'super-source' was added connecting to all terminals, and a 'super-sink' to which all shops lead.
- **Algorithm:** The Edmonds-Karp algorithm is implemented, which iteratively finds augmenting paths in the residual network using a Breadth-First Search (BFS).
- **Analysis:** The script not only calculates the maximum flow but also analyzes the results:
    - Calculates the flow from each terminal to each shop.
    - Identifies 'bottlenecks' — fully saturated routes.
    - Finds routes with the lowest capacity.

---

## Task 2: Extending Trie Functionality

### Task Description

The task was to extend the base `Trie` class by adding two methods:
1.  `has_prefix(prefix)` — checks if there are any words in the trie with the given prefix.
2.  `count_words_with_suffix(suffix)` — counts the number of words ending with a given suffix.

### Implementation

- **`has_prefix`:** This method is implemented using the standard approach for a trie. It simply traverses the trie nodes following the characters of the prefix. If the entire path exists, the method returns `True`.

- **`count_words_with_suffix`:** Searching by suffix is inefficient in a standard trie. To solve this problem effectively, the following approach was used:
    1.  A **second, reversed trie** (`rev_root`) was created.
    2.  When adding a new word to the main trie, its reversed version is added to the reversed trie.
    3.  To search for a suffix `s`, we simply search for the **prefix** `reversed(s)` in the reversed trie.
    4.  After finding the node corresponding to the reversed suffix, we recursively count all terminal words in its subtree.

This approach is significantly more efficient than iterating through all the words in the trie.

---

