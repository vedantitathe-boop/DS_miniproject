from graph import graph

def bfs(start, goal):
    visited = [start]
    queue = [start]
    while queue:
        current = queue.pop(0)
        if current == goal:
            return visited
        for neighbor in graph[current]:
            if neighbor not in visited:
                if neighbor == goal:
                    visited.append(neighbor)
                    return visited
                visited.append(neighbor)
                queue.append(neighbor)
    return visited

def dfs(start, goal):
    visited = []
    stack = [start]
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.append(current)
        if current == goal:
            return visited
        for neighbor in reversed(list(graph[current])):
            if neighbor not in visited:
                stack.append(neighbor)
    return visited

def dijkstra(start, goal):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {start: None}
    visited = []
    while len(visited) < len(graph):
        current = min((node for node in graph if node not in visited), key=lambda node: distances[node])
        if distances[current] == float('inf'):
            return None, float('inf')
        visited.append(current)
        if current == goal:
            break
        for neighbor, weight in graph[current].items():
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
