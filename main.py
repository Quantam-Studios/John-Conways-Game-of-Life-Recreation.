# Imports
import pygame, sys, random

# Variables
# Colors
BLUE = (10, 10, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
# Screen Size
SCREEN_X = 800
SCREEN_Y = 800
# grid cell size
blockSize = 20


def main():
    global SCREEN, CLOCK, color, WHITE, liveCellPositions, running
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    liveCellPositions = []
    color = 0
    FPS = 30
    running = False
    drawGrid()
    while True:
        # loop through all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Detect keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    print("cleared")
                    liveCellPositions = []
                    updateAll(liveCellPositions)
                    running = False
                if event.key == pygame.K_SPACE:
                    print("simulation has begun")
                    running = True
            # Detect Mouse Input (on click)
            if event.type == pygame.MOUSEBUTTONUP and running == False:
                mousePos = pygame.mouse.get_pos()
                color = SCREEN.get_at(pygame.mouse.get_pos())
                # Rect needs to be filled if the color is not white
                if color != WHITE:
                    liveCellPositions.append(toGridSpace(mousePos))
                    updateAll(liveCellPositions)
                # Rect needs to be filled with black
                elif color == WHITE:
                    pos = toGridSpace(mousePos)
                    print(pos)
                    index = liveCellPositions.index(pos)
                    liveCellPositions.remove(liveCellPositions[index])
                    updateAll(liveCellPositions)
            # Simulate
        if running == True:
            updateAll(liveCellPositions)
        pygame.display.update()
        CLOCK.tick(FPS)


# Convert to gridSpace
def toGridSpace(val):
    final = []
    final.append(val[0] // blockSize)
    final.append(val[1] // blockSize)
    return tuple(final)


def updateAll(liveCells):
    SCREEN.fill(BLACK)
    global liveCellPositions
    if running == True:
        liveCells = simulateCells(liveCells)
        liveCellPositions = liveCells
    drawLiveCells(liveCells)


def drawLiveCells(liveCells):
    for x in range(SCREEN_X // blockSize):
        for y in range(SCREEN_Y // blockSize):
            rect = pygame.Rect(x * blockSize, y * blockSize, blockSize,
                               blockSize)
            pos = [x, y]
            if tuple(pos) in liveCells:
                pygame.draw.rect(SCREEN, WHITE, rect, 0)
            else:
                pygame.draw.rect(SCREEN, BLACK, rect, 0)
            pygame.draw.rect(SCREEN, BLUE, rect, 1)


def drawGrid():
    for x in range(SCREEN_X // blockSize):
        for y in range(SCREEN_Y // blockSize):
            rect = pygame.Rect(x * blockSize, y * blockSize, blockSize,
                               blockSize)

            pygame.draw.rect(SCREEN, BLUE, rect, 1)


def simulateCells(lastCells):
    newCells = []
    for x in range(SCREEN_X // blockSize):
        for y in range(SCREEN_Y // blockSize):
            alive = False
            if tuple([x, y]) in lastCells:
                alive = True
            totalNeighbors = 0
            # cell top-mid check
            # #?#
            # ###
            # ###
            if tuple([x - 1, y]) in lastCells:
                totalNeighbors += 1
            # cell top-right check
            # ##?
            # ###
            # ###
            if tuple([x - 1, y + 1]) in lastCells:
                totalNeighbors += 1
            # cell mid-right check
            # ###
            # ##?
            # ###
            if tuple([x, y + 1]) in lastCells:
                totalNeighbors += 1
            # cell bottom-right check
            # ###
            # ###
            # ##?
            if tuple([x + 1, y + 1]) in lastCells:
                totalNeighbors += 1
            # cell bottom-mid check
            # ###
            # ###
            # #?#
            if tuple([x + 1, y]) in lastCells:
                totalNeighbors += 1
            # cell bottom-left check
            # ###
            # ###
            # ?##
            if tuple([x + 1, y - 1]) in lastCells:
                totalNeighbors += 1
            # cell mid-left check
            # ###
            # ?##
            # ###
            if tuple([x, y - 1]) in lastCells:
                totalNeighbors += 1
            # cell top-left check
            # ?##
            # ###
            # ###
            if tuple([x - 1, y - 1]) in lastCells:
                totalNeighbors += 1

            # apply rules based on neighbor count
            if totalNeighbors == 2 and alive or totalNeighbors == 3 and alive:
                newCells.append(tuple([x, y]))
            elif totalNeighbors == 3 and not alive:
                newCells.append(tuple([x, y]))
    print("done")
    return newCells


# Run This Script
main()
