import pygame

YELLOW = (255,255,0)
pygame.init()
screen = pygame.display.set_mode((800,600),pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
background.fill(YELLOW)
background = background.convert()
screen.blit(background,(0,0))
clock = pygame.time.Clock()

mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 30
# How many seconds the "game" is played.
playtime = 0.0

BLOCK_SIZE = 50
rects = []
RED   = (255,   0,   0)
BLACK   = (0,   0,   0)

# for x in range(14):
#     rects.append( pygame.Rect(x*(BLOCK_SIZE+5), BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE) )
#     rects[x].x = x*(BLOCK_SIZE + 5)

for x in range(16):
    rects.append( pygame.Rect(x*(BLOCK_SIZE+5), BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE) )
    rects[x].x = x*(BLOCK_SIZE)
    rects[x].y = 300

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
                for i, r in enumerate(rects):
                        if r.collidepoint(event.pos):
                            selected = i
                            selected_offset_x = r.x - event.pos[0]
                            selected_offset_y = r.y - event.pos[1]
            # x,y = pygame.mouse.get_pos()
            # print('x: ' + str(x)) 
            # print('y: ' + str(y)) 
        elif event.type == pygame.MOUSEBUTTONUP:
                selected = None

        elif event.type == pygame.MOUSEMOTION:
            if selected is not None: # selected can be `0` so `is not None` is required
                # move object
                rects[selected].x = event.pos[0] + selected_offset_x
                rects[selected].y = event.pos[1] + selected_offset_y

                
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

    #Update Pygame display.
    pygame.display.update()

    

# Finish Pygame.  
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))
