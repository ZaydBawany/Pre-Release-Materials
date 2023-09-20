# Import necessary modules
import random  # Module for random number generation
import os      # Module for file operations

# Define the main function
def Main():
    # Initialize variables to control the game loop and keep track of the player's score
    Again = "y"  # Player's choice to play again
    Score = 0    # Player's score
    
    while Again == "y":
        # Prompt the user to either start a standard puzzle or enter the name of a file to load a puzzle
        Filename = input("Press Enter to start a standard puzzle or enter the name of the file to load: ")
        
        if len(Filename) > 0:
            # If a filename is provided, load the puzzle from the file
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            # If no filename is provided, create a new random puzzle
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        
        # Play the puzzle and store the player's score
        Score = MyPuzzle.AttemptPuzzle()
        
        # Print the player's score after finishing the puzzle
        print("Puzzle finished. Your score was: " + str(Score))
        
        # Ask the player if they want to play another puzzle
        Again = input("Do another puzzle? ").lower()

# Define the Puzzle class
class Puzzle():
    def __init__(self, *args):
        if len(args) == 1:
            # Load the puzzle from the specified file if only one argument is provided
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            # Create a new random puzzle if multiple arguments are provided
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []

            # Generate the grid with random cells (90% chance for regular cell, 10% for blocked cell)
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)

            # Initialize allowed patterns and symbols
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []

            # Define and add specific patterns and symbols
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

    def __LoadPuzzle(self, Filename):
        try:
            # Open the specified file for reading
            with open(Filename) as f:
                # Read the number of symbols from the first line of the file
                NoOfSymbols = int(f.readline().rstrip())

                # Read and add allowed symbols to the list
                for Count in range(1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())

                # Read the number of patterns from the file
                NoOfPatterns = int(f.readline().rstrip())

                # Read each pattern line from the file and create Pattern objects
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)

                # Read the grid size from the file
                self.__GridSize = int(f.readline().rstrip())

                # Read each cell's data from the file and create the grid
                for Count in range(1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)

                # Read the player's score and symbols left from the file
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            # Handle exceptions if the puzzle cannot be loaded
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            # Display the current state of the puzzle
            self.DisplayPuzzle()
            
            # Display the player's current score
            print("Current score: " + str(self.__Score))

            # Get the row number from the player
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass

            # Get the column number from the player
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass

            # Get a symbol from the player
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)

            # Check if the symbol can be placed in the current cell
            if CurrentCell.CheckSymbolAllowed(Symbol):
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                
                # If a pattern match is found, update the score
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore

            # Check if the game is finished (no symbols left to place)
            if self.__SymbolsLeft == 0:
                Finished = True
        
        # Display the final state of the puzzle and return the player's score
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        # Get the cell at the specified row and column
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        # Check for pattern matches in the puzzle grid starting from the specified row and column
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    
                    # Check if the pattern matches any allowed patterns.
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            # Add the current symbol to the not allowed symbols of matching cells.
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        # Get a symbol from the player.
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        # Create a horizontal line for displaying the grid.
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        # Display the current state of the puzzle.
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

# Define the Pattern class
class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        # Initialize a Pattern object with a symbol and a pattern sequence.
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def MatchesPattern(self, PatternString, SymbolPlaced):
        # Check if a given pattern matches the current pattern sequence with a symbol placed.
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
        return self.__PatternSequence

# Define the Cell class
class Cell():
    def __init__(self):
        # Initialize a Cell object with an empty symbol and an empty list of symbols not allowed.
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        # Get the symbol in the cell (return "-" if empty).
        if self.IsEmpty():
            return "-"
        else:
            return self._Symbol

    def IsEmpty(self):
        # Check if the cell is empty (no symbol).
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        # Change the symbol in the cell to the specified symbol.
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        # Check if a symbol is allowed to be placed in the cell.
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        # Add a symbol to the list of symbols not allowed in the cell.
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass

# Define the BlockedCell class, which inherits from Cell
class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        # Initialize a BlockedCell object with a symbol "@" (blocked).
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        # Override CheckSymbolAllowed to disallow any symbol in a blocked cell.
        return False

# Check if the script is executed as the main program
if __name__ == "__main__":
    Main()
