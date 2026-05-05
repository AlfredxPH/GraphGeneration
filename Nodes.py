class Node:
    """
    Representa un vértice/nodo dentro de un grafo.
    """

    def __init__(self, name: str, **kwargs):
        """
        Inicializa un nuevo nodo.

        Args:
            name (str): Identificador único del nodo.
            **kwargs: Atributos adicionales (ej. color, coordenadas x/y para PyGame).
        """
        self.name = str(name)
        self.attributes = kwargs

    def get_name(self) -> str:
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Node({self.name})"

    # Implementamos métodos de comparación para que los nodos puedan ser
    # usados fácilmente como llaves en diccionarios o elementos en sets.
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)