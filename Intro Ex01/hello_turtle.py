#################################################
# FILE: hello_turtle.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex1 2015-2016
# DESCRIPTION: draws a 3 flowers
#################################################

import turtle

def draw_petal():
    '''
    draws a petal by drawing lines in different directions
    '''
    turtle.forward(30)
    turtle.left(45)
    turtle.forward(30)
    turtle.left(135)
    turtle.forward(30)
    turtle.left(45)
    turtle.forward(30)
    turtle.left(135)



def draw_flower():
    '''
    draws a flower by drawing petals in different angles
    '''
    turtle.right(45)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(135)
    turtle.forward(150)


def draw_flower_advanced():
    '''
    draws a flower and moves cursor to allow additional flowers to be drawn further along
    '''
    draw_flower()
    turtle.left(90)
    turtle.up()
    turtle.forward(150)
    turtle.left(90)
    turtle.forward(150)
    turtle.right(90)
    turtle.down()


def draw_flower_bed():

    '''
    draws 3 flowers using draw_flower_advanced function
    '''
    turtle.up()
    turtle.left(180)
    turtle.forward(200)
    turtle.right(180)
    turtle.down()
    draw_flower_advanced()
    draw_flower_advanced()
    draw_flower_advanced()
    turtle.done()

