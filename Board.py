import random

class Board:

    def __init__(self, dim):
        self.__dim = dim
        self.genBoard()

    def genBoard(self):
        d1 = ['R', 'I', 'F', 'O', 'B', 'X']
        d2 = ['I', 'F', 'E', 'H', 'E', 'Y']
        d3 = ['D', 'E', 'N', 'O', 'W', 'S']
        d4 = ['U', 'T', 'O', 'K', 'N', 'D']
        d5 = ['H', 'M', 'S', 'R', 'A', 'O']
        d6 = ['L', 'U', 'P', 'E', 'T', 'S']
        d7 = ['A', 'C', 'I', 'T', 'O', 'A']
        d8 = ['Y', 'L', 'G', 'K', 'U', 'E']
        d9 = ['Qu', 'B', 'M', 'J', 'O', 'A']
        d10 = ['E', 'H', 'I', 'S', 'P', 'N']
        d11 = ['V', 'E', 'T', 'I', 'G', 'N']
        d12 = ['B', 'A', 'L', 'I', 'Y', 'T']
        d13 = ['E', 'Z', 'A', 'V', 'N', 'D']
        d14 = ['R', 'A', 'L', 'E', 'S', 'C']
        d15 = ['U', 'W', 'I', 'L', 'R', 'G']
        d16 = ['P', 'A', 'C', 'E', 'M', 'D']
        dice = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16]
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Qu', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        if self.__dim < 2:
            print("no")
            return

        random.shuffle(dice)
        letters = []
        for die in dice:
            letters += [random.choice(die)]
        remaining = max(0, self.__dim**2 - len(letters))
        for i in range(remaining):
            letters += [random.choice(alphabet)]
            
        random.shuffle(letters)
        board = []
        for i in range(self.__dim):
            board += [[]]
            for j in range(self.__dim):
                board[i] += [letters.pop()]

        self.__board = board

    def __str__(self):
        output = ""
        for row in self.__board:
            for col in row:
                if col == 'Qu': output += "Qu "
                else: output += col + "  "
            output += "\n"
        output = output[:-1]
        return output

    def contains(self, word):

        def containsHelper(word, letters, prev):
            if not word:
                return True
            elif word[0:2] == "QU":
                increment = 2
                search = "Qu"
            else:
                increment = 1
                search = word[0]

            for i in range(max(0, prev[0] - 1), min(self.__dim, prev[0] + 2)):
                for j in range(max(0, prev[1] - 1), min(self.__dim, prev[1] + 2)):
                    if letters[i][j] == search:
                        if containsHelper(word[increment:], letters[:i] + [letters[i][:j] + [""] + letters[i][j+1:]] + letters[i+1:], (i, j)):
                            return True
            return False

        word = word.upper()
        letters = self.getLetters()

        if not word:
            return True
        elif word[0:2] == "QU":
            increment = 2
            search = "Qu"
        else:
            increment = 1
            search = word[0]
            
        for i in range(self.__dim):
            for j in range(self.__dim):
                if letters[i][j] == search:
                    if containsHelper(word[increment:], letters[:i] + [letters[i][:j] + [""] + letters[i][j+1:]] + letters[i+1:], (i, j)):
                        return True         
        return False

    def getLetters(self):
        return [row[:] for row in self.__board]
