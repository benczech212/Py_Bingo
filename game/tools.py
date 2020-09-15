import pygame as pg
def check_mouseover(rect):
    mos_x, mos_y = pg.mouse.get_pos()
    if mos_x > rect.left and mos_x < rect.right and mos_y > rect.top and mos_y < rect.bottom:
        return True
    else:
        return False

def debug_msg(msg,lvl,global_lvl):
    if global_lvl >= lvl:
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
        