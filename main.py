import pygame

class Stack(pygame.Rect):
    def __init__(self,left, top, width, height):
        pygame.Rect.__init__(self, left, top, width, height)
        self.stackCount = 1
        self.lastPosition = (None,None)
        self.currentPosition = (None,None)
        self.lastPositionIndex = None
        self.currentPositionIndex = None

    def __str__(self):
        return ('Stack Count: %s\nLast Position: %s\nLast Position Index: %s\nCurrent Position: %s\nCurrent Position Index: %s' % (self.stackCount, self.lastPosition, self.lastPositionIndex, self.currentPosition, self.currentPositionIndex))

def centerStacks():
    #Center stacks
    for r in rects:
        for c in cups:
            if r.colliderect(c):
                c.center = r.center

def isValidMove(stack):
    distance = stack.currentPositionIndex - stack.lastPositionIndex
    print(stack)
    print("Dist: %s" % distance)
    if abs(distance) == stack.stackCount:
        return True

    return False

YELLOW = (255,255,0)
GREEN = (0, 255, 0)
pygame.init()
screen = pygame.display.set_mode((50*23,600))
background = pygame.Surface(screen.get_size())
background.fill(YELLOW)
background = background.convert()
screen.blit(background,(0,0))
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 25)

mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 30
# How many seconds the "game" is played.
playtime = 0.0

BLOCK_SIZE = 50
rects = []
cups = []
stacks = []
BLUE = (0,0,255)
RED   = (255,   0,   0)
BLACK   = (0,   0,   0)
WHITE = (255,255,255)

for x in range(23):
    rects.append( pygame.Rect(x*(BLOCK_SIZE+5), BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE) )
    rects[x].x = x*(BLOCK_SIZE)
    rects[x].y = 300

#Valid positions
validPositions = [r.center for r in rects]

for x in range(23):
    cups.append( Stack(x*(BLOCK_SIZE+5), BLOCK_SIZE, BLOCK_SIZE / 2, BLOCK_SIZE / 2) )
    cups[x].x = x*(BLOCK_SIZE)
    cups[x].y = 300

centerStacks()
for stack in cups:
    stack.lastPosition = stack.center
    stack.lastPositionIndex = validPositions.index(stack.lastPosition)
    stack.currentPosition = stack.lastPosition
    stack.currentPositionIndex = stack.lastPositionIndex

selected = None


while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    playtime += milliseconds / 1000.0 
    
    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if event.button == 1:
                for i, stack in enumerate(cups):
                    if stack.collidepoint(event.pos):
                        selected = i
                        selected_offset_x = stack.x - event.pos[0]
                        selected_offset_y = stack.y - event.pos[1]
                        print("Stack count: %s" % stack.stackCount)
                        stack.lastPosition = stack.center
                        stack.lastPositionIndex = validPositions.index(stack.lastPosition)

        elif event.type == pygame.MOUSEBUTTONUP:
                selected = None
                for i, r in enumerate(cups):
                    if event.button == 1:
                        for dex, c in enumerate(cups):
                            if dex is not i and c.colliderect(r): #One stack collects another
                                centerStacks()
                                # c.currentPosition = c.center
                                c.currentPosition = r.currentPosition
                                c.currentPositionIndex = r.currentPositionIndex
                                # c.currentPositionIndex = validPositions.index(c.currentPosition)
                                #print(c.stackCount)
                                #print(r.stackCount)
                                c.stackCount += r.stackCount
                                cups.remove(r)
                                """
                                if isValidMove(c):
                                    print("valid")
                                    print(c.stackCount)
                                    c.stackCount += r.stackCount
                                    print(c.stackCount)
                                    cups.remove(r)
                                else:
                                    print("NOT valid")
                                    # c.stackCount += r.stackCount
                                    # print(c.stackCount)
                                    # cups.remove(r)
                                    r.currentPosition = r.lastPosition
                                """

                # Ensure position is on the "board"
                for c in cups:
                    if not c.center in validPositions:
                        c.center = c.lastPosition

        elif event.type == pygame.MOUSEMOTION:
            if selected is not None: # selected can be `0` so `is not None` is required
                # move object
                cups[selected].x = event.pos[0] + selected_offset_x
                cups[selected].y = event.pos[1] + selected_offset_y

                
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    screen.fill(WHITE)
    index = 0

    #Redraw game board
    for r in rects:
        if (index % 2 == 0):
            pygame.draw.rect(screen, YELLOW, r)
        else:
            pygame.draw.rect(screen, BLACK, r)

        index += 1

    #Redraw stacks
    for r in cups:
            pygame.draw.circle(screen, BLUE, r.center, 20)
            screen.blit(font.render(str(r.stackCount), True, (255,255,255)), (r.left, r.top))

    centerStacks()

    #Update Pygame display.
    pygame.display.update()

    

# Finish Pygame.  
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))
