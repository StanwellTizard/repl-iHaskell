# author Joseph Bergin

#!/usr/bin/env python
# package: fmg
from PoliceMoveDialog import *

''' The French Military Game
  * @author jbergin
  Copyright 2023, Joseph Bergin 
  Educators are free to use this and adapt it for any classroom or
  training use, with attribution.It will appear shortly in the
  forthcoming "Beyond Monty Karel" by the same author. The book
  will also include and discuss a version using maps rather than
  array-like structure.
 '''


class Police():        
    ''' Handle the actions of the human player representing the police
    '''  
    def init(self):
        '''Reinitialize the Police positions for a new game'''
        #  for a new game
        self._policePositions = [0, 1, 3]

    @staticmethod
    def whereValue(L:int, M:int, R:int)->int:
        '''Compute the numeric value of the Police positions'''
        return int(2**L + 2**M + 2**R)
    
    def __init__(self):
        '''Create a representation of the three police positions at 0, 1, and 3'''
        self._policePositions = []
        self.init()
        self._ALLMOVES = [] #list of all legal police move values as binary numbers
        for L in range(9):
            for M in range(L+1, 10):
                for R in range(M+1, 11):
                    self._ALLMOVES.append(self.whereValue(L, M, R))
        print(self._ALLMOVES) #
    
    def holdingPosition(self, position:int)->bool:
        '''Determine whether any of the Police hold a given position
        @param position: the position to be checked
        '''
        for i in range(3):
            if position == self._policePositions[i]:
                return True
        return False
    
    def dumpAllMoves(self): # for debugging
        '''Debugging aid to look at the indexing array'''
        print(self._ALLMOVES)
        
    def showPosition(self):
        '''Show the three positions of the Police'''
        print('Police position: ', self._policePositions)
    
    def computeValueLocation(self)->int: #lookup the computed position in ALLMOVES
        '''Compute and return the computed value of the Police positions'''
        position = self._policePositions
        a = self.whereValue(position[0], position[1], position[2])
        try:
            return self._ALLMOVES.index(a)
        except Exception as ignored:
            return 0
    
    def warn(self):
        '''Warn about illegal moves'''
        print("Illegal: try again")

    def moveIfLegal(self, from_:int, to:int, fox:int)->bool:
        '''Determine the legality of a Police move and make the move if legal
        @param from_: the location of one police marker
        @param to: the proposed move from the current
        @param fox: the location of the Fox
        '''
        if not MoveRules.legalPoliceMove(from_, to):
            self.warn()
            return False
        if fox.position() == to:
            self.warn()
            return False
        here = -1
        i = 0
        for i in range(len(self._policePositions)):
            if self._policePositions[i] == from_:
                here = i
                break
        if here < 0:
            self.warn()
            return False
        for i in range(len(self._policePositions)):
            if self._policePositions[i] == to:
                self.warn()
                return False
        self._policePositions[here] = to
        return True

       
class Fox(object):
    '''Play the Fox, controlled by this program
    '''

    def init(self, start:int):
        '''Reinitialize the fox location for a new game
        @param start: the start location
        '''
        self._position = start

    def __init__(self, start:bool):
        '''Create the Fox object at a given location
        @param start: the start location
        '''
        self.init(start)

    def position(self)->int:
        '''Return the current location of the Fox'''
        return self._position

    def optimalMove(self, police:Police, memory:object):
        '''Compute the best available move and make it
        @param police: the Police object
        @param memory: the memory history object
        '''
        policeEntry = police.computeValueLocation()
        best = -1
        for trial in range(11):
            if MoveRules.legalFoxMove(self._position, trial) and not police.holdingPosition(trial):
                if best < 0:
                    best = trial
                else:
                    if memory.smaller(policeEntry, best, trial):
                        best = trial
        self._position = best
        
    def showPosition(self):
        '''Print out the current position of the Fox'''
        print ("Fox at " + str(self._position))
        
class MoveRules(object): # static class, no objects
    ''' A static class that represents the rules of the game
    '''
    # tuple of tuples: 11 by 11, rectangular - immutable Class variable
    LAYOUT = ( 
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
    def legalPoliceMove(cls, from_:int, to:int)->bool:
        '''Determine whether a move is legal for the Police
        @param from_: the current location of a police marker
        @param to: a proposed move
        '''
        return cls.LAYOUT[from_][to] == 2

    @classmethod
    def legalFoxMove(cls, from_:int, to:int)->bool:
        '''Determine whether a move is legal for the Fox
        @param from_: the current location of the Fox marker
        @param to: a proposed move
        '''
        return cls.LAYOUT[from_][to] > 0
        
class Display():
    '''  The visual _display in ASCII art for the French Military Game. 
        It shows the game board
        with the fox's current location marked. 
    '''
    
    MAPPER = ( # tuple of pairs - immutable, classVariable
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
            (3, 9), # 10 Maps the game cell numbers to _display array locations
            )
  
    def __init__(self, theFox:int):
        ''' Create a _display for the French Military Game with an initial 
        position for the fox
        * @param theFox: the initial position of the fox player. 
              Usually 5. 
        '''         
        self._theFox = theFox
        where = Display.MAPPER[theFox]
        self._display = ( # a tuple of lists. Entries will be modified
            # during a game to show the Fox. Warning: NOT rectangular
            [ "     ","1","--", "4", "--", "7"],
            [ "    /|\\ | /|\\"],
            [ "   / | \\|/ | \\"],
            [ "  ", "0", "--", "2", "--", "5", "--", "8", "--", "10" ],
            [ "   \\ | /|\\ | /" ],
            [ "    \\|/ | \\|/" ],
            [ "     ", "3", "--", "6", "--", "9"] 
            )
        self._display [where[0]][where[1]] = "F"

    def _unwind(self)->str:
        line = ''
        for entry in self._display:
            for string in entry:
                line += string
            line += '\n' 
        return line

    def show(self):
        '''Print the game board with current fox position marked'''
        print(self._unwind())

    def moveFox(self, fox:Fox):
        '''Move the marked location of the Fox to a new position
        @param fox: the Fox object
        '''
        where = Display.MAPPER[self._theFox]
        self._display[where[0]][where[1]] = str(self._theFox)
        self._theFox = fox.position()
        where = Display.MAPPER[self._theFox]
        self._display[where[0]][where[1]] = "F"
        
class MemoryManager():
    ''' Manage the memory of all games played, including on past runs
    '''
    
    def _buildHistory(self):
        history = []
        for outer in range(165):
            line = []
            for inner in range(11):
                line.append(0)
                history.append(line)
        return tuple(history)

    def __init__(self, filename, maxMoves):
        self._filename = filename
        self._history = self._buildHistory()
        self._thisGame = []

    def smaller(self, row:int, current:int, trial:int)->bool: #public
        '''Compare the history weights for a given police position
        @param row: the computed value of the three police
        @param current: the column of the current Fox location
        @param trial: a proposed move to a different location
        '''
        return self._history[row][current] < self._history[row][trial]

    def summarize(self, moves:list, outcome:int): #public
        '''Copy the current game data into the history
        @param moves: the number of moves in the game
        @param outcome: 1 or -1 depending on whether the Fox won or lost
        '''
        for i in range(moves):
            police = self._thisGame[i][0];
            fox = self._thisGame[i][1];
            self._history[police][fox] += outcome

    def record(self, fox:Fox, police:Police): #public
        '''Append a move outcome to the current game list
        @param fox: the Fox object
        @param police: a reference to the Police object
        '''
        self._thisGame.append((police.computeValueLocation(), fox.position()))

    def getMemoryx(self, smart): #public
        try:
            self._readFile(smart)
        except Exception as ignored: # wipe out the history if no file
            i = 0
            while i < len(self._history):
                j = 0
                while j < len(self._history[i]):
                    self._history[i][j] = 0
                    j += 1
                i += 1

    def getMemory(self, smart:bool): #public
        '''Read the memory file
        @param smart: True to read a file, otherwise create a fresh game
        '''
        try:
            self._readFile(smart)
        except Exception as ignored: # wipe out the history if no file
            for i in range(len(self._history)):
                for j in range(len(self._history[i])):
                    self._history[i][j] = 0

    def _readFile(self, smart:bool):
        memoryFile = None
        if smart:
            memoryFile = open(self._filename)
            text = memoryFile.read()
            strings = list(text.split())
            values = list(map(int, strings))
        k = 0
        for i in range(len(self._history)):
            for j in range(len(self._history[i])):
                if smart:
                    self._history[i][j] = values[k]
                    k += 1
                else:
                    self._history[i][j] = 0
            
    def _readFilex(self, smart):
        memoryFile = None
        if smart:
            memoryFile = open(self._filename)
            text = memoryFile.read()
            strings = list(text.split())
            values = list(map(int, strings))
        i = 0
        k = 0
        while i < len(self._history):
            j = 0
            while j < len(self._history[i]):
                if smart:
                    self._history[i][j] = values[k]
                    k += 1
                else:
                    self._history[i][j] = 0
                j += 1
            i += 1

    def saveMemory(self):
        ''' Write a memory file'''
        allvalues = ""
        for i in range(len(self._history)):
            for j in range(len(self._history[i])):
                allvalues +=  str(self._history[i][j]) + " "
        try:
            out = open(self._filename, 'w')
            out.write(allvalues)
            out.close()
        except Exception as e:
            print( "Could not write the memory file.")
            e.printStackTrace()

    def saveMemoryx(self):
        allvalues = ""
        i = 0
        while i < len(self._history):
            j = 0
            while j < len(self._history[i]):
                allvalues +=  str(self._history[i][j]) + " "
                j += 1
            i += 1
        try:
            out = open(self._filename, 'w')
            out.write(allvalues)
            out.close()
        except Exception as e:
            print( "Could not write the memory file.")
            e.printStackTrace()

class FMG():
    '''The game controller
    '''
    MAX_MOVES = 20
    WON = 1
    LOST = -1

    def __init__(self, startFox:int, smart:bool, filename:str):
        '''Create the game object
        @param startFox: the initial Fox position
        @param smart: whether the game should use the history or start fresh
        @param filename: the path to the history file
        '''
        self._memory = MemoryManager(filename, FMG.MAX_MOVES)
        self._memory.getMemory(smart)
        self._smart = smart
        self._police = Police()
        self._fox = Fox(startFox)
        self._startFox = startFox
        self._display = Display(self._fox.position()) 

    def play(self):
        '''Play a sequence of games using human player feedback'''
        while True:
            self.oneGame()
            print("Play again? - Y or N[N]")
            raw = input().strip() # could use just lstrip()
            if not raw:
                break
            reply = raw[0]
            if reply != 'y' and reply != 'Y':
                break
        if self._smart:
            self._memory.saveMemory()
        else:
            print('Overwrite existing history? - Y or N[N]')
            raw = input()
            if not raw:
                return
            reply = raw[0]
            if reply != 'y' and reply != 'Y':
                return
            print('Writing')
            self._memory.saveMemory()
            
    def showPositions(self):
        '''Show the positions of the player to guide them in playing'''
        self._police.showPosition()
        self._fox.showPosition()
        
    def getMoveFromDialog(self):
        '''Show the game status and get a move from the player using a dialog box.
        '''
        move = []
        while len(move) < 2:
            self.showPositions()
            print("Your move: from to  ( 0 0 to resign)")            
            move = policeMove() #from a dialog
            if len(move) < 2:
                print("Try again:")
        return (int(move[0]), int(move[1]))
        

    def getMove(self)->tuple:
        '''Show the game status and get a move from the player'''
        move = []
        while len(move) < 2:
            try:
                self.showPositions()
                print("Your move: from to  ( 0 0 to resign)")
                move = input().split()
                if len(move) < 2:
                    print("Two Integers needed. Try again:")
                if len(move) >= 2:
                    x = int(move[0])
                    y = int(move[1])
            except Exception as e:
                print("Integers needed. Try again:")
                move = []
        return (x, y)

    def init(self):
        '''Set up a single play'''
        self._fox.init(self._startFox)
        self._police.init()

    def oneGame(self):
        '''Execute the game once'''
        self.init()
        moves = 0
        print("Playing")
        outcome = 0
        while True:
            if moves > FMG.MAX_MOVES:
                print("Fox wins = timeout")
                outcome = FMG.WON
                break
            self._display.show()
            
            move = self.getMoveFromDialog() # 
#            move = self.getMove()

            from_ = move[0]
            to = move[1]
            print('You moved from',from_, 'to', to)
            if from_ == 0 and to == 0:
                print("Fox wins = resign")
                outcome = FMG.WON
                break
            if self._police.moveIfLegal(from_, to, self._fox):
                self._fox.optimalMove(self._police, self._memory)
                position = self._fox.position()
                if position > 0:#
                    self._memory.record(self._fox, self._police)
                moves += 1
                if position == 0:
                    print("Fox wins - home")
                    outcome = FMG.WON
                    break
                elif position < 0:
                    print("Fox loses - trapped")
                    outcome = FMG.LOST
                    break
                self._display.moveFox(self._fox)
                self.showPositions()
        self._memory.summarize(moves - 1, outcome)
               
if __name__ == '__main__' :
    filename = "../src/fmg.memory"
    game = FMG(5, True, filename)
    game.play()#

    for i in dir(Police):#
        print(i)# 
#    help(print)
    print (game._police._ALLMOVES)
   
    
