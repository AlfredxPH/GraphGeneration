"""
Programa:               | Grafos -- Versión 1
Programador:            | Alfredo Peña Hernández
Descripcion:            | Biblioteca para describir y utilizar Grafos.
Fecha de creacion:      | 05/03/2026
Última actualizacción:  | 10/03/2026
Revision:               | Ninguna
"""

from Models.MeshModel import *
from Models.ErReModel import *
from Models.GilbertModel import *
from Models.SimGeoModel import *
from Models.BAModelV import *
from Models.DMModel import *

cantiad_nodos = [50, 200, 500]
# =========================================================
# Primer Modelo: Modelo de Malla.
# =========================================================
d = 5
for i in cantiad_nodos:
    G = build_mesh_model(UndirectedGraph, int(i/d), d, diagonal=True)
    G.to_file_gv("MeshModel", "X", str(i))
    d *= 2

# =========================================================
# Segundo Modelo: Modelo de Erdös y Rényi.
# =========================================================
for i in cantiad_nodos:
    m_edges = int(((i*(i-1))/2)*0.1)
    G = build_erre_model(UndirectedGraph, i, m_edges)
    G.to_file_gv("ErReModel", "X", str(i)+'-'+str(m_edges))

# =========================================================
# Tercer Modelo: Modelo de Gilbert
# =========================================================
for i in cantiad_nodos:
    p = 0.1
    G = build_gilbert_model(UndirectedGraph, i, p)
    G.to_file_gv("GilbertModel", "X", str(i)+'-'+str(p))

# =========================================================
# Cuarto Modelo: Modelo Geográfico Simple
# =========================================================
for i in cantiad_nodos:
    r = 0.2
    G = build_simgeo_model(UndirectedGraph, i, r)
    G.to_file_gv("SimGeoModel", "X", str(i)+'-'+str(r))

# =========================================================
# Quinto Modelo: Variante del Modelo Barabási-Albert
# =========================================================
ds = [2,4,6]
for nodes, d in zip(cantiad_nodos,ds):
    G = build_barabasi_albert_model(UndirectedGraph, nodes, d)
    G.to_file_gv("Barabási-Albert", "X", f"{nodes}-{d}")

# =========================================================
# Sexto Modelo: Modelo Dorogovtsev-Mendes
# =========================================================
for nodes in cantiad_nodos:
    G = build_dorogovtsev_mendes_model(UndirectedGraph, nodes)
    G.to_file_gv("DorogovtsevMendesModel", "x", f"{nodes}")