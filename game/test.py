import pygame as pg
import matplotlib.pyplot as plt
import math
import random
import time
import os
import tools

expected_vals = [0,1,2,3,4,4,3,2,1,0]

def constrain_val(in_val,val_min,val_max,method):    
    if in_val > val_min and in_val < val_max:  # Value is within the boundries, do nothing
        return in_val

    val = in_val
    out_val = 0
    if val_min != 0:                        # if min bound is not 0
        offset = val_min                    #   define how far min_val is from 0, called 'offset'
    else:                                   #
        offset = 0                          #   
    val -= offset                           #  move everything down by offset
    val_min -= offset                       #
    val_max -= offset                       #
    val_range = (val_max-val_min) + 1       #   range should be one more than the max - min


    if method == "clamp":
        # Clamp method - Clamps the returned number at the boundry
        #    min_val if below boundry
        #    max_val if above boundry
        if val < min_val:
            out_val = min_val
        else:
            out_val = max_val


    if method == "zigzag":
        val %= (val_range * 2)
        in_1n_range = (val >= val_min) and (val <= val_max)
        val = val if in_1n_range else val-1
        out_val = val_max - abs(val_max - val - 1)
    if method == "overflow":
        out_val = val % (val_max + 1)
    test = 0

    return out_val


test_range_min = 0
test_range_max = 100
min_bound = 0
max_bound = 4
method = "zigzag"
print("Testing {} method with bounds {} to {} from inputs {} to {}".format(method,min_bound,max_bound,test_range_min,test_range_max))
for i in range(test_range_min,test_range_max):
    
    n = constrain_val(i,min_bound,max_bound,method)
    is_test_passed = False
    if n == expected_vals[i % (len(expected_vals)-1)]:
        is_test_passed = True
    print("{} - [{}] = {}".format(is_test_passed,i,n))




