import pygame
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 700
CELL_SIZE = 150
GRID_OFFSET_X = (WIDTH - CELL_SIZE * 3) // 2
GRID_OFFSET_Y = 100

# Цвета
BACKGROUND_COLOR = (240, 240, 245)
GRID_COLOR = (70, 130, 180)
X_COLOR = (0, 0, 0)  
O_COLOR = (0, 0, 0)  
TEXT_COLOR = (50, 50, 70)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (90, 150, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
WIN_LINE_COLOR = (255, 215, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-Нолики")

# Загрузка звука для хода
try:
    # Загружаем звук для хода (теперь это звук хода, а не победы)
    move_sound = pygame.mixer.Sound("victory.wav")  # Используем тот же файл, но для хода
    print("Звук хода загружен успешно!")
except Exception as e:
    print(f"Не удалось загрузить звуковой файл: {e}")
    move_sound = None

try:
    font = pygame.font.SysFont("Arial", 40)
    button_font = pygame.font.SysFont("Arial", 32)
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
except:
    font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 48)

board = [['' for _ in range(3)] for _ in range(3)]

current_player = 'X'

game_over = False
winner = None
win_line = None  

button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    
    title = title_font.render("Крестики-Нолики", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    for i in range(1, 3):
        pygame.draw.line(screen, GRID_COLOR, 
                        (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y),
                        (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y + 3 * CELL_SIZE), 
                        5)
        pygame.draw.line(screen, GRID_COLOR, 
                        (GRID_OFFSET_X, GRID_OFFSET_Y + i * CELL_SIZE),
                        (GRID_OFFSET_X + 3 * CELL_SIZE, GRID_OFFSET_Y + i * CELL_SIZE), 
                        5)
    
    for row in range(3):
        for col in range(3):
            x = GRID_OFFSET_X + col * CELL_SIZE
            y = GRID_OFFSET_Y + row * CELL_SIZE
            
            if board[row][col] == 'X':
                offset = 30
                pygame.draw.line(screen, X_COLOR, 
                                (x + offset, y + offset), 
                                (x + CELL_SIZE - offset, y + CELL_SIZE - offset), 
                                10)
                pygame.draw.line(screen, X_COLOR, 
                                (x + CELL_SIZE - offset, y + offset), 
                                (x + offset, y + CELL_SIZE - offset), 
                                10)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, 
                                  (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 
                                  CELL_SIZE // 2 - 20, 
                                  10)

def draw_button():
    mouse_pos = pygame.mouse.get_pos()
    
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
    
    button_text = button_font.render("Новая игра", True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, 
                              button_rect.centery - button_text.get_height() // 2))
    
    pygame.draw.rect(screen, (40, 80, 120), button_rect, 3, border_radius=10)

def draw_game_status():
    if game_over:
        if winner:
            status_text = f"Победил: {winner}"
        else:
            status_text = "Ничья!"
        status_color = (200, 50, 50) if winner else (100, 100, 100)
    else:
        status_text = f"Сейчас ходит: {current_player}"
        status_color = X_COLOR if current_player == 'X' else O_COLOR
    
    status_surface = font.render(status_text, True, status_color)
    screen.blit(status_surface, (WIDTH // 2 - status_surface.get_width() // 2, HEIGHT - 140))

def draw_win_line():
    if win_line:
        start_x, start_y, end_x, end_y = win_line
        pygame.draw.line(screen, WIN_LINE_COLOR, 
                        (start_x, start_y), 
                        (end_x, end_y), 
                        8)

def check_winner():
    global winner, game_over, win_line
    
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            winner = board[row][0]
            start_x = GRID_OFFSET_X + 20
            start_y = GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
            end_x = GRID_OFFSET_X + 3 * CELL_SIZE - 20
            end_y = start_y
            win_line = (start_x, start_y, end_x, end_y)
            game_over = True
            return
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            winner = board[0][col]
            start_x = GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
            start_y = GRID_OFFSET_Y + 20
            end_x = start_x
            end_y = GRID_OFFSET_Y + 3 * CELL_SIZE - 20
            win_line = (start_x, start_y, end_x, end_y)
            game_over = True
            return
    
    if board[0][0] == board[1][1] == board[2][2] != '':
        winner = board[0][0]
        start_x = GRID_OFFSET_X + 20
        start_y = GRID_OFFSET_Y + 20
        end_x = GRID_OFFSET_X + 3 * CELL_SIZE - 20
        end_y = GRID_OFFSET_Y + 3 * CELL_SIZE - 20
        win_line = (start_x, start_y, end_x, end_y)
        game_over = True
        return
    
    if board[0][2] == board[1][1] == board[2][0] != '':
        winner = board[0][2]
        start_x = GRID_OFFSET_X + 3 * CELL_SIZE - 20
        start_y = GRID_OFFSET_Y + 20
        end_x = GRID_OFFSET_X + 20
        end_y = GRID_OFFSET_Y + 3 * CELL_SIZE - 20
        win_line = (start_x, start_y, end_x, end_y)
        game_over = True
        return
    
    if all(board[row][col] != '' for row in range(3) for col in range(3)):
        game_over = True

def make_move(row, col):
    global current_player
    
    if board[row][col] == '' and not game_over:
        # Ставим символ на доску
        board[row][col] = current_player
        
        # ВОТ ИЗМЕНЕНИЕ: проигрываем звук при КАЖДОМ ходе
        if move_sound:
            move_sound.play()
        
        # Проверяем, не закончилась ли игра
        check_winner()
        
        # Меняем игрока, если игра продолжается
        if not game_over:
            current_player = 'O' if current_player == 'X' else 'X'

def reset_game():
    global board, current_player, game_over, winner, win_line

    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    winner = None
    win_line = None

def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if button_rect.collidepoint(mouse_pos):
                    reset_game()
                
                elif not game_over:
                    x, y = mouse_pos
                    if (GRID_OFFSET_X <= x < GRID_OFFSET_X + 3 * CELL_SIZE and
                        GRID_OFFSET_Y <= y < GRID_OFFSET_Y + 3 * CELL_SIZE):
                        col = (x - GRID_OFFSET_X) // CELL_SIZE
                        row = (y - GRID_OFFSET_Y) // CELL_SIZE
                        make_move(row, col)
        
        draw_board()
        draw_win_line()
        draw_game_status()
        draw_button()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
