import json
import sys


def load_graph(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        loaded_graph = json.load(file)

    if not isinstance(loaded_graph, dict):
        raise ValueError("the JSON root must be an object of stations")
    if len(loaded_graph) < 2:
        raise ValueError("the graph must contain at least two stations")

    for station, connections in loaded_graph.items():
        if not isinstance(station, str) or not isinstance(connections, dict):
            raise ValueError("each station must map to an object of connections")
        for neighbor, distance in connections.items():
            if neighbor not in loaded_graph:
                raise ValueError(
                    f"connection from {station} refers to unknown station {neighbor}"
                )
            if (not isinstance(distance, (int, float))
                    or isinstance(distance, bool) or distance < 0):
                raise ValueError(
                    f"distance from {station} to {neighbor} must be non-negative"
                )

    return loaded_graph


graph = {}

def bfs(start, goal, graph_data=None):
    if graph_data is None:
        graph_data = graph
    visited = [start]
    queue = [start]
    while queue:
        current = queue.pop(0)
        if current == goal:
            return visited
        for neighbor in graph_data[current]:
            if neighbor not in visited:
                if neighbor == goal:
                    visited.append(neighbor)
                    return visited
                visited.append(neighbor)
                queue.append(neighbor)
    return visited

def dfs(start, goal, graph_data=None):
    if graph_data is None:
        graph_data = graph
    visited = []
    stack = [start]
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.append(current)
        if current == goal:
            return visited
        for neighbor in reversed(list(graph_data[current])):
            if neighbor not in visited:
                stack.append(neighbor)
    return visited

def dijkstra(start, goal, graph_data=None):
    if graph_data is None:
        graph_data = graph

    distances = {node: float('inf') for node in graph_data}
    distances[start] = 0
    parent = {start: None}
    visited = []
    while len(visited) < len(graph_data):
        current = min((node for node in graph_data if node not in visited), key=lambda node: distances[node])
        if distances[current] == float('inf'):
            return None, float('inf')
        visited.append(current)
        if current == goal:
            break
        for neighbor, weight in graph_data[current].items():
            if neighbor not in visited:
                new_distance = distances[current] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent[neighbor] = current
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path, distances[goal]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pathfinding.py <graph.json>", file=sys.stderr)
        raise SystemExit(2)

    graph_file = sys.argv[1]
    try:
        graph = load_graph(graph_file)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not load graph '{graph_file}': {error}", file=sys.stderr)
        raise SystemExit(2)
