import numpy as np 
import pygame 
import math
import sys 
from copy import deepcopy 
import time 
import random 

SQUARE_COUNT = 7 
SQUARE_SIZE = 75 
BLUE = (0,0,255) 
RED = (255,0,0) 
GREY = (182,179,179) 
WHITE = (255,255,255) 
BLACK = (0,0,0) 
width = SQUARE_COUNT * SQUARE_SIZE 
height = SQUARE_COUNT * SQUARE_SIZE 
size = (width, height) 


def create_board_1(): 
    board = np.zeros((SQUARE_COUNT,SQUARE_COUNT))
    board[0][0] = 1
    board[6][6] = 1
    board[0][6] = 2
    board[6][0] = 2
    return board
        

def create_board_2(): 
    board = np.zeros((SQUARE_COUNT,SQUARE_COUNT))
    board[0][0] = 1
    board[6][6] = 1
    board[0][6] = 2
    board[6][0] = 2
    for i in range(SQUARE_COUNT):
        for l in range(SQUARE_COUNT):
            if board[i][l] == 1 or board[i][l] == 2:
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        if i+m <= 6 and i+m >=0 and l+n <= 6 and l+n >=0 and board[i+m][l+n] == 0:  
                            board[i+m][l+n] = 5
    return board
    

def create_board_3(): 
    board = np.zeros((SQUARE_COUNT,SQUARE_COUNT))
    board[0][0] = 1
    board[6][6] = 1
    board[0][6] = 2
    board[6][0] = 2
    for i in range(SQUARE_COUNT):
        board[3][i] = 5
        board[i][3] = 5
    board[3][3] = 0
    return board 
  

def create_board_4(): 
    board = np.zeros((SQUARE_COUNT,SQUARE_COUNT))
    board[0][0] = 1
    board[6][6] = 1
    board[0][6] = 2
    board[6][0] = 2  
    for i in range(-1,2):
        for l in range(-1,2):
            board[3+i][3+l] = 5
    board[3][3] = 0        
    return board   


def create_board_5(): 
    board = np.zeros((SQUARE_COUNT,SQUARE_COUNT))
    board[0][0] = 1
    board[6][6] = 1
    board[0][6] = 2
    board[6][0] = 2
    board[1][3] = 5
    board[2][1] = 5
    board[2][5] = 5
    board[3][2] = 5
    board[3][4] = 5
    board[4][1] = 5
    board[4][5] = 5
    board[5][3] = 5     
    return board


def create_board_6(): 
    board = np.zeros((SQUARE_COUNT,SQUARE_COUNT))
    board[0][0] = 1
    board[6][6] = 1
    board[0][6] = 2
    board[6][0] = 2
    for i in range(1,6):
        board[i][1] = 5
        board[i][5] = 5
    board[1][2] = 5
    board[5][2] = 5
    board[1][4] = 5
    board[5][4] = 5  
    return board


def create_board_7():       
    board = np.zeros((SQUARE_COUNT,SQUARE_COUNT))
    p = 4
    while p != 0:
        if p % 2 == 0:
            x = random.randrange(0, 6)
            y = random.randrange(0, 6)
            board[x][y] = 1
        else:
            x = random.randrange(0, 6)
            y = random.randrange(0, 6)
            board[x][y] = 2
        p -= 1
    num = random.randrange(0, 21)
    while num != 0:
        r = random.randrange(0, 6)
        c = random.randrange(0, 6)
        if board[r][c] == 0:
            board[r][c] = 5
            num -= 1
    return board
    

def place(board, x, y, piece): 
    board[x][y] = piece 


def jump(board, c, r, x, y, piece): 
    board[r][c] = 0
    board[x][y] = piece
               

def change(board, r, c):
    for i in range(SQUARE_COUNT):
        for l in range(SQUARE_COUNT):
            if i == r + 2:
                if (l == c - 2 or l == c - 1 or l == c or l == c + 1 or l == c + 2) and board[i][l] == 0:
                    board[i][l] = 4            
            if i == r + 1:
                if (l == c - 1 or l == c or l == c + 1) and board[i][l] == 0:
                    board[i][l] = 3
                if (l == c - 2 or l == c + 2) and board[i][l] == 0:
                    board[i][l] = 4
            if i == r:
                if (l == c - 1 or l == c + 1) and board[i][l] == 0:
                    board[i][l] = 3
                if (l == c - 2 or l == c + 2) and board[i][l] == 0:
                    board[i][l] = 4
            if i == r - 1:
                if (l == c - 1 or l == c or l == c + 1) and board[i][l] == 0:
                    board[i][l] = 3
                if (l == c - 2 or l == c + 2) and board[i][l] == 0:
                    board[i][l] = 4
            if i == r - 2:
                if (l == c - 2 or l == c - 1 or l == c or l == c + 1 or l == c + 2) and board[i][l] == 0:
                    board[i][l] = 4        
            
                
def change_back(board): 
    for i in range(SQUARE_COUNT):
        for l in range(SQUARE_COUNT):
            if board[i][l] == 3 or board[i][l] == 4:
                board[i][l] = 0        


def eat(board, x, y, not_piece, piece): 
    for m in range(-1, 2):
        for n in range(-1, 2):
            if x+m <= 6 and x+m >=0 and y+n <= 6 and y+n >=0: 
                if board[x+m][y+n] == not_piece:
                    board[x+m][y+n] = piece
                

def piece_counter(board, piece): 
    piece_count = 0
    for r in range(SQUARE_COUNT):
        for c in range(SQUARE_COUNT):
            if board[r][c] == piece:
                piece_count += 1
    return piece_count
        

def available_moves(board, piece):
    available_moves = 0
    for i in range(SQUARE_COUNT):
        for l in range(SQUARE_COUNT):
            if board[i][l] == piece:
                for m in range(-2, 3):
                    for n in range(-2, 3):
                        if i+m <= 6 and i+m >=0 and l+n <= 6 and l+n >=0: 
                            if board[i+m][l+n] == 0:
                                available_moves += 1                           
    return available_moves

        
def draw_pieces(board): 
    for k in range(SQUARE_COUNT):
        for l in range(SQUARE_COUNT):
            if board[k][l] == 1: 
                pygame.draw.circle(screen, RED, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
            elif board[k][l] == 2: 
                pygame.draw.circle(screen, BLUE, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
            elif board[k][l] == 3 or board[k][l] == 4: 
                pygame.draw.circle(screen, GREY, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
            elif board[k][l] == 5: 
                pygame.draw.line(screen, WHITE, (l*SQUARE_SIZE,k*SQUARE_SIZE), ((l+1)*SQUARE_SIZE,(k+1)*SQUARE_SIZE), 3)
                pygame.draw.line(screen, WHITE, (l*SQUARE_SIZE,(k+1)*SQUARE_SIZE), ((l+1)*SQUARE_SIZE,k*SQUARE_SIZE), 3)
            else: 
                pygame.draw.circle(screen, BLACK, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
    pygame.display.update() 
     
        
def draw_lines(board): 
    for i in range(SQUARE_COUNT -  1):
        pygame.draw.line(screen, WHITE, ((i+1)*SQUARE_SIZE,0), ((i+1)*SQUARE_SIZE,SQUARE_SIZE*SQUARE_COUNT), 2) 
        pygame.draw.line(screen, WHITE, (0,(i+1)*SQUARE_SIZE), (SQUARE_SIZE*SQUARE_COUNT,(i+1)*SQUARE_SIZE),2)    
    pygame.display.update() 
    
        
def is_terminal_node(board): 
    if available_moves(board, player_1_piece) == 0 or available_moves(board, player_2_piece) == 0:
        return True


def get_player_1_pieces(board): 
    pieces = []
    for r in range(SQUARE_COUNT):
        for c in range (SQUARE_COUNT): 
            if board[r][c] == player_1_piece:
                pieces.append([r,c])
    return pieces    
    

def get_player_2_pieces(board): 
    pieces = []
    for r in range(SQUARE_COUNT):
        for c in range (SQUARE_COUNT): 
            if board[r][c] == player_2_piece:
                pieces.append([r,c])
    return pieces


def get_player_1_moves(board): 
    moves = []
    for piece in get_player_1_pieces(board):
        temp1_board = deepcopy(board)
        r = piece[0]
        c = piece[1]
        change(temp1_board, r, c)
        for m in range(-3, 3):
            for n in range(-3, 3):
                temp2_board = deepcopy(temp1_board)
                if r+m <= 6 and r+m >=0 and c+n <= 6 and c+n >=0: 
                    if temp1_board[r+m][c+n] == 3:
                        place(temp2_board, r+m, c+n, player_1_piece)
                        eat(temp2_board, r+m, c+n, player_2_piece, player_1_piece)
                        change_back(temp2_board)
                        moves.append(temp2_board)
                    elif temp1_board[r+m][c+n] == 4:
                        jump(temp2_board, c, r, r+m, c+n, player_1_piece)
                        eat(temp2_board, r+m, c+n, player_2_piece, player_1_piece)
                        change_back(temp2_board)
                        moves.append(temp2_board)
    return moves 


def get_player_2_moves(board):
    moves = []
    for piece in get_player_2_pieces(board):
        temp1_board = deepcopy(board)
        r = piece[0]
        c = piece[1]
        change(temp1_board, r, c)
        for m in range(-3, 3):
            for n in range(-3, 3):
                temp2_board = deepcopy(temp1_board)
                if r+m <= 6 and r+m >=0 and c+n <= 6 and c+n >=0: 
                    if temp1_board[r+m][c+n] == 3:
                        place(temp2_board, r+m, c+n, player_2_piece)
                        eat(temp2_board, r+m, c+n, player_1_piece, player_2_piece)
                        change_back(temp2_board)
                        moves.append(temp2_board)
                    elif temp1_board[r+m][c+n] == 4:
                        jump(temp2_board, c, r, r+m, c+n, player_2_piece)
                        eat(temp2_board, r+m, c+n, player_1_piece, player_2_piece)
                        change_back(temp2_board)
                        moves.append(temp2_board)
    return moves
    
    
def greedy(board, piece): 
    if turn == 0:
        max_pieces = -math.inf
        best_move = None
        for move in get_player_1_moves(board):
            player_1_pieces = piece_counter(move, piece)
            if available_moves(move, player_2_piece) == 0:
                return move
            elif player_1_pieces >= max_pieces:
                max_pieces = player_1_pieces
                best_move = move          
        return best_move
    if turn != 0:
        max_pieces = -math.inf
    best_move = None
    for move in get_player_2_moves(board):
        player_2_pieces = piece_counter(move, piece)
        if available_moves(move, player_2_piece) == 0:
            return move
        elif player_2_pieces >= max_pieces:
            max_pieces = player_2_pieces
            best_move = move        
    return best_move

def evaluate1(board): 
    return piece_counter(board, player_1_piece) - piece_counter(board, player_2_piece)    
    
    
def evaluate2(board): 
    return piece_counter(board, player_2_piece) - piece_counter(board, player_1_piece)
    
    
def minimax1(board, depth, max_player): 
    if depth == 0 or is_terminal_node(board):
        return evaluate1(board), board  
    if max_player:  
        maxEval = -math.inf
        best_move = None
        for move in get_player_1_moves(board):
            evaluation = minimax1(move, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else: 
        minEval = math.inf
        best_move = None
        for move in get_player_2_moves(board):
            evaluation = minimax1(move, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move 
    
def minimax2(board, depth, max_player): 
    if depth == 0 or is_terminal_node(board):
        return evaluate2(board), board  
    if max_player: 
        maxEval = -math.inf
        best_move = None
        for move in get_player_2_moves(board):
            evaluation = minimax2(move, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = math.inf
        best_move = None
        for move in get_player_1_moves(board):
            evaluation = minimax2(move, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move
     
        
def random_move(board): 
    if turn == 0 and not game_over:
        num = random.randrange(0, len(get_player_1_moves(board))) 
        move = get_player_1_moves(board)[num] 
        return move    
    if turn != 0 and not game_over:
        num = random.randrange(0, len(get_player_2_moves(board))) 
        move = get_player_2_moves(board)[num] 
        return move    
    

    
         
which_board = int(input("Board (you can see all the boards in the README file): "))
if which_board == 1:
    board = create_board_1() 
elif which_board == 2:    
    board = create_board_2() 
elif which_board == 3:    
    board = create_board_3() 
elif which_board == 4:    
    board = create_board_4()    
elif which_board == 5:    
    board = create_board_5()  
elif which_board == 6:    
    board = create_board_6()     
elif which_board == 7:    
    board = create_board_7() 

    
player_1 = int(input("Player 1(1: Human,2: Greedy, 3:  Minimax, 4: Random Moves): "))
player_2 = int(input("Playes 2(1: Human,2: Greedy, 3: Minimax, 4: Random Moves): ")) 

game_over = False 
turn = 0                             
pygame.init() 
screen = pygame.display.set_mode(size)   
draw_lines(board) 
draw_pieces(board) 
font_size = 50 
myfont = pygame.font.Font(None, font_size) 
clicks = 0 
player_1_piece = 1 
player_2_piece = 2    

if player_1 != 1 and player_2 != 1: 
    time.sleep(3)

while not game_over:
    if turn == 0: 
        if player_1 == 1:
            pygame.display.update() 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  
                    if clicks == 0:
                        posc = event.pos[0] 
                        c = int(math.floor(posc/SQUARE_SIZE)) 
                        posr = event.pos[1] 
                        r = int(math.floor(posr/SQUARE_SIZE)) 
                        if board[r][c] == player_1_piece: 
                            change(board, r, c)
                            draw_pieces(board)
                            clicks = 1
                    if clicks == 1:
                        posy = event.pos[0]
                        y = int(math.floor(posy/SQUARE_SIZE)) 
                        posx = event.pos[1]
                        x = int(math.floor(posx/SQUARE_SIZE)) 
                        if board[x][y] == 3:
                            place(board, x, y, player_1_piece)
                            eat(board, x, y, player_2_piece, player_1_piece)
                            turn += 1  
                            turn = turn % 2 
                            change_back(board)
                            draw_pieces(board)
                            clicks = 0
                            if available_moves(board, player_2_piece) == 0: 
                                if evaluate1(board) > 0: 
                                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK) 
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                                    pygame.display.update()
                                    print("PLAYER 1 WINS!!!") 
                                    game_over = True 
                                elif evaluate2(board) > 0:
                                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK) 
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                                    print("PLAYER 2 WINS!!!")
                                    game_over = True 
                                else:
                                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK) 
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                                    pygame.display.update()
                                    print("IT'S A TIE!!!")
                                    game_over = True 
                        elif board[x][y] == 4: 
                            jump(board, c, r, x, y, player_1_piece)
                            eat(board, x, y, player_2_piece, player_1_piece)
                            turn += 1
                            turn = turn % 2
                            change_back(board)
                            draw_pieces(board)
                            clicks = 0
                            if available_moves(board, player_2_piece) == 0: 
                                if evaluate1(board) > 0: 
                                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK) 
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                                    pygame.display.update()
                                    print("PLAYER 1 WINS!!!") 
                                    game_over = True 
                                elif evaluate2(board) > 0:
                                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK) 
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                                    pygame.display.update()
                                    print("PLAYER 2 WINS!!!")
                                    game_over = True 
                                else:
                                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK) 
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                                    pygame.display.update()
                                    print("IT'S A TIE!!!") 
                                    game_over = True 
                        else: 
                            if board[x][y] == player_1_piece: 
                                change_back(board)
                                r = x 
                                c = y 
                                change(board, r, c)
                                draw_pieces(board)
                            else: 
                                change_back(board)
                                draw_pieces(board)
        elif player_1 == 2 and not game_over:  
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            time.sleep(1) 
            best_move = greedy(board, player_1_piece)
            board = best_move 
            draw_pieces(board)
            turn += 1
            turn = turn % 2        
            if available_moves(board, player_2_piece) == 0:
                if evaluate1(board) > 0: 
                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK) 
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                    pygame.display.update()
                    print("PLAYER 1 WINS!!!")
                    game_over = True 
                elif evaluate2(board) > 0:
                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK) 
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                    pygame.display.update()
                    print("PLAYER 2 WINS!!!") 
                    game_over = True 
                else:
                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK) 
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                    pygame.display.update()
                    print("IT'S A TIE!!!") 
                    game_over = True 
        elif player_1 == 3 and not game_over: 
            draw_pieces(board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            best_move = minimax1(board, 3, True)[1] 
            board = best_move 
            turn += 1
            turn = turn % 2       
            draw_pieces(board)
            if available_moves(board, player_2_piece) == 0: 
                if evaluate1(board) > 0: 
                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK) 
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                    pygame.display.update()
                    print("PLAYER 1 WINS!!!") 
                    game_over = True 
                elif evaluate2(board) > 0:
                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK) 
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                    pygame.display.update()
                    print("PLAYER 2 WINS!!!")
                    game_over = True 
                else:
                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK) 
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                    pygame.display.update()
                    print("IT'S A TIE!!!") 
                    game_over = True 
        elif player_1 == 4 and not game_over: 
            if not game_over: 
                time.sleep(1) 
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                chosen_move = random_move(board) 
                board = chosen_move 
                turn += 1
                turn = turn % 2       
                draw_pieces(board)
                pygame.display.update()
                if available_moves(board, player_2_piece) == 0: 
                    if evaluate1(board) > 0: 
                        label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK) 
                        screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                        pygame.display.update()
                        print("PLAYER 1 WINS!!!")
                        game_over = True 
                    elif evaluate2(board) > 0:
                        label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK) 
                        screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                        pygame.display.update()
                        print("PLAYER 2 WINS!!!")  
                        game_over = True 
                    else:
                        label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK)
                        screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10)) 
                        pygame.display.update()
                        print("IT'S A TIE!!!") 
                        game_over = True 


    if turn != 0:
        if player_2 == 1:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    player_1_piece = 1
                    player_2_piece = 2
                    if clicks == 0:
                        posc = event.pos[0]
                        c = int(math.floor(posc/SQUARE_SIZE))
                        posr = event.pos[1]
                        r = int(math.floor(posr/SQUARE_SIZE))
                        if board[r][c] == player_2_piece:
                            change(board, r, c)
                            draw_pieces(board)
                            clicks = 1
                    if clicks == 1:
                        posy = event.pos[0]
                        y = int(math.floor(posy/SQUARE_SIZE))
                        posx = event.pos[1]
                        x = int(math.floor(posx/SQUARE_SIZE))
                        if board[x][y] == 3:
                            place(board, x, y, player_2_piece)
                            eat(board, x, y, player_1_piece, player_2_piece)
                            turn += 1
                            turn = turn % 2
                            change_back(board)
                            draw_pieces(board)
                            clicks = 0
                            if available_moves(board, player_1_piece) == 0:
                                if evaluate1(board) > 0:
                                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK)
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                                    pygame.display.update()
                                    print("PLAYER 1 WINS!!!")
                                    game_over = True
                                elif evaluate2(board) > 0:
                                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK)
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                                    pygame.display.update()
                                    print("PLAYER 2 WINS!!!")
                                    game_over = True
                                else:
                                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK)
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                                    pygame.display.update()
                                    print("IT'S A TIE!!!")
                                    game_over = True
                        elif board[x][y] == 4:
                            jump(board, c, r, x, y, player_2_piece)
                            eat(board, x, y, player_1_piece, player_2_piece)
                            turn += 1
                            turn = turn % 2
                            change_back(board)
                            draw_pieces(board)
                            clicks = 0
                            if available_moves(board, player_1_piece) == 0:
                                if evaluate1(board) > 0:
                                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK)
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                                    pygame.display.update()
                                    print("PLAYER 1 WINS!!!")
                                    game_over = True
                                elif evaluate2(board) > 0:
                                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK)
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                                    pygame.display.update()
                                    print("PLAYER 2 WINS!!!")
                                    game_over = True
                                else:
                                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK)
                                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                                    pygame.display.update()
                                    print("IT'S A TIE!!!")
                                    game_over = True
                        else:
                            if board[x][y] == player_2_piece:
                                change_back(board)
                                r = x
                                c = y
                                change(board, r, c)
                                draw_pieces(board)
                            else:
                                change_back(board)
                                draw_pieces(board)
        elif player_2 == 2 and not game_over: 
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()               
            time.sleep(1)
            player_1_piece = 1
            player_2_piece = 2
            best_move = greedy(board, player_2_piece)
            board = best_move
            draw_pieces(board)
            turn += 1
            turn = turn % 2        
            if available_moves(board, player_1_piece) == 0:
                if evaluate1(board) > 0:
                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK)
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                    pygame.display.update()
                    print("PLAYER 1 WINS!!!")
                    game_over = True
                elif evaluate2(board) > 0:
                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK)
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                    pygame.display.update()
                    print("PLAYER 2 WINS!!!")
                    game_over = True
                else:
                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK)
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                    pygame.display.update()
                    print("IT'S A TIE!!!")
                    game_over = True
        elif player_2 == 3 and not game_over:
            draw_pieces(board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            player_1_piece = 1
            player_2_piece = 2
            best_move = minimax2(board, 3, True)[1]           
            board = best_move 
            turn += 1
            turn = turn % 2       
            draw_pieces(board)
            if available_moves(board, player_1_piece) == 0:
                if evaluate1(board) > 0:
                    label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK)
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                    pygame.display.update()
                    print("PLAYER 1 WINS!!!")
                    game_over = True
                elif evaluate2(board) > 0:
                    label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK)
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                    pygame.display.update()
                    print("PLAYER 2 WINS!!!")
                    game_over = True
                else:
                    label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK)
                    screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                    pygame.display.update()
                    print("IT'S A TIE!!!")
                    game_over = True       
        elif player_2 == 4 and not game_over:
                time.sleep(1)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                player_1_piece = 1
                player_2_piece = 2
                best_move = random_move(board)        
                board = best_move 
                turn += 1
                turn = turn % 2       
                draw_pieces(board)
                if available_moves(board, player_1_piece) == 0:
                    if evaluate1(board) > 0:
                        label = myfont.render("PLAYER 1 WINS!!!", True, WHITE, BLACK)
                        screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                        pygame.display.update()
                        print("PLAYER 1 WINS!!!")
                        game_over = True
                    elif evaluate2(board) > 0:
                        label = myfont.render("PLAYER 2 WINS!!!", True, WHITE, BLACK)
                        screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                        pygame.display.update()
                        print("PLAYER 2 WINS!!!")
                        game_over = True
                    else:
                        label = myfont.render("IT'S A TIE!!!", True, WHITE, BLACK)
                        screen.blit(label, (110,SQUARE_SIZE*SQUARE_COUNT/2 - 10))
                        pygame.display.update()
                        print("IT'S A TIE!!!")
                        game_over = True
            

while game_over: 
    pygame.display.update()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        
    
        
        
        
        
        
        
        