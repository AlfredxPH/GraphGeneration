from Nodes import *

class Edge:
    """
    Description:
    Permite inicializar una arista (o arco) a partir de dos nodos dentro del grafo
    inicializado. En caso de ser un grafo dirigido, la dirección de los nodos
    inicialiados para la arista sera node1 -> node2.

    Attributes:
        node1 (Node): Primer nodo, dentro del grafo inicializado.
        node2 (Node): Segundo nodo, dentro del grafo inicializado.

    Example:
        >>> E = Edge(node1, node2)
    """
    def __init__(self, node1: Node, node2: Node, name_edge: str = None):
        """
        Inicializa una nueva arista.
        """
        self.node1 = node1
        self.node2 = node2
        self.name = name_edge

    def get_node1(self) -> Node:
        """
        Description:
        Extrae el Nodo 1 del grafo inicializado.

        Args:
        Ninguno

        Returns:
            (Node) El nodo 1 del grafo inicializado.
        """
        return self.node1

    def get_node2(self) -> Node:
        """
        Description:
        Extrae el Nodo 2 del grafo inicializado.

        Args:
        Ninguno

        Returns:
            (Node) El nodo 2 del grafo inicializado.
        """
        return self.node2

    def get_name(self) -> str:
        """
        Description:
        Extrae el nombre de la Arista del grafo inicializado.

        Args:
        Ninguno

        Returns:
            (str) El nombre del nodo del grafo inicializado.
        """
        return self.name

    def __str__(self):
        return f"{self.node1.get_name()} -> {self.node2.get_name()}"