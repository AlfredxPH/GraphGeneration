import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Graphs import Graph
from Nodes import Node
from Edges import Edge


class DFS_I:
    """
    Description:
    Algoritmo de búsqueda en profundidad (Depth-First Search) en su versión iterativa.
    """

    def __init__(self, graph: Graph, start_node: Node):
        self.graph = graph
        self.start_node = start_node

    def search(self) -> Graph:
        """
        Description:
        Ejecuta el algoritmo DFS iterativo desde el nodo inicial usando una pila.

        Returns:
            (Graph) Un nuevo grafo dirigido que representa el árbol de búsqueda DFS.
        """
        tree = Graph()
        visited = set()

        # La pila almacena tuplas de (Nodo_Padre, Nodo_Actual)
        stack = [(None, self.start_node)]

        while stack:
            parent, current_node = stack.pop()

            if current_node.get_name() not in visited:
                visited.add(current_node.get_name())
                tree.add_node(current_node)

                if parent is not None:
                    name_edge = f"Edge_{parent.get_name()}_{current_node.get_name()}"
                    tree.add_edge(Edge(parent, current_node, name_edge))

                try:
                    neighbors = self.graph.get_neighbors(current_node)
                except ValueError:
                    neighbors = []

                # Invertimos los vecinos antes de agregarlos a la pila para que
                # el orden de visita sea idéntico al de la versión recursiva.
                for neighbor in reversed(neighbors):
                    if neighbor.get_name() not in visited:
                        stack.append((current_node, neighbor))

        return tree