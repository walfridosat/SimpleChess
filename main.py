import pygame as pg
import sys, random, asyncio

class Board():

    def __init__(self) -> None:
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


    def getAllMoves(self):
        moves = [[None]*8 for i in range(8)]
        for i in range(8):
             for j in range(8):
                  if self.board[i][j] is not None:
                       moves[i][j] = self.board[i][j].generateMoves()
                       
        return moves

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
         self.possibleMoves = self.getAllMoves()


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
                            if self.board[temp1][temp2].id == 1:
                                 self.checks.append([temp1,temp2])
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
                      if self.board[i+iterate][j].id == 1:
                            self.checks.append((i+iterate,j))
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
                      if self.board[i][j+iterate].id == 1:
                           self.checks.append((i,j+iterate))
                      break
                 else:
                      break
                 j+=iterate
        return moves_on_side

    def returnPosition(self, position: tuple):
         return self.board[position[0]][position[1]]

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
                            if self.board[temp1][temp2].id == 1:
                                 self.checks.append((temp1,temp2))
                    
                    temp1,temp2 = i+iterate_2,j+iterate_1
                    if self.isValid((temp1,temp2)):
                        if self.board[temp1][temp2] is None:
                            moves_on_leap.append((temp1,temp2))
                        
                        elif self.board[temp1][temp2].team != team_check:
                            moves_on_leap.append((temp1,temp2))
                            if self.board[temp1][temp2].id == 1:
                                 self.checks.append((temp1,temp2))
        return moves_on_leap         

    def getPush(self, position: tuple, team_check: int):
        i,j = position[0], position[1]
        moves_on_push = [] 

        if i==6 and team_check==0 and self.board[i-1][j] is None and self.board[i-2][j] is None:
             moves_on_push.append((i-2,j))
        if i==1 and team_check==1 and self.board[i+1][j] is None and self.board[i+2][j] is None:
             moves_on_push.append((i+2,j))

        if team_check:
            mover = 1
        else:
            mover = -1

        if self.isValid((i+mover,j)):
                if self.board[i+mover][j] is None:
                    moves_on_push.append((i+mover,j))
        
        if self.isValid((i+mover,j+1)):
                if self.board[i+mover][j+1] is not None and self.board[i+mover][j+1].team != team_check:
                    moves_on_push.append((i+mover,j+1))
                    if self.board[i+mover][j+1].id == 1:
                                 self.checks.append((i+mover,j+1))

        if self.isValid((i+mover,j-1)):
                if self.board[i+mover][j-1] is not None and self.board[i+mover][j-1].team != team_check:
                    moves_on_push.append((i+mover,j-1))
                    if self.board[i+mover][j-1].id == 1:
                         self.checks.append((i+mover,j-1))

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
                            moves_on_king.append(self.board[i+iterate1][j+iterate2])
        
        return moves_on_king
    
    #useless
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
              return
         if piece.team != self.player:
              return
         pieceMoves = self.possibleMoves[piece.position[0]][piece.position[1]]
         for move in pieceMoves:
              if move[0] == pos[0] and move[1] == pos[1]:
                    self.board[move[0]][move[1]] = piece
                    self.board[piece.position[0]][piece.position[1]] = None
                    piece.position = (move[0],move[1])
                    self.possibleMoves = self.getAllMoves()
                    self.player = (self.player+1)%2
                    break

class Queen():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 2
        self.value = 8
        self.gameEnviroment = board
        self.position = position
        self.team = team
    def generateMoves(self):
        return self.gameEnviroment.getDiagonals(self.position, self.team)+ self.gameEnviroment.getSides(self.position, self.team)
    
class Rook():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 5
        self.value = 5
        self.gameEnviroment = board
        self.position = position
        self.team = team
    def generateMoves(self):
        return self.gameEnviroment.getSides(self.position, self.team)

class Knight():    
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 4
        self.value = 3
        self.gameEnviroment = board
        self.position = position
        self.team = team
    def generateMoves(self):
        return self.gameEnviroment.getLeaps(self.position, self.team)
    
class Pawn():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 6
        self.value = 1
        self.gameEnviroment = board
        self.position = position
        self.team = team
    def generateMoves(self):
        return self.gameEnviroment.getPush(self.position, self.team)
    
class King():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 1
        self.value = 1
        self.gameEnviroment = board
        self.position = position
        self.team = team
    def generateMoves(self):
        return self.gameEnviroment.getKing(self.position, self.team)

class Bishop():
    def __init__(self, board: Board, position: tuple, team:int):
        self.id = 3
        self.value = 3
        self.gameEnviroment = board
        self.position = position
        self.team = team
    def generateMoves(self):
        return self.gameEnviroment.getDiagonals(self.position, self.team)

pg.init()

h = pg.display.Info().current_h
colors = [(235,236,208),(115,149,82),(255,0,0)]
screen = pg.display.set_mode((h,h))
pg.display.init()
pg.display.set_caption("ChessBoard")
clock = pg.time.Clock()



async def main():

    images = [[pg.image.load('king-w.svg'), pg.image.load('queen-w.svg'), pg.image.load('bishop-w.svg'), pg.image.load('knight-w.svg'), pg.image.load('rook-w.svg'), pg.image.load('pawn-w.svg')],
              [pg.image.load('king-b.svg'), pg.image.load('queen-b.svg'), pg.image.load('bishop-b.svg'), pg.image.load('knight-b.svg'), pg.image.load('rook-b.svg'), pg.image.load('pawn-b.svg')]]
    
    h = pg.display.Info().current_h
    const = h//8
    for i in range(2):
        for j in range(6):
             images[i][j] = pg.transform.scale(images[i][j],(const,const))
    game = Board()
    game.setDefaultBoard()
    tab = game.board
    clicked = [[0]*8 for i in range(8)]
    lastClick = None
    possibleBoards = []
    
    while True:
        for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    state = pg.mouse.get_pressed()
                    mousePos = pg.mouse.get_pos()
                    if state[2]:
                        cords = [mousePos[1]//const, mousePos[0]//const]
                        clicked[cords[0]][cords[1]] = (clicked[cords[0]][cords[1]]+1)%2
                    if state[0]:
                        if lastClick is None:
                            lastClick = [mousePos[1]//const, mousePos[0]//const]
                        else:
                            game.tryMove(tab[lastClick[0]][lastClick[1]],[mousePos[1]//const, mousePos[0]//const])
                            lastClick = None
                    
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                    exit()

        for i in range(8):
            for j in range(8):
                pg.draw.rect(screen, colors[(i+j)%2], pg.Rect(const*i, const*j, const, const))
        
        for i in range(8):
            for j in range(8):
                if clicked[i][j]:
                    pg.draw.rect(screen, (255,0,0), pg.Rect(const*j, const*i, const, const))
                    piece = tab[i][j]
                    if piece is not None:
                        possibleMoves = piece.generateMoves()
                        for move in possibleMoves:
                            pg.draw.rect(screen, (255,0,0), pg.Rect(const*move[1], const*move[0], const, const))

        for linha in range(8):
            for coluna in range(8):
                if tab[linha][coluna]:
                    piece = tab[linha][coluna]
                    imagem = images[piece.team][piece.id-1]
                    posicao = (const*piece.position[1], const*piece.position[0])
                    screen.blit(imagem,posicao)
        

        print(clock.get_fps())
        pg.display.update()
        clock.tick(165)
        await asyncio.sleep(0)

asyncio.run(main())