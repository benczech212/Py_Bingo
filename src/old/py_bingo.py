import pygame as pg
import math
import random

col_num_min = 1
col_num_max = 15
col_num_range = col_num_max  - col_num_min + 1

row_count = 5
col_count = 5






#daubing = 


class Ball:
    letters = ["B","I","N","G","O"]
    def __init__(self):
        min_val = col_num_min
        max_val = col_num_range * row_count
        self.num = random.randrange(min_val,max_val)
        self.col_num = self.num % col_num_range
        #self.letter = self.letters[col_num_range]
        #self.print(num)

class Card:
    count = 0
    def __init__(self,row_count,col_count):
        self.id = self.count
        self.row_count = row_count
        self.col_count = col_count
        Card.count += 1
        self.dob_num = []
        self.dob_transposed = []
        self.test_accumulator = 1
        for col in range(self.col_count):
            self.dob_num.append([])
            for row in range(self.row_count):
                rand_num = random.randrange(1,15)
                rand_num += col_num_range * col
                while rand_num in self.dob_num[col]:
                    rand_num = random.randrange(1,15)
                    rand_num += col_num_range * col
                self.dob_num[col].append({rand_num:False})       
        print("Done making card")
        self.transpose()

    def transpose(self):
        self.dob_transposed = []
        

    def print_card(self):
        transposed = []
        for i in range(self.row_count):
            transposed.append([row[i] for row in self.dob_num])

        for r_num in range(len(transposed)):
            # Row Header
            print("|{:^7d}|".format(r_num + 1), end = " ")
        print()
        print("-"*self.col_count*10)
        for r_num, r in enumerate(transposed):
            for c in r:
                for num in c:
                    print("| {:>3d} {:<} |".format(num,c[num]),end = " ")
            print()

    def dob(self,ball):
        for r in self.dob_num:
            for c in r:
                for num in c:
                    if ball.num == num:
                        c[num] = True
                        print("DOB! {}".format(ball.num))
                        self.print_card()
        
    def check_bingo(self):
        for r in range(len(self.row_count)):
            
        pass








test_card = Card(row_count,col_count)
test_card.print_card()

for ball_num in range(10):
    ball = Ball()
    test_card.dob(ball)
