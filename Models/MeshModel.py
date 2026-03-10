from Graphs import *

def build_mesh_model(c: type, m: int, n:int, diagonal: bool = False) -> Graph:
    """
    Description:
    Construye un modelo de grafo utilizando el modelo de grafos aleatorios
    de Malla.

    La malla se construye con nodos organizados en una cuadrícula donde
    cada nodo (i, j) se conecta con sus vecinos según el parámetro diagonal.

    Args:
        c (type): Clase constructora del grafo.
        m (int): Número de filas de la malla (dimensión vertical). Debe ser >= 1.
        n (int): Número de columnas de la malla (dimensión horizontal). Debe ser >= 1.
        diagonal (bool): Si False, conectividad 4-vecinos (arriba, abajo, izq, der).
                  Si True, conectividad 8-vecinos (incluye diagonales).
                  Default: False

    Returns:
        Graph: Grafo de malla con m*n nodos etiquetados como "Node_i_j"
               donde i es la fila y j la columna

    Raises:
        ValueError: Si m < 1 o n < 1

    Time Complexity:
        O(m*n)

    Example:
        >>> # Malla 3x3 sin diagonales
        >>> g = build_mesh_model(Graph, 3, 3, diagonal=False)
        >>> len(g.get_nodes())
        9

        >>> # Malla 4x5 con diagonales (8-vecinos)
        >>> g = build_mesh_model(Graph, 4, 5, diagonal=True)
    """
    nodes = []
    g = c()

    for i in range(m):
        rows_nodes = []
        for j in range(n):
            node = Node(f"Node_{i}_{j}")
            g.add_node(node)
            rows_nodes.append(node)
        nodes.append(rows_nodes)

    edges = []
    for i in range(m):
        for j in range(n):
            if i < m-1:
                edges.append(Edge(nodes[i][j], nodes[i+1][j]))
            if j < n-1:
                edges.append(Edge(nodes[i][j], nodes[i][j+1]))
            if diagonal and i < m-1 and j < n-1:
                edges.append(Edge(nodes[i][j], nodes[i+1][j+1]))
            if diagonal and 0 < i and j < n-1:
                edges.append(Edge(nodes[i][j], nodes[i-1][j+1]))

    for edge in edges:
        g.add_edge(edge)

    return g
