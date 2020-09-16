DEBUG_LEVEL = 2



import pygame as pg
def check_mouseover(rect):
    mos_x, mos_y = pg.mouse.get_pos()
    if mos_x > rect.left and mos_x < rect.right and mos_y > rect.top and mos_y < rect.bottom:
        return True
    else:
        return False

def debug_msg(msg,lvl):
    if DEBUG_LEVEL >= lvl:
        print(msg)

def filter_list(targets,search):
    for target in targets:
        for target_name in target:
            if target_name == search:
                return target[search]
def adjust_hsla(in_color,hsla_delta):
        in_color = list(in_color)
        hsla_delta = list(hsla_delta)
        out_color = []
        min_num = 0
        max_num = 100
        for i in range(len(in_color)):
            out = in_color[i] + hsla_delta[i]
            if out > max_num:
                out = max_num
            elif out < min_num:
                out = min_num
            out_color.append(out)
        return tuple(out_color)
        
    
def color_from_hsla(h,s,l,a):
    color = pg.Color(0)
    color.hsla = h,s,l,a
    return color

def color_to_hsla(r,g,b,a=255):
    return pg.Color(r,g,b,a).hsla 
    