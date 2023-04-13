import pygame as p
import chess_engine

WIDTH = HEIGHT = 400
DIM = 8
SQ_SIZE = WIDTH // DIM
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ["bR","bN","bB","bQ","bK","bp","wp","wR","wB","wN","wQ","wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(piece+".png"),(SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    board = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    gs = chess_engine.game_state()
    valid_moves = gs.valid_moves()
    made_move = False
    load_images()
    running = True
    count = 0
    prev_move = []

    while running:
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_f:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                j = loc[0] // SQ_SIZE
                i = loc[1] // SQ_SIZE
                count+=1
                if count%2==1:
                    startsq = [i,j]
                else:
                    endsq = [i,j]
                    move = chess_engine.Move(gs.board,startsq,endsq)
                    print(len(valid_moves))
                    if move in valid_moves:
                        prev_move.append(move)
                        gs.make_move(move)
                        draw_piece(board,gs.board)
                        made_move = True
                    else:
                        print('invalid move')
            elif e.type == p.KEYDOWN and e.key == p.K_z:
                count-=2
                made_move = True
                gs.undo_move(prev_move.pop())

        if made_move:
            valid_moves = gs.valid_moves()     
            made_move = False  
        print_game_state(board,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_piece_click(board,piece_name,loc_piece):
    board.blit(IMAGES[piece_name],loc_piece)

def draw_squares(board):
    color2 = p.Color("gray")
    color1 = (255,255,255)
    for i in range(8):
        for j in range(8):
            p.draw.rect(board,color1 if (i+j)%2==0 else color2,p.Rect(j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def draw_piece(board,board_array):
    for i in range(8):
        for(j) in range(8):
            if board_array[i][j] != '--':
                board.blit(IMAGES[board_array[i][j]],(j*SQ_SIZE,i*SQ_SIZE))

def print_game_state(board,gs):
    draw_squares(board)
    draw_piece(board,gs.board)



main()

