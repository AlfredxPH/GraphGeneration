from Graphs import Graph


def run_mst_tests():
    scenarios = [("pocos", 20), ("muchos", 100)]

    generators = [
        ("Mesh", lambda g, n: g.generate_mesh(int(n ** 0.5), int(n ** 0.5), weighted=True)),
        ("Erdos-Renyi", lambda g, n: g.generate_erdos_renyi(n, int(((n * (n - 1)) / 2) * 0.1), weighted=True)),
        ("Gilbert", lambda g, n: g.generate_gilbert(n, 0.1, weighted=True)),
        ("Barabasi-Albert-V1", lambda g, n: g.generate_barabasi_albert(n, 6, weighted=True)),
        #("Barabasi-Albert-V2", lambda g, n: g.generate_barabasi_albert_v2(n, 4, weighted=True)),
        ("Dorogovtsev-Mendes", lambda g, n: g.generate_dorogovtsev_mendes(n, weighted=True)),
        ("Geographic", lambda g, n: g.generate_simple_geographic(n, 0.2, weighted=True))
    ]

    for model_name, gen_func in generators:
        print(f"\n" + "=" * 60)
        print(f" ANALIZANDO MST: {model_name}")
        print("=" * 60)

        for label, size in scenarios:
            # 1. Grafo Base (Aseguramos que sea conexo para que el MST sea válido)
            g = Graph(directed=False)
            gen_func(g, size)

            # Nota: Si el grafo es ralo, el MST podría no incluir todos los nodos
            # si no es conexo de origen.
            g.to_file_gv(f"MST_BASE_{model_name}_{label}", show_weights=True)

            # 2. Ejecutar Algoritmos
            # Kruskal Directo
            kd = g.KruskalD()
            cost_kd = kd.get_total_cost()
            kd.to_file_gv(f"MST_KruskalD_{model_name}_{label}", show_weights=True)

            # Kruskal Inverso
            ki = g.KruskalI()
            cost_ki = ki.get_total_cost()
            ki.to_file_gv(f"MST_KruskalI_{model_name}_{label}", show_weights=True)

            # Prim
            pr = g.Prim()
            cost_pr = pr.get_total_cost()
            pr.to_file_gv(f"MST_Prim_{model_name}_{label}", show_weights=True)

            print(f"[{label.upper()}] Nodos: {size}")
            print(f"   > Costo Kruskal Directo: {cost_kd:.2f}")
            print(f"   > Costo Kruskal Inverso: {cost_ki:.2f}")
            print(f"   > Costo Prim:            {cost_pr:.2f}")
            print(f"   {'-' * 30}")


if __name__ == "__main__":
    run_mst_tests()