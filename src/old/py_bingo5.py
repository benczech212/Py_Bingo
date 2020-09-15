import pygame as pg
import math
import random
import time
DEBUG_LEVEL = 0

WIN_WIDTH = 1280
WIN_HEIGHT = 1024




pg.font.init()
pg.display.init()
pg.init()



WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT),pg.RESIZABLE)

class Fonts:
    def __init__(self):
        #self.show_fonts()
        self.cell_font = pg.font.SysFont("arial", 50)
        self.ball_font = pg.font.SysFont("comicsans", 50)
        self.calibri = pg.font.SysFont("calibri", 50)
    def show_fonts(self):
        fonts = pg.font.get_fonts()
        for font in fonts:
            print(font)

class Game:
    tropical_theme = [
            pg.Color(210, 191, 29),
            pg.Color(29, 210, 101),
            pg.Color(29, 48, 210),
            pg.Color(210, 29, 138),
            pg.Color(210, 29, 29)
        ]
    easter_theme = [
            pg.Color(29, 210, 150),
            pg.Color(59, 29, 210),
            pg.Color(210, 29, 89),
            pg.Color(180, 210, 29)
        ]
    default_theme = []
    def __init__(self):
        self.clock = pg.time.Clock()
        self.started_at = self.clock.get_time()
        self.players = []
        self.col_num_min = 1
        self.col_num_max = 15
        self.row_count = 5
        self.col_count = 5
        self.balls = shuffle_balls(self.col_num_min,self.col_num_max * self.col_count )
        self.current_ball_id = 0
        self.game_over = False
        self.ball_history_display = Ball_History_Display()
        self.events = Game_Events()
        self.bingo_letters = ["B","I","N","G","O"]
        self.system_colors = self.default_theme
        self.generate_colors = False

        if self.generate_colors:
            self.system_colors = auto_colors()
        
        self.col_num_range = self.col_num_max - self.col_num_min + 1

        
    def auto_color(self):
        colors = []
        for c in range(self.col_count):
            offset = 216
            hue = offset + (c * (255 / self.col_count))
            colors.append(wheel(hue))
        return colors

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
        if self.current_ball_id < len(GAME.balls):
            ball = self.balls[self.current_ball_id]
            self.ball_history_display.add_ball(ball)
        else:
            GAME.game_over = True
            
        for player in GAME.players:
            for card in player.cards:
                card.tick(ball)

FONT = Fonts()              



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
    
    ball_count = 0
    def __init__(self,num):
        self.num = None
        if num == None:    
            self.num = random.randrange(GAME.col_num_min,GAME.col_num_range * GAME.row_count)
        else:
            self.num = num
        self.ball_id = self.ball_count
        Ball.ball_count+=1
        debug_msg("Ball Picked: {}".format(self.num),1)
        
class Card_Cell:
    def __init__(self, pos, size, num, unit_pos, bg_color):
        self.pos = pos
        self.unit_pos = unit_pos
        self.size = size
        self.num = num
        self.is_daubed = False
        self.rect = pg.Rect(pos,size)
        self.bg_color = bg_color
        self.border_color = (0,0,0)
        self.text_color = (0,0,0)
        self.text_assist_color = (255,0,0)
        self.text_daubed_color = (255,255,255)


    def draw(self):
        # BG
        pg.draw.rect(WIN,self.bg_color,self.rect, 0)

        #Border
        pg.draw.rect(WIN,self.border_color,self.rect, 1)

        #header row
        text = "{:^}".format(self.num)
        text_label = FONT.cell_font.render(text,1,self.text_color)
        text_num_pos = text_label.get_rect(center=(self.rect.center))
        WIN.blit(text_label,text_num_pos)

class Card:
    count = 0
    def __init__(self):
        self.pos = (100,300)
        self.cell_size = (60,60)
        self.cell_bg_color = (96,96,82)
        self.header_row_size = self.cell_size
        self.unit_width = 5
        self.unit_height = 5
        self.card_size = (self.unit_width * self.cell_size[0], self.unit_height * self.cell_size[1])
        self.nums = []
        self.generate_nums()
        self.cells = []
        self.header_cells = []
        self.populate_cells()
        self.assist_mode = False
        self.auto_mode = True
        self.id = self.count
        self.bingo = False
        self.is_shown = True
        self.text_color = (0,0,0)
        self.assist_text_color = (255,0,0)
        Card.count +=1
    
        
    def draw(self):
        for cell in self.header_cells:
            cell.draw()
        for cell in self.cells:
            cell.draw()

    def populate_cells(self):
        # header row
        for x in range(self.unit_width):
            cell_pos_x = self.pos[0] + (x * self.cell_size[0])                
            cell_pos_y = self.pos[1]
            cell_pos = (cell_pos_x, cell_pos_y)
            num = GAME.bingo_letters[x]
            unit_pos = (x,-1)
            bg_color = GAME.tropical_theme[x]
            self.header_cells.append(Card_Cell(cell_pos,self.header_row_size,num,unit_pos,bg_color))
        # cells
        for x in range(self.unit_width):
            for y in range(self.unit_height):
                cell_pos_x = self.pos[0] + (x * self.cell_size[0])                
                cell_pos_y = self.pos[1] + self.header_row_size[1] + (y * self.cell_size[1])
                cell_pos = (cell_pos_x, cell_pos_y)
                num = self.nums[x][y]
                unit_pos = (x,y)
                self.cells.append(Card_Cell(cell_pos,self.cell_size,num,unit_pos,self.cell_bg_color))

        
    def generate_nums(self):
        num_id = 0
        self.nums = []
        for x in range(self.unit_width):
            self.nums.append([])
            rand_min = ((x + 0) * GAME.col_num_range) + 1 
            rand_max = ((x + 1) * GAME.col_num_range) + 1 
            random_nums = random.sample(range(rand_min,rand_max),self.unit_height)
            for num in random_nums:
                self.nums[x].append(num)

    def auto_daub(self,ball):
        if self.auto_daub:
            for cell in self.cells:
                if cell.num == ball.num and not cell.is_daubed:
                    cell.is_daubed = True
        #self.check_bingo()

    

    def tick(self, ball):
        self.auto_daub(ball)
        if self.is_shown:
            self.draw()
        #self.assist_mode()
                    


        
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

    #def draw(self):
        #for cell in self.cells:
            #cell.draw()
            


class History_Item:
    move_speed = 2
    def __init__(self,num,start_pos,size):
        self.pos = start_pos
        self.target_pos = self.pos
        self.num = num
        self.color = (255,0,128)
        
        self.size = size
        self.radius = min(self.size)//2
        self.rect = pg.Rect(self.pos,self.size)

    def draw(self):
        pg.draw.circle(WIN, num_to_color(self.num),self.pos,self.radius)

        text_color = (0,0,0)
        text_offset = (-20,-20)
        line_spacing = 20
        text_letter = "{:^}".format(num_to_let(self.num))
        text_letter_label = FONT.cell_font.render(text_letter,1,text_color)
        text_letter_pos = text_letter_label.get_rect(center=(self.pos[0],self.pos[1] - line_spacing))
        WIN.blit(text_letter_label,text_letter_pos)

        text_num = "{:^}".format(self.num)
        text_num_label = FONT.cell_font.render(text_num,1,text_color)
        text_num_pos = text_num_label.get_rect(center=(self.pos[0],self.pos[1] - line_spacing))
        WIN.blit(text_num_label,text_num_pos)

        

    def move(self,display):
        if abs(self.pos[0] - self.target_pos[0]) > self.move_speed:
            new_pos_x = self.pos[0] - self.move_speed
            new_pos_y = self.pos[1]
            new_pos = (new_pos_x,new_pos_y)
            self.pos = new_pos
        else:
            self.pos = self.target_pos
        if self.pos[0] < display.l_bound_rect.left:
            self.remove(display)
        self.rect = pg.Rect(self.pos,self.size)
    def remove(self,display):
        display.items.remove(self)

            


class Ball_History_Display:
    item_size = (100,100)
    items_shown = 8
    side_boundry_size = (100,100)
    canvas_size = ((item_size[0] * items_shown) + (side_boundry_size[0] * 2),item_size[1])
    pos_offset = (0,0)   
    def __init__(self):
        self.items = []
        self.pos_offset = (0, 0)
        self.l_bound_rect = pg.Rect( self.pos_offset, self.item_size)
        self.r_bound_rect = pg.Rect( ((self.item_size[0] * (self.items_shown + 2)),self.pos_offset[1]), self.item_size)
        self.bg_rect = pg.Rect(self.pos_offset,self.canvas_size)
        self.in_motion = False
        pg.display.update()


    def add_ball(self,ball):
       self.items.append(History_Item(ball.num,self.r_bound_rect.center,self.item_size))
       for item in self.items:
           new_target_x = item.target_pos[0] - (self.item_size[0])
           new_target_y = item.target_pos[1]
           new_target = (new_target_x,new_target_y)
           item.target_pos = new_target

        
    def draw(self):
        pg.draw.rect(WIN,(32,32,32),self.bg_rect)
        for item in self.items:
            item.move(self)
            item.draw()
        pg.draw.rect(WIN,pg.Color(64,64,64, a=64),self.l_bound_rect)
        pg.draw.rect(WIN,pg.Color(64,64,64, a=64),self.r_bound_rect)

class Game_Events:
    offset = pg.USEREVENT
    def __init__(self):
        self.events = [
            {
                "id":(self.offset + 1),
                "name":"Next Ball",
                "duration":1000,
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

def constrainVal(val,valMin,valMax):
    valRange = valMax - valMin + 1
    if val < valMin:
        while val < valMin:
            val += valRange
    elif val > valMax:
        while val > valMax:
            val -= valRange
    return val 

def wheel(pos):
    wheelMin = 0
    wheelMax = 255
    pos = constrainVal(pos,wheelMin,wheelMax)
    if pos < 85:
        r = int(pos * 3)
        g = int(wheelMax - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(wheelMax - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(wheelMax - pos*3)
    return (r, g, b)
            
def num_to_let(num):
    return GAME.bingo_letters[(num-1) // GAME.col_num_max]
def num_to_color(num):
    return GAME.system_colors[(num-1) // GAME.col_num_max]    

def debug_msg(msg,lvl):
    if DEBUG_LEVEL >= lvl:
        print(msg)

def shuffle_balls(min_num,max_num):
    balls = []
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
    for player in players:
        if player in players:
            for card in player.cards:
                if card.is_shown:
                    card.draw()

    pg.display.update()

def color_from_hsla(h,s,l,a):
    color = pg.Color(0)
    color.hsla = h,s,l,a
    return color

def color_to_hsla(r,g,b,a=255):
    return pg.Color(r,g,b,a).hsla 
    
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
        
