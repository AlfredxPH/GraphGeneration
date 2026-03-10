from Graphs import *
from Models.OtherFuncs import *
import random

def build_gilbert_model(c: type, n_nodes: int, p: float) -> Graph:
    """
    Description:
    Construye un modelo de grafo utilizando el modelo de grafos aleatorios
    de Gilbert.

   Se unen cada par de nodos indepentientes y uniformemente con probabilidad p.

    Args:
        c (type): Clase constructora del grafo (debe ser instanciable sin argumentos).
        n_nodes (int): Número de nodos a crear en el grafo.
        p (float): Probabilidad de poner una arista.

    Returns:
        Graph: Grafo construido con aristas creadas con probabilidad p.

    Raises:
        ValueError: Si n_nodes es negativo o p es menor que 0 y mayor que 1.

    Example:
        >>> G = build_gilbert_model(Graph, 250, 0.01)
        >>> G.to_file_gv("GilbertModel_digraph", "X", "250-0.01")
    """
    g = c()

    for i in range(n_nodes):
        node = Node(f"Node_{i}")
        g.add_node(node)

    for element in combinatios(list(g.get_nodes()), 2):
        if random.random() < p:
            g.add_edge(Edge(element[0], element[1]))

    return g
