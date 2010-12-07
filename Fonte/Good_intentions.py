from Game import *
from Menu import *

import Garbage
import gc

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
    
def set_credits_menu():
    width = 1024
    height = 768
    pygame.display.init
    menu_screen = pygame.display.set_mode((width,height))
    # Background
    background = pygame.image.load(os.path.join('', 'images', 'creditos_menu_bg.jpg'))
    background = background.convert()

    # Cursor
    pygame.mouse.set_visible(False)
    cursor = Cursor(16,16,'images/cursor.png')

    #Options in menu
    back = Option(700,645,279,92,'images/voltar.png','images/voltar_big.png',main_menu, 1.182648402,0.05)

    # Menu
    menu = Menu()
    menu.append(back)
    
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
    stage1 = Option(100,150,250,327,'images/fase1_small.jpg','images/fase1.jpg',stage1_function,1.2,0.05,True)
    stage2 = Option(400,400,250,278,'images/fase2.jpg','images/fase2_big.jpg',stage2_function,1.2,0.05,True)
    # ...
    
    
    # Create menu
    select_menu = Menu()
    select_menu.append(stage1)
    select_menu.append(stage2)
    # ...
    
    select_menu.main_loop(cursor,screen,background)
    

# Stage 1 Function
def stage1_function():
    chances = STAGE_CHANCE
    # Put here the prolog story
    prolog = Story('prologo01', 9, 1,'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
    prolog.play_loop(1)
    game = Game("fase1.tmx",100000,150,525,'Dicennian_Running_Past.ogg')
    while(chances > 0):
        print "chances: " + str(chances)
        posx, posy , time, win = game.main_loop()
        print("POSICAO NO FINAL")
        print(posx ,posy, win)
        if win:
            # Put here the final story 
            print "Ganhou!"
            success = Story('suceed01', 7, 1, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
            #fail = Story('fail01', 3, 2, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
            success.bg_music.play_load_music(1)
            success.play_loop(1)
            #flag, frame = success.test_commands(1)
            #while flag:
            #    print flag, frame
            #    if frame in [2,3,4,5,6,7]:
            #        flag, frame = success.play(frame)
            #    else:
            #        flag, frame = success.test_commands(frame)
            #print flag , frame
            #if frame == -1:
            #    fail.play_loop(2)
            success.bg_music.fadeout_music(1)
            del(game)
            gc.collect()
            return
        else:
            chances = chances - 1
            game = Game("fase1.tmx",time,posx,posy,'Dicennian_Running_Past.ogg')
            posx, posy, time, win = game.main_loop()
            print("POSICAO NO FINAL")
            print(posx ,posy, win)
    # Put here the failed story
    print "Perdeu!"
    fail = fail = Story('fail01', 3, 1, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
    fail.play_loop(1)
    del(game)
    gc.collect()
    game_over_menu = set_game_over_menu(stage1_function,main_menu)
    
def stage2_function():
    chances = STAGE_CHANCE
    # Put here the prolog story
    prolog = Story('prologo02', 7, 1,'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
    prolog.play_loop(1)
    game = Game("fase2.tmx",100000,150,525,'lost_dreams.ogg')
    while(chances > 0):
        print "chances: " + str(chances)
        posx, posy , time, win = game.main_loop()
        print("POSICAO NO FINAL")
        print(posx ,posy, win)
        if win:
            # Put here the final story 
            print "Ganhou!"
            success = Story('suceed02', 5, 1, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
            #fail = Story('fail02', 3, 2, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
            success.bg_music.play_load_music(1)
            success.play_loop(1)
            #flag, frame = success.test_commands(1)
            #while flag:
            #    print flag, frame
            #    if frame in [2,3,4,5,6,7]:
            #        flag, frame = success.play(frame)
            #    else:
            #        flag, frame = success.test_commands(frame)
            #print flag , frame
            #if frame == -1:
            #    fail.play_loop(2)
            success.bg_music.fadeout_music(1)
            del(game)
            gc.collect()
            return
        else:
            chances = chances - 1
            game = Game("fase2.tmx",time,posx,posy,'lost_dreams.ogg')
            posx, posy, time, win = game.main_loop()
            print("POSICAO NO FINAL")
            print(posx ,posy, win)
    # Put here the failed story
    print "Perdeu!"
    fail = fail = Story('fail02', 3, 1, 'Gluck-Melodie-Orfeo-ed-Euridice-1951.ogg')
    fail.play_loop(1)
    del(game)
    gc.collect()
    game_over_menu = set_game_over_menu(stage2_function,main_menu)
    
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
    new_game = Option(300,250,161,63,'images/jogar.png','images/jogar_big.png',stage_select,1.248,0.05,True)
    creditos = Option(290,350,256,87,'images/creditos.png','images/creditos_big.png',set_credits_menu,1.85,0.05,True)

    # Menu
    main_menu = Menu()
    main_menu.append(new_game)
    main_menu.append(creditos)
    
    main_menu.main_loop(cursor,menu_screen,background)
    
    
if __name__ == '__main__': 
    main_menu()
    #Garbage.log_garbage()
    Garbage.print_garbage()
