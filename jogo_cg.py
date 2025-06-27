import pygame
import random
import time
from config import *

SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + UI_HEIGHT

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + UI_HEIGHT, CELL_SIZE, CELL_SIZE)
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.reveal_progress = 0

    def draw_bomb_icon(self, surface):
        center = self.rect.center
        pygame.draw.circle(surface, BLACK, center, CELL_SIZE // 3 + 1)
        pygame.draw.line(surface, BLACK, (center[0] + 3, center[1] - 8), (center[0] + 8, center[1] - 12), 3)
        pygame.draw.circle(surface, WHITE, (center[0] - 5, center[1] - 5), 2)

    def draw(self, surface, font, game_over=False, mine_clicked=False, dt=0, hint_cell=None, hint_time=0):
        if self.is_revealed:
            if self.reveal_progress < 1:
                self.reveal_progress += dt * 4
            scale = min(1, self.reveal_progress)
            scaled_rect = self.rect.inflate(-CELL_SIZE * (1 - scale), -CELL_SIZE * (1 - scale))

            color = pygame.Color(*COLOR_HIDDEN).lerp(pygame.Color(*COLOR_REVEALED), scale)
            if self == hint_cell and time.time() - hint_time < 1:
                color = (255, 255, 100)  # destaque amarelo claro

            pygame.draw.rect(surface, color, scaled_rect)
            pygame.draw.line(surface, COLOR_BORDER_DARK, scaled_rect.topleft, scaled_rect.topright)
            pygame.draw.line(surface, COLOR_BORDER_DARK, scaled_rect.topleft, scaled_rect.bottomleft)

            if self.is_mine:
                if mine_clicked:
                    pygame.draw.rect(surface, COLOR_MINE, scaled_rect)
                self.draw_bomb_icon(surface)
            elif self.neighbor_mines > 0:
                color = NUMBER_COLORS.get(self.neighbor_mines, COLOR_TEXT)
                text = font.render(str(self.neighbor_mines), True, color)
                text_rect = text.get_rect(center=scaled_rect.center)
                surface.blit(text, text_rect)
        else:
            pygame.draw.rect(surface, COLOR_HIDDEN, self.rect)
            pygame.draw.line(surface, COLOR_BORDER_LIGHT, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(surface, COLOR_BORDER_LIGHT, self.rect.topleft, self.rect.bottomleft, 2)
            pygame.draw.line(surface, COLOR_BORDER_DARK, self.rect.bottomright, self.rect.topright, 2)
            pygame.draw.line(surface, COLOR_BORDER_DARK, self.rect.bottomright, self.rect.bottomleft, 2)
            if self.is_flagged:
                pole_rect = pygame.Rect(self.rect.centerx - 2, self.rect.centery - 8, 4, 16)
                pygame.draw.rect(surface, BLACK, pole_rect)
                flag_points = [(self.rect.centerx, self.rect.centery - 8),
                               (self.rect.centerx, self.rect.centery + 2),
                               (self.rect.centerx - 10, self.rect.centery - 3)]
                pygame.draw.polygon(surface, COLOR_FLAG, flag_points)

        if game_over and self.is_mine and not self.is_revealed:
            self.draw_bomb_icon(surface)

        if game_over and not self.is_mine and self.is_flagged:
            pygame.draw.line(surface, COLOR_MINE, self.rect.topleft, self.rect.bottomright, 3)
            pygame.draw.line(surface, COLOR_MINE, self.rect.topright, self.rect.bottomleft, 3)

class Smiley:
    # Inicializar o smiley com posição e tamanho
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.state = "playing"      # Pode ser: playing, win, dead, wow

    # Desenha o smiley com base no estado atual (morto, feliz, surpreso etc.)
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), self.rect.center, self.rect.width // 2)
        pygame.draw.circle(surface, BLACK, self.rect.center, self.rect.width // 2, 2)
        eye_l_pos = (self.rect.centerx - 8, self.rect.centery - 5)
        eye_r_pos = (self.rect.centerx + 8, self.rect.centery - 5)
        if self.state == "dead":
            for eye in [eye_l_pos, eye_r_pos]:
                pygame.draw.line(surface, BLACK, (eye[0] - 3, eye[1] - 3), (eye[0] + 3, eye[1] + 3), 2)
                pygame.draw.line(surface, BLACK, (eye[0] + 3, eye[1] - 3), (eye[0] - 3, eye[1] + 3), 2)
            pygame.draw.arc(surface, BLACK, self.rect.inflate(-20, -20).move(0, 7), 3.14, 0, 2)
        elif self.state == "win":
            pygame.draw.rect(surface, BLACK, (self.rect.centerx - 15, self.rect.centery - 8, 30, 8))
            pygame.draw.line(surface, BLACK, (self.rect.centerx - 20, self.rect.centery - 4), (self.rect.centerx - 15, self.rect.centery - 4), 2)
            pygame.draw.line(surface, BLACK, (self.rect.centerx + 20, self.rect.centery - 4), (self.rect.centerx + 15, self.rect.centery - 4), 2)
            pygame.draw.arc(surface, BLACK, self.rect.inflate(-20, -20).move(0, 5), 0, 3.14, 2)
        else:
            pygame.draw.circle(surface, BLACK, eye_l_pos, 3)
            pygame.draw.circle(surface, BLACK, eye_r_pos, 3)
            pygame.draw.arc(surface, BLACK, self.rect.inflate(-20, -20).move(0, 8), 0, 3.14, 2)

    def handle_click(self, pos):
        return self.rect.collidepoint(pos)

def tela_creditos(screen, font):
    screen.fill(COLOR_BG)
    title = font.render("Créditos", True, WHITE)
    nomes = [
        "Everton Santos de Castro",
        "Felipe Lemos Oliveira",
        "Leonardo Pinto Machado",
        "Pedro Henrique Canabarro"
    ]

    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))
    for i, nome in enumerate(nomes):
        texto = font.render(nome, True, COLOR_TEXT)
        screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, 120 + i * 40))

    voltar_font = pygame.font.SysFont(None, 30)
    voltar_text = voltar_font.render("Voltar", True, BLACK)
    voltar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 80, 120, 40)
    pygame.draw.rect(screen, COLOR_REVEALED, voltar_rect)
    pygame.draw.rect(screen, COLOR_BORDER_DARK, voltar_rect, 3)
    screen.blit(voltar_text, voltar_text.get_rect(center=voltar_rect.center))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_rect.collidepoint(event.pos):
                    return

def tela_inicial(screen, font):
    screen.fill(COLOR_BG)
    title = font.render("Campo Minado", True, WHITE)

    button_font = pygame.font.SysFont(None, 30)
    iniciar_text = button_font.render("Iniciar Jogo", True, BLACK)
    creditos_text = button_font.render("Créditos", True, BLACK)

    iniciar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 50)
    creditos_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)

    pygame.draw.rect(screen, COLOR_REVEALED, iniciar_rect)
    pygame.draw.rect(screen, COLOR_BORDER_DARK, iniciar_rect, 3)
    pygame.draw.rect(screen, COLOR_REVEALED, creditos_rect)
    pygame.draw.rect(screen, COLOR_BORDER_DARK, creditos_rect, 3)

    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
    screen.blit(iniciar_text, iniciar_text.get_rect(center=iniciar_rect.center))
    screen.blit(creditos_text, creditos_text.get_rect(center=creditos_rect.center))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if iniciar_rect.collidepoint(event.pos):
                    return
                elif creditos_rect.collidepoint(event.pos):
                    tela_creditos(screen, font)
                    return tela_inicial(screen, font)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Campo Minado")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, CELL_SIZE - 5, bold=True)
    ui_font = pygame.font.SysFont("digital-7", 40)
    smiley = Smiley(SCREEN_WIDTH // 2, UI_HEIGHT // 2, 40)

    tela_inicial(screen, pygame.font.SysFont(None, 50))

    board = [[Cell(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    first_click = True
    game_state = "playing"
    start_time = None
    clicked_mine_cell = None
    hint_used = False
    hint_cell = None
    hint_time = 0

    def reset_game():
        nonlocal board, first_click, game_state, start_time, clicked_mine_cell, hint_used
        board = [[Cell(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        first_click = True
        game_state = "playing"
        start_time = None
        clicked_mine_cell = None
        hint_used = False
        smiley.state = "playing"

    def place_mines(exclude):
        positions = set()
        while len(positions) < NUM_MINES:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if abs(x - exclude[0]) <= 1 and abs(y - exclude[1]) <= 1:
                continue
            positions.add((x, y))
        for x, y in positions:
            board[y][x].is_mine = True
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell = board[y][x]
                if not cell.is_mine:
                    cell.neighbor_mines = sum(
                        1 for i in range(-1, 2) for j in range(-1, 2)
                        if 0 <= x + j < GRID_SIZE and 0 <= y + i < GRID_SIZE and board[y + i][x + j].is_mine
                    )

    def reveal_cell(x, y):
        cell = board[y][x]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        if cell.neighbor_mines == 0 and not cell.is_mine:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = x + j, y + i
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        reveal_cell(nx, ny)

    running = True
    ignore_clicks_this_frame = False  # Flag para ignorar cliques logo após mudança de estado


    while running:
        dt = clock.tick(FPS) / 1000
        screen.fill(COLOR_BG)

        # Defina o hint_rect ANTES do loop de eventos!
        hint_font = pygame.font.SysFont(None, 30)
        hint_text = hint_font.render("Dica", True, BLACK)
        hint_rect = pygame.Rect(SCREEN_WIDTH // 2 + 100, 5, 100, 40)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Clicar no botão de dica
                
                # Se for o primeiro clique, não é permitido utilizar a dica
                if(not first_click):
                    if hint_rect.collidepoint(event.pos) and not hint_used and game_state == "playing":
                        safe_cells = [c for row in board for c in row if not c.is_revealed and not c.is_mine]
                        if safe_cells:
                            hint_cell = random.choice(safe_cells)
                            hint_cell.is_revealed = True

                            if(not safe_cells):
                                hint_cell.is_revealed = False

                            hint_time = time.time()
                        
                if smiley.handle_click(event.pos):
                    reset_game()
                else:
                    mx, my = event.pos
                    col, row = mx // CELL_SIZE, (my - UI_HEIGHT) // CELL_SIZE
                    if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                        cell = board[row][col]
                        if first_click and event.button == 1:
                            place_mines((col, row))
                            start_time = time.time()
                            first_click = False
                        if event.button == 1 and not cell.is_flagged:
                            if cell.is_mine:
                                cell.is_revealed = True
                                clicked_mine_cell = cell
                                game_state = "game_over"
                                smiley.state = "dead"
                                ignore_clicks_this_frame = True
                            else:
                                reveal_cell(col, row)
                        elif event.button == 3 and not cell.is_revealed:
                            cell.is_flagged = not cell.is_flagged
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hint_rect.collidepoint(event.pos) and not hint_used and game_state == "playing":
                    safe_cells = [c for row in board for c in row if not c.is_revealed and not c.is_mine]
                    if safe_cells:
                        hint_cell = random.choice(safe_cells)
                        hint_cell.is_revealed = True
                        hint_used = True
                        hint_time = time.time()


        for row in board:
            for cell in row:
                cell.draw(screen, font, game_state != "playing", clicked_mine_cell == cell, dt, hint_cell)

        smiley.draw(screen)

        pygame.draw.rect(screen, COLOR_REVEALED, hint_rect)
        pygame.draw.rect(screen, COLOR_BORDER_DARK, hint_rect, 3)
        screen.blit(hint_text, hint_text.get_rect(center=hint_rect.center))

        if start_time and game_state == "playing":
            elapsed = int(time.time() - start_time)
            timer = ui_font.render(f"{elapsed:03}", True, COLOR_TEXT)
            screen.blit(timer, (SCREEN_WIDTH - 80, 5))

        flags = sum(1 for row in board for c in row if c.is_flagged)
        flags_txt = ui_font.render(f"{NUM_MINES - flags:03}", True, COLOR_TEXT)
        screen.blit(flags_txt, (15, 5))

        if game_state == "playing" and not first_click:
            revealed = sum(1 for row in board for c in row if c.is_revealed)
            if revealed == GRID_SIZE * GRID_SIZE - NUM_MINES:
                game_state = "win"
                smiley.state = "win"
                ignore_clicks_this_frame = True

        if game_state in ["game_over", "win"]:
            button_font = pygame.font.SysFont(None, 30)
            restart_text = button_font.render("Reiniciar", True, BLACK)
            home_text = button_font.render("Retornar", True, BLACK)

            countdown_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 40)
            restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)
            home_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 40)

            pygame.draw.rect(screen, COLOR_REVEALED, restart_rect)
            pygame.draw.rect(screen, COLOR_BORDER_DARK, restart_rect, 3)
            screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

            pygame.draw.rect(screen, COLOR_REVEALED, home_rect)
            pygame.draw.rect(screen, COLOR_BORDER_DARK, home_rect, 3)
            screen.blit(home_text, home_text.get_rect(center=home_rect.center))

            pygame.display.update()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not ignore_clicks_this_frame:
                    if restart_rect.collidepoint(event.pos):
                        reset_game()
                    elif home_rect.collidepoint(event.pos):
                        tela_inicial(screen, pygame.font.SysFont(None, 50))
                        reset_game()

        ignore_clicks_this_frame = False  # Libera cliques novamente no próximo frame
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
