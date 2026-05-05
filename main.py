from Graphs import Graph

def run_generation_tests():
    # Definimos los modelos y sus parámetros para los tamaños 50, 200, 500
    # Para Malla, usaremos aproximaciones (10x5, 20x10, 25x20)
    sizes = [50, 200, 500]
    models = ["Mesh", "Erdos-Renyi", "Gilbert", "Barabasi-Albert", "Dorogovtsev-Mendes", "Geographic"]

    for size in sizes:
        print(f"--- Generando grafos de tamaño {size} ---")

        # 1. Malla
        g_mesh = Graph(directed=False)
        rows, cols = (10, 5) if size == 50 else (20, 10) if size == 200 else (25, 20)
        g_mesh.generate_mesh(rows, cols)
        g_mesh.to_file_gv(f"Mesh_{size}", show_names=True)

        # 2. Erdos-Renyi (m = n * 2 para que no sea muy ralo)
        g_er = Graph(directed=False)
        m_edges = int(((size * (size - 1)) / 2) * 0.1)
        g_er.generate_erdos_renyi(size, m_edges)
        g_er.to_file_gv(f"ErdosRenyi_{size}", show_names=False)

        # 3. Gilbert (p = 0.1)
        g_gi = Graph(directed=False)
        g_gi.generate_gilbert(size, 0.1)
        g_gi.to_file_gv(f"Gilbert_{size}", show_names=False)

        # 4. Barabasi-Albert (d = 6)
        g_ba = Graph(directed=False)
        g_ba.generate_barabasi_albert(size, 6)
        g_ba.to_file_gv(f"BarabasiAlbert_{size}", show_names=False)

        # 4.1. Barabasi-Albert_v2 (d = 4)
        g_ba = Graph(directed=False)
        g_ba.generate_barabasi_albert_v2(size, 6)
        g_ba.to_file_gv(f"BarabasiAlbertV2_{size}", show_names=False)

        # 5. Dorogovtsev-Mendes
        g_dm = Graph(directed=False)
        g_dm.generate_dorogovtsev_mendes(size)
        g_dm.to_file_gv(f"DorogovtsevMendes_{size}", show_names=False)

        # 6. Geográfico (r = 0.2)
        g_geo = Graph(directed=False)
        g_geo.generate_simple_geographic(size, 0.2)
        g_geo.to_file_gv(f"Geographic_{size}", show_names=False)


if __name__ == "__main__":
    run_generation_tests()