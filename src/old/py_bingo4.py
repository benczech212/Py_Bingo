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


class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.started_at = self.clock.get_time()
        self.players = []
        self.balls = shuffle_balls()
        self.current_ball_id = 0
        self.game_over = False
        self.ball_history_display = Ball_History_Display()
        self.events = Game_Events()


    def add_player(self,player):
        self.players.append(player)
        debug_msg("{} joined the game".format(player.name),1)
    def remove_player(self,player):
        self.players.remove(player)
        debug_msg("{} left the game".format(player.name),1)
    
    def tick():
        pass

    def next_ball(self):
        self.current_ball_id += 1
        self.ball_history_display.add_ball(self.balls[self.current_ball_id])



#daubing = 
class Player:
    count = 0
    def_card_count = 1
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
        self.ball_id = self.ball_count
        Ball.ball_count+=1
        debug_msg("Ball Picked: {}".format(self.num),1)
        
    
class Card:
    count = 0
    def __init__(self):
        self.nums = []
        self.width = 5
        self.height = 5
        self.generate_nums()
        
        self.id = self.count
        self.bingo = False
        self.cells = []
        Card.count +=1
        self.display_size = (250,250)
        self.position = (0,0)
        self.cell_height = self.display_size[0] // self.height
        self.cell_width = self.display_size[1] // self.width
        self.cell_size = (self.width, self.cell_height)
        self.fill_cells()
        
    def generate_nums(self):
        num_id = 0
        self.nums = []
        for x in range(self.width):
            self.nums.append([])
            rand_min = ((x + 0) * col_num_range) + 1 
            rand_max = ((x + 1) * col_num_range) + 1 
            random_nums = random.sample(range(rand_min,rand_max),self.height)
            for num in random_nums:
                self.nums[x].append(num)

    def fill_cells(self):
        for x in range(self.width):
            for y in range(self.height):
                num = self.nums[x][y]
                cell_pos_x = self.position[0] + (x * self.cell_width)
                cell_pos_y = self.position[1] + (y * self.cell_height)
                cell_pos = (cell_pos_x,cell_pos_y)
                self.cells.append(Cell(num,x,y,cell_pos,self.cell_size))
                  

    def check_ball(self,ball):
        change_made = False
        for cell in self.cells:
            if cell.num == ball.num:
                cell.is_dobbed = True
                change_made = True
        return change_made
        
    def check_bingo(self):
        bingo = False
        check_cols = []
        check_rows = []
        check_col_nums = []
        check_row_nums = []
        check_diag = []
        check_diag_nums = []
        check_diag_inv = []
        check_diag_inv_nums = []
        for x in range(self.width):
            check_cols.append([])
            check_rows.append([])
            check_col_nums.append([])
            check_row_nums.append([])
        for x in range(self.width):
            for y in range(self.height):        
                for cell in self.cells:
                    if cell.x == x and cell.y == y:
                        check_cols[y].append(cell.is_dobbed)
                        check_col_nums[y].append(cell.num)
                        check_rows[x].append(cell.is_dobbed)
                        check_row_nums[x].append(cell.num)
                        #check_rows[y].append(cell.is_dobbed)
                        if cell.x == cell.y:
                            check_diag.append(cell.is_dobbed)
                            check_diag_nums.append(cell.num)
                        #if 5 - x == y:
                            #check_diag_inv.append(cell.is_dobbed)
                    
        checks = [check_cols,check_rows]
        check_nums = [check_col_nums,check_row_nums]
        check_names = ["Colunm Bingo","Row Bingo"]
        for check_num, check in enumerate(checks):
            for group_num, dobbed in enumerate(check):
                if all(dobbed) and len(dobbed)>0:
                    check_name = str(checks[check_num])
                    print("{} at # {}".format(check_names[check_num],group_num))
                    print(check_nums[check_num][group_num])
                    bingo = True



        return bingo

    def draw(self):
        for cell in self.cells:
            cell.draw()
            


class Cell:
    default_height = 50
    default_width = 50
    count = 0
    def __init__(self,num,x,y,position,size):
        if num == None:
            self.num = 0
        else:
            self.num = num
        self.id = self.count
        self.position = position
        self.size = size
        self.is_dobbed = False
        self.dobbed_color = (255,0,0)
        self.undobbed_color = (0,0,0)
        self.rect = pg.Rect(self.position,self.size)
        self.surface = pg.Surface(self.size)
        self.x = x
        self.y = y
        Cell.count += 1

    def draw(self):
        if self.is_dobbed:
            color = self.dobbed_color
        else:
            color = self.undobbed_color
        text = "{:^4}".format(self.num)
        text_label = CELL_FONT.render(text,1,color)
        WIN.blit(text_label,self.position)


class Ball_History_Display:
    
    item_size = (100,100)
    items_shown = 8
    side_boundry_size = (100,100)
    canvas_size = ((item_size[0] * items) + (side_boundry_size[0] * 2),item_size[1])
    
    max_in_log = 10
    
    def __init__(self):
        self.balls = []
        self.ball_nums = []
        self.size = (400,50)
        self.pos = (100, 100)
        self.item_size = (50,50)
        self.item_limit = self.size[0] // self.item_size[0]
        self.surface = pg.Surface(self.size)
        self.Rect = pg.Rect(self.pos,self.size)
        self.bg_color = (32,32,32)
        self.pos_offset = 0
        self.pos_offset_act = 0


    def add_ball(self,ball):
        self.ball_nums.append(ball.num)
        self.balls.append(ball)
        self.pos_offset += self.item_size[0]
        if len(self.balls) > self.items_shown:
            self.balls.remove(self.balls[0])
            self.ball_nums.remove(self.ball_nums[0])
        
    def draw(self):
        ball_nums = []
        if self.pos_offset != self.pos_offset_act:
            self.pos_offset_act += 1
            time.sleep(0.1)
        for ball_id, ball in enumerate(self.balls):
            pos_x = self.log_position_x + (self.ball_size_px[0]*ball_id)
            pos_y = self.log_position_y
            pos = (pos_x,pos_y)
            cent_x = pos_x + (self.item_size[0]//2) - self.pos_offset_act
            cent_y = pos_y + (self.item_size[1]//2)
            cent = (cent_x,cent_y)
            radius = min(self.item_size[0],self.item_size[1])//2            
            steps  = 10
            r_step = radius / steps
            
            grad_start = [255,128,0]
            grad_end = [128,64,0]
            color_delta = []
            color_step = []
            color = []
            
            for i in range(len(grad_start)):
                delta = grad_end[i] - grad_start[i]
                step = delta / steps
                color_delta.append(delta)
                color_step.append(step)
            for s in range(steps):
                color = []
                for i in range(len(grad_start)):
                    val = grad_start[i] + int(color_step[i] * s)
                    color.append(val)
                color_tup = (color[0],color[1],color[2])
                r = int((steps - s) * r_step)
                circle = pg.draw.circle(WIN,color_tup,cent,r)
                pg.display.update()

            
            text = "{:^4}".format(ball.num)
            text_color = (0,0,0)
            text_label = CELL_FONT.render(text,1,text_color)
            text_pos = (pos[0] - self.pos_offset_act, pos[1])
            WIN.blit(text_label,text_pos)

class Game_Events:
    offset = pg.USEREVENT
    def __init__(self):
        self.events = [
            {
                "id":(self.offset + 1),
                "name":"Next Ball",
                "duration":5000,
            },
            {
                "id":(self.offset + 2),
                "name":"Unused",
                "duration":10000
            }
        ]
        self.set_timers()
    def set_timers(self):
        for event in self.events:
            pg.time.set_timer(event['id'],event['duration'])


            

        

def debug_msg(msg,lvl):
    if DEBUG_LEVEL >= lvl:
        print(msg)

def shuffle_balls():
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
        




def check_events():
    done = False
    for event in pg.event.get(): # User did something
        if event.type == pg.QUIT: # If user clicked close
            GAME_OVER=True
        if event.type == GAME.events.events[0]['id']:
            GAME.next_ball()

def draw_stuff():
    WIN.fill((255,255,255))
    players = GAME.players
    GAME.ball_history_display.draw()
    pg.display.update()

    
    
def game_loop():
    check_events()
    draw_stuff()
    GAME.clock.tick(TARGET_FPS)






##### GLOBAL FLAGS
TARGET_FPS = 60

#### GLOBAL GAME OBJECTS
GAME = Game()
GAME.add_player(Player("Ben"))




### Startup

for player in GAME.players:
    player.give_cards(player.def_card_count)
###########



while not GAME.game_over:
    game_loop()
print("Game Over!")            
        
