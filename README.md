# Graph Management Project

A Python console application for managing weighted graphs with various operations and algorithms.

## Project Architecture

The project is organized into multiple modules, each with a specific responsibility:

### File Structure

```
├── main.py              # Main entry point - run this file
├── config.py            # Configuration constants (file paths, etc.)
├── graph.py             # Graph data structure (Graph class)
├── algorithms.py        # Graph algorithms (BFS, Dijkstra)
├── file_manager.py      # File operations (save/load)
├── menu.py              # User interface and menu functions
├── graph.json           # Saved graph file (created automatically)
└── README.md            # This file
```

### Module Descriptions

#### `config.py`
- Contains configuration constants
- Defines the default file path for saving/loading graphs

#### `graph.py`
- **Graph class**: Core data structure
- Represents a weighted graph using an adjacency list (dictionary of dictionaries)
- Methods for:
  - Adding/removing nodes
  - Adding edges (transitions)
  - Getting neighbors
  - Checking if graph is empty or if a node exists

#### `algorithms.py`
- **breadth_first_search()**: BFS traversal algorithm
- **dijkstra()**: Dijkstra's shortest path algorithm
- Both functions work with the Graph class

#### `file_manager.py`
- **save_graph()**: Saves graph to JSON file (write mode 'w')
- **load_graph()**: Loads graph from JSON file (read mode 'r')
- Demonstrates different file access modes

#### `menu.py`
- **create_graph()**: Interactive graph creation
- **display_graph_bfs()**: Display graph using BFS
- **modification_menu()**: Sub-menu for graph modifications
- **perform_dijkstra()**: Interactive shortest path calculation
- **main_menu()**: Main menu loop and navigation

#### `main.py`
- Entry point of the application
- Simply calls `main_menu()` to start the program

## Features

- ✅ Create/input a new graph
- ✅ Save graph to file (write mode - overwrites existing file)
- ✅ Load graph from file (read mode)
- ✅ Display graph using **breadth-first search (BFS)** traversal
- ✅ Modify graph:
  - Add a node
  - Remove a node (and all its edges)
  - Add an edge between two existing nodes
- ✅ Calculate **shortest path** using **Dijkstra's algorithm**
- ✅ Quit the program

## How to Run

```bash
python main.py
```

## Usage Flow

1. **Start the program** → Main menu appears
2. **Create a graph** (option 1) → Enter nodes and edges → Graph is automatically saved
3. **Display graph** (option 3) → Shows nodes and neighbors using BFS
4. **Modify graph** (option 4) → Add/remove nodes or edges
5. **Calculate shortest path** (option 5) → Enter start and end nodes → Dijkstra algorithm runs
6. **Save graph** (option 6) → Manually save current graph state
7. **Quit** (option 0) → Exit the program

## File Operations

The project demonstrates different file access modes:

- **Write mode (`'w'`)**: Used when saving the graph - overwrites the existing file
- **Read mode (`'r'`)**: Used when loading the graph - reads the file content

The graph is saved in JSON format for easy reading and editing.

## Example Graph

```
A --5--> B
|        |
2        1
|        |
v        v
C <--1-- B
```

This graph would be represented as:
```json
{
  "A": {"B": 5.0, "C": 2.0},
  "B": {"C": 1.0},
  "C": {}
}
```