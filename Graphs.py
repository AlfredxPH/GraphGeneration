import os
import math
import heapq
import random
from Nodes import Node
from Edges import Edge
from itertools import combinations


class Graph:
    """
    Clase principal para la creación y manejo de grafos.
    """

    def __init__(self, directed: bool = False):
        """
        Inicializa un nuevo grafo.

        Args:
            directed (bool): Define si el grafo completo se tratará como dirigido o no.
        """
        self.directed = directed
        # Usaremos un diccionario como lista de adyacencia: {Node: [Edge, Edge, ...]}
        self.graph = {}

    def add_node(self, node: Node) -> None:
        """Agrega un nodo al grafo si no existe previamente."""
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, edge: Edge) -> None:
        """Agrega una arista al grafo, asegurando que los nodos existan."""
        node1 = edge.get_node1()
        node2 = edge.get_node2()

        # Nos aseguramos de que ambos nodos existan en el diccionario
        self.add_node(node1)
        self.add_node(node2)

        # Agregamos la arista a la lista de adyacencia del nodo origen
        self.graph[node1].append(edge)

        # Si el grafo es no dirigido, agregamos la conexión inversa automáticamente
        if not self.directed and not edge.is_directed():
            reverse_edge = Edge(node2, node1, edge.get_weight(), directed=False)
            self.graph[node2].append(reverse_edge)

    def get_nodes(self) -> list:
        """Devuelve una lista con todos los nodos del grafo."""
        return list(self.graph.keys())

    def get_neighbors(self, node: Node) -> list:
        """Devuelve una lista de nodos vecinos al nodo dado."""
        if node in self.graph:
            return [edge.get_node2() for edge in self.graph[node]]
        raise ValueError(f"El nodo {node.get_name()} no existe en el grafo.")

    def _clear_graph(self):
        """Limpia el grafo actual para generar uno nuevo."""
        self.graph = {}

    # =====================================================================
    # MODELOS DE GENERACIÓN
    # =====================================================================

    def generate_mesh(self, rows:int, cols: int, weighted: bool = False):
        """
        Genera un grafo tipo malla (grid) de m x n.
        """
        self._clear_graph()
        nodes_matrix = []

        # 1. Crear nodos
        for r in range(rows):
            row_nodes = []
            for c in range(cols):
                node = Node(f"({r},{c})")
                self.add_node(node)
                row_nodes.append(node)
            nodes_matrix.append(row_nodes)

        # 2. Crear aristas (conexiones horizontales y verticales)
        for r in range(rows):
            for c in range(cols):
                weight = random.uniform(1, 10) if weighted else 1.0

                # Conexión horizontal
                if c + 1 < cols:
                    self.add_edge(Edge(nodes_matrix[r][c], nodes_matrix[r][c + 1], weight, self.directed))

                # Conexión vertical
                if r + 1 < rows:
                    self.add_edge(Edge(nodes_matrix[r][c], nodes_matrix[r + 1][c], weight, self.directed))


    def generate_erdos_renyi(self, n: int, m: int, weighted: bool = False):
        """
        Modelo de Erdös y Rényi: Elige m aristas al azar de entre todos los pares posibles.
        """
        self._clear_graph()
        if m > n * (n - 1) / (1 if self.directed else 2):
            raise ValueError("m supera el número máximo de aristas posibles.")

        # Crear n nodos
        nodes = [Node(f"Node_{i}") for i in range(n)]
        for node in nodes:
            self.add_node(node)

        # Generar todos los pares posibles y elegir m al azar
        all_possible_edges = list(combinations(nodes, 2))
        selected_edges = random.sample(all_possible_edges, m)

        for u, v in selected_edges:
            weight = random.uniform(1, 10) if weighted else 1.0
            self.add_edge(Edge(u, v, weight, self.directed))


    def generate_gilbert(self, n: int, p: float, weighted: bool = False):
        """
        Modelo de Gilbert: Cada par de nodos se conecta con una probabilidad p.
        """
        self._clear_graph()
        if not (0 <= p <= 1):
            raise ValueError("La probabilidad p debe estar entre 0 y 1.")

        nodes = [Node(f"Node_{i}") for i in range(n)]
        for node in nodes:
            self.add_node(node)

        for u, v in combinations(nodes, 2):
            if random.random() < p:
                weight = random.uniform(1, 10) if weighted else 1.0
                self.add_edge(Edge(u, v, weight, self.directed))

    def generate_barabasi_albert_v2(self, n: int, d: int, weighted: bool = False):
        """
        Modelo de Barabási-Albert: Preferential Attachment.
        Los nuevos nodos se conectan a 'd' nodos existentes, prefiriendo aquellos con mayor grado.
        """
        self._clear_graph()
        if d < 1 or d >= n:
            raise ValueError("El grado d debe ser mayor que 0 y menor que la cantidad de nodos n.")

        nodes = [Node(f"Node_{i}") for i in range(n)]

        # 1. Empezamos con un grafo completo de 'd' nodos
        for i in range(d):
            self.add_node(nodes[i])

        for i, j in combinations(range(d), 2):
            weight = random.uniform(1, 10) if weighted else 1.0
            self.add_edge(Edge(nodes[i], nodes[j], weight, self.directed))

        # Lista de probabilidad ponderada para Preferential Attachment
        # Un nodo aparece en esta lista tantas veces como conexiones tenga
        target_list = []
        for node in self.graph:
            # Multiplicamos la aparición del nodo por su número de conexiones actuales
            target_list.extend([node] * len(self.graph[node]))

        # 2. Agregamos el resto de los nodos
        for i in range(d, n):
            new_node = nodes[i]
            self.add_node(new_node)

            # Seleccionamos 'd' nodos destino únicos basados en su popularidad
            targets = set()
            while len(targets) < d:
                targets.add(random.choice(target_list))

            for target in targets:
                weight = random.uniform(1, 10) if weighted else 1.0
                self.add_edge(Edge(new_node, target, weight, self.directed))

                # Actualizamos las probabilidades (ambos nodos ganan una conexión)
                target_list.append(new_node)
                target_list.append(target)

    def generate_barabasi_albert(self, n: int, d: int, weighted: bool = False):
        """
        Versión 2 del modelo Barabási-Albert (Basado en la lógica original del usuario).
        Utiliza una probabilidad p = 1 - (grado / d) para limitar el crecimiento
        según un grado máximo d.
        """
        self._clear_graph()
        if n < 2 or d < 1:
            raise ValueError("n debe ser >= 2 y d >= 1")

        # 1. Crear todos los nodos primero
        nodes = [Node(f"Node_{i}") for i in range(n)]
        for node in nodes:
            self.add_node(node)

        # 2. Iterar para crear conexiones siguiendo tu lógica
        for i in range(1, n):
            current_node = nodes[i]

            # Obtenemos los nodos creados anteriormente y los mezclamos
            previous_nodes = nodes[:i]
            random.shuffle(previous_nodes)

            for target_node in previous_nodes:
                # Calculamos grados actuales
                # (len de la lista de adyacencia en nuestro diccionario self.graph)
                degree_target = len(self.graph[target_node])
                degree_current = len(self.graph[current_node])

                # Tu lógica de probabilidad: p = 1 - (grado_actual / d)
                p = 1 - (degree_target / d)

                if random.random() < p:
                    # Verificamos que ambos tengan espacio según el grado máximo d
                    if degree_current < d and degree_target < d:
                        weight = random.uniform(1, 10) if weighted else 1.0
                        self.add_edge(Edge(current_node, target_node, weight, self.directed))

                        # Actualizamos el grado del nodo actual para la siguiente iteración del loop interno
                        degree_current += 1

    def generate_dorogovtsev_mendes(self, n: int, weighted: bool = False):
        """
        Modelo de Dorogovtsev-Mendes.
        Comienza con un triángulo. Cada nuevo nodo se conecta a los dos extremos de una arista aleatoria.
        """
        self._clear_graph()
        if n < 3:
            raise ValueError("Se requieren al menos 3 nodos para iniciar el triángulo.")

        nodes = [Node(f"Node_{i}") for i in range(n)]
        for i in range(3):
            self.add_node(nodes[i])

        edges_list = []

        def add_dm_edge(u, v):
            weight = random.uniform(1, 10) if weighted else 1.0
            self.add_edge(Edge(u, v, weight, self.directed))
            edges_list.append((u, v))

        # Crear triángulo inicial
        add_dm_edge(nodes[0], nodes[1])
        add_dm_edge(nodes[1], nodes[2])
        add_dm_edge(nodes[2], nodes[0])

        # Agregar el resto de nodos
        for i in range(3, n):
            new_node = nodes[i]
            self.add_node(new_node)

            # Elegir una arista al azar de las existentes
            u, v = random.choice(edges_list)

            # Conectar el nuevo nodo a los extremos de la arista elegida
            add_dm_edge(new_node, u)
            add_dm_edge(new_node, v)

    def generate_simple_geographic(self, n: int, r: float, weighted: bool = False):
        """
        Modelo Geográfico Simple.
        Se colocan n nodos en un plano unitario [0,1]. Si la distancia Euclidiana es <= r, se conectan.
        """
        self._clear_graph()
        if not (0 <= r <= 1.4143):  # La máxima distancia en un cuadrado unitario es ~1.4142 (sqrt(2))
            raise ValueError("El radio r debe estar entre 0 y la raíz cuadrada de 2 (~1.4142).")

        nodes = []
        for i in range(n):
            # ¡Aquí guardamos las coordenadas dentro del nodo usando los **kwargs!
            pos_x, pos_y = random.random(), random.random()
            node = Node(f"Node_{i}", x=pos_x, y=pos_y)
            nodes.append(node)
            self.add_node(node)

        # Evaluar la distancia entre todos los pares posibles
        for u, v in combinations(nodes, 2):
            dx = u.attributes['x'] - v.attributes['x']
            dy = u.attributes['y'] - v.attributes['y']
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance <= r:
                weight = random.uniform(1, 10) if weighted else 1.0
                self.add_edge(Edge(u, v, weight, self.directed))

    # =====================================================================
    # ALGORITMOS DE BÚSQUEDA (Devuelven un nuevo Graph)
    # =====================================================================

    def _get_node_by_name(self, name: str) -> Node:
        """Función auxiliar para buscar un nodo por su nombre en el diccionario."""
        for node in self.graph:
            if node.get_name() == str(name):
                return node
        raise ValueError(f"El nodo '{name}' no existe en el grafo.")

    def bfs(self, start_node_name: str) -> 'Graph':
        """
        Búsqueda en Anchura (Breadth-First Search).
        Retorna un nuevo Grafo (árbol dirigido) con el recorrido.
        """
        start_node = self._get_node_by_name(start_node_name)
        tree = Graph(directed=True)  # Los árboles de búsqueda suelen ser dirigidos
        tree.add_node(start_node)

        visited = {start_node}
        queue = [start_node]

        while queue:
            current = queue.pop(0)

            for edge in self.graph[current]:
                neighbor = edge.get_node2()
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

                    # Añadimos al árbol de resultados conservando el peso
                    tree.add_node(neighbor)
                    tree.add_edge(Edge(current, neighbor, edge.get_weight(), directed=True))

        return tree

    def dfs_iterative(self, start_node_name: str) -> 'Graph':
        """
        Búsqueda en Profundidad Iterativa (Depth-First Search Iterative).
        Retorna un nuevo Grafo (árbol dirigido) con el recorrido.
        """
        start_node = self._get_node_by_name(start_node_name)
        tree = Graph(directed=True)
        tree.add_node(start_node)

        visited = set()
        # Guardamos tuplas: (Nodo_Padre, Nodo_Actual, Peso_Arista)
        stack = [(None, start_node, 1.0)]

        while stack:
            parent, current, weight = stack.pop()

            if current not in visited:
                visited.add(current)
                tree.add_node(current)

                if parent is not None:
                    tree.add_edge(Edge(parent, current, weight, directed=True))

                # Para mantener el orden convencional, invertimos los vecinos antes de apilar
                neighbors_edges = list(self.graph[current])
                for edge in reversed(neighbors_edges):
                    neighbor = edge.get_node2()
                    if neighbor not in visited:
                        stack.append((current, neighbor, edge.get_weight()))

        return tree

    def dfs_recursive(self, start_node_name: str) -> 'Graph':
        """
        Búsqueda en Profundidad Recursiva (Depth-First Search Recursive).
        Retorna un nuevo Grafo (árbol dirigido) con el recorrido.
        """
        start_node = self._get_node_by_name(start_node_name)
        tree = Graph(directed=True)
        visited = set()

        def _dfs(parent, current, weight):
            if current not in visited:
                visited.add(current)
                tree.add_node(current)

                if parent is not None:
                    tree.add_edge(Edge(parent, current, weight, directed=True))

                for edge in self.graph[current]:
                    neighbor = edge.get_node2()
                    if neighbor not in visited:
                        _dfs(current, neighbor, edge.get_weight())

        _dfs(None, start_node, 1.0)
        return tree

    # =====================================================================
    # CALCULAR COSTO TOTAL
    # =====================================================================

    def get_total_cost(self) -> float:
        """
        Calcula la suma de los pesos de todas las aristas en el grafo.
        """
        total_cost = 0.0
        edges_counted = set()

        for node, edges in self.graph.items():
            for edge in edges:
                n1 = edge.get_node1().get_name()
                n2 = edge.get_node2().get_name()

                # Firma única para evitar sumar la arista de ida y de vuelta en grafos no dirigidos
                edge_sig = tuple(sorted([n1, n2])) if not self.directed else (n1, n2)

                if edge_sig not in edges_counted:
                    total_cost += edge.get_weight()
                    edges_counted.add(edge_sig)

        return total_cost

    # =====================================================================
    # ALGORITMO DE DIJKSTRA
    # =====================================================================

    def dijkstra(self, start_node_name: str) -> 'Graph':
        """
        Algoritmo de Dijkstra para encontrar los caminos más cortos desde un nodo fuente.
        Retorna un nuevo Grafo (árbol) donde los nombres de los nodos incluyen la distancia.
        """
        start_node = self._get_node_by_name(start_node_name)

        # distancias = {nodo_objeto: valor_float}
        distances = {node: float('inf') for node in self.graph}
        distances[start_node] = 0

        # parent_map = {nodo_hijo: (nodo_padre, peso_arista)}
        parent_map = {node: None for node in self.graph}

        # Priority Queue: (distancia, id_unico_para_desempate, nodo_objeto)
        # Usamos id(node) para evitar que heapq compare los objetos Node directamente
        pq = [(0, id(start_node), start_node)]

        while pq:
            current_distance, _, u = heapq.heappop(pq)

            if current_distance > distances[u]:
                continue

            for edge in self.graph[u]:
                v = edge.get_node2()
                weight = edge.get_weight()
                distance = current_distance + weight

                if distance < distances[v]:
                    distances[v] = distance
                    parent_map[v] = (u, weight)
                    heapq.heappush(pq, (distance, id(v), v))

        # Construcción del árbol resultante
        tree = Graph(directed=True)

        # Creamos un diccionario para mapear objetos originales a sus nuevos nodos con etiqueta de distancia
        new_nodes_map = {}
        for node, dist in distances.items():
            if dist != float('inf'):
                # Formateamos el nombre: "Nombre (Distancia)"
                label_name = f"{node.get_name()} ({dist:.2f})"
                new_node = Node(label_name)
                tree.add_node(new_node)
                new_nodes_map[node] = new_node

        # Añadimos las aristas al árbol
        for child_node, info in parent_map.items():
            if info is not None:
                parent_node, weight = info
                u_tree = new_nodes_map[parent_node]
                v_tree = new_nodes_map[child_node]
                tree.add_edge(Edge(u_tree, v_tree, weight, directed=True))

        return tree

    # =====================================================================
    # ALGORITMOS DE MST
    # =====================================================================

    def _get_unique_edges(self):
        unique_edges = []
        seen = set()
        for node in self.graph:
            for edge in self.graph[node]:
                u, v = edge.get_node1().get_name(), edge.get_node2().get_name()
                sig = tuple(sorted((u, v))) if not self.directed else (u, v)
                if sig not in seen:
                    unique_edges.append(edge)
                    seen.add(sig)
        return unique_edges

    def _count_components(self) -> int:
        """
        Cuenta el número de componentes conexos (islas) en el grafo.
        Reemplaza a _is_connected para soportar grafos desconectados.
        """
        visited = set()
        components = 0
        for node in self.graph:
            if node.get_name() not in visited:
                components += 1
                queue = [node]
                visited.add(node.get_name())
                while queue:
                    curr = queue.pop(0)
                    for edge in self.graph[curr]:
                        neighbor = edge.get_node2()
                        if neighbor.get_name() not in visited:
                            visited.add(neighbor.get_name())
                            queue.append(neighbor)
        return components

    def _remove_edge(self, u_name: str, v_name: str):
        for node in self.graph:
            if node.get_name() == u_name:
                self.graph[node] = [e for e in self.graph[node] if e.get_node2().get_name() != v_name]
            if not self.directed and node.get_name() == v_name:
                self.graph[node] = [e for e in self.graph[node] if e.get_node2().get_name() != u_name]

    def copy(self):
        new_graph = Graph(directed=self.directed)
        nodes_map = {}
        for node in self.graph:
            new_node = Node(node.get_name(), **node.attributes)
            new_graph.add_node(new_node)
            nodes_map[node.get_name()] = new_node
        for node, edges in self.graph.items():
            for edge in edges:
                u = nodes_map[edge.get_node1().get_name()]
                v = nodes_map[edge.get_node2().get_name()]
                new_graph.add_edge(Edge(u, v, edge.get_weight(), self.directed))
        return new_graph

    def KruskalD(self) -> 'Graph':
        """Kruskal Directo: Agrega aristas más baratas que no formen ciclos."""
        mst = Graph(directed=self.directed)
        for node in self.graph:
            mst.add_node(Node(node.get_name()))

        edges = self._get_unique_edges()
        edges.sort(key=lambda x: x.get_weight())

        parent = {node.get_name(): node.get_name() for node in self.graph}

        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False

        for edge in edges:
            u, v = edge.get_node1(), edge.get_node2()
            if union(u.get_name(), v.get_name()):
                mst.add_edge(Edge(mst._get_node_by_name(u.get_name()),
                                  mst._get_node_by_name(v.get_name()),
                                  edge.get_weight(), self.directed))
        return mst

    def KruskalI(self) -> 'Graph':
        """Kruskal Inverso adaptado para Bosques de Expansión Mínima."""
        mst = self.copy()
        edges = mst._get_unique_edges()
        edges.sort(key=lambda x: x.get_weight(), reverse=True)

        # Guardamos cuántas islas tiene el grafo originalmente
        initial_components = mst._count_components()

        for edge in edges:
            u, v = edge.get_node1().get_name(), edge.get_node2().get_name()
            weight = edge.get_weight()
            mst._remove_edge(u, v)

            # Si quitar la arista crea MÁS islas, la arista era vital y la regresamos
            if mst._count_components() > initial_components:
                mst.add_edge(Edge(mst._get_node_by_name(u), mst._get_node_by_name(v), weight, self.directed))

        return mst

    def Prim(self) -> 'Graph':
        """Algoritmo de Prim adaptado para Bosques de Expansión Mínima."""
        mst = Graph(directed=self.directed)
        # Añadimos todos los nodos para que no se pierdan los aislados
        for node in self.graph:
            mst.add_node(Node(node.get_name()))

        visited = set()

        # Iteramos por TODOS los nodos para asegurarnos de explorar todas las islas
        for node in self.graph:
            if node.get_name() not in visited:
                visited.add(node.get_name())
                pq = []

                def push_edges(curr_node):
                    for edge in self.graph[curr_node]:
                        if edge.get_node2().get_name() not in visited:
                            heapq.heappush(pq, (edge.get_weight(), id(edge), edge))

                push_edges(node)

                while pq:
                    weight, _, edge = heapq.heappop(pq)
                    u, v = edge.get_node1(), edge.get_node2()

                    if v.get_name() not in visited:
                        visited.add(v.get_name())
                        mst.add_edge(Edge(mst._get_node_by_name(u.get_name()),
                                          mst._get_node_by_name(v.get_name()),
                                          weight, self.directed))
                        push_edges(v)
        return mst

    # =====================================================================
    # EXPORTACIÓN
    # =====================================================================

    def to_file_gv(self, filename: str, show_names: bool = True, show_weights: bool = False) -> None:
        """
        Exporta el grafo a un archivo .gv para Graphviz.

        Args:
            filename (str): Nombre del archivo (sin extensión).
            show_names (bool): Si es True, muestra el nombre de los nodos. Si es False, los oculta.
            show_weights (bool): Si es True, muestra el peso en las aristas.
        """
        # Crear la carpeta Results si no existe
        os.makedirs("Results", exist_ok=True)
        filepath = os.path.join("Results", f"{filename}.gv")

        graph_type = "digraph" if self.directed else "graph"
        connector = "->" if self.directed else "--"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{graph_type} {filename} {{\n")

            # Escribir nodos
            for node in self.graph:
                label = node.get_name() if show_names else ""
                f.write(f'    "{node.get_name()}" [label="{label}"];\n')

            # Escribir aristas (usamos un set para no duplicar visualmente en grafos no dirigidos)
            edges_written = set()
            for node, edges in self.graph.items():
                for edge in edges:
                    n1_name = edge.get_node1().get_name()
                    n2_name = edge.get_node2().get_name()

                    # Crear una firma única para la arista para evitar duplicados en no dirigidos
                    edge_sig = tuple(sorted([n1_name, n2_name])) if not self.directed else (n1_name, n2_name)

                    if edge_sig not in edges_written:
                        weight_label = f' [label="{edge.get_weight()}"]' if show_weights else ""
                        f.write(f'    "{n1_name}" {connector} "{n2_name}"{weight_label};\n')
                        edges_written.add(edge_sig)

            f.write("}\n")
        print(f"Archivo exportado exitosamente en: {filepath}")

    # =====================================================================
    # VISUALIZACIÓN PYGAME (Algoritmo Spring - Eades 1984)
    # =====================================================================

    def randomize_positions(self, width: int, height: int):
        """Asigna coordenadas (x, y) aleatorias a todos los nodos."""
        for node in self.graph:
            # Usamos los kwargs del nodo para guardar la posición
            node.attributes['x'] = random.uniform(50, width - 50)
            node.attributes['y'] = random.uniform(50, height - 50)

    def spring_layout_step(self, width: int, height: int,
                           c1: float = 20.0, c2: float = 100.0,
                           c3: float = 10000.0, c4: float = 0.1):
        """
        Calcula y aplica una iteración del algoritmo de P. Eades.
        Args:
            c1: Multiplicador de atracción (fuerza del resorte).
            c2: Longitud natural del resorte (distancia ideal entre nodos unidos).
            c3: Multiplicador de repulsión (qué tanto se odian los nodos no unidos).
            c4: Tamaño del paso o "temperatura" (qué tan rápido se mueven).
        """
        displacements = {node: [0.0, 0.0] for node in self.graph}
        nodes = list(self.graph.keys())

        # 1. Calcular Fuerza de Repulsión (Todos contra todos)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]

                dx = v.attributes['x'] - u.attributes['x']
                dy = v.attributes['y'] - u.attributes['y']
                dist_sq = dx * dx + dy * dy

                if dist_sq < 0.0001:  # Evitar división por cero
                    dist_sq = 0.0001
                    dx, dy = random.random(), random.random()

                dist = math.sqrt(dist_sq)

                # Fórmula de Eades: Repulsión = c3 / dist^2
                force_rep = c3 / dist_sq

                fx = (dx / dist) * force_rep
                fy = (dy / dist) * force_rep

                # u es empujado alejándose de v, y v alejándose de u
                displacements[u][0] -= fx
                displacements[u][1] -= fy
                displacements[v][0] += fx
                displacements[v][1] += fy

        # 2. Calcular Fuerza de Atracción (Solo nodos conectados por aristas)
        edges = self._get_unique_edges()
        for edge in edges:
            u = self._get_node_by_name(edge.get_node1().get_name())
            v = self._get_node_by_name(edge.get_node2().get_name())

            dx = v.attributes['x'] - u.attributes['x']
            dy = v.attributes['y'] - u.attributes['y']
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < 0.0001: dist = 0.0001

            # Fórmula de Eades: Atracción = c1 * log(dist / c2)
            force_att = c1 * math.log(dist / c2)

            fx = (dx / dist) * force_att
            fy = (dy / dist) * force_att

            # u es atraído hacia v, y v hacia u
            displacements[u][0] += fx
            displacements[u][1] += fy
            displacements[v][0] -= fx
            displacements[v][1] -= fy

        # 3. Aplicar los desplazamientos a las posiciones
        for node in self.graph:
            node.attributes['x'] += displacements[node][0] * c4
            node.attributes['y'] += displacements[node][1] * c4

            # Mantener los nodos dentro de los límites de la pantalla
            #node.attributes['x'] = max(20, min(width-20, node.attributes['x']))
            #node.attributes['y'] = max(20, min(height-20, node.attributes['y']))

    # =====================================================================
    # FORCE-DIRECTED LAYOUTS (Fruchterman-Reingold & Barnes-Hut)
    # =====================================================================

    def fr_step(self, width: int, height: int, temp: float, k: float):
        """Fruchterman-Reingold estándar O(n^2)."""
        displacements = {node: [0.0, 0.0] for node in self.graph}
        nodes = list(self.graph.keys())

        # 1. Fuerzas de Repulsión (Todos contra todos)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                dx = v.attributes['x'] - u.attributes['x']
                dy = v.attributes['y'] - u.attributes['y']
                dist = math.hypot(dx, dy)

                if dist < 0.0001:
                    dist, dx, dy = 0.0001, random.random(), random.random()

                force_rep = (k * k) / dist
                fx, fy = (dx / dist) * force_rep, (dy / dist) * force_rep

                displacements[u][0] -= fx
                displacements[u][1] -= fy
                displacements[v][0] += fx
                displacements[v][1] += fy

        # 2. Fuerzas de Atracción (Solo aristas)
        for edge in self._get_unique_edges():
            u = self._get_node_by_name(edge.get_node1().get_name())
            v = self._get_node_by_name(edge.get_node2().get_name())
            dx = v.attributes['x'] - u.attributes['x']
            dy = v.attributes['y'] - u.attributes['y']
            dist = math.hypot(dx, dy)
            if dist < 0.0001: dist = 0.0001

            force_att = (dist * dist) / k
            fx, fy = (dx / dist) * force_att, (dy / dist) * force_att

            displacements[u][0] += fx
            displacements[u][1] += fy
            displacements[v][0] -= fx
            displacements[v][1] -= fy

        # 3. Aplicar desplazamiento limitado por la "Temperatura"
        self._apply_displacements(displacements, temp, width, height)

    def fr_barnes_hut_step(self, width: int, height: int, temp: float, k: float, theta: float = 0.5):
        """Fruchterman-Reingold optimizado con Barnes-Hut O(n log n)."""
        displacements = {node: [0.0, 0.0] for node in self.graph}
        nodes = list(self.graph.keys())

        # 1. Construir QuadTree para la repulsión
        qt = QuadNode(0, 0, width, height)
        for node in nodes:
            qt.insert(node)

        # Función recursiva para calcular la repulsión usando Barnes-Hut
        def calculate_bh_repulsion(u_node, q_node):
            if q_node.mass == 0:
                return

            dx = q_node.cm_x - u_node.attributes['x']
            dy = q_node.cm_y - u_node.attributes['y']
            dist = math.hypot(dx, dy)

            if dist < 0.0001:
                dist, dx, dy = 0.0001, random.random(), random.random()

            # Si es hoja, o si está lo suficientemente lejos (aproximación)
            if (not q_node.children) or (q_node.size / dist < theta):
                if q_node.graph_node != u_node:
                    # Multiplicar la repulsión por la masa del cuadrante
                    force_rep = ((k * k) / dist) * q_node.mass
                    displacements[u_node][0] -= (dx / dist) * force_rep
                    displacements[u_node][1] -= (dy / dist) * force_rep
            else:
                for child in q_node.children:
                    calculate_bh_repulsion(u_node, child)

        # 2. Calcular repulsión
        for node in nodes:
            calculate_bh_repulsion(node, qt)

        # 3. Fuerzas de Atracción (Igual que el estándar)
        for edge in self._get_unique_edges():
            u = self._get_node_by_name(edge.get_node1().get_name())
            v = self._get_node_by_name(edge.get_node2().get_name())
            dx = v.attributes['x'] - u.attributes['x']
            dy = v.attributes['y'] - u.attributes['y']
            dist = math.hypot(dx, dy)
            if dist < 0.0001: dist = 0.0001

            force_att = (dist * dist) / k
            fx, fy = (dx / dist) * force_att, (dy / dist) * force_att

            displacements[u][0] += fx
            displacements[u][1] += fy
            displacements[v][0] -= fx
            displacements[v][1] -= fy

        # 4. Aplicar desplazamiento
        self._apply_displacements(displacements, temp, width, height)

    def _apply_displacements(self, displacements: dict, temp: float, width: int, height: int):
        """Aplica las fuerzas calculadas limitadas por la temperatura."""
        for node in self.graph:
            dx, dy = displacements[node]
            disp_len = math.hypot(dx, dy)

            if disp_len > 0:
                limited_disp = min(disp_len, temp)
                node.attributes['x'] += (dx / disp_len) * limited_disp
                node.attributes['y'] += (dy / disp_len) * limited_disp

            # Mantener en la pantalla dejando un margen
            #node.attributes['x'] = max(30, min(width - 30, node.attributes['x']))
            #node.attributes['y'] = max(30, min(height - 30, node.attributes['y']))


class QuadNode:
    """Clase auxiliar para el QuadTree de Barnes-Hut."""

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, depth: int = 0):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.x_mid = (x_min + x_max) / 2
        self.y_mid = (y_min + y_max) / 2
        self.size = max(x_max - x_min, y_max - y_min)

        # --- Control de profundidad ---
        self.depth = depth
        self.MAX_DEPTH = 25
        # -------------------------------------

        self.mass = 0
        self.cm_x = 0.0
        self.cm_y = 0.0
        self.graph_node = None
        self.children = []

    def insert(self, node):
        nx, ny = node.attributes['x'], node.attributes['y']

        # --- Jitter (Ruido para evitar superposición exacta) ---
        if self.mass == 1 and self.graph_node is not None:
            gx, gy = self.graph_node.attributes['x'], self.graph_node.attributes['y']
            if abs(gx - nx) < 0.001 and abs(gy - ny) < 0.001:
                # Desplazar ligeramente el nuevo nodo
                nx += random.uniform(-0.1, 0.1)
                ny += random.uniform(-0.1, 0.1)
                node.attributes['x'] = nx
                node.attributes['y'] = ny
        # -------------------------------------------------------------

        # Actualizar centro de masa
        self.cm_x = (self.cm_x * self.mass + nx) / (self.mass + 1)
        self.cm_y = (self.cm_y * self.mass + ny) / (self.mass + 1)
        self.mass += 1

        # Si es hoja vacía
        if self.mass == 1:
            self.graph_node = node
            return

        # Si hay un nodo aquí, subdividimos
        if not self.children:
            # --- Evitar recursión infinita ---
            if self.depth < self.MAX_DEPTH:
                self._subdivide()
                if self.graph_node:
                    self._insert_into_children(self.graph_node)
                    self.graph_node = None
            else:
                # Si llegamos al límite máximo, los agrupamos juntos
                return

        if self.children:
            self._insert_into_children(node)

    def _subdivide(self):
        # Aumentamos la profundidad al crear hijos
        self.children = [
            QuadNode(self.x_min, self.y_min, self.x_mid, self.y_mid, self.depth + 1),  # NW
            QuadNode(self.x_mid, self.y_min, self.x_max, self.y_mid, self.depth + 1),  # NE
            QuadNode(self.x_min, self.y_mid, self.x_mid, self.y_max, self.depth + 1),  # SW
            QuadNode(self.x_mid, self.y_mid, self.x_max, self.y_max, self.depth + 1)  # SE
        ]

    def _insert_into_children(self, node):
        nx, ny = node.attributes['x'], node.attributes['y']
        if nx < self.x_mid:
            if ny < self.y_mid:
                self.children[0].insert(node)
            else:
                self.children[2].insert(node)
        else:
            if ny < self.y_mid:
                self.children[1].insert(node)
            else:
                self.children[3].insert(node)