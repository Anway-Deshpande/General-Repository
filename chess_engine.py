import numpy as np

class game_state():
    def __init__(self):
        self.board = np.array([["bR","bN","bB","bQ","bK","bB","bN","bR"],
                               ["bp","bp","bp","bp","bp","bp","bp","bp"],
                               ["--","--","--","--","--","--","--","--"],
                               ["--","--","--","--","--","--","--","--"],
                               ["--","--","--","--","--","--","--","--"],
                               ["--","--","--","--","--","--","--","--"],
                               ["wp","wp","wp","wp","wp","wp","wp","wp"],
                               ["wR","wN","wB","wQ","wK","wB","wN","wR"]])
        self.white_move = True
        self.moves = []

    def make_move(self,move):
        move.board[move.startrow][move.startcol] = '--'
        move.board[move.endrow][move.endcol] = move.piecemoved
        if(move.piececaptured != '--'):
            self.moves.append(move.notation()[0]+'x'+move.notation()[1]+str(move.notation()[2]))
        else:
            self.moves.append(move.notation()[0]+move.notation()[1]+str(move.notation()[2]))
        print(self.moves[0])
        self.moves.clear()
        self.white_move = not self.white_move

    def undo_move(self,move):
        move.board[move.startrow][move.startcol] = move.piecemoved
        move.board[move.endrow][move.endcol] = move.piececaptured
        self.white_move = not self.white_move

    def valid_moves(self):
        return self.get_all_moves()

    def get_all_moves(self):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if (piece[0]=='w' and self.white_move) or (piece[0]=='b' and not self.white_move):
                    if piece[1]=='p':
                        self.get_pawn_moves(i,j,possible_moves)
                    elif piece[1]=='N':
                        self.get_knight_moves(i,j,possible_moves)
                    elif piece[1]=='B':
                        self.get_bishop_moves(i,j,possible_moves)
                    elif piece[1]=='R':
                        self.get_rook_moves(i,j,possible_moves)
                    elif piece[1]=='Q':
                        self.get_queen_moves(i,j,possible_moves)
                    elif piece[1]=='K':
                        self.get_king_moves(i,j,possible_moves)
        return possible_moves
    
    def get_pawn_moves(self,i,j,moves):
        if self.white_move:
            if i!=0 and self.board[i-1][j] == '--' :
                moves.append(Move(self.board,[i,j],[i-1,j]))
                if i == 6 and self.board[i-2][j] == '--':
                    moves.append(Move(self.board,[i,j],[i-2,j]))
            if i!=0 and j!=7 and self.board[i-1][j+1][0]=='b' :
                moves.append(Move(self.board,[i,j],[i-1,j+1]))
            if i == 3 and self.board[i][j+1] == 'bp' :
                self.board[i][j+1] = '--'
                moves.append(Move(self.board,[i,j],[i-1,j+1]))
            if i!=0 and j!=0 and self.board[i-1][j-1][0]=='b' :
                moves.append(Move(self.board,[i,j],[i-1,j-1]))
            if i == 3 and self.board[i][j-1] == 'bp' :
                self.board[i][j-1] = '--'
                moves.append(Move(self.board,[i,j],[i-1,j-1]))
            
        else:
            if i!=7 and self.board[i+1][j] == '--' :
                moves.append(Move(self.board,[i,j],[i+1,j]))
                if i == 1 and self.board[i+2][j] == '--':
                    moves.append(Move(self.board,[i,j],[i+2,j]))
            if i!=7 and j!=7 and self.board[i+1][j+1][0]=='w' :
                moves.append(Move(self.board,[i,j],[i+1,j+1]))
            if i == 4 and self.board[i][j+1] == 'bp' :
                self.board[i][j+1] = '--'
                moves.append(Move(self.board,[i,j],[i+1,j+1]))
            if i!=7 and j!=0 and self.board[i+1][j-1][0]=='w' :
                moves.append(Move(self.board,[i,j],[i+1,j-1]))
            if i == 4 and self.board[i][j+1] == 'bp' :
                self.board[i][j-1] = '--'
                moves.append(Move(self.board,[i,j],[i+1,j+1]))


    def get_knight_moves(self,i,j,moves):
            if i>1 and j>0 and ((self.board[i-2][j-1][0] != 'w' and self.white_move) or (self.board[i-2][j-1][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i-2,j-1]))
            if i>0 and j>1 and ((self.board[i-1][j-2][0] != 'w' and self.white_move) or (self.board[i-1][j-2][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i-1,j-2]))
            if i<6 and j<7 and ((self.board[i+2][j+1][0] != 'w' and self.white_move) or (self.board[i+2][j+1][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i+2,j+1]))
            if i<7 and j<6 and ((self.board[i+1][j+2][0] != 'w' and self.white_move) or (self.board[i+1][j+2][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i+1,j+2]))
            if i>1 and j<7 and ((self.board[i-2][j+1][0] != 'w' and self.white_move) or (self.board[i-2][j+1][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i-2,j+1]))
            if i<6 and j>0 and ((self.board[i+2][j-1][0] != 'w' and self.white_move) or (self.board[i+2][j-1][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i+2,j-1]))
            if i>0 and j<6 and ((self.board[i-1][j+2][0] != 'w' and self.white_move) or (self.board[i-1][j+2][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i-1,j+2]))
            if i<7 and j>1 and ((self.board[i+1][j-2][0] != 'w' and self.white_move) or (self.board[i+1][j-2][0] != 'b' and not self.white_move)):
                moves.append(Move(self.board,[i,j],[i+1,j-2]))
                

    def get_bishop_moves(self,i,j,moves):
        pass

    def get_rook_moves(self,i,j,moves):
        pass

    def get_queen_moves(self,i,j,moves):
        pass

    def get_king_moves(self,i,j,moves):
        pass

class Move():
    def __init__(self,board,startsq,endsq):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.board = board
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.piecemoved = board[self.startrow][self.startcol]
        self.piececaptured = board[self.endrow][self.endcol]
        self.moveID = self.startrow*1000 + self.startcol*100 + self.endrow*10 + self.endcol

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    
    def notation(self):
        self.rank = 8 - self.endrow
        self.num_to_file = {'0':'a', '1':'b', '2':'c', '3':'d', '4':'e', '5':'f','6':'g', '7':'h'}
        self.file = self.num_to_file[str(self.endcol)]
        return(self.piecemoved[1],self.file,self.rank)
