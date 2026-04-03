# Data Structure & Advanced Algorithm Visualizer

A comprehensive, interactive Data Structure and Algorithm Visualizer desktop application designed to illustrate algorithmic mechanics conceptually and visually for all technical levels.

## Run Instructions
1. Ensure you have Python 3 installed.
2. Install the GUI dependency:
   ```bash
   pip install customtkinter
   ```
3. Run the main application file from this directory:
   ```bash
   python main.py
   ```

## Included Data Structures & Visualizations

### 1. Fundamental Structures
- **Stack & Queue**: Visualize sliding bounds and memory shifts seamlessly (`Push`/`Pop`, `Enqueue`/`Dequeue`).
- **Singly Linked List**: Observe pointer rewiring and nodes shifting smoothly on inserts and deletes.
- **Binary Search Tree (BST)**: Generate, delete, search, and traverse standard binary trees to learn hierarchical data logic.
- **Binary Heap**: Synchronized **Array** and **Tree** views. Watch nodes miraculously swap across both representations during `heapify` routines.
- **AVL Tree**: Dynamic self-balancing tree showing Left-Left, Right-Right, Left-Right, and Right-Left structural rotations occurring step-by-step.

### 2. Searching & Sorting (Array Visuals)
- **Sorting Algorithms**: Visualizes arrays as dynamic bar charts. Watch comparisons (Red bars) and swaps (Yellow bars) dynamically restructure your dataset until finalized (Green).
  - Bubble Sort, Insertion Sort, Quick Sort, Merge Sort.
- **Searching Algorithms**: Tracks pointer positions across continuous data blocks.
  - Linear Search, Binary Search (dynamically resizes the `Left`, `Right`, and `Mid` query windows).

### 3. Advanced Graph Theory
Create robust graphs with **Weighted Edges** to execute advanced traversals and pathfinding. Includes:
- **Shortest Paths**: 
  - Dijkstra’s Algorithm
  - Bellman-Ford
- **Minimum Spanning Tree (MST)**:
  - Prim's Algorithm
  - Kruskal's Algorithm
- **Traversals**: Detailed Breadth-First Search (BFS) and Depth-First Search (DFS).

### 4. Dynamic Programming & Greedy Approach
- **Knapsack Variations**: 
  - **Fractional (Greedy)**: See items sorted by Value-to-Weight ratio and perfectly sliced fractionally into the capacity bag. 
  - **0/1 Knapsack (DP)**: Watch the classic DP 2D-Matrix Tabulation grid algorithmically populate step-by-step.
- **Longest Common Subsequence (LCS)**: View 2D grid matrix mapping string combinations to backtrack the optimal subset paths!

## Premium Desktop Aesthetic
This application runs under a modern, highly contrasted **Dark Theme**.
Vibrant visualization colors (`#10B981` Emerald, `#6366F1` Indigo, `#EC4899` Pink, `#F59E0B` Amber) pop distinctly off the glass-paneled backgrounds. This ensures that animations are not just educational, but profoundly appealing to the eye and perfect for technical demonstrations.

## Technical Architecture
To prevent the Tkinter `mainloop` from freezing during nested algorithmic loops, this application adheres to a strong Model-View separation powered by Python **Generators** (`yield`):
- **Models**: Implement the pure algorithms but yield their intermediate mathematical state mid-loop.
- **Views**: Process the yielded dictionary states sequentially (utilizing `tkinter.Canvas.after()`), executing gorgeous continuous multi-node motion without imposing UI locks or multithreading synchronization complexities.
