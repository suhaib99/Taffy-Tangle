import pygame, sys, os, random, copy, itertools
from pygame.locals import *

global NUM_OF_GEMS, NUM_OF_ROWS, NUM_OF_COLUMNS, SPACE_SIZE, HIGHLIGHT_COLOR, EMPTY_SPACE, STARTING_Y , FALL_SPEED, MOVE_SPEED, SCREEN_SIZE, BG_COLOR, GRID_COLOR
NUM_OF_GEMS = 6 #6 means 7 different gems
NUM_OF_ROWS = 8
NUM_OF_COLUMNS = 8
SPACE_SIZE = 64
HIGHLIGHT_COLOR = (230, 100, 230)
EMPTY_SPACE = -1
STARTING_Y  = 460
FALL_SPEED = 4
MOVE_SPEED = 3
SCREEN_SIZE = (700,650)
BG_COLOR = (255,250,255)
GRID_COLOR = (220,220,220)

global THREE_IN_ROW, FOUR_IN_A_ROW, FIVE_IN_A_ROW, BONUS
THREE_IN_A_ROW = 100
FOUR_IN_A_ROW = 200
FIVE_IN_A_ROW = 250
BONUS = 500
GIVEHINT = 0
class GameBoard:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption('Taffy Tangle')
        self.rows = NUM_OF_ROWS
        self.columns = NUM_OF_COLUMNS

        self.board = []
        for r in range(self.rows):
            self.board.append([])
        for row in self.board:
            for c in range(self.columns):
                row.append(None)

        self.boardRects = []
        for r in range(self.rows):
            self.boardRects.append([])
            

        self.animationProgress = 0
        self.state = 'starting'
        
    def setBoard(self):

        x,y = 0,0
        for row in self.boardRects:
            for c in range(self.columns):
                rect = pygame.Rect(x,y,SPACE_SIZE, SPACE_SIZE)
                row.append(rect)
                x += SPACE_SIZE
            x = 0
            y += SPACE_SIZE

        for r in range(self.rows):
            for c in range(self.columns):
                image = random.randint(0, NUM_OF_GEMS)
                x,y = self.boardRects[r][c].left, self.boardRects[r][c].top - STARTING_Y
                cell = Cell(image, (x,y))
                self.board[r][c] = cell
                
        #Check horizontal
        for row, column in itertools.product(range(self.rows), range(self.columns-2)):
            if self.board[row][column].image == self.board[row][column+1].image == self.board[row][column+2].image:
                top, bottom, left, right = None, None, None, None
                if row+1 < self.rows:
                    bottom = self.board[row+1][column].image
                if row-1 > 0:
                    top = self.board[row-1][column].image
                if column+1 < self.columns:
                    right = self.board[row][column+1].image
                if column-1 > 0:
                    left = self.board[row][column-1].image

                surrounding_gems = [top,bottom, left, right]
                
                gem_types = []
                for x in range(NUM_OF_GEMS+1):
                    gem_types.append(x)

                for gem in surrounding_gems:
                    if gem in gem_types:
                        gem_types.remove(gem)

                self.board[row][column].image = random.choice(gem_types)
                    
                    

        #Check vert
        for row, column in itertools.product(range(self.rows-2), range(self.columns)): 
            if self.board[row][column].image == self.board[row+1][column].image == self.board[row+2][column].image:

                top, bottom, left, right = None, None, None, None
                if row+1 < self.rows:
                    bottom = self.board[row+1][column].image
                if row-1 > 0:
                    top = self.board[row-1][column].image
                if column+1 < self.columns:
                    right = self.board[row][column+1].image
                if column-1 > 0:
                    left = self.board[row][column-1].image

                surrounding_gems = [top,bottom, left, right]
                
                gem_types = []
                for x in range(NUM_OF_GEMS+1):
                    gem_types.append(x)

                for gem in surrounding_gems:
                    if gem in gem_types:
                        gem_types.remove(gem)

                self.board[row][column].image = random.choice(gem_types)

    def getBoard(self):
        for row in self.board:
            yield row
    
    def startingAnimation(self):    
        if self.board[0][0].rect.top < self.boardRects[0][0].top:
            for row in self.board:
                for cell in row:
                    cell.rect.move_ip(0, +FALL_SPEED)

        else:
            #reset
            for r in range(self.rows):
                for c in range(self.columns):
                    self.board[r][c].rect.topleft = self.boardRects[r][c].topleft

            self.state = 'standby'

    def checkMouseClick(self, mousepos):
        for row in self.board:
            for cell in row:
                if cell.rect.collidepoint(mousepos):
                    r = self.board.index(row)
                    c = row.index(cell)
                    return (r,c)

        return None

    def swapGems(self, pos1, pos2):
        row1, column1 = pos1
        row2, column2 = pos2
        self.board[row1][column1].image, self.board[row2][column2].image  = self.board[row2][column2].image, self.board[row1][column1].image

    def animateSwap(self, pos1, pos2):
        row1, column1 = pos1
        row2, column2 = pos2

        cell1 = self.board[row1][column1]
        cell2 = self.board[row2][column2]

        direction1 = []
        direction2 = []

        if cell1.direction == [] and cell2.direction == []:
            if cell1.rect.x < cell2.rect.x and cell1.rect.y == cell2.rect.y:
                direction1 = [+MOVE_SPEED,0]
                direction2 = [-MOVE_SPEED,0]

            elif cell1.rect.x > cell2.rect.x and cell1.rect.y == cell2.rect.y:
                direction1 = [-MOVE_SPEED,0]
                direction2 = [+MOVE_SPEED,0]
                
            elif cell1.rect.y < cell2.rect.y and cell1.rect.x == cell2.rect.x:
                direction1 = [0,+MOVE_SPEED]
                direction2 = [0,-MOVE_SPEED]
                
            elif cell1.rect.y > cell2.rect.y and cell1.rect.x == cell2.rect.x:
                direction1 = [0,-MOVE_SPEED]
                direction2 = [0,+MOVE_SPEED]

            cell1.direction = direction1
            cell2.direction = direction2
            
            
        if self.animationProgress < SPACE_SIZE+1:
            cell1.rect.move_ip(cell1.direction)
            cell2.rect.move_ip(cell2.direction)
            

            self.animationProgress += MOVE_SPEED

        else:
            self.animationProgress = 0

            cell1.direction = []
            cell2.direction = []
            for r in range(self.rows):
                for c in range(self.columns):
                    self.board[r][c].rect.topleft = self.boardRects[r][c].topleft

            return 1 #Animation complete

    def checkIfAdjacent(self, pos1, pos2):
        if pos1[0] + 1 == pos2[0] or pos1[0] - 1 == pos2[0]:
            return True

        elif pos1[1] + 1 == pos2[1] or pos1[1] - 1 == pos2[1]:
            return True

        return False
            
    
    def isValidMove(self, pos1, pos2):
        if self.checkIfAdjacent(pos1, pos2) == True:
            self.swapGems(pos1, pos2)
            
            matches = self.checkMatches()
            if len(matches)>0:
                self.swapGems(pos1, pos2)
                return True

            self.swapGems(pos1, pos2)
        return False
    def checkMatches(self):
        skip = []
        matches = []
        for row in self.board:
            for column in range(self.columns-2):
                if (row[column].image == row[column+1].image == row[column+2].image) and (row[column].image != EMPTY_SPACE):
                    r = self.board.index(row)
                    if (r,column) in skip:
                        continue

                    else:
                        match = [(r, column), (r, column+1), (r, column+2)]
                        if column + 3 < self.columns and row[column+3].image == row[column].image:
                            match.append((r, column+3))

                        elif column + 4 < self.columns and row[column+4].image == row[column].image:
                            match.append((r, column+4))

                        matches.append(match)
                        skip.extend(match)

                
        skip = []
        for column in range(self.columns):
            for row in range(self.rows-2):
                if (self.board[row][column].image == self.board[row+1][column].image == self.board[row+2][column].image) and (self.board[row][column].image != EMPTY_SPACE):
                    if (row, column) in skip:
                        continue
                    else:
                        match = [(row,column),(row+1,column), (row+2,column)]
                        if row + 3 < self.rows and self.board[row+3][column].image == self.board[row][column].image:
                            match.append((row+3, column))

                        elif row + 4 < self.rows and self.board[row+4][column].image == self.board[row][column].image:
                            match.append((row+4, column))

                        matches.append(match)
                        skip.extend(matches)
                    
        return matches
                    
    
    def removeMatches(self):
        matches = self.checkMatches()

        threes = 0
        fours = 0
        fives = 0
        bonus = 0

        for match in matches:
            #print len(match)
            row, column = match[0]
                
            if len(match) == 3:
                threes += 1
                for pos in match:
                    row, column = pos
                    self.board[row][column].image = EMPTY_SPACE
            elif len(match) == 4:
                fours += 1
                row1, column1 = match[0]
                self.board[row][column].image = EMPTY_SPACE
                match.remove(match[0])
                for pos in match:
                    row, column = pos
                    self.board[row][column].image = EMPTY_SPACE
                    
            elif len(match) == 5:
                fives += 1
                for pos in match:
                    row, column = pos
                    self.board[row][column].image = EMPTY_SPACE
            

        if len(matches) > 0:
            return threes, fours, fives, bonus #There were matches

        return 0 #There were no matches, used to see if after pullDownGems, there needs to be an re-iteration for removing matches and pulling down again

    def animatePullDown(self, dropSlots):
        #Pull every cell over an empty cell 1 row down.
        #What cells should be animated? Only the ones in the same column as an empty space, but above the empty space as well.
        anim = []
        for dropSlot in dropSlots:
            row, column = dropSlot
            for r in range(row, -1, -1):
                if self.board[r][column].image != EMPTY_SPACE:
                    if self.board[r][column].rect.bottom != self.board[row][column].rect.bottom:
                        anim.append(self.board[r][column])


        if self.animationProgress < SPACE_SIZE:
            for cell in anim:
                cell.rect.move_ip(0, +MOVE_SPEED)

            self.animationProgress += MOVE_SPEED

        else:
            #Reset the board based on the board copy
            for row in range(self.rows):
                for column in range(self.columns):
                    self.board[row][column].rect.topleft = self.boardRects[row][column].topleft

            #Actually pull down the gems 1 row, by setting every cell's image to the image of the cell above it
            for dropSlot in dropSlots:
                row, column = dropSlot
                for r in range(row, -1, -1):
                    if r == 0:
                        self.board[r][column].image = random.randint(0, NUM_OF_GEMS)

                    else:
                        self.board[r][column].image = self.board[r-1][column].image

            self.animationProgress = 0 #Reset animation progress meter
                    
            return 1
        
    def getDropSlots(self):
        dropSlots = [] #A list of the bottom-most empty spaces in every column
        
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c].image == EMPTY_SPACE:
                    if r + 1 < self.rows:
                        while self.board[r+1][c].image == EMPTY_SPACE: #Find the bottom-most empty space in the column
                            if r + 1 < self.rows-1:
                                r += 1
                            else:
                                break
                            
                    if not (r,c) in dropSlots:
                        dropSlots.append((r,c))
                    

        return dropSlots
    
                
    def draw(self):
        for row in self.board:
            for cell in row:
                cell.draw(self.screen)


class Cell:
    #images found at voxol.com
    def __init__(self, image, pos):
        self.images = [pygame.image.load(os.path.join("images",'gem0.png')),
                     pygame.image.load(os.path.join("images",'gem1.png')),
                     pygame.image.load(os.path.join("images",'gem2.png')),
                     pygame.image.load(os.path.join("images",'gem3.png')),
                     pygame.image.load(os.path.join("images",'gem4.png')),
                     pygame.image.load(os.path.join("images",'gem5.png')),
                     pygame.image.load(os.path.join("images",'gem6.png'))]
        self.image = image
        """for i in range(0 ,7):
            image = pygame.transform.smoothscale(image, (SPACE_SIZE, SPACE_SIZE))"""
        self.rect = pygame.Rect(0,0,SPACE_SIZE, SPACE_SIZE)
        self.rect.topleft = pos

        self.direction = []



    def draw(self, surface):
        if self.image > EMPTY_SPACE:
            surface.blit(self.images[self.image], self.rect)
    def highlight(self, surface):
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, self.rect, 3)

class Score:
    def __init__(self, startingScore):
        self.score = startingScore
        self.font = pygame.font.SysFont("Arial", 32)

    def draw(self, screen, pos):
        score = self.font.render("Score: %d" % self.score, 1, (240,120,240))
        screen.blit(score, pos)

class Timer:
    def __init__(self):
        self.currentTime = pygame.time.get_ticks() / 1000
        self.timeLimit = self.currentTime + 60
        self.font = pygame.font.Font(None, 32)

        #self.image = pygame.image.load(os.path.join('images', 'timebar.png'))
        #self.increment = pygame.image.load("images/time_increment.png")


    def tick(self):
        time = pygame.time.get_ticks() / 1000
        self.currentTime = int(time)
    def gameEnd(self):
        if self.currentTime == int(self.timeLimit):
            return True
        return False

    def draw(self, screen, pos):
        timeLeft = self.timeLimit - self.currentTime
        timeText = self.font.render("Time Left: %d" % timeLeft, 1, (190,0,190))
        screen.blit(timeText, pos)

        bar_pos = (pos[0], pos[1] + 20)
        #screen.blit(self.image, bar_pos)

        

class Text:
    def __init__(self, font_size, message, pos=(0,0), color=(0,0,0)):
        self.font = pygame.font.Font(None, font_size)
        
        self.font_size = font_size
        self.message = message
        self.pos = pos
        self.color = color
        
        self.text = self.font.render(message, 1, color)
        self.rect = self.text.get_rect(topleft = pos)

        self.showing = True
        self.timeAtShow = 0

    def changeMessage(self, newMessage):
        self.message = newMessage
        self.text = self.font.render(self.message, 1, self.color)

    def changeFontSize(self, newSize):
        self.font_size = newSize
        self.font = pygame.font.Font(None, self.font_size)
        self.text = self.font.render(self.message, 1, self.color)
        self.rect = self.text.get_rect()

    def changeColor(self, newColor):
        self.color = newColor
        self.text = self.font.render(self.message, 1, self.color)

    def changePosition(self, newPos):
        self.pos = newPos
        self.rect.topleft = self.pos

    def tick(self):
        time = pygame.time.get_ticks() / 1000
        if time > self.timeAtShow + 1:
            self.showing = False

    def draw(self, screen):
        if self.showing == True:
            screen.blit(self.text, self.rect)

        
def runGame():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    gameBoard = GameBoard()
    gameBoard.setBoard()

    clock = pygame.time.Clock()

    pick1, pick2 = None, None
    dropSlots = []

    score = Score(0)
    timer = Timer()

    gameEnd = False

    #Text for the gameOver screen
    gameOverText = Text(64, "Game Over", (100,100))
    newGameText = Text(50, "Start New Game?", (100, 300))
    quitText = Text(50, "Quit", (440, 300))
    scoreText = Text(50, "Your Score is: %d" % score.score, (300, 250))

    #Text for comments
    goodText = Text(64, "Good!", color=(255,0,0))
    niceText = Text(64, "Nice!", color=(255,0,0))
    goodText.showing, niceText.showing = False, False
    comments = [goodText, niceText]

    lastScore = None
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if gameEnd == False:
                    if gameBoard.state == 'standby':
                        if pick1 == None:
                            pick1 = gameBoard.checkMouseClick(event.pos)

                        elif pick1 != None and pick2 == None:
                            pick2 = gameBoard.checkMouseClick(event.pos)

                        elif pick1 != None and pick2 != None:
                            pick1, pick2 = None, None
                else:
                    if newGameText.rect.collidepoint(event.pos):
                        runGame() #Reset game
                    elif quitText.rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                        
            elif event.type == MOUSEMOTION:
                if gameEnd == True:
                    if quitText.rect.collidepoint(event.pos):
                        quitText.changeColor((200,25,25))

                    else:
                        quitText.changeColor((0,0,0))

                    if newGameText.rect.collidepoint(event.pos):
                        newGameText.changeColor((200,25,25))

                    else:
                        newGameText.changeColor((0,0,0))
                        


        #Update Phase
        clock.tick(120)

        timer.tick()
        #Game On
        if gameEnd == False:
            #Check if time is up
            if timer.gameEnd() == True:
                #Game is over, get final score
                gameEnd = True
                scoreText.changeMessage("Score: %d" % score.score)

            #If a comment is showing, update its state, after a set time, it should dissappear 
            for comment in comments:
                if comment.showing == True:
                    comment.tick()

            #Starting Animation 
            if gameBoard.state == 'starting':
                gameBoard.startingAnimation()

            elif gameBoard.state == 'standby':
                #If two unique gems were picked, swap them, by changing gameBoard's state to swapping
                if pick1 != None and pick2 != None and pick1 != pick2:
                    if gameBoard.isValidMove(pick1, pick2) == True:
                        gameBoard.state = 'swapping'

                    else:
                        pick1, pick2 = None, None

                #However, if the same gem was selected twice, unselect both
                elif pick1 == pick2:
                    pick1, pick2 = None, None

            elif gameBoard.state == 'swapping':
                if gameBoard.animateSwap(pick1, pick2) == 1: #i.e. animation is done
                    gameBoard.swapGems(pick1, pick2)
                    pick1, pick2 = None, None
                    gameBoard.state = 'removeMatches'

            elif gameBoard.state == 'removeMatches':
                removed =  gameBoard.removeMatches() #i.e. there were matches, and all matches were removed
                if removed != 0:            
                    dropSlots = gameBoard.getDropSlots()
                    gameBoard.state = 'pullDown'
                    score.score += removed[0] * THREE_IN_A_ROW
                    score.score += removed[1] * FOUR_IN_A_ROW
                    score.score += removed[2] * FIVE_IN_A_ROW
                    score.score += removed[3]

                    if lastScore != None: #The player made a move, and that match was removed. However the resulting pullDown of gems created new matches
                        comment = random.choice(comments)
                        comment.changePosition((gameBoard.board[dropSlots[0][0]][dropSlots[0][1]].rect.topleft))
                        comment.showing = True
                        comment.timeAtShow = pygame.time.get_ticks() / 1000
                        print("WORKING") #REMOVE BEFORE TURNING IN
                elif removed == 0: #There were no matches, return to standby
                    gameBoard.state = 'standby'
                    lastScore = None

            elif gameBoard.state == 'pullDown':
                if gameBoard.animatePullDown(dropSlots) == 1:
                    dropSlots = gameBoard.getDropSlots()
                    if dropSlots != []:
                        gameBoard.state = 'pullDown'

                    else:
                        gameBoard.state = 'removeMatches'
                        lastScore = score.score
            

        #Draw to Screen Phase
        if gameEnd == False:
            screen.fill(BG_COLOR)
            
            #Draw the grid for the board
            for x in range(0,SPACE_SIZE*(NUM_OF_COLUMNS+1), SPACE_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (x, 0), (x,SPACE_SIZE*NUM_OF_ROWS))
            for y in range(0, SPACE_SIZE*(NUM_OF_ROWS+1), SPACE_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (0,y), (SPACE_SIZE*NUM_OF_COLUMNS, y))
                
            gameBoard.draw()
            score.draw(screen, (520,100))
            timer.draw(screen, (100, 530))
            if pick1 != None:
                gameBoard.board[pick1[0]][pick1[1]].highlight(screen) #Highlight the first chosen gem
            for comment in comments: #Draw any comments
                comment.draw(screen)

            pygame.display.update()

        else:
            screen.fill(BG_COLOR)
            
            gameOverText.draw(screen)
            newGameText.draw(screen)
            quitText.draw(screen)
            scoreText.draw(screen)

            pygame.display.update()


if __name__ == '__main__':
    runGame()
