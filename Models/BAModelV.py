import random

from Graphs import *
from Models.OtherFuncs import *

def build_barabasi_albert_model(c: type, n_nodes: int, d: int) -> Graph:
    """
    Description:
    Construye un modelo de grafo utilizando el modelo de grafos aleatorios
    de Barabási-Albert.

    Asigna a cada uno d aristas a vértices distintos de tal manera que la
    probabilidad de que el vértice nuevo se conecte a un vértice existente
    v es proporcional a la cantidad de aristas que v tiene actualmente.

    Args:
        c (type): Clase constructora del grafo (debe ser instanciable sin argumentos).
        n_nodes (int): Número de nodos a crear en el grafo.
        d (int): grado máximo esperado por cada nodo.

    Returns:
        Graph: Grafo construido.

    Raises:
        ValueError: Si n_nodes es negativo o d es menor a 1.

    Example:
        >>> G = build_barabasi_albert_model(UndirectedGraph, 1000, 8)
        >>> G.to_file_gv("BAModel_graph", "X", "1000-8")
    """
    g = c()
    list_nodes = []
    for i in range(n_nodes):
        node = Node(f"Node_{i}")
        list_nodes.append(node)
        g.add_node(node)

    for i in range(1,n_nodes):
        random_nodes = list_nodes[:i]
        random.shuffle(random_nodes)
        for j in range(len(random_nodes)):
            degree = g.get_degree(random_nodes[j])
            p = 1 - (degree / d)
            if random.random() < p:
                if random_nodes[j] != list_nodes[i]:
                    if g.get_degree(list_nodes[i]) < d and g.get_degree(random_nodes[j]) < d:
                        g.add_edge(Edge(list_nodes[i], random_nodes[j]))

    return g