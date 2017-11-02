
import pygame
 
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

 
# This sets the margin between each cell
MARGIN = 5
class Board:
    def __init__(self, dim,dimm2,grid):
        self.dim = dim
        self.dimm2 = dimm2
        self.grid = grid        
        self.reset()
    

    def reset(self):
        self.select = []
        self.turn = 'r'
        self.preventDeselect = False
       

    def processMouse(self, mx, my):
        """ mouse is in grid coordinates """
        #nothing is selected, find a piece to select
        if len(self.select) == 0:
            #if self.grid[my][mx].lower() == self.turn:
            self.select = [mx, my]
            print(self.select)

        #There is a selected piece, deselect?
        elif mx == self.select[0] and my == self.select[1] and \
                not self.preventDeselect:
            self.select = []

        #else:
    def draw(self, screen):
        for row in range(5):
            for column in range(1):
                pygame.draw.rect(screen,LBROWN,[(WIDTH)*column,(HEIGHT)*row,WIDTH,HEIGHT])
        for row in range(1):
            for column in range(5):
                pygame.draw.rect(screen,LBROWN,[(WIDTH)*column,(HEIGHT)*row,WIDTH,HEIGHT])

        for row in range(5):
            for column in range(4,5):
                pygame.draw.rect(screen,LBROWN,[(WIDTH)*column,(HEIGHT)*row,WIDTH,HEIGHT])
        for row in range(4,7):
            for column in range(5):
                pygame.draw.rect(screen,LBROWN,[(WIDTH)*column,(HEIGHT)*row,WIDTH,HEIGHT])
        for row in range(1,5):
            for column in range(1,5):
                color = BROWN
                #if grid[row][column] == 1:
                    #color = GREEN
                pygame.draw.line(screen, BROWN, [60, 60], [540,540], 8)
                pygame.draw.line(screen, BROWN, [60, 540], [540,60], 8)
                pygame.draw.line(screen, TWOBROWN, [300, 540], [540,300], 8)
                pygame.draw.line(screen, TWOBROWN, [60, 300], [300,540], 8)
                pygame.draw.line(screen, TWOBROWN, [300, 60], [540,300], 8)
                pygame.draw.line(screen, TWOBROWN, [60, 300], [300,60], 8)
                        
                pygame.draw.rect(screen,color,[((WIDTH)*column-60),((HEIGHT)*row-60),WIDTH,HEIGHT],8)
        for row in range(7):
            for column in range(8):
                pygame.draw.rect(screen,BLACK,[(WIDTH)*column,(HEIGHT)*row,WIDTH,HEIGHT],1)
        if len(self.select) > 0:
            sx = self.select[0]*GRID
            sy = self.select[1]*GRID
            pygame.draw.rect(screen, YELLOW, [sy, sx, GRID, GRID], 5)


                

        

def main():            
    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    
    for row in range(10):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(10):
            grid[row].append(0)  # Append a cell
     
    # Set row 1, cell 5 to one. (Remember rows and
    # column numbers start at zero.)
    grid[1][5] = 1
    pygame.init()                   # Initialize pygame   
    WINDOW_SIZE = [950, 700]        # Set the HEIGHT and WIDTH of the screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Bagh-Chal Board Game")
     
    done = False                   # Loop until the user clicks the close button.
    clock = pygame.time.Clock()    # Used to manage how fast the screen updates
    board = Board(DIM,dimm2,grid)
    #-------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True        # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                                   # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                board.processMouse(row, column)
                # Set that location to one
                grid[row][column] = 1
                print("Click ", pos, "Grid coordinates: ", row, column)
            
        screen.fill(BWHITE)       # Set the screen background 
        board.draw(screen)        #Drawing code for Draw the grid
        clock.tick(60)            # Limit to 60 frames per second
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
    # Be IDLE friendly. If you forget this line, the program will 'hang' on exit
    pygame.quit()



if __name__ == '__main__':
    main()






