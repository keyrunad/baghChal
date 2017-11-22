import pygame
import os

pygame.init()
pygame.display.set_caption("Bagh Chal")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,50) #display game window at top left of the screen
 
# Define some colors
BLACK = (0, 0, 0)
BWHITE = (255,248,220)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GOLD = (222,184,135)
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

def game_reset():
    #start game variables
    global coords
    global tiger_coords
    global goat_coords
    global non_empty_coords
    global empty_coords
    global pos_moves
    global temp_tiger
    global temp_goat
    global adj
    global gkill
    global gdanger
    global trapped
    global odd_coords
    coords = [] #list for all coords
    for i in range(60, 660, 120):
        for j in range(60, 660, 120):
            coords.append([i, j])
    tiger_coords = [[60, 60], [540, 540], [60, 540], [540, 60]] #list for tiger coords
    goat_coords = [] #list for goat coords
    non_empty_coords = tiger_coords + goat_coords #list for non empty positions
    empty_coords = [] #list for empty positions
    for i in coords:
        if i not in non_empty_coords:
            empty_coords.append(i)
    pos_moves = [] #list for possible moves
    temp_tiger = [] #temporary list for selected tiger coords
    temp_goat = [] #temporary list for selected goat coords
    adj = [] #list for adjacent positions
    gkill = [] #goat kill list
    gdanger = [] #goats in danger list
    trapped = [] #trapped tiger list
    odd_coords = [[60, 180], [60, 420], [540, 180], [540, 420], [180, 60], [420, 60], [180, 540], [420, 540], [300, 180], [180, 300], [420, 300], [300, 420]] #list for all coords in which characters can't make diagonal moves
#end game variables

class Board:
    """
    def __init__(self, dim,dimm2,grid):
        self.dim = dim
        self.dimm2 = dimm2
        self.grid = grid  
    """

    def draw(self, screen):
        for row in range(1,5):
            for column in range(1,5):
                #color = BROWN
                #if row == 1 and color == 1:
                    #color = GREEN
                pygame.draw.line(screen, BLACK, [90, 90], [570,570], 6)
                pygame.draw.line(screen, BLACK, [90, 570], [570,90], 6)
                pygame.draw.line(screen, BLACK, [330, 570], [570,330], 6)
                pygame.draw.line(screen, BLACK, [90, 330], [330,570], 6)
                pygame.draw.line(screen, BLACK, [330, 90], [570,330], 6)
                pygame.draw.line(screen, BLACK, [90, 330], [330,90], 6)
                pygame.draw.rect(screen, BLACK,[((WIDTH)*column-30),((HEIGHT)*row-30),WIDTH,HEIGHT],4)
                
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
    def draw_res(self, screen):
        #draw reset button
        res = pygame.image.load('restart.png')
        screen.blit(res, [640, 60])
    def printme(self,screen):
        print("hello")
        mssg = "Direction of the game go here Talk .\n"
        mssg1 = "Direction of the game go here Talk .\n"
        mssg2 = "Direction of the game go here Talk .\n"
        mssg3 = "Direction of the game go here Talk .\n"
        
        font2 = pygame.font.SysFont("comicsansms",15)
        pygame.draw.rect(screen, GREY, [630, 270, 300, 200])
        pygame.draw.line(screen, BLACK, [900, 270], [915,290], 2)
        pygame.draw.line(screen, BLACK, [915, 270], [900,290], 2)
        textSurf = font2.render(mssg, True, BLACK)
        textSurf1 = font2.render(mssg1, True, BLACK)
        textSurf2 = font2.render(mssg2, True, BLACK)
        textSurf3 = font2.render(mssg3, True, BLACK)
        screen.blit(textSurf,(635,280))
        screen.blit(textSurf1,(635,300))
        screen.blit(textSurf2,(635,320))
        screen.blit(textSurf3,(635,340))

    def button(self,msg,x,y,w,h,gg,screen):
        font2 = pygame.font.SysFont("comicsansms",20)
        textSurf = font2.render(msg, True, BLACK)
        textRect = ( (x+(w/6)), (y+(h/3)) )
        screen.blit(textSurf, textRect)
        pygame.draw.rect(screen, gg, [x,y,w,h], 3)
        
        
           

    def draw_start(self, screen):
        #draw start button
        start = pygame.image.load('start.png')
        screen.blit(start, [640, 60])
    def draw_quit(self, screen):
        #draw quit button
        res = pygame.image.load('quit.png')
        screen.blit(res, [810, 60])

def main():

    #-------- Main Program Loop -----------
    WINDOW_SIZE = [950, 650]        # Set the HEIGHT and WIDTH of the screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    done = False                   # Loop until the user clicks the close button.
    clock = pygame.time.Clock()    # Used to manage how fast the screen updates
    board = Board()
    turn = 1
    gcount = 0
    selected = 0
    refresh = True
    reset = True
    fmsg = ''
    msg = 'Click Start button to begin.'
    game_end = False
    start = False
    def displayvars():
        print('**************************************')
        font2 = pygame.font.SysFont("erasmediumitc ",25,2)
        text1="Turn: Player "+str(turn)
        text2="Goats in hand: "+str(20-gcount)
        text3="Goats killed: "+str(len(gkill))
        text4="Goats on board: "+str(gcount-len(gkill))
        text5= msg
        text6= fmsg
        tt = []
        for kk in trapped:
            if kk not in tt:
                tt.append(kk)
        text="Tiger's trapped: "+str(len(tt))
        textSurf = font2.render(text1, True, BLACK)
        screen.blit(textSurf,(60,15))
        textSurf = font2.render(text2, True, BLACK)
        screen.blit(textSurf,(640,420))
        textSurf = font2.render(text3, True, BLACK)
        screen.blit(textSurf,(640,330))
        textSurf = font2.render(text4, True, BLACK)
        screen.blit(textSurf,(640,180))
        
        textSurf = font2.render(text, True, BLACK)
        screen.blit(textSurf,(640,300))
        textSurf = font2.render(text5, True, BLACK)
        screen.blit(textSurf,(580,15))
        font3 = pygame.font.SysFont("erasmediumitc ",35,4)
        
        textSurf = font3.render(text6, True, WHITE)
        if len(gkill) == 5 or len(tt) == 4: 
            pygame.draw.rect(screen, GOLD, [50, 270, 560, 100])
            screen.blit(textSurf,(80,300))
        
        #print('Turn: Player ', turn)
        #print('Goats in hand: ', 20-gcount)
        #print('Goats on board: ', gcount-len(gkill))
        #print('Goats killed: ', len(gkill))
        #print('Tigers trapped: ', len(tt))
        print(msg)
       

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
        
        if reset == True:
            game_reset()
            turn = 1
            gcount = 0
            selected = 0
            reset = False
        if len(gkill) == 5:     
            fmsg = 'GAME OVER! TIGER WON!'   
            reset = True
            game_end = True
            
        tt = []
        for kk in trapped:
            if kk not in tt:
                tt.append(kk)
        if len(tt) == 4:
            fmsg = 'GAME OVER! GOAT WON!'  #not working when I print to console also.
            reset = True
            game_end = True
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
            board.button("HELP",650, 540, 70, 50,BLACK,screen)
            if start == True:
                board.draw_res(screen)
            if start == False:
                board.draw_start(screen)
            board.draw_quit(screen)
            displayvars()
            refresh = False
            msg = ''
            fmsg = ''
            
        for event in pygame.event.get():   # User did something
            if event.type == pygame.MOUSEBUTTONDOWN and start == False: #start the game
                pos = pygame.mouse.get_pos()
                column = pos[0]
                row = pos[1]
                if column >= 640 and column <=790 and row >=60 and row <=100:
                    start = True
                    refresh = True
                    msg = '       Game started.'
                    continue
            if event.type == pygame.MOUSEBUTTONDOWN and game_end == True and start == True: #reset the game after game is over and if restart button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    if column >= 640 and column <=790 and row >=60 and row <=100:
                        reset = True
                        refresh = True
                        game_end = False
                        msg = '       Game restarted.'
            if event.type == pygame.MOUSEBUTTONDOWN and game_end == True and start == True: #quit if quit button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    if column >= 810 and column <=910 and row >=60 and row <=100:
                        done = True
            if event.type == pygame.MOUSEBUTTONDOWN : 
                    pos = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()
                    column = pos[0]
                    row = pos[1]
                    print(column,row)
                    #if x+w > mouse[0] > x and y+h> mouse[1] > y:
                    if column >= 630 and column <=730 and row >=550 and row <=600:
                        if click[0] == 1:
                            board.printme(screen)
                    if column >= 830 and column <=940 and row >=250 and row <=300:
                        if click[0] == 1:
                            refresh = True
            if event.type == pygame.MOUSEBUTTONDOWN and game_end == False and start == False: #quit if quit button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    if column >= 810 and column <=910 and row >=60 and row <=100:
                        done = True
						
            if event.type == pygame.QUIT:  # If user clicked close
                done = True        # Flag that we are done so we exit this loop

            
            elif game_end == False and start == True: #when game is started but not over
                if event.type == pygame.MOUSEBUTTONDOWN: #reset the game if restart button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    if column >= 640 and column <=790 and row >=60 and row <=100:
                        reset = True
                        refresh = True
                        msg = '      Game restarted.'
                if event.type == pygame.MOUSEBUTTONDOWN: #quit if quit button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    if column >= 810 and column <=910 and row >=60 and row <=100:
                        done = True
                if event.type == pygame.MOUSEBUTTONDOWN and turn == 1 and gcount < 20: #first place 20 goats on the board
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
        if done == True:
            pygame.quit()
#start = input("Do you want to play the game? Enter 's' to start, any other key to exit: ")
#if start.lower() == 's':
main()
