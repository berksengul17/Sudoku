import pygame, requests
import numpy as np
from buttonClass import *
from sudokuSolver import *
from bs4 import BeautifulSoup

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 550

STARTPOS = [50, 75]
SIZE = 50

BUTTON_WIDTH = 70
BUTTON_HEIGHT = 30

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHTBLUE = (105, 229, 240)
GRAY = (128, 122, 105)
GREEN = (39, 161, 39)
YELLOW = (240,240,24)
LIGHTYELLOW = (255, 255, 0)
RED = (207, 11, 0)
LIGHTRED = (255,0,0)
DARKGRAY = (51, 51, 51)
LIGHTGREEN = (53, 222, 53)



class Sudoku:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Sudoku")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.selected = False
        self.running = True
        self.isBoardFull = False
        self.offset = 15
        self.lockedCells = []
        self.buttons = []
        self.grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]])

        self.createButtons()
        self.getPuzzle(1)
        self.run()

    def run(self):
        while self.running:
            self.events()
            self.draw()
            self.update()

    def update(self):
        if self.checkIfBoardFull():
            self.isBoardFull = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.buttons:
                        if button.isMouseOverButton():
                            self.load()
                            button.onClick()
                            print("Button", self.grid)
                            print("\n")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.isBoardFull:
                    self.resetBoard()
                    solve(self.grid)
                    print("Solve", self.grid)
                if self.selected and self.selected not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[0]][self.selected[1]] = int(event.unicode)
                        if not self.isValidInput((self.selected[0], self.selected[1])):
                            self.grid[self.selected[0]][self.selected[1]] = 0

    def getPuzzle(self, difficulty):
        URL = f"https://nine.websudoku.com/?level={difficulty}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        ids = ["f00","f10","f20","f30","f40","f50","f60","f70","f80",
            "f01", "f11", "f21", "f31", "f41", "f51", "f61", "f71", "f81",
            "f02", "f12", "f22", "f32", "f42", "f52", "f62", "f72", "f82",
            "f03", "f13", "f23", "f33", "f43", "f53", "f63", "f73", "f83",
            "f04", "f14", "f24", "f34", "f44", "f54", "f64", "f74", "f84",
            "f05", "f15", "f25", "f35", "f45", "f55", "f65", "f75", "f85",
            "f06", "f16", "f26", "f36", "f46", "f56", "f66", "f76", "f86",
            "f07", "f17", "f27", "f37", "f47", "f57", "f67", "f77", "f87",
            "f08", "f18", "f28", "f38", "f48", "f58", "f68", "f78", "f88"]

        for id in ids:
            tag = soup.find("input", {"id":id})
            try:
                self.grid[int(tag["id"][2])][int(tag["id"][1])] = tag["value"]
                self.lockedCells.append((int(tag["id"][2]), int(tag["id"][1])))
            except KeyError:
                pass



    def getMousePos(self):
        mousePos = pygame.mouse.get_pos()
        return mousePos

    def mouseOnGrid(self):
        mouseX, mouseY = self.getMousePos()

        if STARTPOS[0] <= mouseX <= STARTPOS[0] + 450 and STARTPOS[1] <= mouseY <= STARTPOS[1] + 450:
            row = (mouseY - STARTPOS[1]) // SIZE
            column = (mouseX - STARTPOS[0]) // SIZE
            return (row, column)
        else:
            return None

    def draw(self):
        self.screen.fill(WHITE)
        if self.selected:
            self.select()

        for button in self.buttons:
            button.drawButton()

        self.drawLockedCells()
        self.draw_board()
        self.drawNumbersOnGrid()


        if self.isBoardFull:
            self.display("Congratulations", (200, 40), 30, GREEN)

        pygame.display.flip()

    def draw_board(self):
        for i in range(10):
            if i % 3 == 0:
                #VERTICAL
                pygame.draw.line(self.screen, BLACK, (STARTPOS[0]+SIZE * i,STARTPOS[1]), (STARTPOS[0]+SIZE * i,STARTPOS[1]+450), 5)
                #HORIZONTAL
                pygame.draw.line(self.screen, BLACK, (STARTPOS[0], STARTPOS[1]+SIZE * i), (STARTPOS[0]+450, STARTPOS[1]+SIZE * i), 5)

            else:
                #VERTICAL
                pygame.draw.line(self.screen, BLACK, (STARTPOS[0]+SIZE * i,STARTPOS[1]), (STARTPOS[0]+SIZE * i,STARTPOS[1]+450))
                #HORIZONTAL
                pygame.draw.line(self.screen, BLACK, (STARTPOS[0], STARTPOS[1]+SIZE * i), (STARTPOS[0]+450, STARTPOS[1]+SIZE * i))

    def drawNumbersOnGrid(self):
        for row in range(9):
            for column in range(9):
                number = self.grid[row][column]
                if number != 0:
                    self.display(number, (STARTPOS[0] + column*SIZE + self.offset, STARTPOS[1] + row*SIZE - 3), 50, BLACK)

    def drawLockedCells(self):
        for row in range(9):
            for column in range(9):
                if (row,column) in self.lockedCells:
                    pygame.draw.rect(self.screen, GRAY, (STARTPOS[0]+column*SIZE, STARTPOS[1]+row*SIZE, SIZE, SIZE))

    def createButtons(self):
        midPoint = SCREEN_WIDTH // 2

        self.buttons.append(Button(self.screen, "Easy", GREEN, LIGHTGREEN, BUTTON_WIDTH, BUTTON_HEIGHT, midPoint - 200, 30, self.getPuzzle, 1))
        self.buttons.append(Button(self.screen, "Medium",YELLOW, LIGHTYELLOW, BUTTON_WIDTH, BUTTON_HEIGHT, midPoint - 30, 30, self.getPuzzle, 2))
        self.buttons.append(Button(self.screen, "Hard",RED, LIGHTRED, BUTTON_WIDTH, BUTTON_HEIGHT, midPoint + 130, 30, self.getPuzzle, 3))

    def select(self):
        row = self.selected[0]
        column = self.selected[1]

        pygame.draw.rect(self.screen, LIGHTBLUE, (column*SIZE + STARTPOS[0], row*SIZE + STARTPOS[1], SIZE, SIZE))

    def checkIfBoardFull(self):
        for row in range(9):
            for column in range(9):
                if self.grid[row][column] == 0:
                    return False

        return True

    def resetBoard(self):
        for row in range(9):
            for column in range(9):
                if (row, column) not in self.lockedCells:
                    self.grid[row][column] = 0

    def isValidInput(self, pos):
        if self.checkRows(pos) and self.checkColumns(pos) and self.checkSquares(pos):
            return True

        return False

    def checkRows(self, pos):
        numToCheck = self.grid[pos[0]][pos[1]]

        for column in range(9):
            if self.grid[pos[0]][column] == numToCheck and column != pos[1]:
                return False

        return True

    def checkColumns(self, pos):
        numToCheck = self.grid[pos[0]][pos[1]]

        for row in range(9):
            if self.grid[row][pos[1]] == numToCheck and row != pos[0]:
                return False

        return True

    def checkSquares(self, pos):
        row = pos[0]
        column = pos[1]

        numToCheck = self.grid[row][column]

        startRow = row - (row % 3)
        startColumn = column - (column % 3)

        for i in range(startRow, startRow + 3):
            for j in range(startColumn, startColumn + 3):
                if self.grid[i][j] == numToCheck and (i,j) != (row, column):
                    return False

        return True

    def load(self):
        self.isBoardFull = False
        self.lockedCells = []

        for row in range(9):
            for column in range(9):
                self.grid[row][column] = 0


    def display(self, text, position, fontSize, color):
        font = pygame.font.SysFont("arial", fontSize)
        text = font.render(str(text), True, color)
        self.screen.blit(text, position)

    def isInt(self, key):
        try:
            int(key)
            return True
        except:
            return False


if __name__ == '__main__':
    sudoku = Sudoku()