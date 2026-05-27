"""
Algorithms module - Graph algorithms implementation.
Contains BFS (Breadth-First Search) and Dijkstra's shortest path algorithm.
"""

import math
import heapq
from typing import Dict, List, Tuple, Optional, Set

from graph import Graph


def breadth_first_search(graph: Graph, start: str) -> List[str]:
    """
    Perform a breadth-first search (BFS) traversal of the graph.
    
    Args:
        graph: The graph to traverse
        start: Starting node name
        
    Returns:
        List of nodes visited in BFS order
    """
    if not graph.has_node(start):
        return []

    visited: Set[str] = set()
    queue: List[str] = [start]
    visited.add(start)
    order: List[str] = []

    while queue:
        current = queue.pop(0)  # Dequeue from front
        order.append(current)
        
        # Visit all neighbors
        neighbors = graph.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # Enqueue at back
    
    return order


def dijkstra(graph: Graph, start: str, end: str) -> Tuple[float, List[str]]:
    """
    Find the shortest path between two nodes using Dijkstra's algorithm.
    
    Args:
        graph: The graph to search
        start: Starting node name
        end: Destination node name
        
    Returns:
        Tuple of (minimum_distance, path_list)
        If no path exists, returns (math.inf, [])
    """
    if not graph.has_node(start) or not graph.has_node(end):
        return math.inf, []

    # Initialize distances: all nodes have infinite distance except start
    distances: Dict[str, float] = {node: math.inf for node in graph.get_nodes()}
    previous: Dict[str, Optional[str]] = {node: None for node in graph.get_nodes()}
    distances[start] = 0.0

    # Priority queue: (distance, node)
    priority_queue: List[Tuple[float, str]] = [(0.0, start)]

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)
        
        # Skip if we already found a better path
        if current_dist > distances[current_node]:
            continue
        
        # If we reached the destination, we can stop
        if current_node == end:
            break

        # Check all neighbors
        neighbors = graph.get_neighbors(current_node)
        for neighbor, weight in neighbors.items():
            new_distance = current_dist + weight
            
            # If we found a shorter path, update it
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # If no path was found
    if distances[end] == math.inf:
        return math.inf, []

    # Reconstruct the path from end to start
    path: List[str] = []
    current: Optional[str] = end
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    return distances[end], path
