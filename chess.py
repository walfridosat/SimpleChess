class Board():

    def __init__(self) -> None:

        # default settings

        self.board = [[None]*8 for i in range(8)]
        self.ids = {
             1 : "king",
             2 : "queen",
             3 : "bishop",
             4 : "knight",
             5 : "rook",
             6 : "pawn"
        }
        self.player = 0
        self.enpassant = [[False]*8,[False]*8]

    def updateMoves(self):
        for i in range(8):
             for j in range(8):
                  if self.board[i][j] is not None:
                       self.board[i][j].generateMoves()
                       

    def getDefaultBoard(self):
        
        defaultBoard = []

        Line1 = [Rook(self,(0,0),1), Knight(self,(0,1),1), Bishop(self,(0,2),1)]
        Line1 += [Queen(self,(0,3),1)] + [King(self,(0,4),1)]
        Line1 += [Bishop(self,(0,5),1), Knight(self,(0,6),1), Rook(self,(0,7),1)]

        Line2 = [Pawn(self,(1,i),1) for i in range(8)]

        Line3_6 = [[None]*8 for i in range(4)]

        Line7 = [Pawn(self,(6,i),0) for i in range(8)]

        Line8 = [Rook(self,(7,0),0), Knight(self,(7,1),0), Bishop(self,(7,2),0)]
        Line8 += [Queen(self,(7,3),0)] + [King(self,(7,4),0)]
        Line8 += [Bishop(self,(7,5),0), Knight(self,(7,6),0), Rook(self,(7,7),0)]

        defaultBoard.append(Line1)
        defaultBoard.append(Line2)

        for line in Line3_6:
            defaultBoard.append(line)

        defaultBoard.append(Line7)
        defaultBoard.append(Line8)

        return defaultBoard
    
    def setDefaultBoard(self):
         self.board = self.getDefaultBoard()
         self.updateMoves()


    def isValid(self, pos: tuple):
        return pos[0] >= 0 and pos[0] < 8 and pos[1] >=0 and pos[1] < 8

    def getDiagonals(self, position: tuple, team_check: int):
        
        i,j = position[0], position[1]
        moves_on_diagonal = []
        
        for iterate_1 in [1,-1]:
            
            for iterate_2 in [1,-1]:
                temp1,temp2 = i+iterate_1,j+iterate_2
                
                while self.isValid((temp1,temp2)):
                        if self.board[temp1][temp2] is None:
                            moves_on_diagonal.append((temp1,temp2))
                        
                        elif self.board[temp1][temp2].team != team_check:
                            moves_on_diagonal.append((temp1,temp2))
                            break
                        else:
                            break

                        temp1+=iterate_1
                        temp2+=iterate_2

        return moves_on_diagonal
    
    def getSides(self, position: tuple, team_check: int):
        
        
        moves_on_side = []
        for iterate in [1,-1]:

            i,j = position[0], position[1]
            while self.isValid((i+iterate,j)):
                 if self.board[i+iterate][j] is None:
                      moves_on_side.append((i+iterate,j))
                 elif self.board[i+iterate][j].team != team_check:
                      moves_on_side.append((i+iterate,j))
                      break
                 else:
                      break
                 i+=iterate

            i,j = position[0], position[1]
            while self.isValid((i,j+iterate)):
                 if self.board[i][j+iterate] is None:
                      moves_on_side.append((i,j+iterate))
                 elif self.board[i][j+iterate].team != team_check:
                      moves_on_side.append((i,j+iterate))
                      break
                 else:
                      break
                 j+=iterate
        return moves_on_side

    def getLeaps(self, position: tuple, team_check: int):
        
        i,j = position[0], position[1]
        moves_on_leap = []

        for iterate_1 in [2,-2]:
             
             for iterate_2 in [1,-1]:
                    temp1,temp2 = i+iterate_1,j+iterate_2


                    if self.isValid((temp1,temp2)):
                        if self.board[temp1][temp2] is None:
                            moves_on_leap.append((temp1,temp2))
                        
                        elif self.board[temp1][temp2].team != team_check:
                            moves_on_leap.append((temp1,temp2))
                            
                    
                    temp1,temp2 = i+iterate_2,j+iterate_1
                    if self.isValid((temp1,temp2)):
                        if self.board[temp1][temp2] is None:
                            moves_on_leap.append((temp1,temp2))
                        
                        elif self.board[temp1][temp2].team != team_check:
                            moves_on_leap.append((temp1,temp2))
                            
        return moves_on_leap         

    def getPush(self, position: tuple, team_check: int):
        i,j = position[0], position[1]
        moves_on_push = [] 

        if i==6 and team_check==0 and self.board[i-1][j] is None and self.board[i-2][j] is None:
             moves_on_push.append((i-2,j))
        if i==1 and team_check==1 and self.board[i+1][j] is None and self.board[i+2][j] is None:
             moves_on_push.append((i+2,j))

        mover = 1 if team_check else -1

        # very bad ifs
        if self.isValid((i,j-1)):
            if self.board[i][j-1]:
                if self.board[i][j-1].id == 6:
                    if self.board[i][j-1].enpassant:
                        moves_on_push.append((i+mover,j-1))
        
        if self.isValid((i,j+1)):
            if self.board[i][j+1]:
                if self.board[i][j+1].id == 6:
                    if self.board[i][j+1].enpassant:
                        moves_on_push.append((i+mover,j+1))
                  

        if self.isValid((i+mover,j)):
                if self.board[i+mover][j] is None:
                    moves_on_push.append((i+mover,j))
        
        if self.isValid((i+mover,j+1)):
                if self.board[i+mover][j+1] is not None and self.board[i+mover][j+1].team != team_check:
                    moves_on_push.append((i+mover,j+1))

        if self.isValid((i+mover,j-1)):
                if self.board[i+mover][j-1] is not None and self.board[i+mover][j-1].team != team_check:
                    moves_on_push.append((i+mover,j-1))

        return moves_on_push
    
    def getKing(self, position: tuple, team_check: int):
        i,j = position[0], position[1]
        moves_on_king = []

        for iterate1 in [-1,0,1]:
             for iterate2 in [-1,0,1]:
                  if self.isValid((i+iterate1,j+iterate2)) and (iterate1!=0 or iterate2!=0):
                        if self.board[i+iterate1][j+iterate2] is None:
                            moves_on_king.append((i+iterate1,j+iterate2))
                        elif self.board[i+iterate1][j+iterate2].team != team_check:
                            moves_on_king.append((i+iterate1,j+iterate2))
        
        return moves_on_king
    
    def returnPosition(self, position: tuple):
         return self.board[position[0]][position[1]]

    def validSide(self, piece, pos2):
        pos1 = piece.position
        return pos1[0]==pos2[0] or pos1[1] == pos2[1]
    
    def validDiagonal(self, piece, pos2):
        pos1 = piece.position 
        return abs(pos1[0]-pos2[0]) == abs(pos1[1]-pos2[1])

    def validLeap(self, piece, pos2):
        pos1 = piece.position 
        a = abs(pos1[0]-pos2[0])
        b = abs(pos1[1]-pos2[1])
        return (a == 2 and b == 1) or (a == 1 and b == 2)

    def validPush(self, piece, pos2):
        pos1 = piece.position
        if (pos1[0] == 7 and piece.team == 0) or (pos1[0] == 1 and piece.team == 1):
            return abs(pos1[0]-pos2[0])<3
        return abs(pos1[0]-pos2[0])<2

    def validKing(self, pos1, pos2):
        a = abs(pos1[0]-pos2[0])
        b = abs(pos1[1]-pos2[1])
        return (a<2 and b<2)

    def checkCheck(self):
        for line in self.board:
             for piece in line:
                  if piece:
                        for move in piece.generateMoves():
                            if self.returnPosition(move).id:
                                return piece
        return None
    
    def tryMove(self, piece, pos):
         if piece is None:
              return False
         if piece.team != self.player:
              return False
         if pos in piece.possibleMoves.keys():
              if piece.id == 6:
                   if abs(pos[0]-piece.position[0])==2:
                        piece.enpassant = True
                   else:
                        piece.enpassant = False
              if piece.id == 6 and pos[1] != piece.position[1] and self.board[pos[0]][pos[1]] is None:
                   # black é 1
                   mover = -1 if piece.team else 1
                   if self.board[pos[0]+mover][pos[1]].id == 6:
                        if self.board[pos[0]+mover][pos[1]].enpassant:
                             self.board[pos[0]+mover][pos[1]] = None
                        
              self.board[pos[0]][pos[1]] = piece
              self.board[piece.position[0]][piece.position[1]] = None
              piece.position = (pos[0],pos[1])
              self.player = (self.player+1)%2
              self.updateMoves()
              return True
         return False

class Queen():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 2
        self.value = 8
        self.gameEnviroment = board
        self.position = position
        self.team = team
        self.possibleMoves = {}
    def generateMoves(self):
        self.possibleMoves.clear()
        for move in self.gameEnviroment.getDiagonals(self.position, self.team) + self.gameEnviroment.getSides(self.position, self.team):
             self.possibleMoves[move] = 1
    
class Rook():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 5
        self.value = 5
        self.gameEnviroment = board
        self.position = position
        self.team = team
        self.possibleMoves = {}

    def generateMoves(self):
        self.possibleMoves.clear()
        for move in self.gameEnviroment.getSides(self.position, self.team):
             self.possibleMoves[move] = 1

class Knight():    
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 4
        self.value = 3
        self.gameEnviroment = board
        self.position = position
        self.team = team
        self.possibleMoves = {}

    def generateMoves(self):
        self.possibleMoves.clear()
        for move in self.gameEnviroment.getLeaps(self.position, self.team):
             self.possibleMoves[move] = 1
        
    
class Pawn():
    def __init__(self, board: Board, position: tuple, team:int):
        self.enpassant = False
        self.id = 6
        self.value = 1
        self.gameEnviroment = board
        self.position = position
        self.team = team
        self.possibleMoves = {}

    def generateMoves(self):
        self.possibleMoves.clear()
        for move in self.gameEnviroment.getPush(self.position, self.team):
             self.possibleMoves[move] = 1
             
    
class King():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 1
        self.value = 1
        self.gameEnviroment = board
        self.position = position
        self.team = team
        self.possibleMoves = {}

    def generateMoves(self):
        self.possibleMoves.clear()
        for move in self.gameEnviroment.getKing(self.position, self.team):
             self.possibleMoves[move] = 1

class Bishop():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 3
        self.value = 3
        self.gameEnviroment = board
        self.position = position
        self.team = team
        self.possibleMoves = {}

    def generateMoves(self):
        self.possibleMoves.clear()
        for move in self.gameEnviroment.getDiagonals(self.position, self.team):
             self.possibleMoves[move] = 1