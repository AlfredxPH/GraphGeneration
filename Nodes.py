class Node:
    """
    Description:
    Permite inicializar un nuevo nodo

    Attributes:
        name (str): Primer nodo, dentro del grafo inicializado.

    Example:
        >>> N = Node(name)
    """
    def __init__(self, name: str):
        """
        Inicializa una nueva arista.
        """
        self.name = name

    def get_name(self) -> str:
        """
        Description:
        Extrae el nombre del Nodo del grafo inicializado.

        Args:
        Ninguno

        Returns:
            (str) El nombre del nodo del grafo inicializado.
        """
        return self.name

    def __str__(self):
        return self.name
