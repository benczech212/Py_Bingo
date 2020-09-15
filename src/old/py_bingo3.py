import pygame as pg
import math
import random
import time

DEBUG_LEVEL = 0

WIN_WIDTH = 1280
WIN_HEIGHT = 1024

col_num_min = 1
col_num_max = 15
col_num_range = col_num_max - col_num_min + 1

ROW_COUNT = 5
COL_COUNT = 5

pg.font.init()
pg.display.init()
pg.init()

CELL_FONT = pg.font.SysFont("comicsans", 50)

WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT),pg.RESIZABLE)


class Background:
    
    WIDTH = 1000
    HEIGHT = 1000
    VEL = 2
    def __init__(self,x,y):
        self.y = y
        self.x1 = x
        self.x2 = self.x1 + self.WIDTH
        self.surface = pg.Surface((self.WIDTH,self.HEIGHT))


    def draw(self,win):
        w,h = pg.display.get_surface().get_size()
        color = (255,255,255)
        rect = pg.Rect(0,0,w,h)
        pg.draw.rect(self.surface, color, rect)

#daubing = 
class Player:
    count = 0
    def __init__(self,name):
        self.name = name
        self.id = self.count
        self.cards = []
        self.score = 0
        self.bingos = 0
        Player.count+=1

    def give_cards(self,count):
        debug_msg("Giving card to {}".format(self.name),1)
        for card in range(count):
            self.cards.append(Card())

    def bingo(self, card):
        print("Player {} just got a BINGO with card {}".format(self.id,card.id))
        self.score += 100
        self.bingos += 1
        


class Ball:
    letters = ["B","I","N","G","O"]
    ball_count = 0
    def __init__(self,num):
        self.num = None
        if num == None:    
            self.num = random.randrange(col_num_min,col_num_range * ROW_COUNT)
        else:
            self.num = num
        self.col_num = self.num % col_num_range
        self.ball_id = self.ball_count
        Ball.ball_count+=1
        debug_msg("Ball Picked: {}".format(self.num),1)
        
    
class Card:
    count = 0
    def __init__(self):
        self.nums = []
        self.width = 5
        self.height = 5
        self.fill_nums()
        self.id = self.count
        self.bingo = False
        Card.count +=1
        
    def fill_nums(self):
        num_id = 0
        self.nums = []
        for x in range(self.width):
            self.nums.append([])
            rand_min = ((x + 0) * col_num_range) + 1 
            rand_max = ((x + 1) * col_num_range) + 1 
            random_nums = random.sample(range(rand_min,rand_max),self.height)
            for num in random_nums:
                self.nums[x].append({num:False})

    def check_ball(self,ball):
        for x in range(self.width):
            for y in range(self.height):
                for num in self.nums[x][y]:
                    if num  == ball.num:
                        self.nums[x][y][num] = True
                        debug_msg("DOB {} on card {} at ({}, {})".format(ball.num,self.id,x,y),1)
                    else:
                        pass
        return self.check_bingo()
        
    def check_bingo(self):
        bingo = False
        for x in range(self.width):
            check_col = []
            check_row = []
            for y in range(self.height):
                for mark in self.nums[x][y]:
                    check_row.append(self.nums[x][y][mark])
                for mark in self.nums[y][x]:
                    check_col.append(self.nums[y][x][mark])
            if all(check_col):
                bingo = True
            elif all(check_row):
                bingo = True
        return bingo


def setup_balls():
    balls = []
    min_num = 1
    max_num = (COL_COUNT * col_num_range)
    rounds = 1
    for round_num in range(rounds):
        for ball_num in range(100):
            ball_nums = random.sample(range(min_num,max_num+1),max_num)
        
        for num in ball_nums:
            balls.append(Ball(num))

    return balls


        
def debug_msg(msg,lvl):
    if DEBUG_LEVEL >= lvl:
        print(msg)

def test_draw():
    WIN.fill((255,255,255))
    w, h = pg.display.get_surface().get_size()
    bg_surf = pg.Surface((w,h))
    bg_rect = pg.Rect(0,0,w,h)
    pg.draw.rect(bg_surf,(255,255,255),bg_rect)
    card = players[0].cards[0]
    dobbed_color = (255,32,32)
    undobbed_color = (0,0,0)
    tile_width = 50
    tile_height = 50
    for x in range(card.width):
        for y in range(card.height):
            for num in card.nums[x][y]:
                position = (tile_width * x, tile_height * y)

                cell_bg_rect = pg.Rect(position,(tile_width,tile_height))
                cell_bg_surf = pg.Surface((tile_width,tile_height))
                cell_bg_color = (128,128,128)
                pg.draw.rect(cell_bg_surf,cell_bg_color,cell_bg_rect)
                dobbed = card.nums[x][y][num]
                text = "{}".format(num,dobbed)
                if dobbed:
                    color = dobbed_color
                else:
                    color = undobbed_color  
                text_label = CELL_FONT.render(text,1,color)
                WIN.blit(text_label, position)
    pg.display.flip()

class Cell:
    default_height = 50
    default_width = 50
    count = 0
    def __init__(self,num,position,size):
        if num == None:
            self.num = 0
        else:
            self.num = num
        self.id = self.count
        self.position = position
        self.size = size
        self.is_dobbed = False
        self.marked_color = (255,0,0)
        self.unmarked_color = (0,0,0)
        self.rect = pg.Rect(self.position,self.size)
        self.surface = pg.Surface(self.size)
        Cell.count += 1
    def draw(self):
        if self.is_dobbed:
            color = self.marked_color
        else:
            color = self.unmarked_color
        text = "{:^4}".format(self.num)
        text_label = CELL.FONT.render(text,1,color)
        WIN.blit(text,label,position)
        

def check_events():
    for event in pg.event.get(): # User did something
        if event.type == pg.QUIT: # If user clicked close
            done=True


    
    
    



players = [Player("player1")]

card_count = 1
for player in players:
    player.give_cards(card_count)

balls = setup_balls()
bingo_count = 0
bingo_count_max = 15
game_over = False

#### TEST


    
done = False
clock = pg.time.Clock()
####


while not game_over:
    while not done:
        #clock.tick(10)
        check_events()
        for ball_num, ball in enumerate(balls):
            test_draw()
            pg.display.update()
            check_events()
            debug_msg("Ball Picked! {}".format(ball.num),1)
            for player in players:
                for card in player.cards:
                    if card.bingo:
                        is_bingo = False                    
                    else:
                        is_bingo = card.check_ball(ball)
                    if is_bingo:
                        bingo_count += 1
                        player.bingo(card)
                        player.cards.remove(card)
                        player.cards.append(Card())
            if bingo_count >= bingo_count_max:
                game_over = True
                break
    
    
    print("Game Over!")            
        
