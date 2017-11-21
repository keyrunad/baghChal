import pygame
import os

pygame.init()
pygame.display.set_caption("Bagh Chal")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,50) #display game window at top left of the screen
 
# Define some colors
BLACK = (0, 0, 0)
BWHITE = (255,248,220)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BROWN = (139,69,19)
TWOBROWN = (160,69,30)
LBROWN = (222,184,135)
GREY = (170, 170, 170)
DKGREY = (85, 85, 85)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

      
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 120
HEIGHT = 120
DIM = 4  # spaces in a row/col
GRID = 120  # for drawing
dimm2=6
grid = []

#game variables
coords = [] #list for all coords
for i in range(60, 660, 120):
    for j in range(60, 660, 120):
        coords.append([i, j])
tiger_coords = [[60, 60], [540, 540], [60, 540], [540, 60]] #list for tiger coords
corner_coords = [[60, 60], [540, 540], [60, 540], [540, 60]] #list for corner coords
side_coords = [[60, 300], [300, 60], [540, 300], [300, 540]] #list for side coords
goat_coords = [] #list for goat coords
non_empty_coords = tiger_coords + goat_coords #list for non empty positions
empty_coords = [] #list for empty positions
pos_moves = [] #list for possible moves
temp_tiger = [] #temporary list for selected tiger coords
temp_goat = [] #temporary list for selected goat coords
adj = [] #list for adjacent positions
gkill = [] #goat kill list
gdanger = [] #goats in danger list
trapped = [] #trapped tiger list
odd_coords = [[60, 180], [60, 420], [540, 180], [540, 420], [180, 60], [420, 60], [180, 540], [420, 540], [300, 180], [180, 300], [420, 300], [300, 420]] #list for all coords in which characters can't make diagonal moves
for i in coords:
    if i not in non_empty_coords:
        empty_coords.append(i)
		
# This sets the margin between each cell
MARGIN = 5
class Board:
    def __init__(self, dim,dimm2,grid):
        self.dim = dim
        self.dimm2 = dimm2
        self.grid = grid        

    def draw(self, screen):
        for row in range(1,5):
            for column in range(1,5):
                #color = BROWN
                #if row == 1 and color == 1:
                    #color = GREEN
                pygame.draw.line(screen, BLACK, [90, 90], [570,570], 8)
                pygame.draw.line(screen, BLACK, [90, 570], [570,90], 8)
                pygame.draw.line(screen, BLACK, [330, 570], [570,330], 8)
                pygame.draw.line(screen, BLACK, [90, 330], [330,570], 8)
                pygame.draw.line(screen, BLACK, [330, 90], [570,330], 8)
                pygame.draw.line(screen, BLACK, [90, 330], [330,90], 8)
                pygame.draw.rect(screen, BLACK,[((WIDTH)*column-30),((HEIGHT)*row-30),WIDTH,HEIGHT],8)

    def draw_tiger(self, screen):
        #draw tiger
        tiger = pygame.image.load('tiger.png')
        for c in tiger_coords:
            screen.blit(tiger, c)

    def draw_goat(self, screen):
        #draw goat
        goat = pygame.image.load('goat.png')
        for c in goat_coords:
            screen.blit(goat, c)

    def place_goat(self, screen, c):
        #place goat on the board
        goat = pygame.image.load('goat.png')
        screen.blit(goat, c)

    def draw_pos(self, screen):
        #draw black circles on all empty positions
        black_square = pygame.image.load('bsquare.png')
        for c in empty_coords:
            screen.blit(black_square, c)

    def get_adj(self, column, row):
	    #get adjacent goat coordinates
        for j in goat_coords:
            if [column+120, row] == j:
                adj.append([column+120, row])
            if [column-120, row] == j:
                adj.append([column-120, row])
            if [column, row+120] == j:
                adj.append([column, row+120])
            if [column, row-120] == j:
                adj.append([column, row-120])
            if [column, row] not in odd_coords:
                if [column+120, row+120] == j:
                    adj.append([column+120, row+120])
                if [column-120, row-120] == j:
                    adj.append([column-120, row-120])
                if [column+120, row-120] == j:
                    adj.append([column+120, row-120])
                if [column-120, row+120] == j:
                    adj.append([column-120, row+120])
	
    def poss_moves(self, column, row):
		#find the possible moves
        for i in empty_coords: #if adjacent coords are empty, append to pos_moves list
            if [column+120, row] == i:
                pos_moves.append([column+120, row])
            if [column-120, row] == i:
                pos_moves.append([column-120, row])
            if [column, row+120] == i:
                pos_moves.append([column, row+120])
            if [column, row-120] == i:
                pos_moves.append([column, row-120])
            if [column, row] not in odd_coords:
                if [column+120, row+120] == i :
                    pos_moves.append([column+120, row+120])
                if [column-120, row-120] == i:
                    pos_moves.append([column-120, row-120])
                if [column+120, row-120] == i:
                    pos_moves.append([column+120, row-120])
                if [column-120, row+120] == i:
                    pos_moves.append([column-120, row+120])
        if [column, row] in tiger_coords: #for tiger, if adjacent coords of goat coords adjacent to tiger are empty, append to pos_moves
            self.get_adj(column, row)
            for j in adj:
                if [j[0]+120, j[1]] in empty_coords and [j[0]-120, j[1]] == [column, row]:
                    pos_moves.append([j[0]+120, j[1]])
                if [j[0]-120, j[1]] in empty_coords and [j[0]+120, j[1]] == [column, row]:
                    pos_moves.append([j[0]-120, j[1]])
                if [j[0], j[1]+120] in empty_coords and [j[0], j[1]-120] == [column, row]:
                    pos_moves.append([j[0], j[1]+120])
                if [j[0], j[1]-120] in empty_coords and [j[0], j[1]+120] == [column, row]:
                    pos_moves.append([j[0], j[1]-120])
                #if [j[0], j[1]] not in odd_coords:
                if [j[0]+120, j[1]+120] in empty_coords and [j[0]-120, j[1]-120] == [column, row] :
                    pos_moves.append([j[0]+120, j[1]+120])
                if [j[0]-120, j[1]-120] in empty_coords and [j[0]+120, j[1]+120] == [column, row]:
                    pos_moves.append([j[0]-120, j[1]-120])
                if [j[0]+120, j[1]-120] in empty_coords and [j[0]-120, j[1]+120] == [column, row]:
                    pos_moves.append([j[0]+120, j[1]-120])
                if [j[0]-120, j[1]+120] in empty_coords and [j[0]+120, j[1]-120] == [column, row]:
                    pos_moves.append([j[0]-120, j[1]+120])		
    def trap_adj(self, column, row):
	    #get adjacent goat coordinates
        ad = []
        for j in goat_coords:
            if [column+120, row] == j:
                ad.append([column+120, row])
            if [column-120, row] == j:
                ad.append([column-120, row])
            if [column, row+120] == j:
                ad.append([column, row+120])
            if [column, row-120] == j:
                ad.append([column, row-120])
            if [column, row] not in odd_coords:
                if [column+120, row+120] == j:
                    ad.append([column+120, row+120])
                if [column-120, row-120] == j:
                    ad.append([column-120, row-120])
                if [column+120, row-120] == j:
                    ad.append([column+120, row-120])
                if [column-120, row+120] == j:
                    ad.append([column-120, row+120])
        return ad
    def trap_moves(self, column, row):
		#find the possible moves
        pos_move = []
        for i in empty_coords: #if adjacent coords are empty, append to pos_move list
            if [column+120, row] == i:
                pos_move.append([column+120, row])
            if [column-120, row] == i:
                pos_move.append([column-120, row])
            if [column, row+120] == i:
                pos_move.append([column, row+120])
            if [column, row-120] == i:
                pos_move.append([column, row-120])
            if [column, row] not in odd_coords:
                if [column+120, row+120] == i :
                    pos_move.append([column+120, row+120])
                if [column-120, row-120] == i:
                    pos_move.append([column-120, row-120])
                if [column+120, row-120] == i:
                    pos_move.append([column+120, row-120])
                if [column-120, row+120] == i:
                    pos_move.append([column-120, row+120])
        if [column, row] in tiger_coords: #for tiger, if adjacent coords of goat coords adjacent to tiger are empty, append to pos_move
            ad = self.trap_adj(column, row)
            for j in ad:
                if [j[0]+120, j[1]] in empty_coords and [j[0]-120, j[1]] == [column, row]:
                    pos_move.append([j[0]+120, j[1]])
                if [j[0]-120, j[1]] in empty_coords and [j[0]+120, j[1]] == [column, row]:
                    pos_move.append([j[0]-120, j[1]])
                if [j[0], j[1]+120] in empty_coords and [j[0], j[1]-120] == [column, row]:
                    pos_move.append([j[0], j[1]+120])
                if [j[0], j[1]-120] in empty_coords and [j[0], j[1]+120] == [column, row]:
                    pos_move.append([j[0], j[1]-120])
                #if [j[0], j[1]] not in odd_coords:
                if [j[0]+120, j[1]+120] in empty_coords and [j[0]-120, j[1]-120] == [column, row] :
                    pos_move.append([j[0]+120, j[1]+120])
                if [j[0]-120, j[1]-120] in empty_coords and [j[0]+120, j[1]+120] == [column, row]:
                    pos_move.append([j[0]-120, j[1]-120])
                if [j[0]+120, j[1]-120] in empty_coords and [j[0]-120, j[1]+120] == [column, row]:
                    pos_move.append([j[0]+120, j[1]-120])
                if [j[0]-120, j[1]+120] in empty_coords and [j[0]+120, j[1]-120] == [column, row]:
                    pos_move.append([j[0]-120, j[1]+120])
        return pos_move

    def get_trapped(self):
        for m in tiger_coords:
            t = self.trap_moves(m[0], m[1])
            if len(t) == 0:
                trapped.append(m)

    def draw_moves(self, screen):
        #draw blue circles on all positions with possible move for characters
        blue_square = pygame.image.load('square.png')
        for c in pos_moves:
            screen.blit(blue_square, c)

    def draw_atiger(self, screen):
	#draw active tiger
        active_tiger = pygame.image.load('atiger.png')
        if temp_tiger:
            screen.blit(active_tiger, temp_tiger[0])

    def draw_agoat(self, screen):
	#draw active goat
        active_goat = pygame.image.load('agoat.png')
        if temp_goat:
            screen.blit(active_goat, temp_goat[0])
			
    def draw_dgoat(self, screen):
    #draw goat in danger
        dgoat = pygame.image.load('dgoat.png')
        for c in gdanger:
            screen.blit(dgoat, c)
			
    def draw_dtiger(self, screen):
    #draw trapped tiger
        self.get_trapped()
        dtiger = pygame.image.load('dtiger.png')
        for c in trapped:
            screen.blit(dtiger, c)

def main():

    #-------- Main Program Loop -----------
    WINDOW_SIZE = [950, 650]        # Set the HEIGHT and WIDTH of the screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    done = False                   # Loop until the user clicks the close button.
    clock = pygame.time.Clock()    # Used to manage how fast the screen updates
    board = Board(DIM,dimm2,grid)
    turn = 1
    gcount = 0
    selected = 0
    refresh = True
    msg = ''
	
    def displayvars():
        print('**************************************')
        print('Turn: Player ', turn)
        print('Goats in hand: ', 20-gcount)
        print('Goats on board: ', gcount-len(gkill))
        print('Goats killed: ', len(gkill))
        tt = []
        for kk in trapped:
            if kk not in tt:
                tt.append(kk)
        print('Tigers trapped: ', len(tt))
        print(msg)
        print('**************************************')

    while not done:
        """
        for i in range(10):
            for j in range(1):
                pygame.draw.rect(screen, BLUE, [60*j, 60*i, 60, 60], 1)
        for i in range(1):
            for j in range(10):
                pygame.draw.rect(screen, BLUE, [60*j, 60*i, 60, 60], 1)
        for i in range(10):
            for j in range(4,5):
                pygame.draw.rect(screen, BLUE, [60*j, 60*i, 60, 60], 1)
        for i in range(4,7):
            for j in range(10):
                pygame.draw.rect(screen, BLUE, [60*j, 60*i, 60, 60], 1)
        for i in range(1,10):
            for j in range(1, 10):
                pygame.draw.rect(screen, BLUE, [60*j, 60*i, 60, 60], 1)
        """
        if len(gkill) == 5:
            print('GAME OVER! TIGER WON!')
            break
        tt = []
        for kk in trapped:
            if kk not in tt:
                tt.append(kk)
        if len(tt) == 4:
            print('GAME OVER! GOAT WON!')
            break
        if refresh == True:
            screen.fill(BWHITE)       # Set the screen background
            board.draw(screen)        #Drawing code for Draw the grid
            board.draw_tiger(screen) #Drawing tigers
            board.draw_pos(screen)
            board.draw_goat(screen)
            board.draw_moves(screen)
            board.draw_atiger(screen)
            board.draw_agoat(screen)
            board.draw_dgoat(screen)
            board.draw_dtiger(screen)
            displayvars()
            refresh = False
            msg = ''
            
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True        # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1 and gcount < 20: #first place 20 goats on the board
                pos = pygame.mouse.get_pos()
                column = 60*(pos[0] // 60)
                row = 60*(pos[1] // 60)
                if [column, row] in empty_coords:
                    board.place_goat(screen, [column, row])
                    empty_coords.remove([column, row])
                    goat_coords.append([column, row])
                    gcount += 1
                    turn = 2
                    refresh = True
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1 and gcount == 20 and selected == 0: #select goat after 20 goats have been placed
                pos = pygame.mouse.get_pos()
                column = 60*(pos[0] // 60)
                row = 60*(pos[1] // 60)
                if [column, row] in goat_coords: #select the goat
                    board.poss_moves(column, row)
                    if len(pos_moves) == 0: #if selected goat has no moves
                        msg = 'No possible moves'
                        del pos_moves[:]
                        refresh = True
                        continue
                    temp_goat.append([column, row])
                    goat_coords.remove(temp_goat[0])
                    selected = 1
                    refresh = True
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1 and gcount == 20 and selected == 1: #move the goat
                pos = pygame.mouse.get_pos()
                column = 60*(pos[0] // 60)
                row = 60*(pos[1] // 60)
                if [column, row] in temp_goat: #if goat is deselected
                    goat_coords.append([column, row])
                    selected = 0
                    del pos_moves[:]
                    del temp_goat[:]
                    refresh = True
                if [column, row] in pos_moves: #if goat is moved
                    goat_coords.append([column, row])
                    empty_coords.append(temp_goat[0])
                    empty_coords.remove([column, row])
                    del temp_goat[:]
                    del pos_moves[:]
                    del trapped[:]
                    selected = 0
                    turn = 2
                    refresh = True
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 2 and selected == 0: #select the tiger
                pos = pygame.mouse.get_pos()
                column = 60*(pos[0] // 60)
                row = 60*(pos[1] // 60)
                if [column, row] in tiger_coords: #select the tiger
                    board.poss_moves(column, row)
                    if len(pos_moves) == 0: #if selected tiger is trapped
                        msg = 'Can not selected trapped tiger'
                        refresh = True
                        del pos_moves[:]
                        continue
                    temp_tiger.append([column, row])
                    tiger_coords.remove(temp_tiger[0])
                    for i in pos_moves:
                        tgx = (i[0]+temp_tiger[0][0])/2
                        tgy = (i[1]+temp_tiger[0][1])/2
                        if [tgx, tgy] in goat_coords:
                            gdanger.append([tgx, tgy])
                    selected = 1
                    refresh = True
					
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 2 and selected == 1: #move the tiger
                pos = pygame.mouse.get_pos()
                column = 60*(pos[0] // 60)
                row = 60*(pos[1] // 60)
                if [column, row] in temp_tiger: #if tiger is deselected
                    tiger_coords.append([column, row])
                    selected = 0
                    del pos_moves[:]
                    del temp_tiger[:]
                    del adj[:]
                    del gdanger[:]
                    refresh = True
                if [column, row] in pos_moves: #if tiger is moved
                    tiger_coords.append([column, row])
                    empty_coords.append(temp_tiger[0])
                    selected = 0
                    empty_coords.remove([column, row])
                    tgx = (column + temp_tiger[0][0])/2
                    tgy = (row + temp_tiger[0][1])/2
                    if [tgx, tgy] in goat_coords:
                        gkill.append([tgx, tgy])
                        goat_coords.remove([tgx, tgy])
                        empty_coords.append([tgx, tgy])
                    del pos_moves[:]
                    del temp_tiger[:]
                    del adj[:]
                    del gdanger[:]
                    del trapped[:]
                    turn = 1
                    refresh = True

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
    # Be IDLE friendly. If you forget this line, the program will 'hang' on exit
    pygame.quit()


start = input("Do you want to play the game? Enter 's' to start, any other key to exit: ")
if start.lower() == 's':
    main()