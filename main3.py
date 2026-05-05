from Graphs import Graph


def run_dijkstra_tests():
    scenarios = [("pocos", 20), ("muchos", 100)]

    generators = [
        ("Mesh", lambda g, n: g.generate_mesh(int(n ** 0.5), int(n ** 0.5), weighted=True)),
        ("Erdos-Renyi", lambda g, n: g.generate_erdos_renyi(n, int(((n * (n - 1)) / 2) * 0.1), weighted=True)),
        ("Gilbert", lambda g, n: g.generate_gilbert(n, 0.1, weighted=True)),
        ("Barabasi-Albert-V1", lambda g, n: g.generate_barabasi_albert(n, 6, weighted=True)),
        #("Barabasi-Albert-V2", lambda g, n: g.generate_barabasi_albert_v2(n, 5, weighted=True)),
        ("Dorogovtsev-Mendes", lambda g, n: g.generate_dorogovtsev_mendes(n, weighted=True)),
        ("Geographic", lambda g, n: g.generate_simple_geographic(n, 0.2, weighted=True))
    ]

    for model_name, gen_func in generators:
        print(f"\n" + "=" * 50)
        print(f"MODELO: {model_name}")
        print("=" * 50)

        for label, size in scenarios:
            # 1. Crear y generar grafo base
            g = Graph(directed=False)
            gen_func(g, size)
            g.to_file_gv(f"DIJKSTRA_BASE_{model_name}_{label}", show_weights=True)

            # 2. Ejecutar Dijkstra
            start_node = "(0,0)" if model_name == "Mesh" else "Node_0"

            try:
                # El árbol que retorna Dijkstra es un objeto 'Graph'
                shortest_path_tree = g.dijkstra(start_node)

                # --- AQUÍ ESTÁ LA MODIFICACIÓN ---
                # Calculamos el costo total del árbol resultante
                total_cost = shortest_path_tree.get_total_cost()

                print(f"[{label.upper()}] Nodos: {size}")
                print(f"   > Costo total del árbol de caminos cortos: {total_cost:.2f}")
                # ---------------------------------

                # Guardamos el archivo .gv
                shortest_path_tree.to_file_gv(f"DIJKSTRA_TREE_{model_name}_{label}", show_weights=True)

            except Exception as e:
                print(f"   > Error procesando {model_name} ({label}): {e}")


if __name__ == "__main__":
    run_dijkstra_tests()