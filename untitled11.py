# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:07:48 2023

@author: maana
"""

import turtle

def draw_checkered_pattern():
    square_size = 50
    num_squares = 8
    colors = ["black", "white"]

    turtle.speed(0)
    turtle.penup()

    for row in range(num_squares):
        for col in range(num_squares):
            color_index = (row + col) % len(colors)
            turtle.goto(col * square_size, row * square_size)
            turtle.pendown()
            turtle.fillcolor(colors[color_index])
            turtle.begin_fill()
            for _ in range(4):
                turtle.forward(square_size)
                turtle.right(90)
            turtle.end_fill()
            turtle.penup()

    turtle.done()

draw_checkered_pattern()