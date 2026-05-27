"""
Graph module - Graph data structure implementation.
This module contains the Graph class that represents a weighted graph
using an adjacency list (dictionary of dictionaries).
"""

from typing import Dict, Set


class Graph:
    """
    Represents a weighted graph using an adjacency list.
    
    Structure:
        adjacency = {
            "A": {"B": 5.0, "C": 2.0},
            "B": {"C": 1.0},
            ...
        }
    """

    def __str__(self) -> str:
        """
        Return a readable string representation of the graph.
        """
        result = "Graph:\n"
        for node, neighbors in self.adjacency.items():
            if neighbors:
                edges = ", ".join(f"{dest}({weight})" for dest, weight in neighbors.items())
                result += f"  {node} -> {edges}\n"
            else:
                result += f"  {node} -> No neighbors\n"
        return result

    def __init__(self) -> None:
        """Initialize an empty graph."""
        self.adjacency: Dict[str, Dict[str, float]] = {}

    def add_node(self, name: str) -> None:
        """
        Add a node to the graph.
        
        Args:
            name: Name of the node to add
        """
        if name not in self.adjacency:
            self.adjacency[name] = {}

    def remove_node(self, name: str) -> None:
        """
        Remove a node from the graph.
        Also removes all edges connected to this node.
        
        Args:
            name: Name of the node to remove
        """
        if name not in self.adjacency:
            return
        
        # Remove the node itself
        self.adjacency.pop(name, None)
        
        # Remove all edges pointing to this node from other nodes
        for neighbors in self.adjacency.values():
            if name in neighbors:
                neighbors.pop(name)

    def add_edge(self, source: str, destination: str, weight: float, directed: bool) -> None:
        """
        Add an edge (transition) between two nodes.
        If the graph is undirected, also adds the reverse edge.
        
        Args:
            source: Source node name
            destination: Destination node name
            weight: Weight/cost of the edge
            directed: If True, creates a directed edge only. If False, creates bidirectional edge.
        """
        # Add nodes if they don't exist
        if source not in self.adjacency:
            self.add_node(source)
        if destination not in self.adjacency:
            self.add_node(destination)

        # Add the edge
        self.adjacency[source][destination] = weight
        
        # If undirected, add reverse edge
        if not directed:
            self.adjacency[destination][source] = weight

    def get_nodes(self) -> Set[str]:
        """
        Get all node names in the graph.
        
        Returns:
            Set of all node names
        """
        return set(self.adjacency.keys())

    def remove_edge(self, source: str, destination: str) -> None:
        """
        Remove an edge between two nodes.
        Works for directed and undirected graphs.
        """
        if source in self.adjacency and destination in self.adjacency[source]:
            del self.adjacency[source][destination]

        if destination in self.adjacency and source in self.adjacency[destination]:
            del self.adjacency[destination][source]

    def get_neighbors(self, node: str) -> Dict[str, float]:
        """
        Get all neighbors of a node with their edge weights.
        
        Args:
            node: Name of the node
            
        Returns:
            Dictionary mapping neighbor names to edge weights
        """
        return self.adjacency.get(node, {}).copy()

    def is_empty(self) -> bool:
        """
        Check if the graph is empty.
        
        Returns:
            True if the graph has no nodes, False otherwise
        """
        return len(self.adjacency) == 0

    def has_node(self, node: str) -> bool:
        """
        Check if a node exists in the graph.
        
        Args:
            node: Name of the node to check
            
        Returns:
            True if the node exists, False otherwise
        """
        return node in self.adjacency
    
    def has_edge(self, source: str, destination: str) -> bool:
        """
        Check if an edge exists between source and destination.

        Args:
            source: Source node name
            destination: Destination node name

        Returns:
            True if the edge exists, False otherwise
        """
        return source in self.adjacency and destination in self.adjacency[source]
    def rename_node(self, old_name: str, new_name: str) -> None:
        """
        Rename a node while preserving its edges.
        """

        if old_name not in self.adjacency:
            print("Node does not exist.")
            return

        if new_name in self.adjacency:
            print("A node with this name already exists.")
            return

        # rename key
        self.adjacency[new_name] = self.adjacency.pop(old_name)

        # update all references in neighbors
        for node in self.adjacency:
            if old_name in self.adjacency[node]:
                self.adjacency[node][new_name] = self.adjacency[node].pop(old_name)