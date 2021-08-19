import pygame, random

pygame.init()

BgGray = (187, 173, 160)
GrayForBlank = (204, 192, 178)
GrayFor2 = (238, 228, 218)
GrayFor4 = (236, 224, 200)
OrangeFor8 = (242, 177, 121)
OrangeFor16 = (224, 149, 100)
RedFor32 = (245, 124, 95)
RedFor64 = (246, 93, 59)
YellowFor128 = (237, 206, 113)
YellowFor256 = (237, 204, 97)
YellowFor512 = (236, 200, 80)
YellowFor1024 = (237, 197, 65)

ColorsForNum = {0: GrayForBlank, 2: GrayFor2, 4: GrayFor4, 8: OrangeFor8, 16: OrangeFor16, 32: RedFor32, 64: RedFor64, 128: YellowFor128,
                256: YellowFor256, 512: YellowFor512, 1024: YellowFor1024}

RowCol = 4
RowColGap = 7
TotalGapNum = 5
SqSize = 90

font = pygame.font.Font("04B_19.ttf", 30)
reStartFont = pygame.font.Font("04B_19.ttf", 20)

nums = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4]

WIDTH = RowCol*SqSize + TotalGapNum*RowColGap
clock = pygame.time.Clock()


def drawChar(screen, char, row, col, gapTimeCol, gapTimeRow):
    rect = pygame.Rect(col*SqSize+RowColGap*gapTimeCol, row*SqSize+RowColGap*gapTimeRow, SqSize, SqSize)
    pygame.draw.rect(screen, ColorsForNum[char], rect)

    if char != 0:
        num = font.render(str(char), True, (255, 255, 255))
        numRect = num.get_rect(center=(col * SqSize + RowColGap * gapTimeCol + 45, row * SqSize + RowColGap * gapTimeRow + 45))
        screen.blit(num, numRect)


def mainDraw(screen, board):
    gapTimeCol = 1
    gapTimeRow = 1
    for col in range(0, 4):
        for row in range(0, 4):
            char = board[row][col]
            if char != 0:
                char = int(char)
            drawChar(screen, char, row, col, gapTimeCol, gapTimeRow)
            gapTimeRow += 1
        gapTimeRow = 1
        gapTimeCol += 1


def gameOverWinScreen(screen, text):
    backGroundScreen = pygame.Surface((WIDTH, WIDTH))
    backGroundScreen.set_alpha(180)
    backGroundScreen.fill((255, 255, 255))
    screen.blit(backGroundScreen, (0, 0))

    gameOverText = font.render(f"{text}", True, (190, 190, 190))
    gameOverRect = gameOverText.get_rect(center=(WIDTH//2, WIDTH//2-35))
    screen.blit(gameOverText, gameOverRect)

    reStartText = reStartFont.render("Re Start", True, (190, 190, 190))
    reStartRect = gameOverText.get_rect(center=(WIDTH//2+reStartText.get_width()//2, WIDTH//2+reStartText.get_height()//2+10))

    buttonRect = pygame.Rect(WIDTH//2-reStartText.get_width()//2+1, WIDTH//2, reStartText.get_width()+10, reStartText.get_height()+10)
    pygame.draw.rect(screen, (255, 255, 255, ), buttonRect)
    screen.blit(reStartText, reStartRect)
    # print(buttonRect.top, buttonRect.bottom, buttonRect.right, buttonRect.left) 197 227 251 155


def checkWin(board, screen):
    for row in range(0, 4):
        for col in range(0, 4):
            if board[row][col] == 2048:
                gameOverWinScreen(screen, "You Win")
                break


def addNum(board):
    SQ = []
    newChar = random.choice(nums)
    for row in range(0, 4):
        for col in range(0, 4):
            if board[row][col] == 0:
                SQ.append([row, col])

    sqNone = random.choice(SQ)
    board[sqNone[0]][sqNone[1]] = newChar

    return board

def stack(board):
    new_matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        fill_position = 0
        for j in range(4):
            if board[i][j] != 0:
                new_matrix[i][fill_position] = board[i][j]
                fill_position += 1
    board = new_matrix
    return board


def combine(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                board[i][j] *= 2
                board[i][j + 1] = 0
    return board


def reverse(board):
    new_matrix = []
    for i in range(4):
        new_matrix.append([])
        for j in range(4):
            new_matrix[i].append(board[i][3 - j])
    board = new_matrix
    return board


def transpose(board):
    new_matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_matrix[i][j] = board[j][i]
    board = new_matrix
    return board


def left(board):
    newBoard = stack(board)
    newBoard = combine(newBoard)
    newBoard = stack(newBoard)
    if newboard != board:
        newBoard = addNum(newBoard)
    return newBoard


def right(board):
    newBoard = reverse(board)
    newBoard = stack(newBoard)
    newBoard = combine(newBoard)
    newBoard = stack(newBoard)
    newBoard = reverse(newBoard)
    if newBoard != board:
        newBoard = addNum(newBoard)
    return newBoard


def up(board):
    newBoard = transpose(board)
    newBoard = stack(newBoard)
    newBoard = combine(newBoard)
    newBoard = stack(newBoard)
    newBoard = transpose(newBoard)

    if newBoard != board:
        newBoard = addNum(newBoard)
    return newBoard


def down(board):
    newBoard = transpose(board)
    newBoard = reverse(newBoard)
    newBoard = stack(newBoard)
    newBoard = combine(newBoard)
    newBoard = stack(newBoard)
    newBoard = reverse(newBoard)
    newBoard = transpose(newBoard)

    if newBoard != board:
        newBoard = addNum(newBoard)
    return newBoard


    # Check if any moves are possible
def horizontal_move_exists(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1]:
                return True
    return False


def vertical_move_exists(board):
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i + 1][j]:
                return True
    return False


def isGameEnd(board, screen, GameStart):
    if not any(0 in row for row in board) and not horizontal_move_exists(board) and not vertical_move_exists(board):
        GameStart = False
        gameOverWinScreen(screen, "Game Over")
        return GameStart


def main():
    board = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             ]

    board = addNum(board)
    board = addNum(board)
    run = True
    gameStart = True

    screen = pygame.display.set_mode((WIDTH, WIDTH))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameStart is False:
                    location = pygame.mouse.get_pos()
                    print(location)
                    if 155 < location[0] < 251:
                        if 197 < location[1] < 229:
                            main()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    board = right(board)
                elif event.key == pygame.K_LEFT:
                    board = left(board)
                elif event.key == pygame.K_UP:
                    board = up(board)
                elif event.key == pygame.K_DOWN:
                    board = down(board)


        screen.fill(BgGray)
        mainDraw(screen, board)

        gameStart = isGameEnd(board, screen, gameStart)
        if gameStart is False:
            gameOverWinScreen(screen, "Game Over")
        checkWin(board, screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
