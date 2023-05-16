'''
    AI 2023
    แก้ code ได้เฉพาะใน file นี้เท่านั้น 
    จะเพิ่ม function ก็สามารถทำได้นะ แต่ชื่อ class กับชื่อ findBestMove method ห้ามแก้เด็ดขาด
    นอกนั้น ทำได้หมด จะเพิ่มตัวแปรก็ทำได้
    ห้ามใช้ library ที่ อจ ต้อง install เพิ่มเติมจากที่กำหนดให้
'''
import copy,random
from board import Board
from time import time
# use deepcopy to copy a list เนื่องจาก list ใน python ส่งค่าแบบ pass by reference
# ดังนั้นเราเลยต้องใช้ deepcopy function ใน copy เพื่อให้เป็นการส่งค่า pass by value แทน


MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]


# ห้ามแก้ชื่อ class
class ComputeOthello:
    
    # ห้ามแก้ __init__ method
    def __init__(self,board,num_tiles,n = 8):
        self.board = board
        self.num_tiles = num_tiles
        self.time_play = [0,0]
        self.n = n
        self.current_player = 0
        self.opponent = 1
        self.conner = False

    def make_move(self):
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.flip_tiles()
    
    def flip_tiles(self):
        curr_tile = self.current_player + 1 
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move, direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[1] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        self.num_tiles[self.current_player] += 1
                        self.num_tiles[(self.current_player + 1) % 2] -= 1
                        i += 1

    def has_tile_to_flip(self, move, direction):
        i = 1
        if self.current_player in (0, 1) and \
           self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or \
                    self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def has_legal_move(self):
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False
    
    def get_legal_moves(self):
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)
        
        if self.conner:
            connerset = [0,7]
            result = [sublist for sublist in moves if any(item in sublist for item in connerset)]
            if result:
                return result
        return moves

    def is_legal_move(self, move):
        if move != () and self.is_valid_coord(move[0], move[1]) \
           and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False

    def is_valid_coord(self, row, col):
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False


    # ทำ function นี้ให้สมบูรณ์
    # ห้ามแก้ชื่อ function และตัว arguments ที่เป็น input ของ function
    def max_value(self, alpha, beta, depth):

        max_score = float('-inf')
        for move in self.get_legal_moves():
            self.move = move
            self.make_move()
            self.current_player, self.opponent = self.opponent, self.current_player
            score = self.min_value(alpha, beta, depth-1)
            if score > max_score:
                max_score = score
            if max_score >= beta:
                return max_score
            alpha = max(alpha, max_score)
        return max_score

    def min_value(self, alpha, beta, depth):

        min_score = float('inf')
        for move in self.get_legal_moves():
            self.move = move
            self.make_move()
            self.current_player, self.opponent = self.opponent, self.current_player
            score = self.max_value(alpha, beta, depth-1)
            if score < min_score:
                min_score = score
            if min_score <= alpha:
                return min_score
            beta = min(beta, min_score)
        return min_score

    def findBestMove(self, board, current_player, opponent, num_tiles):
        self.board = board
        self.num_tiles = num_tiles
        self.current_player = current_player
        self.opponent = opponent
        depth = 0

        best_move = None
        max_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in self.get_legal_moves():
            self.move = move
            self.make_move()
            self.current_player, self.opponent = self.opponent, self.current_player
            score = self.min_value(alpha, beta, depth-1)
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, max_score)
        return best_move
position_scores = []

position_score_1 = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, 0, 0, 0, 0, -2, 10],
    [5, -2, 0, 0, 0, 0, -2, 5],
    [5, -2, 0, 0, 0, 0, -2, 5],
    [10, -2, 0, 0, 0, 0, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]
position_scores.append(position_score_1)

position_score_2 = [
    [50, -10, 5, 2, 2, 5, -10, 50],
    [-10, -20, -1, -1, -1, -1, -20, -10],
    [5, -1, 0, 0, 0, 0, -1, 5],
    [2, -1, 0, 0, 0, 0, -1, 2],
    [2, -1, 0, 0, 0, 0, -1, 2],
    [5, -1, 0, 0, 0, 0, -1, 5],
    [-10, -20, -1, -1, -1, -1, -20, -10],
    [50, -10, 5, 2, 2, 5, -10, 50]
]
position_scores.append(position_score_2)
position_score_random = [
    [10, -3, 5, 4, 4, 5, -3, 10],
    [-3, -5, -1, -1, -1, -1, -5, -3],
    [5, -1, 0, 0, 0, 0, -1, 5],
    [4, -1, 0, 0, 0, 0, -1, 4],
    [4, -1, 0, 0, 0, 0, -1, 4],
    [5, -1, 0, 0, 0, 0, -1, 5],
    [-3, -5, -1, -1, -1, -1, -5, -3],
    [10, -3, 5, 4, 4, 5, -3, 10]
]
position_scores.append(position_score_random)
position_score_aggressive = [
    [100, -25, 10, 5, 5, 10, -25, 100],
    [-25, -50, -2, -2, -2, -2, -50, -25],
    [10, -2, 1, 1, 1, 1, -2, 10],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [10, -2, 1, 1, 1, 1, -2, 10],
    [-25, -50, -2, -2, -2, -2, -50, -25],
    [100, -25, 10, 5, 5, 10, -25, 100]
]
position_scores.append(position_score_aggressive)
position_score_hybrid = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, 1, 1, 1, 1, -2, 10],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [10, -2, 1, 1, 1, 1, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]
position_scores.append(position_score_hybrid)

def evaluate_position(self):
    total_score = 0
    for i in range(8):
        for j in range(8):
            if self.board[i][j] == self.current_player:
                # ใช้ตาราง position_score_1
                total_score += position_scores[0][i][j]
            elif self.board[i][j] == self.opponent:
                # ใช้ตาราง position_score_2
                total_score += position_scores[1][i][j]
            elif self.board[i][j] == self.opponent:
                
                total_score += position_scores[2][i][j]
            elif self.board[i][j] == self.opponent:
                
                total_score += position_scores[3][i][j]
            elif self.board[i][j] == self.opponent:
                
                total_score += position_scores[4][i][j]    
            
    return total_score