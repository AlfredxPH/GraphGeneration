from Graphs import Graph

def run_search_tests():
    sizes = [30, 100, 500]

    # Lista de funciones de generación y sus nombres para iterar
    # Nota: Usamos lambdas para estandarizar la llamada a pesar de distintos parámetros
    generators = [
        ("Mesh",
         lambda g, s: g.generate_mesh(6, 5) if s == 30 else g.generate_mesh(10, 10) if s == 100 else g.generate_mesh(25,20)),
        ("Erdos-Renyi", lambda g, s: g.generate_erdos_renyi(s, int(((s * (s - 1)) / 2) * 0.1))),
        ("Gilbert", lambda g, s: g.generate_gilbert(s, 0.1)),
        ("Barabasi-Albert", lambda g, s: g.generate_barabasi_albert(s, 6)),
        ("Dorogovtsev-Mendes", lambda g, s: g.generate_dorogovtsev_mendes(s)),
        ("Geographic", lambda g, s: g.generate_simple_geographic(s, 0.2))
    ]

    for model_name, gen_func in generators:
        for size in sizes:
            print(f"Procesando {model_name} con {size} nodos...")

            # Crear y generar el grafo base (No dirigido)
            base_graph = Graph(directed=False)
            gen_func(base_graph, size)
            base_graph.to_file_gv(f"SEARCH_BASE_{model_name}_{size}")

            # Definir nodo de inicio (Malla usa coordenadas, otros usan Node_i)
            start_node = "(0,0)" if model_name == "Mesh" else "Node_0"

            # 1. BFS
            tree_bfs = base_graph.bfs(start_node)
            tree_bfs.to_file_gv(f"BFS_{model_name}_{size}")

            # 2. DFS Iterativo
            tree_dfsi = base_graph.dfs_iterative(start_node)
            tree_dfsi.to_file_gv(f"DFS_Iter_{model_name}_{size}")

            # 3. DFS Recursivo
            tree_dfsr = base_graph.dfs_recursive(start_node)
            tree_dfsr.to_file_gv(f"DFS_Rec_{model_name}_{size}")


if __name__ == "__main__":
    run_search_tests()