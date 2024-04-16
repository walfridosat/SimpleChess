import pygame as pg
import sys, random, asyncio, chess

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
    game = chess.Board()
    game.setDefaultBoard()
    tab = game.board
    clicked = None
    drag = None
    display = None
    possibleBoards = []
    frames = 0
    
    while True:

        fps = clock.get_fps()

        for event in pg.event.get():
                state = pg.mouse.get_pressed()
                mousePos = pg.mouse.get_pos()
                if event.type == pg.MOUSEBUTTONDOWN:
                         clickedFrame = frames
                         clicked = (mousePos[1]//const, mousePos[0]//const)
                         drag = game.board[clicked[0]][clicked[1]]
                         display = game.board[mousePos[1]//const][mousePos[0]//const]
                if event.type == pg.MOUSEBUTTONUP:
                         if frames >= clickedFrame + fps//8:
                            succesfull = game.tryMove(tab[clicked[0]][clicked[1]],(mousePos[1]//const, mousePos[0]//const))
                            clicked = None
                            drag = None
                            clickedFrame = None
                            display = None
                         else:
                            display = None
                            clicked = None
                            clickedFrame = None
                            drag = None
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                    exit()

        for i in range(8):
            for j in range(8):
                pg.draw.rect(screen, colors[(i+j)%2], pg.Rect(const*i, const*j, const, const))

        for linha in range(8):
            for coluna in range(8):
                if tab[linha][coluna]:
                    piece = tab[linha][coluna]
                    imagem = images[piece.team][piece.id-1]
                    posicao = (const*piece.position[1], const*piece.position[0])
                    screen.blit(imagem,posicao)
        
        if display is not None:
             for move in display.possibleMoves.keys():
                  pg.draw.circle(screen, (50, 50, 50), (const*move[1]+const//2, const*move[0]+const//2), const/6)

        if drag is not None:
            pos = drag.position
            i,j = pos[1],pos[0]
            imagem = images[drag.team][drag.id-1]
            pg.draw.rect(screen, colors[(i+j)%2], pg.Rect(const*i, const*j, const, const))
            screen.blit(imagem,(mousePos[0]-const//3,mousePos[1]-const//3))
        
        frames+=1
        frames = frames%3600
        print(clock.get_fps())
        pg.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())