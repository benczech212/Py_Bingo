import pygame as pg
import math
import random
import time
import os
import tools

WIN_WIDTH = 1280
WIN_HEIGHT = 1024
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

pg.font.init()
pg.display.init()
pg.init()


class Assets:
    default_img_format = "png"
    theme_tropical = [
            pg.Color(210, 191, 29),
            pg.Color(29, 210, 101),
            pg.Color(29, 48, 210),
            pg.Color(210, 29, 138),
            pg.Color(210, 29, 29)
        ]
    theme_easter = [
            pg.Color(29, 210, 150),
            pg.Color(59, 29, 210),
            pg.Color(210, 29, 89),
            pg.Color(180, 210, 29)
        ]
    theme_default = [
            pg.Color('#D21D1D'),
            pg.Color('#D1B31F'),
            pg.Color('#59D11D'),
            pg.Color('#1D95D1'),
            pg.Color('#1D1DD1'),
            pg.Color('#B31DD1'),

        ]
    def __init__(self):
        self.imgs_path = os.path.join(DIR_PATH,"imgs")
        self.img_balls = [pg.image.load(os.path.join(self.imgs_path,"ball_{:>02}.{}".format(x,self.default_img_format))) for x in range(5)]
        self.img_card_deck = pg.image.load(os.path.join(self.imgs_path,"Card Deck.{}".format(self.default_img_format)))
    
    def gen_colors(self, offset):
        colors = []
        for c in range(GAME.col_count):
            hue = offset + (c * (255 / GAME.col_count))
            colors.append(wheel(hue))
        return colors

ASSETS = Assets()
    

class Screen:
    default_width = 1280
    default_height = 1024
    def __init__(self):
        self.width = self.default_width
        self.height = self.default_height
        self.win = pg.display.set_mode((self.width, self.height),pg.RESIZABLE)
SCREEN = Screen()

class Fonts:    
    def __init__(self):
        self.font_names = ["arial","comicsans","calibri","segoe ui"]
        self.all_fonts = []
        self.font_size_count = 10
        self.font_size_step = 10
        for font_name in self.font_names:
            self.all_fonts.append({font_name:[]})
            for i in range(self.font_size_count):
                size = (i + 1) * self.font_size_step
                font_group = tools.filter_list(self.all_fonts,font_name)
                font_group.append(pg.font.SysFont("font_name",size))
                
                
            
        self.cell_font =     self.use_font("arial",      5)
        self.ball_letter =   self.use_font("segoe ui",   2)
        self.ball_num =      self.use_font("calibri",    3)

    

    def use_font(self,name,size):
        try:
            font = tools.filter_list(self.all_fonts,name)
            return font[size]
        except:
            tools.debug_msg("Font Error!",1)


    def show_fonts(self):
        fonts = pg.font.get_fonts()
        print("found {} fonts on the system".format(len(fonts)))
        for font in fonts:
            print(font)
        return fonts
FONTS = Fonts()

class Game:
    
    def __init__(self):
        self.clock = pg.time.Clock()
        self.started_at = self.clock.get_time()
        self.generate_colors = False
        self.players = []
        self.col_num_min = 1
        self.col_num_max = 15
        self.row_count = 5
        self.col_count = 5
        self.col_num_range = self.col_num_max - self.col_num_min + 1
        self.balls = shuffle_balls(self.col_num_min,self.col_num_max * self.col_count )
        self.current_ball_id = 0
        self.bingo_score_val = 100
        self.game_over = False
        self.ball_history_display = Ball_History_Display()
        self.events = Game_Events()
        self.bingo_letters = ["B","I","N","G","O"]
        self.system_colors = Assets.theme_default
        
        if self.generate_colors:
            self.system_colors = Assets.gen_colors()
        
        

        
    

    def add_player(self,player):
        self.players.append(player)
        tools.debug_msg("{} joined the game".format(player.name),1)
    def remove_player(self,player):
        self.players.remove(player)
        tools.debug_msg("{} left the game".format(player.name),1)
    
    def tick():
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()



    def next_ball(self):
        self.current_ball_id += 1
        if self.current_ball_id < len(GAME.balls):
            ball = self.balls[self.current_ball_id]
            self.ball_history_display.add_ball(ball)
        else:
            GAME.game_over = True
            
        for player in GAME.players:
            for card in player.card_deck.cards:
                try:
                    card.tick(ball)
                except:
                    print("Error, fix this")
    def player_bingo(self, player, bingo_count):
        if bingo_count == 1:
            # Single Bingo
            pass
        else:
            # Mult bingo
            pass

        
        score_multiplier = (bingo_count)
        player.score += (self.bingo_score_val * bingo_count) * score_multiplier

class Card_Deck:
    img = ASSETS.img_card_deck
    def __init__(self,player):
        self.player = player
        self.cards = []
        self.size = (1000,800)
        self.pos = (100,300)
        self.rect = pg.Rect(self.pos,self.size)
        self.surf = pg.Surface(self.img.get_size())
        self.card_size = (300,400)
        self.card_margins = (50,50)
        self.card_deck_rect = pg.Rect(self.pos,self.size)
        
    def draw(self):
        SCREEN.win.blit(self.img,self.pos)
        for i, card in enumerate(self.cards):
            card.draw()

    def give_card(self):
        self.cards.append(Card(self.player))
        self.arrange_cards()

    def arrange_cards(self):
        for i, card in enumerate(self.cards):
            x = (self.card_margins[0]//2) + (i * (self.card_size[0] + self.card_margins[0]//2)) + self.pos[0]
            y = (self.card_margins[1]//2) + self.pos[1]
            card.pos = (x,y)
            card.populate_cells()
    

class Player:
    count = 0
    def_card_count = 3
    def __init__(self,name):
        self.name = name
        self.id = self.count
        self.card_deck = Card_Deck(self)
        self.score = 0
        self.bingos = 0
        Player.count+=1

    def give_cards(self,count):
        tools.debug_msg("Giving card to {}".format(self.name),1)
        for i in range(count):
            self.card_deck.give_card()


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
        tools.debug_msg("Ball Picked: {}".format(self.num),1)


class Cell:
    def __init__(self, card, pos, num, unit_pos, bg_color, is_clickable):
        self.card = card
        pos_x = self.card.pos[0] + (unit_pos[0] * card.cell_size[0])
        pos_y = self.card.pos[1] + (unit_pos[1] * card.cell_size[1])
        self.pos = (pos_x,pos_y)
        self.unit_pos = unit_pos
        self.size = self.card.cell_size
        self.num = num
        self.is_daubed = False
        self.near_bingo = False
        self.rect = pg.Rect(self.pos,self.size)
        self.bg_color_default = pg.Color(bg_color[0],bg_color[1],bg_color[2])
        self.bg_color = self.bg_color_default
        self.bg_color_active = pg.Color(64,64,64)
        self.bg_color_daubed = pg.Color(0,0,255)
        self.bg_color_near_bingo = pg.Color(96,96,96)
        self.border_color = (0,0,0)
        self.text_color = (0,0,0)
        self.text_assist_color = (255,0,0)
        self.text_daubed_color = (255,0,0)
        self.is_clickable = is_clickable
        self.is_active = False
        
    
    def on_click(self,event):
        if GAME.current_ball_id > 0:
            balls_called = GAME.balls[0:GAME.current_ball_id]
            for ball in balls_called:
                if ball.num == self.num:
                    self.daub()

    def daub(self):
        self.is_daubed = True
        tools.debug_msg("{} is now daubbed".format(self.num))

        
    def draw(self,card_rect):
        self.is_active = tools.check_mouseover(self.rect)
        
        if self.is_daubed:       
            bg_color = self.bg_color_daubed
            text = ""
        else:
            text = "{:^}".format(self.num)
            #if self.is_clickable:
            if self.near_bingo: bg_color = self.bg_color_near_bingo
            elif self.is_active: bg_color = self.bg_color_active
            else: bg_color = self.bg_color
            


        

        
        # BG
        
        pg.draw.rect(SCREEN.win,bg_color,self.rect, 0)

        #Border
        pg.draw.rect(SCREEN.win,self.border_color,self.rect, 1)

        text_label = FONTS.cell_font.render(text,1,self.text_color)
        text_label_pos = text_label.get_rect(center=(self.rect.center))
        SCREEN.win.blit(text_label,text_label_pos)
    
class Card:
    count = 0
    def __init__(self,player):
        self.player = player
        self.pos = (0,0)
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
        #self.populate_cells()
        self.assist_mode = False
        self.auto_daub_mode = True
        self.id = self.count
        self.bingo = False
        self.is_shown = True
        self.text_color = (0,0,0)
        self.assist_text_color = (255,0,0)
        self.border_color = pg.Color(0,0,0)
        self.rect = pg.Rect(self.pos,self.card_size)
        Card.count +=1
    
        
    def draw(self):
        
        for cell in self.header_cells:
            cell.draw(pg.Rect(self.pos,self.card_size))
        for cell in self.cells:
            cell.draw(pg.Rect(self.pos,self.card_size))
        

    def populate_cells(self):
        # header row
        self.cells = []
        for x in range(self.unit_width):
            cell_pos_x = self.pos[0] + (x * self.cell_size[0])                
            cell_pos_y = self.pos[1]
            cell_pos = (cell_pos_x, cell_pos_y)
            num = GAME.bingo_letters[x]
            unit_pos = (x,-1)
            bg_color = GAME.system_colors[x]
            self.header_cells.append(Cell(self,cell_pos,num,unit_pos,bg_color,False))
        # cells
        for x in range(self.unit_width):
            for y in range(self.unit_height):
                cell_pos_x = self.pos[0] + (x * self.cell_size[0])                
                cell_pos_y = self.pos[1] + self.header_row_size[1] + (y * self.cell_size[1])
                cell_pos = (cell_pos_x, cell_pos_y)
                num = self.nums[x][y]
                unit_pos = (x,y)
                bg_color = (128,128,128)
                self.cells.append(Cell(self,cell_pos,num,unit_pos,bg_color,True))       

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
        if self.auto_daub_mode:
            cell = self.cell_by_num(ball.num)
            if cell != None:
                if not cell.is_daubed:
                    cell.is_daubed = True
        self.check_bingo()

    def tick(self, ball):
        self.auto_daub(ball)
        if self.is_shown:
            self.draw()
        
        #self.assist_mode()
    
    



    def check_bingo(self):
        daubs = self.get_daubs()
        bingo_count = 0
        width = self.unit_width
        height = self.unit_height
        checks = [[],[]]
        x_min = 0
        x_mid = int(width/2)
        x_max = width-1
        y_min = 0
        y_mid = int(height/2)
        y_max = height-1

        # row or colunm bingo
        for x in range(width):
            for y in range(height):
                checks[0].append(daubs[x][y])
                checks[1].append(daubs[y][x])
            for check in checks:
                if all(check):
                    bingo_count += 1
                elif check.count(False) == 1:
                    cell = None
                    if check == checks[0]:
                        cell = self.cell_by_unitpos((x,y)) 
                    elif check == checks[1]:
                        cell = self.cell_by_unitpos((y,x))
                    if cell != None:
                        cell.near_bingo = True
                    
                    
                #elif check.count(True) > 3:
                    #x = check.index(False)
                    #cell = self.cell_by_unitpos[x,y]
                    #cell.near_bingo = True                  
            checks = [[],[]]

        # corners and center
        if daubs[x_min][y_min] and daubs[x_min][y_max] and daubs[x_max][y_min] and daubs[x_max][y_max] and daubs[x_mid][y_mid]:
            bingo_count += 1

        # diagonal 
        for i in range(width):
            j = (width-1)-i
            checks[0].append(daubs[i][i]) # Normal Diagonal   (0,0), (1,1), (2,2), (3,3), (4,4)
            checks[1].append(daubs[i][j]) # Inverted Daigonal (0,4), (1,3), (2,2), (3,1), (4,0)
        for check in checks:
            if all(check):
                bingo_count += 1
        checks = [[],[]]
        if bingo_count > 0:
            GAME.player_bingo(self.player,bingo_count)


                   
         
                

    def cell_by_unitpos(self,unit_pos):
        for cell in self.cells:
            if cell.unit_pos == unit_pos:
                return cell
    def cell_by_num(self,num):
        for cell in self.cells:
            if cell.num == num:
                return cell

    def cells_by_isdaubbed(self):    
        cells = [cell for cell in self.cells if cell.is_daubed]
        return cells

    def get_daubs(self):
        daubs = [[False for y in range(self.unit_height)] for x in range(self.unit_width)]
        for cell in self.cells:
            daubs[cell.unit_pos[0]][cell.unit_pos[1]] = cell.is_daubed
        return daubs
            
            

class History_Item:
    base_imgs = ASSETS.img_balls
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
        #pg.draw.circle(SCREEN.win, num_to_color(self.num),self.pos,self.radius)
        img_pos = (self.rect.center[0] - self.base_imgs[0].get_size()[0],self.rect.center[1] - self.base_imgs[0].get_size()[1])
        img = ASSETS.img_balls[num_to_col(self.num)]
        SCREEN.win.blit(img,img_pos)

        text_color = (0,0,0)
        text_offset = (-20,-20)
        line_spacing = 10
        text_letter = "{:^}".format(num_to_let(self.num))
        text_letter_label = FONTS.ball_letter.render(text_letter,1,text_color)
        text_letter_pos = text_letter_label.get_rect(center=(self.pos[0],self.pos[1] - line_spacing))
        SCREEN.win.blit(text_letter_label,text_letter_pos)

        text_num = "{:^}".format(self.num)
        text_num_label = FONTS.ball_num.render(text_num,1,text_color)
        text_num_pos = text_num_label.get_rect(center=(self.pos[0],self.pos[1] + line_spacing))
        SCREEN.win.blit(text_num_label,text_num_pos)

        

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
    canvas_size = (SCREEN.win.get_width(),item_size[1])
    pos_offset = (0,0)   
    def __init__(self):
        self.items = []
        self.pos_offset = (0, 0)
        self.l_bound_rect = pg.Rect( self.pos_offset, self.item_size)
        self.r_bound_rect = pg.Rect((self.canvas_size[0] - self.item_size[0] + self.pos_offset[0],self.pos_offset[1]),self.item_size)
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
        pg.draw.rect(SCREEN.win,(32,32,32),self.bg_rect)
        for item in self.items:
            item.move(self)
            item.draw()
        pg.draw.rect(SCREEN.win,pg.Color(64,64,64, a=64),self.l_bound_rect)
        pg.draw.rect(SCREEN.win,pg.Color(64,64,64, a=64),self.r_bound_rect)

class Game_Events:
    offset = pg.USEREVENT
    def __init__(self):
        self.event_timers = [
            {
                "id":(self.offset + 1),
                "name":"Next Ball",
                "duration":1000,
            },
            {
                "id":(self.offset + 2),
                "name":"Mouse",
                "duration":10000
            }
        ]
        self.set_timers()

    def set_timers(self):
        for event in self.event_timers:
            pg.time.set_timer(event['id'],event['duration'])

    def check_events(self):
        done = False
        debug_enabled = True
        events = pg.event.get()
        for event in events:
            if debug_enabled:
                tools.debug_msg("Event {} - {} Called!".format(event.type,pg.event.event_name(event.type)),1)
            if event.type == pg.QUIT: # If user clicked close
                GAME_OVER=True
            if event.type == self.event_timers[0]['id']:
                #timer #1 
                GAME.next_ball()
            if pg.event.event_name(event.type) == "MouseButtonDown":
                self.on_mouseclick(event)

    def on_mouseclick(self,event):
        tools.debug_msg("on_mouseclick Called",2)
        for player in GAME.players:
            for card in player.cards:
                if card.is_shown:
                    for cell in card.cells:
                        if tools.check_mouseover(cell.rect):
                            cell.on_click(event)
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
    return GAME.bingo_letters[num_to_col(num)]
def num_to_color(num):
    return GAME.system_colors[num_to_col(num)]    
def num_to_col(num):
    return (num-1) // GAME.col_num_max

def shuffle_balls(min_num,max_num):
    balls = []
    rounds = 1
    for round_num in range(rounds):
        for ball_num in range(100):
            ball_nums = random.sample(range(min_num,max_num+1),max_num)
        for num in ball_nums:
            balls.append(Ball(num))
    return balls
 


def draw_stuff():
    SCREEN.win.fill((255,255,255))
    players = GAME.players
    GAME.ball_history_display.draw()
    for player in players:
        if player in players:
            player.card_deck.draw()
            for card in player.card_deck.cards:
                if card.is_shown:
                    card.draw()

    pg.display.update()

def game_loop():
    GAME.events.check_events()
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
        
