from Nodes import Node


class Edge:
    """
    Representa una arista o arco que conecta dos nodos en un grafo.
    """

    def __init__(self, node1: Node, node2: Node, weight: float = 1.0, directed: bool = True):
        """
        Inicializa una nueva arista.

        Args:
            node1 (Node): Nodo de origen.
            node2 (Node): Nodo de destino.
            weight (float): Peso de la arista (por defecto 1.0).
            directed (bool): Indica si la conexión es unidireccional (True) o bidireccional (False).
        """
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.directed = directed

    def get_node1(self) -> Node:
        return self.node1

    def get_node2(self) -> Node:
        return self.node2

    def get_weight(self) -> float:
        return self.weight

    def is_directed(self) -> bool:
        return self.directed

    def __str__(self):
        arrow = "->" if self.directed else "--"
        return f"{self.node1.get_name()} {arrow} {self.node2.get_name()} (w: {self.weight})"

    def __repr__(self):
        return self.__str__()