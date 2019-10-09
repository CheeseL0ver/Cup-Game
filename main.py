import pygame

pygame.init()
screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
background = pygame.Surface(screen.get_size())
background.fill((255,255,0))
background = background.convert()
screen.blit(background,(0,0))
clock = pygame.time.Clock()

mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 30
# How many seconds the "game" is played.
playtime = 0.0

size = 100
pygame.draw.rect(screen,8,(0,0,100,100))
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
        elif event.type == pygame.VIDEORESIZE:
            print("Resized...%s %s" % event.size)
            screen = pygame.display.set_mode(event.size,pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(background,event.size), (0,0))
            pygame.display.flip()

                
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))
