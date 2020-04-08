import pygame,sys

from pygame.locals import *


pygame.font.init()

#COLORS
# -----------R    G     B

WHITE  =  (255 , 255, 255)
BLACK  =  (0   , 0,     0)
RED    =  (255 , 0,     0)
BLUE   =  (0   ,255,    0)
GREY   =  (128 ,122,  120)
HIGH   =  (160 ,190,   225)


#DIRECTIONS

NORTH = 'north'
SOUTH = 'south'
WEST  = 'west'
EAST  = 'east'


class Game:
    """
    main game control
    """
    def __init__(self):
        self.board = Board()
        self.graphics = Graphics()
        self.turn = BLACK
        a = Piece(BLACK)
        b = Piece(WHITE)
        self.pebbles = [a,b,a,b,a,b,a,b,a,b,a,b,a,b,a,b,a,b,a,b,a,b,a,b]
        self.selected_piece = None
        self.default_piece = a
        self.selected_legal_moves = []

        self.phase = False

    def setup(self):
        """
        draws the window with board
        """
        self.graphics.setup_window()

    def event_loop(self):

        self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # returns the mouse location

        if self.selected_piece != None:
            self.selected_legal_moves =self.board.legal_moves(self.selected_piece,self.hop,self.phase)
            
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.terminate_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.phase  == False: # in phase B
                    if self.board.location(self.mouse_pos).occupant != None:
                        self.selected_piece = self.mouse_pos
                    elif self.selected_piece != None  and self.mouse_pos in self.board.legal_moves(self.selected_piece):
                        
                        self.move_piece(self.selected_piece, self.mouse_pos)
                        
                        if self.mouse_pos not in self.board.adjacent(self.selected_piece):
                            self.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2,
                                                    self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2)
                            
                            self.phase = True 
                            self.selected_piece = self.mouse_pos
                        
                        else:
                            self.end_turn()
                    
                if self.phase == True: # in phase A
                    if self.board.location(self.mouse_pos).occupant != None and self.default_piece != None and self.default_piece.color == self.turn :

                        while len(pebbles) != 0:
                            self.put_pebble(self.default_piece, self.mouse_pos)
                            
                            del self.pebbles[0]
                            self.default_piece = self.pebbles[0]
                                 
                        self.end_turn()
                            
                        
                    else:
                        self.selected_piece = self.mouse_pos
                                
                    
    def update(self):
        """
        Calls on the graphics class to update the game display
        """
        self.graphics.update_display(self.board,self.selected_legal_moves,self.selected_piece)
        
    def terminate_game(self):
        pygame.quit()
        sys.exit
        
    def main(self):
        self.setup()
        
        while True:# main game loop
            self.event_loop()
            self.update()
        
    def end_turn(self):
        """
        Ends turn of current player and resets game attributes
        """
        if self.turn == BLACK:
            self.turn = WHITE
            
        else:
            self.turn = BLACK
            
        self.selected_piece= None
        self.selected_legal_moves =[]
        self.phase = False
        
        if self.check_for_endgame():
            if self.turn == BLACK:
                self.graphics.draw_message("BLACK WINS!")
                
            else:
                self.graphics.draw_message("WHITE WINS!")
        
    def check_for_endgame(self):
        """
        Checks to see if the player has run out of pieces or moves
        """
        
        for x in range(6):
            for y in reange(6):
                if self.board.location(x,y).occupant != None and self.board.location(x,y).occupant.color ==self.turn:
                    if self.board.legal_moves(x,y) != []:
                        return False
                    
        return True
                        

class Graphics:
    
    def __init__(self):
        self.caption = "Bukaam3"
        
        self.fps = 60
        self.clock  = pygame.time.Clock()
        
        self.window_size = 600
        self.screen = pygame.display.set_mode((self.window_size,self.window_size))
        
        self.background = pygame.image.load("kaam3background.jpg")
        
        self.square_size = self.window_size / 8
        self.piece_size  = self.square_size / 2
        
        self.message = False
        
    def setup_window(self):
        """
        This initializes the window and sets the caption at the top
        """
        pygame.init()
        pygame.display.set_caption(self.caption)
        
    def update_display(self,board,legal_moves,selected_piece):
        """
        Update the current display
        """

        self.screen.blit(self.background, (0,0))
        self.highlight_squares(legal_moves,selected_piece)
        self.draw_board_pieces(board)
        
        if self.message:
            self.screen.blit(self.surface_txt_obj,self.txt_rect_obj)
            
        pygame.display.update()
        
        self.clock.tick(self.fps)
        
    def draw_board_squares(self,board):
        """
        Takes a board object and draws all of its squares to the display
        """
        for i in range(6):
            for j in range(6):
                pygame.draw.rect(
                    self.screen, board[i][j].color,
                                (i * self.square_size, j*self.square_size, 
                                  self.square_size,self.square_size))
            
    def draw_board_pieces(self,board):
        """
        Takes a board object andd draws all of its piecees objects to display
        """
        for x in range(6):
            for y in range(6):
                if board.matrix[x][y].occupant != None:
                    
                    pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color,
                                       self.pixel_coords(x,y),self.piece_size )
                    
                    
    def pixel_coords(self, board_coords):
        """
        Takes in a tuple of board coordinates (x,y)
        and returns the pixel coordinates of the center of the square at that location
        """
        return (board_coords[0]*self.square_size + self.piece_size,board_coords[1]*self.square_size + self.piece_size )
        
        
    def board_coords(self,coords):
        
        """
        Takes a tuple of pixel coordinates and returns what square they are in
        """
        
        return (coords[0] / self.square_size , coords[1] / self.square_size)
        
        
    def highlight_squares(self ,squares ,origin):
        """
        Squares is a list of board coordinates
        highlight_squares  highlights them
        
        """
        for square in squares:
            pygame.draw.rect(self.screen ,HIGH, (square[0] * self.square_size,
                                                 square[1] * self.square_size ,
                                                 
                                                 self.square_size,
                                                
                                                 self.square_size))
    
    
    
        if origin != None:
            pgame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size,
                                                origin[1] * self.square_size,
                                                self.square_size,
                                                self.square_size))
            
            
    def draw_message(self,message):
        self.message = True  
        self.font_obj= pygame.font.Font("freesansbold.ttf",44)
        self.text_surface_obj = self.font_obj.render(message,True,HIGH,BLACK)
        self.text_rect_obj    = self.text_surface_obj.get_rect()
        self.text_recct_obj.center = (self.window_size / 2 , self.window_size / 2)
            
            
            
class Board:
    def __init__(self):
        self.matrix = self.new_board()
        
        
    def new_board(self):
        """
        Create a new board
        """
        # initialize empty squares and put them in a matrix 
        
        matrix = [6* [None] for i in range(6)] 
        
        
        for i in range(6):
            for j in range(6):
                matrix[i][j] = Square(WHITE)
                
        return matrix
        
        
    def rel(sef,direction, x,y):
        """
        Returns the coordinates one square in a different direction to (x,y)
        """
        if direction == NORTH:
            return (x,y+1)
        
        elif direction == SOUTH:
            
            return (x, y-1)
        
        elif direction == EAST:
            return (x+1,y)
        
        elif direction == WEST:
            return (x-1,y)
        
        else:
            return 0
        
        
    def adjacent(self,x,y):
        """
        Returns list of squares that are adjacent to (x,y)
        """
        
        return [self.rel(NORTH,x,y), self.rel(SOUTH, x,y), self.rel(WEST,x,y), self.rel(EAST,x,y) ]
        
    
    def location(self, x,y):
        """
        Takes a set of coordinates (x,y) and returns self.matrix[x][y]
        """
        return self.matrix[x][y]
    
    def blind_legal_moves(self,x,y):
        """
        Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
        Reurns an empty list if that location is empty
        """
        if self.matrix[x][y].occupant != None:
            
            if self.matrix[x][y].occupant.color == BLACK and self.matrix[self.rel(NORTH,x,y)].occupant != None:
                if self.matrix[self.rel(NORTH,x,y)].occupant.color == BLACK:
                    self.blind_legal_moves  = [self.rel(WEST,x,y), self.rel(EAST,x,y)]
                    
                
            elif self.matrix[x][y].occupant.color == BLACK and self.matrix[self.rel(SOUTH,x,y)].occupant != None:
                if self.matrix[self.rel(SOUTH,x,y)].occupant.color == BLACK:
                    self.blind_legal_moves = [self.rel(WEST, x,y),self.rel(EAST,x,y)]
                    
            elif self.matrix[x][y].occupant.color == BLACK and self.matrix[self.rel(WEST,x,y)].occupant != None:
                if self.matrix[self.rel(WEST,x,y)].occupant.color == BLACK:
                    self.blind_legal_moves = [self.rel(SOUTH,x,y), self.rel(NORTH,x,y)]
                
            elif self.matrix[x][y].occupant.color == BLACK and self.matrix[self.rel(EAST,x,y)].occupant != None:
                if self.matrix[self.rel(EAST,x,y)].occupant.color == BLACK:
                    self.blind_legal_moves = [self.rel(SOUTH, x,y), self.rel(NORTH,x,y)]
                    
            elif self.matrix[x][y].occupant.color == WHITE and self.matrix[self.rel(NORTH,x,y)].occupant != None:
                if self.matrix[self.rel(NORTH,x,y)].occupant.color == WHITE:
                    self.blind_legal_moves  = [self.rel(WEST,x,y), self.rel(EAST,x,y)]
                    
                
            elif self.matrix[x][y].occupant.color == WHITE and self.matrix[self.rel(SOUTH,x,y)].occupant != None:
                if self.matrix[self.rel(SOUTH,x,y)].occupant.color == WHITE:
                    self.blind_legal_moves = [self.rel(WEST, x,y),self.rel(EAST,x,y)]
                    
            elif self.matrix[x][y].occupant.color == WHITE and self.matrix[self.rel(WEST,x,y)].occupant != None:
                if self.matrix[self.rel(WEST,x,y)].occupant.color == WHITE:
                    self.blind_legal_moves = [self.rel(SOUTH,x,y), self.rel(NORTH,x,y)]
                
            elif self.matrix[x][y].occupant.color == WHITE and self.matrix[self.rel(EAST,x,y)].occupant != None:
                if self.matrix[self.rel(EAST,x,y)].occupant.color == WHITE:
                    self.blind_legal_moves = [self.rel(SOUTH, x,y), self.rel(NORTH,x,y)]
                    
            
            else:
                self.blind_legal_moves =[self.rel(NORTH,x,y), 
                                         self.rel(SOUTH,x,y), 
                                         self.rel(EAST,x,y),
                                         self.rel(WEST,x,y) ]
    
        else:
            blind_legal_moves = []
            
        return blind_legal_moves

    def legal_moves(self, x,y, phase = False ):
        """
        Returns a list of legal moves a given set of coordinates (x,y) on the board
        if that location is empty,then legal moves return an empty list
        """
        
        blind_legal_moves = self.blind_legal_moves(x,y)
        
        legal_moves = []
        
        for move in blind_legal_moves:
            
            if phase == False:# in phaseB 
                if self.on_board(move):
                    if self.location(move).occupant == None:
                        legal_moves.append(move)
                        
            else:# in phaseA
                for move in blind_legal_moves:
                    if self.on_board(move) and self.location(move).occupant != None:
                        legal_moves.append(move)
                        
            
        return legal_moves
    
    def remove_piece(self, x,y):
        """
        Remove piece at board position (x,y)
        """
        self.matrix[x][y].occupant = None

    def put_pebble(self,pebble,x,y):
        self.matrix[x][y].occupant = pebble

    def move_piece(self, start_x,sart_y, end_x, end_y):
        """
        Move piece from postion (start_x,start_y) to (end_x, end_y)
        """
        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
        self.remove_piece(start_x,start_y)

    def is_end_square(self,coords):

        if coords[0] == 0 and coords[1] == 5:
            return True

        else:
            return False


    def on_board(self,x,y):
        if x < 0 or y < 0 or x > 5 or y > 5:
            return False
        else:
            return True




                        
class Piece:
    def __init__(self,color):
        self.color = color 
    
    
class Square:
    def __init__(self,color,occupant=None):
        self.occupant = occupant # occupant is a square object
        self.color = color # either BLACK or WHITE
    
    
        

def main():
    game = Game()
    game.main()
    
    
if __name__ == "__main__":
    main()
                        
                        
            





