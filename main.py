import pygame

class Square(pygame.Rect):
    def __init__(self,left, top, width, height):
        pygame.Rect.__init__(self, left, top, width, height)
        self.stackCount = 1

YELLOW = (255,255,0)
GREEN = (0, 255, 0)
pygame.init()
screen = pygame.display.set_mode((800,600))
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

for x in range(16):
    rects.append( pygame.Rect(x*(BLOCK_SIZE+5), BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE) )
    rects[x].x = x*(BLOCK_SIZE)
    rects[x].y = 300

for x in range(16):
    cups.append( Square(x*(BLOCK_SIZE+5), BLOCK_SIZE, BLOCK_SIZE / 2, BLOCK_SIZE / 2) )
    cups[x].x = x*(BLOCK_SIZE)
    cups[x].y = 300

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
            print('x: ' + str(x)) 
            print('y: ' + str(y)) 
            if event.button == 1:
                for i, r in enumerate(cups):
                    if r.collidepoint(event.pos):
                        selected = i
                        selected_offset_x = r.x - event.pos[0]
                        selected_offset_y = r.y - event.pos[1]
                        print("Stack count: %s" % r.stackCount)
                        for dex, c in enumerate(cups):
                            if dex is not i and c.colliderect(r): #One stack collects another
                                c.stackCount += r.stackCount
                                cups.remove(r)
                                print(rects)
                                print(cups)

        elif event.type == pygame.MOUSEBUTTONUP:
                selected = None
                for i, r in enumerate(cups):
                    if event.button == 1:
                        for dex, c in enumerate(cups):
                            if dex is not i and c.colliderect(r): #One stack collects another
                                c.stackCount += r.stackCount
                                cups.remove(r)

        elif event.type == pygame.MOUSEMOTION:
            if selected is not None: # selected can be `0` so `is not None` is required
                # move object
                cups[selected].x = event.pos[0] + selected_offset_x
                cups[selected].y = event.pos[1] + selected_offset_y

                
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    screen.fill(YELLOW)
    index = 0
    for r in rects:
        if (index % 2 == 0):
            pygame.draw.rect(screen, RED, r)
        else:
            pygame.draw.rect(screen, BLACK, r)

        index += 1

    for r in cups:
            pygame.draw.rect(screen, BLUE, r)
            screen.blit(font.render(str(r.stackCount), True, (255,0,0)), (r.left, r.top))

    #Center squares
    for r in rects:
        for c in cups:
            if r.colliderect(c):
                c.center = r.center

    #Update Pygame display.
    pygame.display.update()

    

# Finish Pygame.  
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))
