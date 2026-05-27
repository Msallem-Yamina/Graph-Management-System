"""
Menu module - User interface and menu functions.
Handles all user interactions, input validation, and menu navigation.
"""
import os

import math
from typing import Optional

from graph import Graph
from algorithms import breadth_first_search, dijkstra
from file_manager import save_graph, load_graph
from config import GRAPH_FILE


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_graph() -> Graph:
    """
    Interactive function to create a new graph by user input.
    
    Returns:
        A new Graph object with nodes and edges entered by the user
    """
    graph = Graph()
    print("\n=== Create a new graph ===")

    # Input nodes
    while True:
        try:
            num_nodes = int(input("Number of nodes: "))
            if num_nodes <= 0:
                print("Please enter a positive number of nodes.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    for i in range(num_nodes):
        while True:  
            original_name = input(f"Node name #{i + 1}: ").strip()
            if not original_name:
                print("Empty name ignored. Please enter a valid node name.")
                continue
            
            # Check case-insensitive duplicates
            if any(n.lower() == original_name.lower() for n in graph.get_nodes()):
                print("Node already exists. Please enter a different name.")
                continue
            
            # Add node with original case
            graph.add_node(original_name)
            break

    if len(graph.get_nodes()) == 0:
        print("No nodes created. Graph is empty. Exiting.")
        return graph

    # Input edges
    print("\n--- Enter edges (transitions) ---")
    print("Format: source destination weight (e.g., A B 3.5)")
    print("Leave empty to stop.")

    while True:
        line = input("Edge: ").strip()
        if not line:
            break
        
        parts = line.split()
        if len(parts) != 3:
            print("Invalid format. Use: source destination weight")
            continue
        
        source_orig, dest_orig, weight_str = parts
        source_orig = source_orig.strip()
        dest_orig = dest_orig.strip()

        try:
            weight = float(weight_str)
        except ValueError:
            print("Invalid weight. Please enter a number.")
            continue

        # Checks that both nodes exist
        if not graph.has_node(source_orig) and not graph.has_node(dest_orig):
            print(f"Both nodes are missing: '{source_orig}' and '{dest_orig}' do not exist.")
            continue
        elif not graph.has_node(source_orig):
            print(f"Source node '{source_orig}' does not exist.")
            continue
        elif not graph.has_node(dest_orig):
            print(f"Destination node '{dest_orig}' does not exist.")
            continue

        # Check edge duplicate (case-insensitive)
        if any(
            s.lower() == source_orig.lower() and d.lower() == dest_orig.lower()
            for s, neighbors in graph.adjacency.items()
            for d in neighbors
        ):
            print("Edge already exists.")
            continue

        # Directed 
        while True:
            directed_input = input("Directed edge? (y/n): ").strip().lower()
            if directed_input in ("y", "n"):
                directed = directed_input == "y"
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        
        # Add edge with original case
        graph.add_edge(source_orig, dest_orig, weight, directed=directed)
    
    # Summary
    print("\nGraph summary:")
    print(graph)
    print("\nGraph created in memory.")
    return graph

def display_graph_bfs(graph: Graph) -> None:
    """
    Display the graph using breadth-first search traversal.
    Shows each node and its neighbors with weights.
    
    Args:
        graph: The graph to display
    """
    if graph.is_empty():
        print("No graph in memory.")
        return

    start = input("Starting node for breadth-first traversal: ").strip()
    order = breadth_first_search(graph, start)
    
    if not order:
        print("Starting node not found or graph is empty.")
        return

    print("\n=== Breadth-First Search Traversal ===")
    for node in order:
        neighbors = graph.get_neighbors(node)
        if neighbors:
            neighbor_list = ", ".join(f"{n}(weight={w})" for n, w in neighbors.items())
            print(f"{node} -> {neighbor_list}")
        else:
            print(f"{node} -> (no neighbors)")

def ask_yes_no(message):
    while True:
        ans = input(message).strip().lower()
        if ans in ("y", "n"):
            return ans == "y"
        print("Enter y or n only.")

def modify_node(graph: Graph):
    if graph.is_empty():
        print("Graph is empty.")
        return

    node = input("Enter node name to modify: ").strip()
    if not graph.has_node(node):
        print("Node not found.")
        return

    while True:
        print(f"\n--- Modify Node '{node}' ---")
        print("1 - Rename node")
        print("2 - Add edge")
        print("3 - Remove edge")
        print("4 - Back")

        choice = input("Choice: ").strip()

        # rename node
        if choice == "1":
            new_name = input("New name: ").strip()
            if not new_name:
                print("Invalid name.")
                continue
            if graph.has_node(new_name):
                print("Name already exists.")
                continue

            graph.rename_node(node, new_name)
            node = new_name
            print("Node renamed successfully.")

        # add edge
        elif choice == "2":
            dest = input("Destination node: ").strip()
            if not graph.has_node(dest):
                print("Destination does not exist.")
                continue

            try:
                weight = float(input("Weight: "))
            except ValueError:
                print("Invalid weight.")
                continue

            directed = input("Directed? (y/n): ").strip().lower() == "y"
            graph.add_edge(node, dest, weight, directed)
            print("Edge added.")

        # remove edge
        elif choice == "3":
            dest = input("Destination node to remove: ").strip()
            if not graph.has_edge(node, dest):
                print("Edge does not exist.")
                continue

            graph.remove_edge(node, dest)
            print("Edge removed.")

        elif choice == "4":
            if ask_yes_no("Save changes? (y/n): "):
                save_graph(graph, GRAPH_FILE)
            break

        else:
            print("Invalid choice.")

def modification_menu(graph: Graph, mode: str) -> None:
    """
    Sub-menu for graph modifications.
    Allows adding nodes, removing nodes, and adding edges.
    
    Args:
        graph: The graph to modify
    """
    if mode == "r":
        print("Graph is in Read only mode. Modifications are not allowed.")
        return
    
    while True:
        print("\n=== Graph Modification Menu ===")
        print("1 - Add a node")
        print("2 - Update a node")
        print("3 - Remove a node")
        print("4 - Add or Update an edge between two existing nodes")
        print("5 - Delete an edge")
        print("0 - Return to main menu")

        choice = input("Your choice: ").strip()

        if choice == "1":
            add_node_with_neighbors(graph)

        elif choice == "2":
            modify_node(graph)   

        elif choice == "3":
            name = input("Node name to remove: ").strip()
            if not graph.has_node(name):
                print("This node does not exist.")
                continue
            graph.remove_node(name)
            print(f"Node '{name}' removed with all its edges.")

        elif choice == "4":
            source = input("Source node: ").strip()
            destination = input("Destination node: ").strip()

            if not graph.has_node(source) or not graph.has_node(destination):
                print("Both nodes must exist in the graph.")
                continue

            try:
                weight = float(input("Edge weight: "))
            except ValueError:
                print("Invalid weight.")
                continue

            while True:
                directed_input = input("Directed edge? (y/n): ").strip().lower()
                if directed_input in ("y", "n"):
                    directed = directed_input == "y"
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            graph.add_edge(source, destination, weight, directed=directed)
            print(f"Edge between '{source}' and '{destination}' with weight {weight} added.")

        elif choice == "5":
            source = input("Source node: ").strip()
            destination = input("Destination node: ").strip()

            if not graph.has_edge(source, destination):
                print("Edge does not exist.")
                continue

            graph.remove_edge(source, destination)
            print("Edge removed.")

        elif choice == "0":
            if ask_yes_no("Save changes? (y/n): "):
                save_graph(graph, GRAPH_FILE)
            break

        else:
            print("Invalid choice.")

def perform_dijkstra(graph: Graph) -> None:
    """
    Interactive function to find shortest path using Dijkstra's algorithm.
    
    Args:
        graph: The graph to search
    """
    if graph.is_empty():
        print("No graph in memory.")
        return

    start = input("Starting node: ").strip()
    end = input("Destination node: ").strip()

    distance, path = dijkstra(graph, start, end)
    
    if distance == math.inf or not path:
        print("No path found between these two nodes.")
    else:
        path_str = " -> ".join(path)
        print(f"\nShortest path: {path_str}")
        print(f"Total distance: {distance}")

def add_node_with_neighbors(graph: Graph) -> None:
    # add node
    while True:
        node_name = input("Enter new node name (or leave empty to cancel): ").strip()
        if not node_name:
            print("Cancelled adding node.")
            return

        if any(n.lower() == node_name.lower() for n in graph.get_nodes()):
            print("Node already exists. Try a different name.")
            continue

        graph.add_node(node_name)
        print(f"Node '{node_name}' added successfully.")
        break

    # Add edges
    while True:
        print("\nAdd edges from this node to existing neighbors.")
        print("Format: destination_node weight directed(y/n) (exp: A 2 y)")
        print("Leave empty to stop adding edges.")

        line = input("Edge: ").strip()
        if not line:
            break

        parts = line.split()
        if len(parts) != 3:
            print("Invalid format. Use: destination_node weight directed(y/n)")
            continue

        dest, weight_str, directed_input = parts
        if not graph.has_node(dest):
            print(f"Destination node '{dest}' does not exist. Try again.")
            continue

        try:
            weight = float(weight_str)
        except ValueError:
            print("Invalid weight. Must be a number.")
            continue

        directed_input = directed_input.lower()
        if directed_input not in ("y", "n"):
            print("Directed must be 'y' or 'n'.")
            continue

        directed = directed_input == "y"

        # verify edge duplicate (case-insensitive)
        if any(
            s.lower() == node_name.lower() and d.lower() == dest.lower()
            for s, neighbors in graph.adjacency.items()
            for d in neighbors
        ):
            print("Edge already exists.")
            continue

        graph.add_edge(node_name, dest, weight, directed=directed)
        print(f"Edge {node_name} -> {dest} (weight={weight}, directed={directed}) added.")

def main_menu() -> None:
    """
    Main menu loop - entry point for the application.
    Handles all menu options and navigation.
    """
    graph: Optional[Graph] = None
    graph_mode: str = "r" 

    while True:
        print("\n=== Main Menu - Graph Management ===")
        print("1 - Create / input a new graph")
        print("2 - Load graph from file")
        print("3 - Display graph (breadth-first search)")
        print("4 - Modify graph")
        print("5 - Shortest path (Dijkstra)")
        print("6 - Save graph to file")
        print("0 - Quit")

        choice = input("Your choice: ").strip()

        if choice == "1":
            graph = create_graph()
            graph_mode = "r+"
            # Auto-save after creation
            if ask_yes_no("Do you want to save the graph? (y/n): "):
                if save_graph(graph, GRAPH_FILE):
                    print(f"Graph saved to '{GRAPH_FILE}'.")
                else:
                    print("Failed to save the graph.")

        elif choice == "2":
            print("Choose file mode:")
            print("1. Read only")
            print("2. Read and Write")
            mode_choice = input("Your choice (1 or 2): ")
            mode = "r" if mode_choice == "1" else "r+"
            graph_mode = mode

            graph = load_graph(GRAPH_FILE, mode=mode)
            if graph:
                mode_name = "Read only" if mode == "r" else "Read and Write"
                print(f"Graph loaded successfully in mode '{mode_name}'")
            else:
                print("Failed to load graph.")

        elif choice == "3":
            if graph is None:
                print("No graph in memory. Create or load a graph first.")
            else:
                display_graph_bfs(graph)

        elif choice == "4":
            if graph is None:
                print("No graph in memory. Create or load a graph first.")
            else:
                modification_menu(graph, graph_mode)

        elif choice == "5":
            if graph is None:
                print("No graph in memory. Create or load a graph first.")
            else:
                perform_dijkstra(graph)

        elif choice == "6":
            if graph is None:
                print("No graph in memory to save.")
            elif graph_mode == "r":
                print("Cannot save. Graph is in Read only mode.")
            else:
                if save_graph(graph, GRAPH_FILE):
                    print(f"Graph saved to '{GRAPH_FILE}'.")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice, please try again.")

        