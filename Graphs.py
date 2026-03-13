from Edges import Edge
from Nodes import Node

class Graph:
    """
    Description:
    Permite crear un grafo dirigido

    Attributes:
    Niguno

    Example:
        >>> G = Graph()
    """
    def __init__(self):
        """
        Inicializa un nuevo grafo.
        """
        self.graph = {}

    def add_node(self, new_node: Node) -> None:
        """
        Description:
        Agrega un nodo al grafo inicializado.

        Args:
            new_node (Node): Nodo que se agrega al grafo.

        Returns:
            (None).
        """
        for node in self.graph:
            if node.get_name() == new_node.get_name():
                raise ValueError(f"Node {new_node.get_name()} already exists")
        self.graph[new_node] = []
        return None

    def add_edge(self, new_edge: Edge) -> None:
        """
        Description:
        Agrega una arista (o arco) al grafo inicializado.

        Args:
            new_edge (Edge): Arista que se agrega al grafo.

        Returns:
            (None).
        """
        node1 = new_edge.get_node1()
        node2 = new_edge.get_node2()
        nodes = [x.get_name() for x in list(self.graph.keys())]

        if node1.get_name() not in nodes:
            raise ValueError(f"Node {node1.get_name()} does not exist")
        if node2.get_name() not in nodes:
            raise ValueError(f"Node {node2.get_name()} does not exist")
        else:
            self.graph[node1].append(node2)

    def get_node(self, node_search: Node) -> Node:
        """
        Description:
        Extrae un nodo en específico del grafo inicializado.

        Args:
            node_search (Node): Nodo en el grafo que se desea extraer.

        Returns:
            (Node) El nodo del grafo inicializado.
        """
        for node in self.graph:
            if node.get_name() == node_search.get_name():
                return node
        raise ValueError(f"Node {node_search.get_name()} does not exist")

    def node_in_graph(self, node_search: Node) -> bool:
        """
        Description:
        Identifica si un nodo existe en el grafo inicializado.

        Args:
            node_search (Node): Nodo en el grafo que se desea saber.

        Returns:
            (bool) El si el nodo esta o no el el grafo inicializado.
        """
        for node in self.graph:
            if node.get_name() == node_search.get_name():
                return True
        return False

    def get_nodes(self) -> list:
        """
        Description:
        Obtiene los nodos en el grafo inicializado.

        Args:
        Ninguno

        Returns:
            (list) Los nodos del grafo inicializado.
        """
        return list(self.graph.keys())

    def get_no_nodes(self) -> int:
        """
        Description:
        Obtiene el número de nodos en el grafo inicializado.

        Args:
        Ninguno

        Returns:
            (int) El total de nodos del grafo inicializado.
        """
        return len(list(self.graph))

    def get_neighbors(self, node_search: Node) -> list:
        """
        Description:
        Obtiene los nodos vecinos de un nodo en el grafo inicializado.

        Args:
            node_search (Node): nodo en el grafo del que se desea buscar sus
            vecinos.

        Returns:
            (list) Los nodos vecinos al nodo del grafo inicializado.
        """
        for node in self.graph:
            if node.get_name() == node_search.get_name():
                return self.graph[node]
        raise ValueError(f"Node {node_search.get_name()} does not exist")

    def get_degree(self, node_search: Node) -> int:
        """
        Description:
        Obtiene el grado de un nodo en el grafo inicializado.

        Args:
            node_search (Node): nodo en el grafo del que se desea saber su grado.

        Returns:
           (int) El grado del nodo del grafo inicializado.
        """
        n_output = 0
        n_input = 0
        if node_search.get_name() in [n.get_name() for n in self.graph]:
            for node in self.graph:
                if node.get_name() == node_search.get_name():  # aristas de salida
                    n_input = len(self.graph[node])
                elif node_search.get_name() in [n.get_name() for n in self.graph[node]]: # aristas de entrada
                    n_output += 1
        else:
            raise ValueError(f"Node {node_search.get_name()} does not exist")
        return n_output + n_input

    def to_file_gv(self, name_model: str, name_grafo: str, nodes: str) -> None:
        """
        Description:
        Exporta un archivo .gv del grafo inicializado.

        Args:
            name_model (str): Nombre del modelo para crear el grafo, en caso de
            que se haya usado uno.
            name_grafo (str): Nombre del grafo inicializado.
            nodes (str): Número de nodos dentro del grafo inicializado.

        Returns:
            (.gv) Archivo .gv para gephi.
        """
        fichero = open(f"Results/Directed-Graph/DG-{name_model}_{nodes}.gv", 'w')
        fichero.write(f"digraph {name_grafo}" + " {\n")

        for node1 in self.graph:
            for node2 in self.graph[node1]:
                fichero.write(f"{node1.get_name()} -> {node2.get_name()};\n")

        fichero.write("}")
        fichero.close()

    def __str__(self):
        all_edges = ''
        for node1 in self.graph:
            for node2 in self.graph[node1]:
                all_edges += f"{node1.get_name()} -> {node2.get_name()}\n"
        return all_edges


class UndirectedGraph(Graph):
    """
    Description:
    Permite crear un grafo no dirigido

    Attributes:
    Niguno

    Example:
        >>> G = UndirectedGraph()
        "s -> a"
        "a -> s"
    """
    def add_edge(self, new_edge):
        """
        Description:
        Agrega una arista (o arco) al grafo inicializado asegurando que la
        dirección entre los nodos no sea dirigida.

        Args:
            new_edge (Edge): Arista que se agrega al grafo.

        Returns:
            (None).
        """
        Graph.add_edge(self, new_edge)
        edge_back = Edge(new_edge.get_node2(), new_edge.get_node1())
        Graph.add_edge(self, edge_back)

    def get_degree(self, node_search: Node) -> int:
        """
        Description:
        Obtiene el grado de un nodo en el grafo inicializado.

        Args:
            node_search (Node): nodo en el grafo del que se desea saber su grado.

        Returns:
           (int) El grado del nodo del grafo inicializado.
        """
        for node in self.graph:
            if node.get_name() == node_search.get_name():
                return len(self.graph[node])
        raise ValueError(f"Node {node_search.get_name()} does not exist")

    def to_file_gv(self, name_model: str, name_grafo: str, nodes: str) -> None:
        """
        Description:
        Exporta un archivo .gv del grafo inicializado.

        Args:
            name_model (str): Nombre del modelo para crear el grafo, en caso de
            que se haya usado uno.
            name_grafo (str): Nombre del grafo inicializado.
            nodes (str): Número de nodos dentro del grafo inicializado.

        Returns:
            (.gv) Archivo .gv para gephi.
        """
        fichero = open(f"Results/Undirected-Graph/G-{name_model}_{nodes}.gv", 'w')
        fichero.write(f"graph {name_grafo}" + " {\n")

        for node1 in self.graph:
            for node2 in self.graph[node1]:
                fichero.write(f"{node1.get_name()} -> {node2.get_name()};\n")

        fichero.write("}")
        fichero.close()