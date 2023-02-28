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

# Define the font
font = pygame.font.SysFont(None, 100)

# Position decided by bot
def bestMove(spaces):
    return random.choice(spaces)

# Draw the board
def draw_board():
    game_display.fill(green)
    pygame.draw.line(game_display, dark_green, (0, 100), (300, 100), 5)
    pygame.draw.line(game_display, dark_green, (0, 200), (300, 200), 5)
    pygame.draw.line(game_display, dark_green, (100, 0), (100, 300), 5)
    pygame.draw.line(game_display, dark_green, (200, 0), (200, 300), 5)
    for row in range(3):
        for col in range(3):
            color = (84, 84, 84) if board[row][col]=="X" else (242, 235, 211)
            text = font.render(board[row][col], True, color)
            text_rect = text.get_rect()
            text_rect.center = (col * 100 + 50, row * 100 + 50)
            game_display.blit(text, text_rect)

# Check for any wins
def check():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return [-1, 1][board[i][1]=='O'], ("i", i)
        if board[0][i] == board[1][i] == board[2][i] != "":
            return [-1, 1][board[i][1]=='O'], ("j", i)
    if board[0][0] == board[1][1] == board[2][2] != "":
        return [-1, 1][board[1][1]=='O'], ("i-j", 0)
    if board[0][2] == board[1][1] == board[2][0] != "":
        return [-1, 1][board[1][1]=='O'], ("i+j", 0)
    free_space = [(i, j) for j in range(3) for i in range(3) if board[i][j] == '']
    return ("NA", 0) if free_space != [] else (0, 0)
    
        

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
            if dir == "i":
                color = (84, 84, 84) if board[pos][0]=="X" else (242, 235, 211)
                pygame.draw.line(game_display, color, (30, pos*100 + 50), (270, pos*100 + 50), 10)
            if dir == "j":
                color = (84, 84, 84) if board[0][pos]=="X" else (242, 235, 211)
                pygame.draw.line(game_display, color, (pos*100 + 50, 30), (pos*100 + 50, 270), 10)
            if dir == "i-j":
                color = (84, 84, 84) if board[1][1]=="X" else (242, 235, 211)
                pygame.draw.line(game_display, color, (50, 50), (250, 250), 10)
            if dir == "i+j":
                color = (84, 84, 84) if board[1][1]=="X" else (242, 235, 211)
                pygame.draw.line(game_display, black, (250, 50), (50, 250), 10)
            
        else:

            # Fill screen with text "DRAW"
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
