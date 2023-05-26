import pygame
import sys
from chessAI import RandomAI

from const import *
from game import Game
from square import Square
from move import Move
import random
import time

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.ai = RandomAI('black')  # AI plays as black

    def choose_move(self, game):
        board = game.board
        valid_moves = board.get_all_valid_moves(self.color)
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger


        while True:
            
            if game.next_player == 'white':  # Player's turn     
                # show methods
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)
      
                

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # if clicked square has a piece ?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            # valid piece (color) ?
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods 
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                    
                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)
                    
                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # valid move ?
                            if board.valid_move(dragger.piece, move):
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)                            

                                # sounds
                                game.play_sound(captured)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()
                        
                        dragger.undrag_piece()
                    
                    # key press
                    elif event.type == pygame.KEYDOWN:
                        # changing themes
                        if event.key == pygame.K_t:
                            game.change_theme()

                        # changing themes
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger

                    # quit application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            else:  # AI's turn
                ai_move = self.ai.choose_move(game)
                # Sleep for 5 seconds
 

                if ai_move:
                    initial_square, final_move = ai_move
                    captured = board.squares[final_move.final.row][final_move.final.col].has_piece()
                    board.move(initial_square.piece, final_move)
                    board.set_true_en_passant(initial_square.piece)   
                    game.play_sound(captured)
                    game.next_turn()
                 


            pygame.display.update()


main = Main()
main.mainloop()