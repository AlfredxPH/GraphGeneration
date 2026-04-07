import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Graphs import Graph
from Nodes import Node
from Edges import Edge


class DFS_R:
    """
    Description:
    Algoritmo de búsqueda en profundidad (Depth-First Search) en su versión recursiva.
    """

    def __init__(self, graph: Graph, start_node: Node):
        self.graph = graph
        self.start_node = start_node
        self.tree = Graph()
        self.visited = set()

    def search(self) -> Graph:
        """
        Description:
        Ejecuta el algoritmo DFS recursivo desde el nodo inicial.

        Returns:
            (Graph) Un nuevo grafo dirigido que representa el árbol de búsqueda DFS.
        """
        # Reiniciamos el árbol y visitados por si el método se llama múltiples veces
        self.tree = Graph()
        self.visited = set()

        self._dfs_recursive(None, self.start_node)
        return self.tree

    def _dfs_recursive(self, parent: Node, current_node: Node):
        if current_node.get_name() not in self.visited:
            self.visited.add(current_node.get_name())
            self.tree.add_node(current_node)

            if parent is not None:
                name_edge = f"Edge_{parent.get_name()}_{current_node.get_name()}"
                self.tree.add_edge(Edge(parent, current_node, name_edge))

            try:
                neighbors = self.graph.get_neighbors(current_node)
            except ValueError:
                neighbors = []

            for neighbor in neighbors:
                if neighbor.get_name() not in self.visited:
                    self._dfs_recursive(current_node, neighbor)