# Tic-Tac-Toe program with Pygame

import copy
import random
import sys
import time

import numpy as np
import pygame
from const import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')
screen.fill(BG_COLOR)


class Computer:
    def __init__(self, lvl=1, player=1):
        self.lvl = lvl
        self.player = player

    def rand(self, main_board):
        # time.sleep(0.75)
        return main_board.get_vac_sqrs()[random.randrange(0, len(main_board.get_vac_sqrs()))]

    def minimax(self, board, maximizing):
        if board.fin_state() == 1:
            return 1, None
        if board.fin_state() == 2:
            return -1, None
        if board.marked_sqrs == 9:
            return 0, None

        if maximizing == True:
            max_eval = -2
            best_move = None
            empty_sqrs = board.get_vac_sqrs()

            for (row, col) in empty_sqrs:
                temp = copy.deepcopy(board)
                temp.mark_sqr(row, col, 1, False)
                eval = self.minimax(temp, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif maximizing == False:
            min_eval = 2
            best_move = None
            empty_sqrs = board.get_vac_sqrs()

            for (row, col) in empty_sqrs:
                temp = copy.deepcopy(board)
                temp.mark_sqr(row, col, 2, False)
                eval = self.minimax(temp, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    def eval(self, main_board):
        if self.lvl == 0:
            move = self.rand(main_board)
        else:
            move = self.minimax(main_board, False)[1]
        return move


class Position:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = np.copy(self.squares)
        self.marked_sqrs = 0

    def fin_state(self):
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        return 0

    def mark_sqr(self, row, col, player, show):
        self.squares[row][col] = player
        self.marked_sqrs += 1
        if show:
            print(self.squares)

    def vacant_square(self, row, col):
        return self.squares[row][col] == 0

    def get_vac_sqrs(self):
        vac_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.vacant_square(row, col):
                    vac_sqrs.append((row, col))
        return vac_sqrs


class Board:
    def __init__(self):
        self.position = Position()
        self.player = 2
        self.computer = Computer()
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    def show_lines(self):
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0),
                         (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQSIZE, 0),
                         (WIDTH-SQSIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE),
                         (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQSIZE),
                         (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)

    def next_player(self):
        self.player = 1 if self.player == 2 else 2

    def draw_fig(self, row, col):
        # 1 is cross and 2 is circle
        if self.player == 1:
            start_des = (col*SQSIZE+OFFSET, row*SQSIZE+OFFSET)
            end_des = (col*SQSIZE+SQSIZE-OFFSET, row*SQSIZE+SQSIZE-OFFSET)
            start_asc = (col*SQSIZE+OFFSET, row*SQSIZE+SQSIZE-OFFSET)
            end_asc = (col*SQSIZE+SQSIZE-OFFSET, row*SQSIZE+OFFSET)
            pygame.draw.line(screen, CROSS_COL, start_des,
                             end_des, CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COL, start_asc,
                             end_asc, CROSS_WIDTH)
        elif self.player == 2:
            center = (col*SQSIZE+SQSIZE//2, row*SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen, CIRC_COL, center, SQSIZE//4, CIRC_WIDTH)

    def is_over(self):
        return self.position.fin_state() != 0 or self.position.marked_sqrs == 9


def main():

    new_board = Board()
    ai = new_board.computer
    print('New game has started!')
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1]//SQSIZE
                col = pos[0]//SQSIZE
                if new_board.position.vacant_square(row, col) and new_board.running:
                    new_board.position.mark_sqr(
                        row, col, new_board.player, True)
                    new_board.draw_fig(row, col)
                    new_board.next_player()
                    if new_board.is_over():
                        new_board.running = False
        if new_board.gamemode == 'ai' and new_board.player == ai.player and new_board.running:
            pygame.display.update()
            row, col = ai.eval(new_board.position)
            new_board.position.mark_sqr(row, col, ai.player, True)
            new_board.draw_fig(row, col)
            new_board.next_player()
            if new_board.is_over():
                new_board.running = False
                print('Game over!')
        pygame.display.update()


main()
