from Game import *
from Menu import *

# Global Variable that define tha actual stage of he player
ACTUAL_STAGE = 1
STAGE_WIN = (0,0)
STAGE_CHANCE = 2

# The game over menu
def set_game_over_menu(function_retry,function_quit=sys.exit):
    width = 1024
    height = 768
    pygame.display.init
    menu_screen = pygame.display.set_mode((width,height))
    # Background
    background = pygame.image.load(os.path.join('', 'images', 'game_over_bg.jpg'))
    background = background.convert()

    # Cursor
    pygame.mouse.set_visible(False)
    cursor = Cursor(16,16,'images/cursor.png')

    #Options in menu
    retry = Option(100,200,550,61,'images/retry.png','images/retry_big.png',function_retry, 1.109,0.05)
    quit = Option(100,270,274,60,'images/quit.png','images/quit_big.png',function_quit, 1.11,0.05)

    # Menu
    menu = Menu()
    menu.append(retry)
    menu.append(quit)
    
    menu.main_loop(cursor,menu_screen,background)

# The Stage Select Menu
def stage_select():
    # Screen
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    ACTUAL_STAGE
    #Background
    background = pygame.image.load(os.path.join('', 'images', 'menu_bg.jpg'))
    background = background.convert()
    
    #Cursor
    pygame.mouse.set_visible(False)
    cursor = Cursor(16,16,'images/cursor.png')
    
    #Put Here the Stages of the game
    stage1 = Option(200,200,173,89,'images/little.png','images/big.png',stage1_function,1.42,0.05,True)
    stage2 = Option(500,500,173,89,'images/little.png','images/big.png',stage1_function,1.42,0.05,False)
    # ...
    
    
    # Create menu
    select_menu = Menu()
    select_menu.append(stage1)
    select_menu.append(stage2)
    # ...
    
    select_menu.main_loop(cursor,screen,background)
    

# Stage 1 Function
def stage1_function():
    global ACTUAL_STAGE
    chances = STAGE_CHANCE
    # Put here the prolog story
    prolog = Story('prologo01', 9, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
    prolog.play()
    game = Game("huge_objects.tmx",100000,150,525,'Dicennian_Running_Past.ogg')
    while(chances > 0):
        print "chances: " + str(chances)
        posx, posy , win = game.main_loop()
        print("POSICAO NO FINAL")
        print(posx ,posy, win)
        if win:
            # Put here the final story 
            print "Ganhou!"
            prolog = Story('suceed01', 7, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
            prolog.play(True)
            return
        else:
            chances = chances - 1
            game = Game("huge_objects.tmx",100000,posx,posy,'Dicennian_Running_Past.ogg')
            posx, posy, win = game.main_loop()
            print("POSICAO NO FINAL")
            print(posx ,posy, win)
    # Put here the failed story
    print "Perdeu!"
    fail = Story('fail01', 3, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
    fail.play()
    del(game)
    game_over_menu = set_game_over_menu(stage1_function,main_menu)

def main_menu():

    pygame.display.init
    menu_screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    # Background
    background = pygame.image.load(os.path.join('', 'images', 'menu_bg.jpg'))
    background = background.convert()
    
    # Cursor
    pygame.mouse.set_visible(False)
    cursor = Cursor(16,16,'images/cursor.png')
    
    #Options in menu
    new_game = Option(200,200,173,89,'images/little.png','images/big.png',stage_select,1.42,0.05,True)

    # Menu
    main_menu = Menu()
    main_menu.append(new_game)
    
    main_menu.main_loop(cursor,menu_screen,background)
    
    
if __name__ == '__main__': main_menu()
