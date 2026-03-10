from Graphs import *
from Models.OtherFuncs import *
import random

def build_erre_model(c: type, n_nodes: int, m_edges: int) -> Graph:
    """
    Description:
    Construye un modelo de grafo utilizando el modelo de grafos aleatorios
    de Erdös y Rényi.

    Se eligen al azar m distintos pares de distintos vértices.

    Args:
        c (type): Clase constructora del grafo (debe ser instanciable sin argumentos).
        n_nodes (int): Número de nodos a crear en el grafo.
        m_edges (int): Número de aristas distintas.

    Returns:
        Graph: Grafo construido con m cantidad de aristas.

    Raises:
        ValueError: Si n_nodes es negativo o si el número de aristas m es
        menor que n_nodes-1.

    Example:
        >>> G = build_erre_model(Graph, 250, 3000)
        >>> G.to_file_gv("ErReModel_digraph", "X", "250-3000")
    """
    g = c()

    for i in range(n_nodes):
        node = Node(f"Node_{i}")
        g.add_node(node)

    for element in random.sample(combinatios(list(g.get_nodes()), 2), m_edges):
        g.add_edge(Edge(element[0], element[1]))

    return g