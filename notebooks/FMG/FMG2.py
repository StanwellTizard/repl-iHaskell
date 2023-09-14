#!/usr/bin/env python
# package: fmg

#  The visual display in ASCII art for the French Military Game. It shows the game board
#  * with the fox's current location marked. 
#  * @author jbergin
#  *
#  
class Display():
    # Create a display for the French Military Game with an initial position for the fox
    #      * @param theFox the initial position of the fox player. Usually 5. 
    #      
    
    MAPPER = ( # tuple of pairs - immutable
            (3, 1), # 0
            (0, 1), # 1
            (3, 3), # 2
            (6, 1), # 3
            (0, 3), # 4
            (3, 5), # 5
            (6, 3), # 6
            (0, 5), # 7
            (3, 7), # 8
            (6, 5), # 9
            (3, 9), # 10 Maps the game cell numbers to display array locations
            )
  
    def __init__(self, theFox):
        self.theFox = 5
        where = Display.MAPPER[theFox]
        self.display = ( # a tuple of lists. Entries will be modified
            # during a game to show the Fox. Warning: NOT rectangular
            [ "     ","1","--", "4", "--", "7"],
            [ "    /|\\ | /|\\"],
            [ "   / | \\|/ | \\"],
            [ "  ", "0", "--", "2", "--", "5", "--", "8", "--", "10" ],
            [ "   \\ | /|\\ | /" ],
            [ "    \\|/ | \\|/" ],
            [ "     ", "3", "--", "6", "--", "9"] 
            )
        self.display [where[0]][where[1]] = "F"

    def unwind(self):
        line = ''
        for entry in self.display:
            for string in entry:
                line += string
            line += '\n' 
        return line

    def show(self):
        print(self.unwind())

    def moveFox(self, fox):
        where = Display.MAPPER[self.theFox]
        self.display[where[0]][where[1]] = str(self.theFox)
        self.theFox = fox.position
        where = Display.MAPPER[self.theFox]
        self.display[where[0]][where[1]] = "F"
        
class MemoryManager():
    
    def buildHistory(self):
        history = []
        for outer in range(165):
            line = []
            for inner in range(11):
                line.append(0)
                history.append(line)
        return tuple(history)


    def __init__(self, filename, maxMoves):
        self.filename = filename
        self.history = self.buildHistory()
        self.thisGame = []

    def smaller(self, row, current, trial):
        return self.history[row][current] < self.history[row][trial]

    def summarize(self, moves:list, outcome:int): #public
        '''Copy the current game data into the history
        @param moves: the number of moves in the game
        @param outcome: 1 or -1 depending on whether the Fox won or lost
        '''
        for i in range(moves):
            policeLocation = self.thisGame[i][0];
            foxLocation = self.thisGame[i][1];
            self.history[policeLocation][foxLocation] += outcome

    def record(self, fox, police):
        self.thisGame.append((police.computeValueLocation(), fox.position))

    def getMemory(self, smart):
        try:
            self.readFile(smart)
        except Exception as e: # wipe out the history if no file
            i = 0
            while i < len(self.history):
                j = 0
                while j < len(self.history[i]):
                    self.history[i][j] = 0
                    j += 1
                i += 1

    def readFile(self, smart):
        memoryFile = None
        if smart:
            memoryFile = open(self.filename)
            text = memoryFile.read()
            strings = list(text.split())
            values = list(map(int, strings))
        i = 0
        k = 0
        while i < len(self.history):
            j = 0
            while j < len(self.history[i]):
                if smart:
                    self.history[i][j] = values[k]
                    k += 1
                else:
                    self.history[i][j] = 0
                j += 1
            i += 1

    def saveMemory(self):
        allvalues = ""
        i = 0
        while i < len(self.history):
            j = 0
            while j < len(self.history[i]):
                allvalues +=  str(self.history[i][j]) + " "
                j += 1
            i += 1
        try:
            out = open(self.filename, 'w')
            out.write(allvalues)
            out.close()
        except Exception as e:
            print( "Could not write the memory file.")
            e.printStackTrace()

class Police():          
    def init(self):
        #  for a new game
        self.policePositions = [0, 1, 3]

    @staticmethod
    def whereValue(L, M, R):
        return int(2**L + 2**M + 2**R)
    
    def __init__(self):
        self.policePositions = []
        self.init()
        self.allMoves = [] #list of all legal police move values as binary numbers
        for L in range(9):
            for M in range(L+1, 10):
                for R in range(M+1, 11):
                    self.allMoves.append(self.whereValue(L, M, R))
    
    def holdingPosition(self, position):
        for i in range(3):
            if position == self.policePositions[i]:
                return True
        return False
    
    def dumpAllMoves(self): # for debugging
        print(self.allMoves)
        
    def showPosition(self):
        print('Police position: ', self.policePositions)
    
    def computeValueLocation(self): #lookup the computed position in allMoves
        position = self.policePositions
        a = self.whereValue(position[0], position[1], position[2])
        try:
            return self.allMoves.index(a)
        except Exception as e:
            return 0
    
    def warn(self):
        print("Illegal: try again")

    def moveIfLegal(self, from_, to, fox):
        if not MoveRules.legalPoliceMove(from_, to):
            self.warn()
            return False
        if fox.position == to:
            self.warn()
            return False
        here = -1
        i = 0
        for i in range(len(self.policePositions)):
            if self.policePositions[i] == from_:
                here = i
                break
        if here < 0:
            self.warn()
            return False
        for i in range(len(self.policePositions)):
            if self.policePositions[i] == to:
                self.warn()
                return False
        self.policePositions[here] = to
        return True

       
class Fox(object):

    def init(self):
        self.position = 5

    def __init__(self):
        self.init()

    def position(self):
        return self.position

    def optimalMove(self, police, memory):
        policeEntry = police.computeValueLocation()
        best = -1
        for trial in range(11):
            if MoveRules.legalFoxMove(self.position, trial) and not police.holdingPosition(trial):
                if best < 0:
                    best = trial
                else:
                    if memory.smaller(policeEntry, best, trial):
                        best = trial
        self.position = best
        
    def showPosition(self):
        print ("Fox at " + str(self.position))
        
class MoveRules(object): # static class, no objects
    LAYOUT = ( # tuple of tuples: 11 by 11, rectangular - immutable Class variable
            ( 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0 ),
            ( 1, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0 ),
            ( 1, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0 ),
            ( 1, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0 ),
            ( 0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 0 ),
            ( 0, 1, 1, 1, 2, 0, 2, 2, 2, 2, 0 ),
            ( 0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 0 ),
            ( 0, 0, 0, 0, 1, 1, 0, 0, 2, 0, 2 ),
            ( 0, 0, 0, 0, 0, 1, 0, 2, 0, 2, 2 ),
            ( 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 2 ),
            ( 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0 ) 
            )
    #  fixed tuple of tuples: 11 by 11, rectangular immutable

    @classmethod
    def legalPoliceMove(cls, from_, to):
        return cls.LAYOUT[from_][to] == 2

    @classmethod
    def legalFoxMove(cls, from_, to):
        return cls.LAYOUT[from_][to] > 0
        
class FMG():
    MAX_MOVES = 20
    WON = 1
    LOST = -1

    def __init__(self, smart, filename):
        self.memory = MemoryManager(filename, FMG.MAX_MOVES)
        self.memory.getMemory(smart)
        self.police = Police()
        self.fox = Fox()
        self.display = Display(self.fox.position)

    def play(self):
        while True:
            self.oneGame()
            print("Play again?[no]")
            raw = input()
            if not raw:
                break
            reply = raw[0]
            if reply != 'y' and reply != 'Y':
                break
        self.memory.saveMemory()

    def showPositions(self):
        self.police.showPosition()
        self.fox.showPosition()

    def getMove(self):
        move = []
        while len(move) < 2:
            self.showPositions()
            print("Your move: from to  ( 0 0 to resign)")
            move = input().split()
            if len(move) < 2:
                print("Try again:")
        return (int(move[0]), int(move[1]))

    def init(self):
        self.fox.init()
        self.police.init()

    def oneGame(self):
        self.init()
        moves = 0
        print("Playing")
        outcome = 0
        while True:
            if moves > FMG.MAX_MOVES:
                print("Fox wins = timeout")
                outcome = FMG.WON
                break
            self.display.show()
            move = self.getMove()
            from_ = move[0]
            to = move[1]
            if from_ == 0 and to == 0:
                print("Fox wins = resign")
                outcome = FMG.WON
                break
            if self.police.moveIfLegal(from_, to, self.fox):
                self.fox.optimalMove(self.police, self.memory)
                position = self.fox.position
                if position > 0:
                    self.memory.record(self.fox, self.police)
                    moves += 1
                elif position == 0:
                    print("Fox wins - home")
                    outcome = FMG.WON
                    break
                elif position < 0:
                    print("Fox loses - trapped")
                    outcome = FMG.LOST
                    break
                self.display.moveFox(self.fox)
                self.showPositions()
        self.memory.summarize(moves - 1, outcome)
               
if __name__ == '__main__' :
    filename = "src/fmg.memory"
    game = FMG(True, filename)
    game.play()
