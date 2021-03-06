# Bruce Maxwell
# Fall 2015
# CS 151S Project 9
#
# ball class test
#
# modified slightly by Eric Aaron for CS 152, Spring '19
# slightly updated by Bruce Maxwell for CS 152, Fall 2019
#     simplified the constructor call to just the win variable
# updated by Bruce Maxwell for CS 152, Spring 2019
#     changed signatures of Ball constructors and set functions

import graphicsPlus as gr
import physics_objects as pho
import collision as coll
import time

# create two balls heading towards one another
def main():
    win = gr.GraphWin( 'balls colliding', 500, 500, False )

    ball1 = pho.Ball( win, 20 )
    ball2 = pho.Ball( win, 20 )
    ball1.setPosition( [200, 200] )
    ball2.setPosition( [300, 200] )

    # set up velocity and acceleration so they collide
    ball1.setVelocity( [200, 200] )
    ball2.setVelocity( [-200, 200] )
    ball1.setAcceleration( [0, -200] )
    ball2.setAcceleration( [0, -200] )
    ball1.draw()
    ball2.draw()

    txt = gr.Text( gr.Point( 250, 50), "Click to continue" )
    txt.setSize( 16 )
    txt.draw(win)
    win.getMouse()

    # loop for some time and check for collisions
    dt = 0.01
    for frame in range(120):
        if not coll.collision_ball_ball( ball1, ball2, dt ):
            ball1.update(dt)
        else:
            txt.setText( "Boom!" )

        if not coll.collision_ball_ball( ball2, ball1, dt ):
            ball2.update(dt)
        
        win.update()
        time.sleep(0.5*dt)
        if win.checkMouse() != None:
            break

    txt.setText('Click to quit')
    win.getMouse()

    txt.setText('See ya')
    win.update()
    time.sleep(0.2)
    
    win.close()
    

if __name__ == "__main__":
    main()                       