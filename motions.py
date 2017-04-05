from key_press import *
import random
from datetime import datetime

def close_app():
    stop()
    time.sleep(1)
    key_down('command')
    key_down('option')
    key_down('shift')
    key_down('esc')
    time.sleep(2)
    key_up('command')
    key_up('option')
    key_up('shift')
    key_up('esc')
    print 'App closed at ' + str(datetime.now())


def quit_game():
    stop()
    time.sleep(1)
    key_press('esc')
    time.sleep(.1)
    key_press('up')
    time.sleep(.1)
    key_press('\n')
    time.sleep(3)


def say(line):
    stop()
    time.sleep(2)
    key_press('\n')
    for c in line:
        key_press(c)
    key_press('\n')
    key_press('\n')
    time.sleep(.5)


def boost():
    time.sleep(.05)
    slow_key_press('`')
    time.sleep(.6)


def hyper():
    time.sleep(.05)
    slow_key_press('s')
    time.sleep(.3)


def stance():
    time.sleep(.3)
    slow_key_press('end')
    time.sleep(.3)


def behold():
    time.sleep(.5)
    slow_key_press('f')
    time.sleep(.3)


def speed_pot():
    time.sleep(.03)
    slow_key_press('9')
    time.sleep(.03)


def att_pot():
    time.sleep(.03)
    slow_key_press('8')
    time.sleep(.03)


def acc_pot():
    time.sleep(.03)
    slow_key_press('7')
    time.sleep(.03)


def feed():
    time.sleep(.03)
    slow_key_press('0')
    time.sleep(.03)


def jump():
    key_press('command')


def long_jump():
    key_down('command')
    time.sleep(.05)
    key_up('command')


def turn_left():
    slow_key_press('left')


def turn_right():
    slow_key_press('right')


def move_left(length=None):
    if length is None:
        key_down('left')
    else:
        key_down('left')
        time.sleep(length)
        key_up('left')


def move_right(length=None):
    if length is None:
        key_down('right')
    else:
        key_down('right')
        time.sleep(length)
        key_up('right')


def climb():
    key_down('up')


def stop_climb():
    key_up('up')


def stop():
    key_up('left')
    key_up('right')
    key_up('up')
    key_up('down')


def att():
    key_press('a')
    time.sleep(.68)


def att2():
    key_press('shift')
    time.sleep(.68)


def rev_att_left():
    turn_left()
    time.sleep(.1)
    att()
    turn_right()


def rev_att_right():
    turn_right()
    time.sleep(.1)
    att()
    turn_left()


def jump_att():
    jump()
    time.sleep(.1)
    att()


def jump_att2():
    jump()
    time.sleep(.06)
    att2()


def rev_jump_att_left():
    jump()
    rand = .05 + random.random() * .03
    time.sleep(rand)
    turn_left()
    rand = .05 + random.random() * .03
    time.sleep(rand)
    att()


def rev_jump_att_right():
    jump()
    rand = .05 + random.random() * .03
    time.sleep(rand)
    turn_right()
    rand = .05 + random.random() * .03
    time.sleep(rand)
    att()
