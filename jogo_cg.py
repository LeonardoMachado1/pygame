# Jogo Campo Minado com Pygame
#
# Objetivo: Implementar uma versão funcional e com visual aprimorado do clássico jogo.
#
# Regras:
# - Clique com o botão ESQUERDO para revelar uma célula.
# - Clique com o botão DIREITO para colocar ou remover uma bandeira.
# - Clique no smiley para reiniciar o jogo.
# - O objetivo é revelar todas as células que NÃO contêm minas.

import pygame
import random
import time

# --- Configurações do Jogo ---
GRID_SIZE = 20  # Número de células na horizontal e vertical
CELL_SIZE = 30  # Tamanho de cada célula em pixels
NUM_MINES = 40  # Quantidade de minas no tabuleiro

# --- Dimensões da Tela ---
UI_HEIGHT = 60 # Altura do painel superior da UI
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + UI_HEIGHT
FPS = 60

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_HIDDEN = (189, 189, 189)
COLOR_REVEALED = (224, 224, 224)
COLOR_BORDER_LIGHT = (240, 240, 240)
COLOR_BORDER_DARK = (120, 120, 120)
COLOR_TEXT = (0, 0, 0)
COLOR_MINE = (211, 47, 47)
COLOR_FLAG = (244, 67, 54)
COLOR_BG = (192, 192, 192) # Cinza clássico
COLOR_BUTTON = (100, 100, 100)
COLOR_BUTTON_HOVER = (130, 130, 130)

# Dicionário de cores para os números
NUMBER_COLORS = {
    1: (0, 0, 255),    # Azul
    2: (0, 128, 0),    # Verde
    3: (255, 0, 0),    # Vermelho
    4: (0, 0, 128),    # Azul Escuro
    5: (128, 0, 0),    # Marrom
    6: (0, 128, 128),  # Ciano
    7: (0, 0, 0),      # Preto
    8: (128, 128, 128) # Cinza
}

# =============================================================================
# Classe da Célula
# =============================================================================
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + UI_HEIGHT, CELL_SIZE, CELL_SIZE)
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def draw_bomb_icon(self, surface):
        """Desenha um ícone de bomba."""
        center = self.rect.center
        # Corpo da bomba
        pygame.draw.circle(surface, BLACK, center, CELL_SIZE // 3 + 1)
        # Mecha
        pygame.draw.line(surface, BLACK, (center[0] + 3, center[1] - 8), (center[0] + 8, center[1] - 12), 3)
        # Destaque
        pygame.draw.circle(surface, WHITE, (center[0] - 5, center[1] - 5), 2)


    def draw(self, surface, font, game_over=False, mine_clicked=False):
        """Desenha a célula com um visual melhorado."""
        if self.is_revealed:
            pygame.draw.rect(surface, COLOR_REVEALED, self.rect)
            pygame.draw.line(surface, COLOR_BORDER_DARK, self.rect.topleft, self.rect.topright)
            pygame.draw.line(surface, COLOR_BORDER_DARK, self.rect.topleft, self.rect.bottomleft)
            
            if self.is_mine:
                # Se esta foi a mina clicada, desenha com fundo vermelho
                if mine_clicked:
                    pygame.draw.rect(surface, COLOR_MINE, self.rect)
                self.draw_bomb_icon(surface)
            elif self.neighbor_mines > 0:
                color = NUMBER_COLORS.get(self.neighbor_mines, COLOR_TEXT)
                text = font.render(str(self.neighbor_mines), True, color)
                text_rect = text.get_rect(center=self.rect.center)
                surface.blit(text, text_rect)
        else: # Célula escondida
            pygame.draw.rect(surface, COLOR_HIDDEN, self.rect)
            pygame.draw.line(surface, COLOR_BORDER_LIGHT, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(surface, COLOR_BORDER_LIGHT, self.rect.topleft, self.rect.bottomleft, 2)
            pygame.draw.line(surface, COLOR_BORDER_DARK, self.rect.bottomright, self.rect.topright, 2)
            pygame.draw.line(surface, COLOR_BORDER_DARK, self.rect.bottomright, self.rect.bottomleft, 2)

            if self.is_flagged:
                pole_rect = pygame.Rect(self.rect.centerx - 2, self.rect.centery - 8, 4, 16)
                pygame.draw.rect(surface, BLACK, pole_rect)
                flag_points = [(self.rect.centerx, self.rect.centery - 8), (self.rect.centerx, self.rect.centery + 2), (self.rect.centerx - 10, self.rect.centery - 3)]
                pygame.draw.polygon(surface, COLOR_FLAG, flag_points)
        
        if game_over and self.is_mine and not self.is_revealed:
             self.draw_bomb_icon(surface)
        if game_over and not self.is_mine and self.is_flagged:
            pygame.draw.line(surface, COLOR_MINE, self.rect.topleft, self.rect.bottomright, 3)
            pygame.draw.line(surface, COLOR_MINE, self.rect.topright, self.rect.bottomleft, 3)
            
# =============================================================================
# Classe do Smiley (Botão de Reiniciar)
# =============================================================================
class Smiley:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.state = "playing"
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), self.rect.center, self.rect.width // 2)
        pygame.draw.circle(surface, BLACK, self.rect.center, self.rect.width // 2, 2)
        eye_l_pos = (self.rect.centerx - 8, self.rect.centery - 5)
        eye_r_pos = (self.rect.centerx + 8, self.rect.centery - 5)

        if self.state == "dead":
            pygame.draw.line(surface, BLACK, (eye_l_pos[0]-3, eye_l_pos[1]-3), (eye_l_pos[0]+3, eye_l_pos[1]+3), 2)
            pygame.draw.line(surface, BLACK, (eye_l_pos[0]+3, eye_l_pos[1]-3), (eye_l_pos[0]-3, eye_l_pos[1]+3), 2)
            pygame.draw.line(surface, BLACK, (eye_r_pos[0]-3, eye_r_pos[1]-3), (eye_r_pos[0]+3, eye_r_pos[1]+3), 2)
            pygame.draw.line(surface, BLACK, (eye_r_pos[0]+3, eye_r_pos[1]-3), (eye_r_pos[0]-3, eye_r_pos[1]+3), 2)
            pygame.draw.arc(surface, BLACK, self.rect.inflate(-20, -15).move(0, 10), 3.14, 0, 2)
        elif self.state == "win":
            pygame.draw.rect(surface, BLACK, (self.rect.centerx - 15, self.rect.centery - 8, 30, 8))
            pygame.draw.line(surface, BLACK, (self.rect.centerx - 20, self.rect.centery - 4), (self.rect.centerx - 15, self.rect.centery - 4), 2)
            pygame.draw.line(surface, BLACK, (self.rect.centerx + 20, self.rect.centery - 4), (self.rect.centerx + 15, self.rect.centery - 4), 2)
            pygame.draw.arc(surface, BLACK, self.rect.inflate(-20, -20).move(0, 5), 0, 3.14, 2)
        else:
            pygame.draw.circle(surface, BLACK, eye_l_pos, 3)
            pygame.draw.circle(surface, BLACK, eye_r_pos, 3)
            if self.state == "wow":
                 pygame.draw.circle(surface, BLACK, (self.rect.centerx, self.rect.centery + 5), 5)
            else:
                 pygame.draw.arc(surface, BLACK, self.rect.inflate(-20, -20).move(0, 5), 0, 3.14, 2)
            
    def handle_click(self, pos):
        return self.rect.collidepoint(pos)

# =============================================================================
# Funções de UI
# =============================================================================
def draw_button(surface, rect, text, font, button_color, text_color, hover_color):
    """Desenha um botão genérico e detecta hover."""
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    color = hover_color if is_hovered else button_color
    
    pygame.draw.rect(surface, color, rect, border_radius=8)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    return is_hovered

def draw_game_over_screen(surface, title, message, font_title, font_message):
    """Desenha uma sobreposição translúcida para fim de jogo ou vitória."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))
    
    title_surf = font_title.render(title, True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    
    message_surf = font_message.render(message, True, WHITE)
    message_rect = message_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10))
    
    surface.blit(title_surf, title_rect)
    surface.blit(message_surf, message_rect)
    
# =============================================================================
# Função Principal do Jogo
# =============================================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Campo Minado")
    clock = pygame.time.Clock()
    
    cell_font = pygame.font.SysFont("segoeuisymbol", CELL_SIZE - 5, bold=True)
    ui_font = pygame.font.SysFont("digital-7", 50)
    title_font = pygame.font.SysFont("impact", 80)
    button_font = pygame.font.SysFont("segoeui", 30, bold=True)
    instruction_font = pygame.font.SysFont("segoeui", 22)
    credits_font = pygame.font.SysFont("segoeui", 28)
    
    # Botões da UI
    start_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 30, 200, 50)
    credits_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 90, 200, 50)
    restart_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 60, 200, 50)
    back_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 100, 200, 50)
    
    board = []
    game_state = "start_screen" # start_screen, playing, game_over, win, credits_screen
    first_click = True
    start_time = None
    elapsed_time = 0
    clicked_mine_cell = None

    smiley = Smiley(SCREEN_WIDTH // 2, UI_HEIGHT // 2, 40)

    def reset_game():
        nonlocal board, game_state, first_click, start_time, elapsed_time, smiley, clicked_mine_cell
        board = [[Cell(col, row) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        first_click = True
        start_time = None
        elapsed_time = 0
        smiley.state = "playing"
        clicked_mine_cell = None
        game_state = "playing"

    def place_mines(first_click_pos):
        mine_positions = set()
        first_x, first_y = first_click_pos
        while len(mine_positions) < NUM_MINES:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if abs(x - first_x) > 1 or abs(y-first_y) > 1: mine_positions.add((x, y))
        for x, y in mine_positions: board[y][x].is_mine = True
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if not board[r][c].is_mine:
                    board[r][c].neighbor_mines = sum(1 for i in range(-1, 2) for j in range(-1, 2) if 0 <= r + i < GRID_SIZE and 0 <= c + j < GRID_SIZE and board[r + i][c + j].is_mine)

    def reveal_cell(row, col):
        cell = board[row][col]
        if cell.is_revealed or cell.is_flagged: return
        cell.is_revealed = True
        if cell.neighbor_mines == 0 and not cell.is_mine:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                        reveal_cell(row + i, col + j)
    
    running = True
    while running:
        mouse_down = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
        
        # --- LÓGICA E RENDERIZAÇÃO DOS ESTADOS DO JOGO ---
        if game_state == "start_screen":
            screen.fill((170, 170, 170))
            
            title_surf = title_font.render("Campo Minado", True, (60, 60, 60))
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            
            instruction_surf = instruction_font.render("Encontre todas as minas para vencer!", True, (80, 80, 80))
            instruction_rect = instruction_surf.get_rect(center=(SCREEN_WIDTH / 2, title_rect.bottom + 30))
            
            screen.blit(title_surf, title_rect)
            screen.blit(instruction_surf, instruction_rect)

            start_hovered = draw_button(screen, start_button_rect, "Iniciar", button_font, COLOR_BUTTON, WHITE, COLOR_BUTTON_HOVER)
            credits_hovered = draw_button(screen, credits_button_rect, "Créditos", button_font, COLOR_BUTTON, WHITE, COLOR_BUTTON_HOVER)
            
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_hovered:
                        reset_game()
                    elif credits_hovered:
                        game_state = "credits_screen"

        elif game_state == "credits_screen":
            screen.fill((170, 170, 170))
            title_surf = title_font.render("Créditos", True, (60, 60, 60))
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
            screen.blit(title_surf, title_rect)

            creators = ["Pedro Henrique Canabarro", "Leonardo Pinto Machado", "Felipe Lemos Oliveira", "Everton Santos de Castro"]
            for i, creator in enumerate(creators):
                creator_surf = credits_font.render(creator, True, (80, 80, 80))
                creator_rect = creator_surf.get_rect(center=(SCREEN_WIDTH / 2, title_rect.bottom + 50 + i * 40))
                screen.blit(creator_surf, creator_rect)

            back_hovered = draw_button(screen, back_button_rect, "Voltar", button_font, COLOR_BUTTON, WHITE, COLOR_BUTTON_HOVER)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_hovered:
                    game_state = "start_screen"


        elif game_state in ["playing", "game_over", "win"]:
            screen.fill(COLOR_BG)
            # Desenha tabuleiro
            for row in board:
                for cell in row:
                    mine_was_clicked = (cell == clicked_mine_cell)
                    cell.draw(screen, cell_font, game_state != "playing", mine_was_clicked)

            # Desenha UI Superior
            smiley.draw(screen)
            flags_count = sum(c.is_flagged for r in board for c in r)
            mines_text = ui_font.render(f"{NUM_MINES - flags_count:03}", True, COLOR_MINE)
            screen.blit(mines_text, (15, 5))

            # Lógica do Timer
            if start_time and game_state == "playing":
                elapsed_time = int(time.time() - start_time)
            timer_text = ui_font.render(f"{min(elapsed_time, 999):03}", True, COLOR_MINE)
            screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 15, 5))

            # Eventos do jogo principal
            if game_state == "playing":
                smiley.state = "wow" if mouse_down else "playing"
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if smiley.handle_click(event.pos):
                             reset_game()
                             continue
                        
                        col, row = event.pos[0] // CELL_SIZE, (event.pos[1] - UI_HEIGHT) // CELL_SIZE
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                            if first_click and event.button == 1:
                                place_mines((col, row)); start_time = time.time(); first_click = False
                            
                            cell = board[row][col]
                            if event.button == 1 and not cell.is_flagged:
                                reveal_cell(row, col)
                                if cell.is_mine:
                                    game_state = "game_over"; smiley.state = "dead"; clicked_mine_cell = cell
                            elif event.button == 3 and not cell.is_revealed:
                                cell.is_flagged = not cell.is_flagged
                
                # Verifica condição de vitória
                if not first_click and sum(c.is_revealed for r in board for c in r) == GRID_SIZE*GRID_SIZE - NUM_MINES:
                    game_state = "win"; smiley.state = "win"

            elif game_state == "game_over":
                draw_game_over_screen(screen, "Fim de Jogo!", "Você clicou em uma mina.", title_font, button_font)
                is_hovered = draw_button(screen, restart_button_rect, "Reiniciar", button_font, COLOR_BUTTON, WHITE, COLOR_BUTTON_HOVER)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_hovered:
                        reset_game()
            
            elif game_state == "win":
                draw_game_over_screen(screen, "Você Venceu!", "Parabéns!", title_font, button_font)
                is_hovered = draw_button(screen, restart_button_rect, "Jogar Novamente", button_font, COLOR_BUTTON, WHITE, COLOR_BUTTON_HOVER)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_hovered:
                        reset_game()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
