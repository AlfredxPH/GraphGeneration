from Graphs import *
import random

def build_dorogovtsev_mendes_model(c: type, n_nodes: int) -> Graph:
    """
    Description:
    Construye un modelo de grafo utilizando el modelo de grafos aleatorios
    de Dorogovtsev-Mendes.

    Crea 3 nodos y 3 aristas formando un triángulo. Después, para cada nodo
    adicional, se selecciona una arista al azar y se crean aristas entre el
    nodo nuevo y los extremos de la arista seleccionada.

    Args:
        c (type): Clase constructora del grafo (debe ser instanciable sin argumentos).
        n_nodes (int): Número de nodos a crear en el grafo.

    Returns:
        Graph: Grafo construido.

    Raises:
        ValueError: Si n_nodes es menor a 3.

    Example:
        >>> gp = build_dorogovtsev_mendes_model(Graph, 100) # Si el grafo es dirigido
    """
    g = c()
    node1, node2 = Node("Nodo_0"), Node("Nodo_1")
    g.add_node(node1)
    g.add_node(node2)
    g.add_edge(Edge(node1, node2))
    edges_list = [(node1, node2)]

    for i in range(3, n_nodes+1):
        nodo_a, nodo_b = random.choice(edges_list)
        new_node = Node(f"Nodo_{i-1}")
        g.add_node(new_node)

        g.add_edge(Edge(nodo_a, new_node))
        g.add_edge(Edge(nodo_b, new_node))

        edges_list.append((nodo_a, new_node))
        edges_list.append((nodo_b, new_node))

    return g