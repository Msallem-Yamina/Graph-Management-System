"""
File Manager module - Handles saving and loading graphs to/from files.
Demonstrates different file access modes: read-only ('r') and write ('w').
"""

import json
from typing import Optional

from graph import Graph
from config import GRAPH_FILE


def save_graph(graph: Graph, file_path: str = GRAPH_FILE) -> bool:
    """
    Save the graph to a JSON file.
    Uses write mode ('w') which overwrites the existing file.
    
    Args:
        graph: The graph to save
        file_path: Path to the file (default: GRAPH_FILE from config)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(graph.adjacency, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving graph: {e}")
        return False


def load_graph(file_path: str = GRAPH_FILE, mode: str = "r") -> Optional[Graph]:
    try:
        graph = Graph()
        with open(file_path, mode, encoding="utf-8") as f:
            data = json.load(f)
        # Convert weights to float
        for node, neighbors in data.items():
            graph.adjacency[node] = {neighbor: float(weight) for neighbor, weight in neighbors.items()}
        return graph
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"File '{file_path}' is invalid or corrupted.")
        return None
    except Exception as e:
        print(f"Error loading graph: {e}")
        return None