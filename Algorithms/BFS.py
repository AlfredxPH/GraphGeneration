import sys
import os

# Asegurar que se puedan importar las clases del directorio padre si es necesario
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Graphs import Graph
from Nodes import Node
from Edges import Edge


class BFS:
    """
    Description:
    Algoritmo de búsqueda en anchura (Breadth-First Search).
    """

    def __init__(self, graph: Graph, start_node: Node):
        self.graph = graph
        self.start_node = start_node

    def search(self) -> Graph:
        """
        Description:
        Ejecuta el algoritmo BFS desde el nodo inicial.

        Returns:
            (Graph) Un nuevo grafo dirigido que representa el árbol de búsqueda BFS.
        """
        tree = Graph()
        visited = set()
        queue = [self.start_node]

        # Agregamos el nodo inicial al árbol y a los visitados
        tree.add_node(self.start_node)
        visited.add(self.start_node.get_name())

        while queue:
            current_node = queue.pop(0)

            try:
                neighbors = self.graph.get_neighbors(current_node)
            except ValueError:
                neighbors = []

            for neighbor in neighbors:
                if neighbor.get_name() not in visited:
                    visited.add(neighbor.get_name())
                    queue.append(neighbor)

                    # Agregar nodo y arista al árbol de resultados
                    tree.add_node(neighbor)
                    name_edge = f"Edge_{current_node.get_name()}_{neighbor.get_name()}"
                    tree.add_edge(Edge(current_node, neighbor, name_edge))

        return tree