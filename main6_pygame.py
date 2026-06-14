import pygame
import sys
import math
from Graphs import Graph


def run_fr_visualization():
    pygame.init()
    WIDTH, HEIGHT = 1500, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualización de Grafos: Dirigido por Fuerzas")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    g = Graph(directed=False)
    num_nodes = 500
    g.generate_simple_geographic(num_nodes, 0.2)
    g.randomize_positions(WIDTH, HEIGHT)

    area = WIDTH * HEIGHT
    k = math.sqrt(area / num_nodes) * 0.75
    temp = WIDTH / 10.0
    mode = "EADES"

    # Variables de Cámara
    zoom = 1.0
    pan_x, pan_y = 0.0, 0.0
    dragging = False
    last_mouse = (0, 0)

    def to_screen(world_x, world_y):
        return int(world_x * zoom + pan_x), int(world_y * zoom + pan_y)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "EADES"
                elif event.key == pygame.K_2:
                    mode = "FR"
                elif event.key == pygame.K_3:
                    mode = "FR_BH"
                elif event.key == pygame.K_SPACE:
                    g.randomize_positions(WIDTH, HEIGHT)
                    temp = WIDTH / 10.0

            # --- EVENTOS DE CÁMARA ---
            elif event.type == pygame.MOUSEWHEEL:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = (mouse_x - pan_x) / zoom
                world_y = (mouse_y - pan_y) / zoom

                zoom += event.y * 0.1
                zoom = max(0.05, min(zoom, 10.0))

                pan_x = mouse_x - world_x * zoom
                pan_y = mouse_y - world_y * zoom

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 2, 3):
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

        temp = max(temp * 0.98, 1.0)

        if mode == "EADES":
            g.spring_layout_step(WIDTH, HEIGHT, c1=15.0, c2=80.0, c3=10000.0, c4=0.05)
        elif mode == "FR":
            g.fr_step(WIDTH, HEIGHT, temp, k)
        elif mode == "FR_BH":
            g.fr_barnes_hut_step(WIDTH, HEIGHT, temp, k, theta=0.6)

        screen.fill((240, 245, 250))

        # Aristas
        edge_width = max(1, int(1 * zoom))
        for edge in g._get_unique_edges():
            u = g._get_node_by_name(edge.get_node1().get_name())
            v = g._get_node_by_name(edge.get_node2().get_name())
            pos_u = to_screen(u.attributes['x'], u.attributes['y'])
            pos_v = to_screen(v.attributes['x'], v.attributes['y'])
            pygame.draw.line(screen, (170, 180, 190), pos_u, pos_v, edge_width)

        # Nodos
        node_radius = max(2, int(6 * zoom))
        border_width = max(1, int(1 * zoom))
        for node in g.graph:
            pos_x, pos_y = to_screen(node.attributes['x'], node.attributes['y'])
            pygame.draw.circle(screen, (70, 130, 180), (pos_x, pos_y), node_radius)
            pygame.draw.circle(screen, (30, 60, 100), (pos_x, pos_y), node_radius, border_width)

        # Textos de la UI
        texts = [
            f"Modo Actual: {mode}",
            "1: P. Eades (Spring) | 2: FR | 3: Barnes-Hut",
            "ESPACIO: Reiniciar posiciones",
            "Rueda: Zoom | Clic y arrastrar: Mover cámara",
            f"Nodos: {num_nodes} | Temp: {temp:.2f} | Zoom: {zoom:.1f}x"
        ]

        for i, text in enumerate(texts):
            color = (200, 50, 50) if i == 0 else (50, 50, 50)
            img = font.render(text, True, color)
            screen.blit(img, (10, 10 + (i * 22)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_fr_visualization()