# coding: utf-8
import tkinter as tk

class Gaister:
    def __init__(self):
        self.turn=True
        self.board=[]
        self.selection=[-1,-1]
        self.player=[]
        self.set_board()
        self.set_counter()

    def set_counter(self):
        self.counter=[4,4,0,4,4]

    def set_board(self):
        # -2:青おばけ
        # -1:赤おばけ
        # 0:空
        # 1:敵の青おばけ
        # 2:敵の赤おばけ
        self.board.clear()
        self.board.append([0]+[1 for i in range(4)]+[0])
        self.board.append([0]+[2 for i in range(4)]+[0])
        self.board.append([0 for i in range(6)])
        self.board.append([0 for i in range(6)])
        self.board.append([0]+[-1 for i in range(4)]+[0])
        self.board.append([0]+[-2 for i in range(4)]+[0])

    def judge_victory(self):
        if self.counter[1]==0 or self.counter[3]==0:
            return 1
        elif self.board[0][0]==-2 or self.board[0][5]==-2:
            return 1
        elif self.counter[0]==0 or self.counter[4]==0:
            return -1
        elif self.board[5][0]==1 or self.board[5][5]==1:
            return -1
        else:
            return 0

    def print_board(self):
        print(self.board)

    def reset_selection(self):
        self.selection=[-1,-1]

    def select(self,x,y):
        if self.turn==True and self.board[x][y]<0:
            self.selection=[x,y]
            return True
        elif self.turn==False and self.board[x][y]>0:
            self.selection=[x,y]
            return True
        else:
            self.reset_selection()
            return False

    def judge_swap(self,a,b):
        if self.turn==True and self.board[a][b]<0:
            return False
        elif self.turn==False and self.board[a][b]>0:
            return False
        elif a==self.selection[0] and b==self.selection[1]+1:
            return True
        elif a==self.selection[0] and b==self.selection[1]-1:
            return True
        elif a==self.selection[0]+1 and b==self.selection[1]:
            return True
        elif a==self.selection[0]-1 and b==self.selection[1]:
            return True
        return False

    def swap(self,a,b):
        if self.judge_swap(a,b) is False:
            self.reset_selection()
            return False
        else:
            if self.board[a][b]*self.board[self.selection[0]][self.selection[1]]<0:
                self.count(self.board[a][b])
                self.board[a][b]=0
            tmp=self.board[self.selection[0]][self.selection[1]]
            self.board[self.selection[0]][self.selection[1]]=self.board[a][b]
            self.board[a][b]=tmp
            self.reset_selection()
            return True

    def count(self,a):
        self.counter[a+2]-=1
