# =========================================================
# Modelos de generación de grafos aleatorios
# =========================================================
from Models.MeshModel import *
from Models.ErReModel import *
from Models.GilbertModel import *
from Models.SimGeoModel import *
from Models.BAModelV import *
from Models.DMModel import *

# =========================================================
# Algoritmos de busqueda profunda
# =========================================================
from Algorithms.BFS import BFS
from Algorithms.DFS_R import DFS_R
from Algorithms.DFS_I import DFS_I

cantiad_nodos = [30, 100, 500]
dirigido = False
if dirigido:
    text="FromDG"
else:
    text="FromUG"
# =========================================================
# Primer Modelo: Modelo de Malla.
# =========================================================
d = 5
for i in cantiad_nodos:
    if dirigido:
        G = build_mesh_model(Graph, int(i / d), d, diagonal=True)
    else:
        G = build_mesh_model(UndirectedGraph, int(i/d), d, diagonal=True)

    # Exportar el grafo original
    G.to_file_gv("MeshModel", "X", str(i))
    d *= 2

    # --- IMPLEMENTACIÓN DE LOS ALGORITMOS DE BÚSQUEDA ---

    # 1. Obtenemos los nodos del grafo.
    nodos_del_grafo = G.get_nodes()

    # Nos aseguramos de que el grafo no esté vacío para evitar errores
    if nodos_del_grafo:
        # Tomamos un nodo aleatorio
        nodo_inicial = random.choice(nodos_del_grafo)

        # 2. Búsqueda BFS
        bfs = BFS(G, nodo_inicial)
        arbol_bfs = bfs.search()
        # Exportamos el árbol resultante aprovechando tu metodo to_file_gv
        arbol_bfs.to_file_gv(f"BFS_MeshModel_{text}", "X", str(i),"SearchAlgorithms")

        # 3. Búsqueda DFS Recursivo
        dfs_r = DFS_R(G, nodo_inicial)
        arbol_dfs_r = dfs_r.search()
        arbol_dfs_r.to_file_gv(f"DFS_R_MeshModel_{text}", "X", str(i),"SearchAlgorithms")

        # 4. Búsqueda DFS Iterativo
        dfs_i = DFS_I(G, nodo_inicial)
        arbol_dfs_i = dfs_i.search()
        arbol_dfs_i.to_file_gv(f"DFS_I_MeshModel_{text}", "X", str(i),"SearchAlgorithms")

# =========================================================
# Segundo Modelo: Modelo de Erdös y Rényi.
# =========================================================
for i in cantiad_nodos:
    m_edges = int(((i*(i-1))/2)*0.1)
    if dirigido:
        G = build_erre_model(Graph, i, m_edges)
    else:
        G = build_erre_model(UndirectedGraph, i, m_edges)

    # Exportar el grafo original
    G.to_file_gv("ErReModel", "X", str(i)+'-'+str(m_edges))

    # --- IMPLEMENTACIÓN DE LOS ALGORITMOS DE BÚSQUEDA ---

    # 1. Obtenemos los nodos del grafo.
    nodos_del_grafo = G.get_nodes()

    # Nos aseguramos de que el grafo no esté vacío para evitar errores
    if nodos_del_grafo:
        # Tomamos un nodo aleatorio
        nodo_inicial = random.choice(nodos_del_grafo)

        # 2. Búsqueda BFS
        bfs = BFS(G, nodo_inicial)
        arbol_bfs = bfs.search()
        # Exportamos el árbol resultante aprovechando tu metodo to_file_gv
        arbol_bfs.to_file_gv(f"BFS_ErReModel_{text}", "X", str(i)+'-'+str(m_edges),"SearchAlgorithms")

        # 3. Búsqueda DFS Recursivo
        dfs_r = DFS_R(G, nodo_inicial)
        arbol_dfs_r = dfs_r.search()
        arbol_dfs_r.to_file_gv(f"DFS_R_ErReModel_{text}", "X", str(i)+'-'+str(m_edges),"SearchAlgorithms")

        # 4. Búsqueda DFS Iterativo
        dfs_i = DFS_I(G, nodo_inicial)
        arbol_dfs_i = dfs_i.search()
        arbol_dfs_i.to_file_gv(f"DFS_I_ErReModel_{text}", "X", str(i)+'-'+str(m_edges),"SearchAlgorithms")

# =========================================================
# Tercer Modelo: Modelo de Gilbert
# =========================================================
for i in cantiad_nodos:
    p = 0.1
    if dirigido:
        G = build_gilbert_model(Graph, i, p)
    else:
        G = build_gilbert_model(UndirectedGraph, i, p)

    # Exportar el grafo original
    G.to_file_gv("GilbertModel", "X", str(i)+'-'+str(p))

    # --- IMPLEMENTACIÓN DE LOS ALGORITMOS DE BÚSQUEDA ---

    # 1. Obtenemos los nodos del grafo.
    nodos_del_grafo = G.get_nodes()

    # Nos aseguramos de que el grafo no esté vacío para evitar errores
    if nodos_del_grafo:
        # Tomamos un nodo aleatorio
        nodo_inicial = random.choice(nodos_del_grafo)

        # 2. Búsqueda BFS
        bfs = BFS(G, nodo_inicial)
        arbol_bfs = bfs.search()
        # Exportamos el árbol resultante aprovechando tu metodo to_file_gv
        arbol_bfs.to_file_gv(f"BFS_GilbertModel_{text}", "X", str(i) + '-' + str(p),"SearchAlgorithms")

        # 3. Búsqueda DFS Recursivo
        dfs_r = DFS_R(G, nodo_inicial)
        arbol_dfs_r = dfs_r.search()
        arbol_dfs_r.to_file_gv(f"DFS_R_GilbertModel_{text}", "X", str(i) + '-' + str(p),"SearchAlgorithms")

        # 4. Búsqueda DFS Iterativo
        dfs_i = DFS_I(G, nodo_inicial)
        arbol_dfs_i = dfs_i.search()
        arbol_dfs_i.to_file_gv(f"DFS_I_GilbertModel_{text}", "X", str(i) + '-' + str(p),"SearchAlgorithms")

# =========================================================
# Cuarto Modelo: Modelo Geográfico Simple
# =========================================================
for i in cantiad_nodos:
    r = 0.2
    if dirigido:
        G = build_simgeo_model(Graph, i, r)
    else:
        G = build_simgeo_model(UndirectedGraph, i, r)

    # Exportar el grafo original
    G.to_file_gv("SimGeoModel", "X", str(i)+'-'+str(r))

    # --- IMPLEMENTACIÓN DE LOS ALGORITMOS DE BÚSQUEDA ---

    # 1. Obtenemos los nodos del grafo.
    nodos_del_grafo = G.get_nodes()

    # Nos aseguramos de que el grafo no esté vacío para evitar errores
    if nodos_del_grafo:
        # Tomamos un nodo aleatorio
        nodo_inicial = random.choice(nodos_del_grafo)

        # 2. Búsqueda BFS
        bfs = BFS(G, nodo_inicial)
        arbol_bfs = bfs.search()
        # Exportamos el árbol resultante aprovechando tu metodo to_file_gv
        arbol_bfs.to_file_gv(f"BFS_SimGeoModel_{text}", "X", str(i)+'-'+str(r),"SearchAlgorithms")

        # 3. Búsqueda DFS Recursivo
        dfs_r = DFS_R(G, nodo_inicial)
        arbol_dfs_r = dfs_r.search()
        arbol_dfs_r.to_file_gv(f"DFS_R_SimGeoModel_{text}", "X", str(i)+'-'+str(r),"SearchAlgorithms")

        # 4. Búsqueda DFS Iterativo
        dfs_i = DFS_I(G, nodo_inicial)
        arbol_dfs_i = dfs_i.search()
        arbol_dfs_i.to_file_gv(f"DFS_I_SimGeoModel_{text}", "X", str(i)+'-'+str(r),"SearchAlgorithms")

# =========================================================
# Quinto Modelo: Variante del Modelo Barabási-Albert
# =========================================================
ds = [2,4,6]
for nodes, d in zip(cantiad_nodos,ds):
    if dirigido:
        G = build_barabasi_albert_model(Graph, nodes, d)
    else:
        G = build_barabasi_albert_model(UndirectedGraph, nodes, d)

    # Exportar el grafo original
    G.to_file_gv("Barabási-Albert", "X", f"{nodes}-{d}")

    # --- IMPLEMENTACIÓN DE LOS ALGORITMOS DE BÚSQUEDA ---

    # 1. Obtenemos los nodos del grafo.
    nodos_del_grafo = G.get_nodes()

    # Nos aseguramos de que el grafo no esté vacío para evitar errores
    if nodos_del_grafo:
        # Tomamos un nodo aleatorio
        nodo_inicial = random.choice(nodos_del_grafo)

        # 2. Búsqueda BFS
        bfs = BFS(G, nodo_inicial)
        arbol_bfs = bfs.search()
        # Exportamos el árbol resultante aprovechando tu metodo to_file_gv
        arbol_bfs.to_file_gv(f"BFS_Barabási-Albert_{text}", "X", f"{nodes}-{d}","SearchAlgorithms")

        # 3. Búsqueda DFS Recursivo
        dfs_r = DFS_R(G, nodo_inicial)
        arbol_dfs_r = dfs_r.search()
        arbol_dfs_r.to_file_gv(f"DFS_R_Barabási-Albert_{text}", "X", f"{nodes}-{d}","SearchAlgorithms")

        # 4. Búsqueda DFS Iterativo
        dfs_i = DFS_I(G, nodo_inicial)
        arbol_dfs_i = dfs_i.search()
        arbol_dfs_i.to_file_gv(f"DFS_I_Barabási-Albert_{text}", "X", f"{nodes}-{d}","SearchAlgorithms")

# =========================================================
# Sexto Modelo: Modelo Dorogovtsev-Mendes
# =========================================================
for nodes in cantiad_nodos:
    if dirigido:
        G = build_dorogovtsev_mendes_model(Graph, nodes)
    else:
        G = build_dorogovtsev_mendes_model(UndirectedGraph, nodes)

    # Exportar el grafo original
    G.to_file_gv("DorogovtsevMendesModel", "x", f"{nodes}")

    # --- IMPLEMENTACIÓN DE LOS ALGORITMOS DE BÚSQUEDA ---

    # 1. Obtenemos los nodos del grafo.
    nodos_del_grafo = G.get_nodes()

    # Nos aseguramos de que el grafo no esté vacío para evitar errores
    if nodos_del_grafo:
        # Tomamos un nodo aleatorio
        nodo_inicial = random.choice(nodos_del_grafo)

        # 2. Búsqueda BFS
        bfs = BFS(G, nodo_inicial)
        arbol_bfs = bfs.search()
        # Exportamos el árbol resultante aprovechando tu metodo to_file_gv
        arbol_bfs.to_file_gv(f"BFS_DorogovtsevMendesModel_{text}", "x", f"{nodes}","SearchAlgorithms")

        # 3. Búsqueda DFS Recursivo
        dfs_r = DFS_R(G, nodo_inicial)
        arbol_dfs_r = dfs_r.search()
        arbol_dfs_r.to_file_gv(f"DFS_R_DorogovtsevMendesModel_{text}", "x", f"{nodes}","SearchAlgorithms")

        # 4. Búsqueda DFS Iterativo
        dfs_i = DFS_I(G, nodo_inicial)
        arbol_dfs_i = dfs_i.search()
        arbol_dfs_i.to_file_gv(f"DFS_I_DorogovtsevMendesModel_{text}", "x", f"{nodes}","SearchAlgorithms")
