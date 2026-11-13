# Adjacency List

# Add vertix to the dictionary
def add_vertex(v: int) -> None:
    global graph
    global vertices
    if v in graph: # type: ignore
        print(f"Vertex {v} already exist.")
    else:
        vertices = vertices + 1
    graph[v] = []  # type: ignore


# Add an edge weight "e" between v1 and v2
def add_edge(v1: int, v2: int, e: int) -> None:
    global graph
    if v1 not in graph:  # type: ignore
        print(f"Vertex {v1} doesn't exist.")
    elif v2 not in graph:
        print(f"Vertex {v2} doesn't exist.")
    else:
        temp = [v2, e]
        graph[v1].append(temp)  # type: ignore


# Print graph
def print_graph() -> None:
    global graph
    for vertex in graph:  # type: ignore
        for edge in graph[vertex]: # type: ignore
            print(f"{vertex} -> {edge[0]}, edge weight {edge[1]}")

graph = {}
vertices = 0

add_vertex(1)
add_vertex(2)
add_vertex(3)
add_vertex(4)

add_edge(1, 2, 1)
add_edge(1, 3, 1)
add_edge(2, 3, 3)
add_edge(3, 4, 3)
add_edge(4, 1, 5)

print_graph()

print("Internal representation:", graph)
print("####################################\n")


# Adjacency Matrix

# Add vertex to the set of verteces and the graph
def add_vertex_matrix(v: int) -> None:
    global graph_matrix
    global verteces_num
    global vertices_matrix
    if v in graph_matrix:  # type: ignore
        print(f"Vertex {v} already exist.")
    else:
        verteces_num = verteces_num + 1  # type: ignore
        vertices_matrix.append(v)  # type: ignore
        if verteces_num > 1:
            for vertex in vertices_matrix:  # type: ignore
                vertices_matrix.append(0)  # type: ignore
        temp = []
        for i in range(verteces_num):
            temp.append(0)
        graph_matrix.append(temp)  # type: ignore


# Add an edge between vertex v1 and v2 with edge weight e
def add_edge_matrix(v1: int, v2: int, e: int) -> None:
    global graph_matrix
    global verteces_num
    global vertices_matrix
    if v1 not in vertices_matrix:  # type: ignore
        print(f"Vertex {v1} doesn't exist.")
    elif v2 not in vertices_matrix: # type: ignore
        print(f"Vertex {v2} doesn't exist.")
    else:
        index1 = vertices_matrix.index(v1)  # type: ignore
        index2 = vertices_matrix.index(v2)  # type: ignore
        graph_matrix[index1][index2] = e  # type: ignore


# Print the graph
def print_graph_matrix() -> None:
    global graph_matrix
    global verteces_num
    for i in range(verteces_num):  # type: ignore
        for j in range(vertices_num):  # type: ignore
            if graph_matrix[i][j] != 0:  # type: ignore
                print(f"{vertices_matrix[i]} -> {vertices_matrix[j]}, \
                    edge weight: {graph_matrix[i][j]}")


graph_matrix = []
verteces_num = 0
vertices_matrix = []

add_vertex_matrix(1)
add_vertex_matrix(2)
add_vertex_matrix(3)
add_vertex_matrix(4)

add_edge_matrix(1, 2, 1)
add_edge_matrix(1, 3, 1)
add_edge_matrix(2, 3, 3)
add_edge_matrix(3, 4, 3)
add_edge_matrix(4, 1, 5)

print_graph_matrix()

print("Internal representation:", graph_matrix)
