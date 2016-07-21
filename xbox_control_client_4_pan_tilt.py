## 7/19/16
## Bennett Doherty
## Pan tilt using the Adafruit Servo PWM Hat and xbox controller
import time
import roboclaw

import socket
from socket import error as SocketError
import errno

import pigpio

from Adafruit_PWM_Servo_Driver import PWM


#Windows comport name
#roboclaw.Open("COM3",115200)
#Linux comport name
roboclaw.Open("/dev/ttyACM0",115200)

address = 0x80
overall_speed = 10
direction1 = ""
direction2 = ""


pi = pigpio.pi()
top_servo = 17
mid_servo = 5
btm_servo = 6
mid_pos = 2150
btm_pos = 500
top_pos = 1200
pi.set_servo_pulsewidth(top_servo, top_pos)
pi.set_servo_pulsewidth(mid_servo, mid_pos)
pi.set_servo_pulsewidth(btm_servo, btm_pos)

pi.set_mode(22, pigpio.OUTPUT) #light

pwm = PWM(0x40)     ## Initialize I2C

pwm.setPWMFreq(50)      ## set the frequency to 50 Hz

tilt_pos = 300
pan_pos = 350
pwm.setPWM(0, 0, tilt_pos)
pwm.setPWM(1, 0, pan_pos)

TCP_IP = '192.168.2.122'
TCP_PORT = 5005
BUFFER_SIZE = 1  # Normally 1024, but we want fast response


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## Allows addres to be reused and avoids 'Address already in use error'
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
message = ""


def forward(motor, speed):
    if motor == 1:
        roboclaw.ForwardM1(address, speed)
        global direction1
        direction1 = "forward"

    else:
        roboclaw.ForwardM2(address, speed)
        global direction2
        direction2 = "forward"

def reverse(motor, speed):
    if motor == 1:
        roboclaw.BackwardM1(address, speed)
        global direction1
        direction1 = "reverse"
    else:
        roboclaw.BackwardM2(address, speed)
        global direction2
        direction2 = "reverse"

def stop(motor):
    if motor == 1:
        roboclaw.ForwardM1(address, 0)
        global direction1
        direction1 = "stop"
    else:
        roboclaw.ForwardM2(address, 0)
        global direction2
        direction2 = "stop"
    
def turn_left(speed):
    roboclaw.ForwardM1(address, speed)
    global direction1
    direction1 = "forward"
    roboclaw.BackwardM2(address, speed)
    global direction2
    direction2 = "reverse"

def turn_right(speed):
    roboclaw.BackwardM1(address, speed)
    global direction1
    direcetion1 = "reverse"
    roboclaw.ForwardM2(address, speed)
    global direction2
    direction2 = "forward"

def change_speed(change):
    global overall_speed
    if change == "q":
        overall_speed += 5
        print("Go faster")
    elif change == "e":
        overall_speed -= 5
        print("Go slower")
    else:
         overall_speed = change
         
    print"Speed: " 
    print overall_speed
    global direction1
    global direction2

    if direction1 == "forward":
        forward(1, overall_speed)
    elif direction1 == "reverse":
        reverse(1, overall_speed)
    if direction1 == "stop":
        stop(1)

    if direction2 == "forward":
        forward(2, overall_speed)
    elif direction2 == "reverse":
        reverse(2, overall_speed)
    elif direction2 == "stop":
        stop(2)
temp = "hello"
print temp.find("o")


while(1):

    conn, addr = s.accept()
    while(1):
        global message
        try:
            data = conn.recv(10)
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise # Not error we are looking for
            pass # Handle error here.
        if not data: break
        #print "data: "
        #print data
        if data != "filler":
            message = data
        
        index_L = data.find("L")
        if index_L != -1:
            print index_L
            right_speed_str = data[1:index_L]
            print right_speed_str
            left_speed_str = data[index_L + 1:]
            print left_speed_str

            right_speed_int = int(right_speed_str)
            left_speed_int = int(left_speed_str)

            if right_speed_int > 10:
                forward(1, right_speed_int)
            elif right_speed_int < -15:
                reverse(1, abs(right_speed_int))
            else:
                stop(1)
                
            if left_speed_int > 10:
                forward(2, left_speed_int)
            elif left_speed_int < -10:
                reverse(2, abs(left_speed_int))
            else:
                stop(2)            
        global tilt_pos
        global pan_pos

        if message == "up":
            if tilt_pos < 460:          ## Limit up position
                tilt_pos += 3 
        if message == "down":
            if tilt_pos > 270:          ## Limit down position
                tilt_pos -= 3
        elif message == "left":         
            if pan_pos > 224:           ## Limit up position
                pan_pos -= 3
        elif message == "right":        
            if pan_pos < 464:           ## Limit left position
                pan_pos += 3
##        elif message == "stop":
##            print "stop"
        #else:
            #print "Entry not recognized. Try Again"
        pwm.setPWM(0, 0, tilt_pos)
        pwm.setPWM(1, 0, pan_pos)
        print "tilt_pos: %d" % tilt_pos
        print "pan_pos: %d" % pan_pos

conn.close()       
    

