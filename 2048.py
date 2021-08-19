"""Game 2048"""

import pygame  # for game
import random  # for randomizing
from typing import *  # for type declaration


class Game2048:
    """Game 2048 class"""
    def __init__(self):
        """Initialize Game2048 class"""
        pygame.init()

        # Colors
        self.BgGray: tuple = (187, 173, 160)
        self.GrayForBlank: tuple = (204, 192, 178)
        self.GrayFor2: tuple = (238, 228, 218)
        self.GrayFor4: tuple = (236, 224, 200)
        self.OrangeFor8: tuple = (242, 177, 121)
        self.OrangeFor16: tuple = (224, 149, 100)
        self.RedFor32: tuple = (245, 124, 95)
        self.RedFor64: tuple = (246, 93, 59)
        self.YellowFor128: tuple = (237, 206, 113)
        self.YellowFor256: tuple = (237, 204, 97)
        self.YellowFor512: tuple = (236, 200, 80)
        self.YellowFor1024: tuple = (237, 197, 65)

        # ColorsForNumbers
        self.ColorsForNum: Dict[int : tuple] = {0: self.GrayForBlank, 2: self.GrayFor2, 4: self.GrayFor4, 8: self.OrangeFor8, 16: self.OrangeFor16, 32: self.RedFor32,
                                                64: self.RedFor64, 128: self.YellowFor128,
                                                256: self.YellowFor256, 512: self.YellowFor512, 1024: self.YellowFor1024}

        # row and sizes
        self.RowCol: int = 4
        self.RowColGap: int = 7
        self.TotalGapNum: int = 5
        self.SqSize: int = 90

        # fonts
        self.font: pygame.font = pygame.font.Font("04B_19.ttf", 30)
        self.restartFont: pygame.font = pygame.font.Font("04B_19.ttf", 20)

        # chance of numbers
        self.nums: List[int] = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]

        # sizes of screen
        self.SIZE: int = self.RowCol*self.SqSize + self.TotalGapNum*self.RowColGap

        # clock
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.board: List[List[int]] = [[0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                      ]

        self.gameStart = True

        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))
        pygame.display.set_caption("2048")

        self.run = True

    def checkWin(self) -> None:
        """Check win statment"""
        for row in range(0, 4):
            for col in range(0, 4):
                if self.board[row][col] == 2048:
                    self.gameOverWinScreen("You Win")
                    break

    def addNum(self):
        """Add a number to board"""
        SQ: List[List[int]] = []
        newChar: int = random.choice(self.nums)

        # find
        for row in range(0, 4):
            for col in range(0, 4):
                if self.board[row][col] == 0:
                    SQ.append([row, col])

        # set
        sqNone: List[int] = random.choice(SQ)
        self.board[sqNone[0]][sqNone[1]] = newChar

    def stack(self) -> None:
        """Stack"""
        new_matrix: List[List[int]] = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.board[i][j] != 0:
                    new_matrix[i][fill_position] = self.board[i][j]
                    fill_position += 1
        self.board = new_matrix

    def combine(self) -> None:
        """Combine"""
        for i in range(4):
            for j in range(3):
                if self.board[i][j] != 0 and self.board[i][j] == self.board[i][j + 1]:
                    self.board[i][j] *= 2
                    self.board[i][j + 1] = 0


    def reverse(self) -> None:
        """Reverse"""
        new_matrix: List[List[int]] = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.board[i][3 - j])

        self.board = new_matrix

    def transpose(self) -> None:
        """Transpose"""
        new_matrix: List[List[int]] = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.board[j][i]
        self.board = new_matrix

    def left(self) -> None:
        """Left"""
        copyBoard: List[List[int]] = self.board.copy()

        # move left
        self.stack()
        self.combine()
        self.stack()

        # check adding number
        if copyBoard != self.board:
            self.addNum()

    def right(self) -> None:
        """Right"""
        copyBoard: List[List[int]] = self.board.copy()

        # move right
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()

        # check adding number
        if copyBoard != self.board:
            self.addNum()

    def up(self) -> None:
        copyBoard: List[List[int]] = self.board.copy()

        # move up
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()

        # check adding number
        if copyBoard != self.board:
            self.addNum()

    def down(self) -> None:
        """Move Down"""
        copyBoard: List[List[int]] = self.board.copy()

        # move down
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()

        # check adding number
        if copyBoard != self.board:
            self.addNum()

    # check horizontal move
    def horizontal_move_exists(self) -> bool:
        """Horizontal move exists"""
        for i in range(4):
            for j in range(3):
                if self.board[i][j] == self.board[i][j + 1]:
                    return True
                return False

    # check vertical move
    def vertical_move_exists(self) -> bool:
        """Vertical move exists"""
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i + 1][j]:
                    return True
        return False

    # check is game end
    def isGameEnd(self,):
        """Is game end"""
        if not any(0 in row for row in self.board) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            self.gameStart = False
            self.gameOverWinScreen("Game Over")


    def gameOverWinScreen(self, text) -> None:
        """Show Game Over Or Win Screen"""

        # set background screen
        backgroundScreen: pygame.Surface = pygame.Surface((self.SIZE, self.SIZE))
        backgroundScreen.set_alpha(180)
        backgroundScreen.fill((255, 255, 255))
        screen.blit(backgroundScreen, (0, 0))

        # set game over text
        gameOverText: pygame.font = self.font.render(f"{text}", True, (190, 190, 190))
        gameOverRect: pygame.Rect = gameOverText.get_rect(center=(WIDTH // 2, WIDTH // 2 - 35))
        screen.blit(gameOverText, gameOverRect)

        # set restart text
        restartText: pygame.font = self.restartFont.render("Re Start", True, (190, 190, 190))
        restartRect: pygame.Rect = gameOverText.get_rect(center=(WIDTH // 2 + restartText.get_width() // 2, WIDTH // 2 + restartText.get_height() // 2 + 10))

        # buttons
        buttonRect: pygame.Rect = pygame.Rect(WIDTH // 2 - restartText.get_width() // 2 + 1, self.SIZE // 2, reStartText.get_width() + 10, reStartText.get_height() + 10)
        pygame.draw.rect(screen, (255, 255, 255,), buttonRect)  # draw rect
        screen.blit(restartText, restartRect)  # shor restart

    def start(self) -> None:
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]
                      ]

        # add 2 num
        self.addNum()
        self.addNum()
        self.gameStart = True

    def event(self) -> None:
        """Event loop"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            # mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameStart is False:
                    location = pygame.mouse.get_pos()
                    if 155 < location[0] < 251:
                        if 197 < location[1] < 229:
                            main()

            # move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.right()
                elif event.key == pygame.K_LEFT:
                    self.left()
                elif event.key == pygame.K_UP:
                    self.up()
                elif event.key == pygame.K_DOWN:
                    self.down()

    def main(self):
        """Main"""

        self.start()
        run = True

        while self.run:

            self.event()

            self.screen.fill(self.BgGray)
            self.mainDraw()


            self.isGameEnd()

            if self.gameStart is False:
                self.gameOverWinScreen("Game Over")
            self.checkWin()


            pygame.display.flip()
            self.clock.tick(30)


        pygame.quit()

    def mainDraw(self) -> None:
        """Main Draw"""
        gapTimeCol: int = 1  # Gap Time Col
        gapTimeRow: int = 1  # Gap Time Row

        for col in range(0, 4):
            for row in range(0, 4):
                char: int = self.board[row][col]
                if char != 0:
                    char = int(char)
                # draw chars
                self.drawChar(char, row, col, gapTimeCol, gapTimeRow)
                gapTimeRow += 1

            gapTimeRow = 1  # Change Gap Time Row
            gapTimeCol += 1  # Increase Gap Time Col

    def drawChar(self, char: int, row: int, col: int, gapTimeCol: int, gapTimeRow: int) -> None:
        """Draw A Char"""
        # create and draw rect
        rect: pygame.Rect = pygame.Rect(col * self.SqSize + self.RowColGap * gapTimeCol, row * self.SqSize + self.RowColGap * gapTimeRow, self.SqSize, self.SqSize)
        pygame.draw.rect(self.screen, self.ColorsForNum[char], rect)

        if char != 0:
            # render font and draw it
            num = self.font.render(str(char), True, (255, 255, 255))
            numRect = num.get_rect(
                center=(col * self.SqSize + self.RowColGap * gapTimeCol + 45, row * self.SqSize + self.RowColGap * gapTimeRow + 45))
            self.screen.blit(num, numRect)



if __name__ == "__main__":
    Game2048().main()