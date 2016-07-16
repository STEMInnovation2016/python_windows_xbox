import pygame, sys
from pygame.locals import *

import sys

import socket

from PyQt4.QtCore import *
from PyQt4.QtGui import *

TCP_IP = '192.168.2.122'
TCP_PORT = 5005
BUFFER_SIZE = 1
A = 0

##GREEN = (0, 255, 0)
##BLACK = (0, 0, 0)
##WHITE = (255, 255, 255)

pygame.init()

#windowSurface = pygame.display.set_mode((800, 600), 0, 32)

### Tells the number of joysticks/error detection
joystick_count = pygame.joystick.get_count()
print ("There is ", joystick_count, "joystick/s")
if joystick_count == 0:
    print ("Error, I did not find any joysticks")
else:
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()

#crosshairs = pygame.image.load("crosshairs.png")
#background = pygame.image.load("shooter/image_library/background.jpg")

##x = 300
##y = 300
##### Creates rectangle
##Rectangle = pygame.Rect( x, y, 100, 100)
##Back = pygame.Rect(0, 0, 800, 600)
x_coord_inverted= 0
y_coord = 0

while True:
    global x_coord_inverted
    global y_coord
    for event in pygame.event.get():
        #print event
        #print event.type
        event_type = event.type
        #print str(event.value)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
##        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
##        s.bind((TCP_IP, TCP_PORT))
##        s.send(str(event.value))
##        s.close()
##        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##        s.connect((TCP_IP, TCP_PORT))
##        s.send(str(event.value))
##        #data = s.recv(BUFFER_SIZE)
##        s.close()
##        
        if event_type == 7:
            event_value = event.value
            event_axis = event.axis
            #print event_value
            if event_axis == 1 or event_axis == 0:
                
                #print "Left Joystick"
                if event_axis == 1:
                    y_coord = int(round(event_value*-100))
                    print "y_coord: "
                    print y_coord
                    #print abs(y_speed)
                    
##                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##                    s.connect((TCP_IP, TCP_PORT))
##                    s.send(str(y_speed))
##                    #data = s.recv(BUFFER_SIZE)
##                    s.close()
##                    
##                    if event_value > 0.8:
##                        y_direction = "Backward"
##                        print y_direction
##                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##                        s.connect((TCP_IP, TCP_PORT))
##                        s.send("s")
##                        #data = s.recv(BUFFER_SIZE)
##                        s.close()
##                         
##                    elif event_value < -0.8:
##                        y_direction = "Forward"
##                        print y_direction
##                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##                        s.connect((TCP_IP, TCP_PORT))
##                        s.send("w")
##                        #data = s.recv(BUFFER_SIZE)
##                        s.close()
##                        
##                    else:
##                        y_direction = "Stop"
##                        
##                        
                elif event_axis == 0:
                    x_coord_inverted = int(round(event_value*-100))
                    

                V = ((100 - abs(x_coord_inverted))*(y_coord/100)) + y_coord
                W = ((100 - abs(y_coord))*(x_coord_inverted/100)) + x_coord_inverted
                R = ((V + W)/2)//3
                L = ((V - W)/2)//3

                
                ##Right now this is making it so back and to the left on the joystick makes the rover go back and to the right
                ## to change this we would have to split off back half of the joystick and swap the directions
                print "R: " + str(R)
                print "L: " + str(L)
                
                message = "R" + str(R) + "L" + str(L)
                print message

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                s.send(message)
                #data = s.recv(BUFFER_SIZE)
                s.close()
                
##                    if event_value > 0.8:
##                        x_direction = "Right"
##                        print x_direction
##                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##                        s.connect((TCP_IP, TCP_PORT))
##                        s.send("d")
##                        #data = s.recv(BUFFER_SIZE)
##                        s.close()
##                    elif event_value < -0.8:
##                        x_direction = "Left"
##                        print x_direction
##                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##                        s.connect((TCP_IP, TCP_PORT))
##                        s.send("a")
##                        #data = s.recv(BUFFER_SIZE)
##                        s.close()
##                    else:
##                        x_direction = "Stop"
##                        
##                if y_direction == "Stop" and x_direction == "Stop":
##                    print "Stop"
##                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##                    s.connect((TCP_IP, TCP_PORT))
##                    s.send(" ")
##                    #data = s.recv(BUFFER_SIZE)
##                    s.close()
##                        
##                    
       

        
##    h_axis_pos = my_joystick.get_axis(0)
##    v_axis_pos = my_joystick.get_axis(1)
##    print (h_axis_pos, v_axis_pos)
##    
##    if x < 0:
##        x = 1
##    elif x > 700:
##        x = 700
##    else:    
##        x = int(x + h_axis_pos * 5)
##
##    if y < 0:
##        y = 0
##    elif y > 500:
##        y = 500
##    else: 
##        y = int(y + v_axis_pos * 5)
##    print ("rectangle left, top", x, y)
##    Rectangle.left = x
##    Rectangle.top = y
##    
##    ###windowSurface.fill(WHITE)
##    
##    #windowSurface.blit(background, Back)
##    
##    #windowSurface.blit(crosshairs, Rectangle)
##        
##    pygame.display.update()
