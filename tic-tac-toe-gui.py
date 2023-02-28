import random
import pygame

pygame.init()

display_width = 300
display_height = 300
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tic Tac Toe")

# Define the board
board = [['', '', ''], ['', '', ''], ['', '', '']]

# Define the colors
green = (20, 189, 172)
dark_green = (13, 161, 146)
black = (0, 0, 0)
choose_color = lambda p: (84, 84, 84) if p == "X" else (242, 235, 211)

# Reducing function
draw_line = lambda a, b, c, d: pygame.draw.line(game_display, a, b, c, d)

# Define the font
font = pygame.font.SysFont(None, 100)

# Position decided by bot
def bestMove(spaces):
    bestVal, x, y = -float("inf"), 0, 0
    for i, j in spaces:
        board[i][j] = "O"
        val = minimax(False)
        board[i][j] = ""
        if val > bestVal:
            bestVal, x, y = val, i, j
    return x, y


# Minimax algorithm
def minimax(state):
    result = check()
    if result[0] != "NA":
        return result[0]
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
def draw_board():
    game_display.fill(green)
    for i in range(1, 3):
        draw_line(dark_green, (0, i * 100), (300, i * 100), 5)
        draw_line(dark_green, (i * 100, 0), (i * 100, 300), 5)
    for i in range(3):
        for j in range(3):
            text = font.render(board[i][j], True, choose_color(board[i][j]))
            text_rect = text.get_rect()
            text_rect.center = (j * 100 + 50, i * 100 + 50)
            game_display.blit(text, text_rect)


# Check for any wins
def check():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return [-1, 1][board[i][1] == 'O'], ("i", i)
        if board[0][i] == board[1][i] == board[2][i] != "":
            return [-1, 1][board[1][i] == 'O'], ("j", i)
    if board[0][0] == board[1][1] == board[2][2] != "":
        return [-1, 1][board[1][1] == 'O'], ("i-j", 0)
    if board[0][2] == board[1][1] == board[2][0] != "":
        return [-1, 1][board[1][1] == 'O'], ("i+j", 0)
    free_space = sum(board[i][j] == '' for j in range(3) for i in range(3))
    return ("NA", 0) if free_space != 0 else (0, 0)


# Initiate the board
for w in range(1, 301, 10):
    game_display.fill(green)
    draw_line(dark_green, (0, 100), (w, 100), 5)
    draw_line(dark_green, (300-w, 200), (300, 200), 5)
    draw_line(dark_green, (100, 0), (100, w), 5)
    draw_line(dark_green, (200, 300-w), (200, 300), 5)
    pygame.display.update()
    pygame.time.delay(20)


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

    result = check()
    if result != ("NA", 0):
        if result[0] != 0:

            # Draw strike line
            dir, pos = result[1]
            color = choose_color(result[0])
            for w in range(30, 270):
                if dir == "i":
                    draw_line(color, (30, pos*100 + 50), (w, pos*100 + 50), 10)
                if dir == "j":
                    draw_line(color, (pos*100 + 50, 30), (pos*100 + 50, w), 10)
                if dir == "i-j":
                    draw_line(color, (30, 30), (w, w), 10)
                if dir == "i+j":
                    draw_line(color, (270, 30), (300-w, w), 10)
                pygame.display.update()
                pygame.time.delay(5)

        else:

            # Fill screen with text "DRAW"
            pygame.display.update()
            pygame.time.delay(2000)
            game_display.fill(green)
            draw_text = font.render("DRAW", True, black)
            draw_text_rect = draw_text.get_rect()
            draw_text_rect.center = (150, 150)
            game_display.blit(draw_text, draw_text_rect)

        # Keep the screen for 3 seconds
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        quit()

    # Update the display
    pygame.display.update()
