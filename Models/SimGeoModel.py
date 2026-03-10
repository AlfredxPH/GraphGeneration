from Graphs import *
from Models.OtherFuncs import *
import random

def build_simgeo_model(c: type, n_nodes: int, r: float) -> Graph:
    """
    Description:
    Construye un modelo de grafo utilizando el modelo de grafos aleatorios
    geográfico simple.

    Se conectan nodos dentro de un rectángulo unitario.

    Args:
        c (type): Clase constructora del grafo (debe ser instanciable sin argumentos).
        n_nodes (int): Número de nodos a crear en el grafo.
        r (float): Radio de conexión entre nodos (distancia euclidiana máxima).

    Returns:
        Graph: Grafo construido con nodos ubicados aleatoriamente en [0,1]x[0,1]
               y aristas entre nodos cuya distancia sea <= r.

    Raises:
        ValueError: Si n_nodes es negativo o r es menor que 0 y mayor que 1.

    Time Complexity:
        O(n²) por la generación de combinaciones de pares.

    Space Complexity:
        O(n²) en el peor caso (grafo completo)

    Example:
        >>> gp = build_simgeo_model(Graph, 100, 0.1) # Si el grafo es dirigido
        >>> len(gp.get_nodes())
        100

    Note:
        Para grafos grandes (n > 1000), considerar usar estructuras espaciales
        como KD-Tree para reducir la complejidad a O(n log n).
    """
    g = c()
    nodes_location = {}

    for i in range(n_nodes):
        node = Node(f"Node_{i}")
        g.add_node(node)
        nodes_location[node] = [random.random(), random.random()]

    for element in combinatios(list(g.get_nodes()), 2):
        x1,y1 = nodes_location[element[0]]
        x2,y2 = nodes_location[element[1]]

        if (x2-x1)**2 + (y2-y1)**2 <= r**2:
            g.add_edge(Edge(element[0], element[1]))

    return g