from gpiozero import Servo
from gpiozero import AngularServo
import time, sys
import RPi.GPIO as GPIO
from time import sleep
import pigpio
import asyncio
import threading

#Variable 
def set_angle_h(i):
    print(i)
    pulse= (100/9)*i+500
    pwm.set_servo_pulsewidth(s_1,pulse)
    sleep(0.1)

def set_angle_v(i):
    print(i)
    pulse= (100/9)*i+500
    pwm.set_servo_pulsewidth(s_2,pulse)
    sleep(0.1)
    
def rc_time(pin_to_circuit):
    count = 0
    GPIO.setup(pin_to_circuit,GPIO.OUT)
    GPIO.output(pin_to_circuit,GPIO.LOW)
    time.sleep(0.1)
    #count the pin back            self = super(GPIOMeta, cls).__call__(*args, **kwargs) to input
    GPIO.setup(pin_to_circuit,GPIO.IN)
    #count until pin goes high
    while(GPIO.input(pin_to_circuit)==GPIO.LOW):
        count+=1
    #print(count)
    return count





def rc_time_1():
    pin_to_circuit = 33
    count = 0
    global ldr_1_low
    GPIO.setup(pin_to_circuit,GPIO.OUT)
    GPIO.output(pin_to_circuit,GPIO.LOW)
    time.sleep(0.1)
    #count the pin back            self = super(GPIOMeta, cls).__call__(*args, **kwargs) to input
    GPIO.setup(pin_to_circuit,GPIO.IN)
    #count until pin goes high
    while(GPIO.input(pin_to_circuit)==GPIO.LOW):
        ldr_1_low = True
        count+=1
    #print(count)
    ldr_1_low = False
    return count
    #calc_angle()

def rc_time_2():
    pin_to_circuit = 37
    count = 0
    global ldr_2_low
    GPIO.setup(pin_to_circuit,GPIO.OUT)
    GPIO.output(pin_to_circuit,GPIO.LOW)
    time.sleep(0.1)
    #count the pin back            self = super(GPIOMeta, cls).__call__(*args, **kwargs) to input
    GPIO.setup(pin_to_circuit,GPIO.IN)
    #count until pin goes high
    while(GPIO.input(pin_to_circuit)==GPIO.LOW):
        ldr_2_low = True
        count+=1
    #print(count)
    ldr_2_low = False    
    return count
    #li_2 = count    

def rc_time_3():
    pin_to_circuit = 31
    count = 0
    global ldr_3_low
    GPIO.setup(pin_to_circuit,GPIO.OUT)
    GPIO.output(pin_to_circuit,GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin_to_circuit,GPIO.IN)
    #count until pin goes high
    while(GPIO.input(pin_to_circuit)==GPIO.LOW):
        ldr_3_low = True
        count+=1
    #print(count)
    ldr_3_low = False        
    return count
    #li_3 = count


def rc_time_4():
    pin_to_circuit = 35
    count = 0
    global ldr_4_low
    GPIO.setup(pin_to_circuit,GPIO.OUT)
    GPIO.output(pin_to_circuit,GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin_to_circuit,GPIO.IN)
    while(GPIO.input(pin_to_circuit)==GPIO.LOW):
        ldr_4_low = True
        count+=1
    #print(count)
    ldr_4_low = False
    return count
    #li_4 = count    

def get_reading_1():
    while True:
        global li_1
        li_1 = rc_time_1()
        #print('pin_1',li_1)
    
def get_reading_2():
    while True:
        global li_2
        li_2 = rc_time_2()
        #print('pin_2',li_2)
        
def get_reading_3():
    while True:
        global li_3
        li_3 = rc_time_3()
        #print('pin_3',li_3)
        
def get_reading_4():
    while True:
        global li_4
        li_4 = rc_time_4()
        #print('pin_4',li_1,li_3)
    
def calc_angle():
    while True:
        #print('in calc angle')
        #print('li_1,li_2,li_3,li_4',li_1,li_2,li_3,li_4)
        dtime=0
        tol=50
        avt=(li_1+(li_2))/2 #top
        avd=(li_3+li_4)/2 #bottom
        avr=(li_1+li_3)/2 #right
        avl=((li_2)+li_4)/2 #left/4
        totalavg = (li_1 + li_2 + li_3 + li_4)/4
        dvert=avt-avd #difference btet_angle_vw up n down
        dhoriz=avl-avr
        #print('avl,avr',avl,avr)
        #print('avt,avd',avt,avd)
        #print('totalavg',totalavg)
        if((-1*tol>dvert or dvert>tol)):
            #print('avt,avd',avt,avd)
            if(avt>avd):
                if(avd < 9000):         
                    curr_v = pwm.get_servo_pulsewidth(s_2)
                    
                    ang = (curr_v - 500)/(100/9)
                    ang = ang + 2
                    #print('angled',ang)
                    set_angle_v(ang)

            elif(avt<avd):
                if(avt < 7000):
                    curr_v = pwm.get_servo_pulsewidth(s_2)
                    ang = (curr_v - 500)/(100/9)
                    ang = ang - 2
                    #print('angle2',ang)
                    set_angle_v(ang)
#         #print('avl,avr',avl,avr)
        if(-1*tol>dhoriz or dhoriz>tol):
            #print('checking angle')
            if(avl>avr):
                if(avr < 9000):
                    curr_h = pwm.get_servo_pulsewidth(s_1)
                    ang = (curr_h - 500)/(100/9)
                    ang = ang + 2
                    if(ang < 180):
                        set_angle_h(ang)
                else:
                    curr_h = pwm.get_servo_pulsewidth(s_1)
                    ang = (curr_h - 500)/(100/9)
                    if (ang < 88):
                        for i in range(int(ang),90,1):
                            avgl = (li_2 + li_4)/2
                            if(avgl > 9000):
                                print('avgl',avgl)
                                set_angle_h(i)
                            else:
                                break
                    else:
                        for i in range(int(ang),89,-1):             
                            avgr = (li_1 + li_3)/2
                            if(avgr > 9000):
                                print('avgr',avgr)
                                set_angle_h(i)
                            else:
                                break


            elif(avl< avr):
                print('in opposite')
                if(avl < 9000):
                    curr_h = pwm.get_servo_pulsewidth(s_1)
                    
                    ang = (curr_h - 500)/(100/9)
                    ang = ang - 2
                    if (ang > 0):
                        set_angle_h(ang)
                    print('anglel',ang)


li_1 = 0
li_2 = 0
li_3 = 0
li_4 = 0

ldr_1_low = True
ldr_2_low = True
ldr_3_low = True
ldr_4_low = True
#hORIZTONAL 
s_1= 4
#VERTICAL
s_2 = 17

pwm=pigpio.pi()
pwm.set_mode(s_1,pigpio.OUTPUT)
pwm.set_PWM_frequency(s_1, 50)# try:
pwm.set_mode(s_2,pigpio.OUTPUT)
pwm.set_PWM_frequency(s_2, 50)

#ldr
GPIO.setmode(GPIO.BOARD)

ldr_1=31#tr
ldr_2=37#tl
ldr_3=33#br
ldr_4=35#bl




light_intensity_1 = 0
light_intensity_2 = 0
light_intensity_1 = 0
light_intensity_2 = 0
set_angle_h(90)
set_angle_v(90)


try:
    th1 = threading.Thread(target=get_reading_1)
    th2 = threading.Thread(target=get_reading_2)
    th3 = threading.Thread(target=get_reading_3)
    th4 = threading.Thread(target=get_reading_4)
    th5 = threading.Thread(target=calc_angle)
    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th1.join()
    th2.join()
    th3.join()
    th4.join()
    th5.join()



finally:
    GPIO.cleanup()
       



