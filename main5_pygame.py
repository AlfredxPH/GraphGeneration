import pygame
import sys
from Graphs import Graph


def run_visualization():
    pygame.init()
    WIDTH, HEIGHT = 1500, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Animación de Grafo - Algoritmo Spring (P. Eades)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    # Selección del generador de grafos
    g = Graph(directed=False)
    nodes = 500
    g.generate_simple_geographic(nodes, 0.2)
    g.randomize_positions(WIDTH, HEIGHT)

    running = True
    paused = False

    # Variables de Cámara
    zoom = 1.0
    pan_x, pan_y = 0.0, 0.0
    dragging = False
    last_mouse = (0, 0)

    # Helper para convertir coordenadas del mundo a la pantalla
    def to_screen(world_x, world_y):
        return int(world_x * zoom + pan_x), int(world_y * zoom + pan_y)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

            # --- EVENTOS DE CÁMARA ---
            elif event.type == pygame.MOUSEWHEEL:
                # Zoom centrado en el ratón
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = (mouse_x - pan_x) / zoom
                world_y = (mouse_y - pan_y) / zoom

                zoom += event.y * 0.1
                zoom = max(0.1, min(zoom, 10.0))  # Limitar zoom

                pan_x = mouse_x - world_x * zoom
                pan_y = mouse_y - world_y * zoom

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 2, 3):  # Izquierdo, Medio o Derecho
                    dragging = True
                    last_mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 2, 3):
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx = event.pos[0] - last_mouse[0]
                    dy = event.pos[1] - last_mouse[1]
                    pan_x += dx
                    pan_y += dy
                    last_mouse = event.pos

        if not paused:
            g.spring_layout_step(WIDTH, HEIGHT, c1=15.0, c2=80.0, c3=15000.0, c4=0.08)

        screen.fill((245, 245, 245))

        # Dibujar Aristas
        edge_width = max(1, int(2 * zoom))
        for edge in g._get_unique_edges():
            u = g._get_node_by_name(edge.get_node1().get_name())
            v = g._get_node_by_name(edge.get_node2().get_name())

            pos_u = to_screen(u.attributes['x'], u.attributes['y'])
            pos_v = to_screen(v.attributes['x'], v.attributes['y'])
            pygame.draw.line(screen, (150, 150, 150), pos_u, pos_v, edge_width)

        # Dibujar Nodos
        node_radius = max(2, int(10 * zoom))
        border_width = max(1, int(2 * zoom))
        for node in g.graph:
            pos_x, pos_y = to_screen(node.attributes['x'], node.attributes['y'])

            pygame.draw.circle(screen, (50, 150, 255), (pos_x, pos_y), node_radius)
            pygame.draw.circle(screen, (0, 0, 0), (pos_x, pos_y), node_radius, border_width)

            # Solo mostrar etiquetas si el zoom es lo suficientemente grande (evita el desorden)
            if zoom > 0.6:
                text = font.render(node.get_name(), True, (0, 0, 0))
                screen.blit(text, (pos_x - 20, pos_y - node_radius - 15))

        # Dibujar UI Fija
        instr_texts = [
            "Presiona ESPACIO para pausar/reanudar",
            "Rueda del ratón: Zoom",
            "Clic y arrastrar: Mover cámara"
        ]
        for i, text in enumerate(instr_texts):
            img = font.render(text, True, (100, 100, 100))
            screen.blit(img, (10, 10 + (i * 20)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_visualization()