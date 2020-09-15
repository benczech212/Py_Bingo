import pygame as pg
import math
import random
import time
col_num_min = 1
col_num_max = 5
col_num_range = col_num_max  - col_num_min + 1

row_count = 5
col_count = 5


DEBUG_LEVEL = 1



#daubing = 


class Ball:
    letters = ["B","I","N","G","O"]
    ball_count = 0
    def __init__(self,num):
        if num == None:    
            min_val = col_num_min
            max_val = col_num_range * row_count
            self.num = random.randrange(min_val,max_val)
        else:
            self.num = num
        self.col_num = self.num % col_num_range
        self.ball_id = self.ball_count
        Ball.ball_count+=1
        debug_msg("Ball Picked: {}".format(self.num),1)
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
        self.bingo = False
        i = 1
        for col in range(self.col_count):
            self.dob_num.append([])
            for row in range(self.row_count):
                self.dob_num[col].append({0:False})      
                i+=1 
        print("Done making card")
        

        i = 1
        for row in range(self.row_count):
            nums = []
            for col in range(self.col_count):
                rand_min = (row + 0) * (col_num_range + 1)
                rand_max = (row + 1) * (col_num_range + 0)
                
                for num in self.dob_num[row][col]:
                        nums.append(num)
            rand_num = random.randrange(rand_min,rand_max)
            while rand_num in nums:
                rand_num = random.randrange(rand_min,rand_max)
            self.dob_num[col][row] = {rand_num:False}
            i+=1


    def print_card(self):
        transpose = False
        if transpose:
            nums = []
            for i in range(self.row_count):
                nums.append([row[i] for row in self.dob_num])
        else: nums = self.dob_num
        for r_num in range(len(nums)):
            # Row Header
            print("|{:^7d}|".format(r_num + 1), end = " ")
        print()
        print("-"*self.col_count*10)
        for r_num, r in enumerate(nums):
            for c in r:
                for num in c:
                    print("| {:>3d} {:<} |".format(num,c[num]),end = " ")
            print()

    def dob(self,ball):
        for row_num, r in enumerate(self.dob_num):
            for col_num, c in enumerate(r):
                for num in c:
                    if ball.num == num:
                        c[num] = True
                        print("DOB! {:3d} [row: {:3d} col: {:3d}]".format(ball.num,row_num,col_num))
                        #self.print_card()
        if self.check_bingo():
            win()
        
    def check_bingo(self):
        check_rows = True
        check_cols = True
        check_diags = False
        bingo = False        
        for r in range(self.row_count):    
            check_row = []
            check_col = []
            diag_1 = []
            diag_2 = []
            for c in range(self.col_count):       
                for num in self.dob_num[c][r]:
                    check_col.append(self.dob_num[c][r][num])
                for num in self.dob_num[r][c]:
                    check_row.append(self.dob_num[r][c][num])
                #for i, num in enumerate(self.dob_num[r][r]):
                    #diag_1.append(self.dob_num[i][i][num])
                #for num in self.dob_num[r][self.row_count-r-1]:
                    #diag_2.append(self.dob_num[r][self.row_count-r-1][num])
            if (
                check_rows and all(check_row)
                or check_cols and all(check_col)
                or check_diags and (all(diag_1) or all(diag_2))
            ):
                #or (check_diags and ( all(diag_1) or all(diag_2)):
                self.bingo = True
                break
        
def debug_msg(msg,lvl):
    if DEBUG_LEVEL >= lvl:
        print(msg)




test_card = Card(row_count,col_count)
test_card.print_card()


while True:
    balls = []
    ball_nums = []
    for ball_num in range(100):
        new_ball = Ball(random.randrange(1,25))
        while new_ball.num in ball_nums:
            new_ball = Ball(random.randrange(1,25))    
        balls.append(new_ball)
        test_card.dob(new_ball)
        time.sleep(1)

        if test_card.bingo:
            print("BINGO! in {} moves".format(len(balls)))
            test_card.print_card()
            test_card = Card(row_count,col_count)
            balls = []
            time.sleep(1)
