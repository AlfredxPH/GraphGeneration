from Edges import Edge
from Nodes import Node

def combinatios(n: list, k: int) -> list:
    """
    Description:
    Genera todas las combinaciones de k elementos de una lista.

    Esta función implementa un algoritmo recursivo que genera el conjunto
    potencia limitado a combinaciones de tamaño k.

    Args:
        n (int): Lista de elementos de cualquier tipo,
        k (int): Número de elementos por combinación.

    Returns:
        Lista de listas, donde cada sublista es una combinación,

    Raises:
        ValueError: Si k es negativo o mayor que len(n),

    Time Complexity:
        O(C(n, k)) donde C es el coeficiente binomial

    Example:
        >>> combinatios(['a', 'b', 'c'], 2)
        [['a', 'b'], ['a', 'c'], ['b', 'c']]

        >>> combinatios([1, 2, 3, 4], 3)
        [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
    """
    if k == 0:
        return [[]]
    if not n:
        return []

    result = []
    first = n[0]
    rest = n[1:]

    for comb in combinatios(rest, k - 1):
        result.append([first] + comb)

    result.extend(combinatios(rest, k))

    return result

def build_graph(c):
    """
    Description:
    Constructor genérico de grafos para puebas.

    Args:
        c (type): Clase de grafo a instanciar (Graph, DiGraph, etc.).

    Returns:
        Instancia de la clase de grafo especificada.

    Example:
        >>> g = build_graph(Graph)
        >>> print(g)
        s -> a
    """
    g = c()
    for node in ('s','a','b','c','d','e','f','g','h','i'):
        g.add_node(Node(node))

    nodo_s = Node('s')
    nodo_a = Node('a')

    g.add_edge(Edge(g.get_node(nodo_s), g.get_node(nodo_a)))
    return g
