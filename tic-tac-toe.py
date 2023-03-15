import pygame

pygame.init()

display_width = 300
display_height = 300
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tic Tac Toe")

class Board:
    def __init__(self) -> None:
        self.board = [['']*3, ['']*3, ['']*3]
        self.free_space = [(i, j) for j in range(3) for i in range(3) if self.board[i][j] == '']
    
    def check(self) -> tuple[int, str, str]:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return (i, "i", self.board[i][1])
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return (i, "j", self.board[1][i])
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return (0, "i-j", self.board[1][1])
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return (0, "i+j", self.board[1][1])
        free_space = sum(self.board[i][j]=='' for j in range(3) for i in range(3))
        return (0, "i", "NA") if free_space != 0 else (0, "i", "draw")

    def minimax(self, state: bool) -> int:
        _, _, winner = self.check()
        if winner != "NA":
            return {"X": -1, "draw": 0, "O": 1}[winner]
        bestVal = (3, -3)[state]
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "XO"[state]
                    val = self.minimax(not state)
                    self.board[i][j] = ""
                    if state:
                        bestVal = max(bestVal, val)
                    else:
                        bestVal = min(bestVal, val)
        return bestVal
    
    def draw(self) -> None:
        game_display.fill(green)
        for i in range(1, 3):
            draw_line((0, i * 100), (300, i * 100))
            draw_line((i * 100, 0), (i * 100, 300))
        for i in range(3):
            for j in range(3):
                text = font.render(self.board[i][j], True, choose_color(self.board[i][j]))
                text_rect = text.get_rect()
                text_rect.center = (j * 100 + 50, i * 100 + 50)
                game_display.blit(text, text_rect)
    
    def placeXO(self, row, col) -> None:
        if self.board[row][col] == '':
            self.board[row][col] = 'X'
            self.free_space.remove((row, col))
            if self.free_space != []:
                bestVal, posi, posj = -3, 0, 0
                for i, j in self.free_space:
                    self.board[i][j] = "O"
                    val = self.minimax(False)
                    self.board[i][j] = ""
                    if val > bestVal:
                        bestVal, posi, posj = val, i, j
                self.board[posi][posj] = 'O'
                self.free_space.remove((posi, posj))

# Define the board
board = Board()

# Define the colors
green = (20, 189, 172)
black = (0, 0, 0)
choose_color = lambda p: (84, 84, 84) if p == "X" else (242, 235, 211)

# Reducing function
draw_line = lambda a, b: pygame.draw.line(game_display, (13, 161, 146), a, b, 5)

# Define the font
font = pygame.font.SysFont(None, 100)


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
            board.placeXO(row, col)
            

    # Draw the board
    board.draw()
    pygame.display.update()
    
    # Check for winner
    pos, dir, winner = board.check()
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
                    draw_line((10, pos*100 + 50), (w, pos*100 + 50))
                if dir == "j":
                    draw_line((pos*100 + 50, 10), (pos*100 + 50, w))
                if dir == "i-j":
                    draw_line((10, 10), (w, w))
                if dir == "i+j":
                    draw_line((290, 10), (300-w, w))
                pygame.display.update()
                pygame.time.delay(1)

        # Keep the screen for 3 seconds
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        quit()

