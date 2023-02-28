import pygame

pygame.init()

display_width = 300
display_height = 300
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tic Tac Toe")

# Define the board
board = [['']*3, ['']*3, ['']*3]

# Define the colors
green = (20, 189, 172)
black = (0, 0, 0)
choose_color = lambda p: (84, 84, 84) if p == "X" else (242, 235, 211)

# Reducing function
draw_line = lambda a, b: pygame.draw.line(game_display, (13, 161, 146), a, b, 5)

# Define the font
font = pygame.font.SysFont(None, 100)

# Position decided by bot
def bestMove(spaces: list[tuple[int, int]]) -> tuple[int, int]:
    bestVal, x, y = -float("inf"), 0, 0
    for i, j in spaces:
        board[i][j] = "O"
        val = minimax(False)
        board[i][j] = ""
        if val > bestVal:
            bestVal, x, y = val, i, j
    return x, y

# Minimax algorithm
def minimax(state: bool) -> int:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return {"X":-1, "O":1}[board[i][1]]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return {"X":-1, "O":1}[board[1][i]]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return {"X":-1, "O":1}[board[1][1]]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return {"X":-1, "O":1}[board[1][1]]
    if sum(board[i][j] == '' for j in range(3) for i in range(3)) == 0:
        return 0
    bestVal = (float("inf"), -float("inf"))[state]
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "XO"[state]
                val = minimax(not state)
                board[i][j] = ""
                if state:
                    bestVal = max(bestVal, val)
                else:
                    bestVal = min(bestVal, val)
    return bestVal

# Draw the board
def draw_board() -> None:
    game_display.fill(green)
    for i in range(1, 3):
        draw_line((0, i * 100), (300, i * 100))
        draw_line((i * 100, 0), (i * 100, 300))
    for i in range(3):
        for j in range(3):
            text = font.render(board[i][j], True, choose_color(board[i][j]))
            text_rect = text.get_rect()
            text_rect.center = (j * 100 + 50, i * 100 + 50)
            game_display.blit(text, text_rect)

# Check for any wins
def check() -> tuple[int, str, str]:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return (i, "i", board[i][1])
        if board[0][i] == board[1][i] == board[2][i] != "":
            return (i, "j", board[1][i])
    if board[0][0] == board[1][1] == board[2][2] != "":
        return (0, "i-j", board[1][1])
    if board[0][2] == board[1][1] == board[2][0] != "":
        return (0, "i+j", board[1][1])
    free_space = sum(board[i][j] == '' for j in range(3) for i in range(3))
    return (0, "i", "NA") if free_space != 0 else (0, "i", "draw")

# Initiate the board
for w in range(1, 301, 10):
    game_display.fill(green)
    draw_line((0, 100), (w, 100))
    draw_line((300-w, 200), (300, 200))
    draw_line((100, 0), (100, w))
    draw_line((200, 300-w), (200, 300))
    pygame.display.update()
    pygame.time.delay(10)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONUP:
            # Get the position of the mouse click
            pos = pygame.mouse.get_pos()
            row = pos[1] // 100
            col = pos[0] // 100

            # Make the decision
            if board[row][col] == '':
                board[row][col] = 'X'
                free_space = [(i, j) for j in range(3) for i in range(3) if board[i][j] == '']
                if free_space != []:
                    posi, posj = bestMove(free_space)
                    board[posi][posj] = 'O'

    # Draw the board
    draw_board()
    pygame.display.update()
    
    # Check for winner
    pos, dir, winner = check()
    if winner != "NA":
        if winner == "draw":

            # Fill screen with text "DRAW"
            pygame.display.update()
            pygame.time.delay(1000)
            game_display.fill(green)
            draw_text = font.render("DRAW", True, black)
            draw_text_rect = draw_text.get_rect()
            draw_text_rect.center = (150, 150)
            game_display.blit(draw_text, draw_text_rect)

        else:

            # Draw strike line
            for w in range(10, 291):
                if dir == "i":
                    # Draw horizontally
                    draw_line((10, pos*100 + 50), (w, pos*100 + 50))
                if dir == "j":
                    # Draw vertically
                    draw_line((pos*100 + 50, 10), (pos*100 + 50, w))
                if dir == "i-j":
                    # Draw diagonally from top left
                    draw_line((10, 10), (w, w))
                if dir == "i+j":
                    # Draw diagonally from top right
                    draw_line((290, 10), (300-w, w))
                pygame.display.update()
                pygame.time.delay(1)

        # Keep the screen for 3 seconds
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        quit()

