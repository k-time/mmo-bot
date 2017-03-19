from key_press import *
import random
from datetime import datetime


def close_app():
    stop()
    time.sleep(1)
    KeyDown('command')
    KeyDown('option')
    KeyDown('shift')
    KeyDown('esc')
    time.sleep(2)
    KeyUp('command')
    KeyUp('option')
    KeyUp('shift')
    KeyUp('esc')
    print 'App closed at ' + str(datetime.now())


def quit_game():
    stop()
    time.sleep(1)
    KeyPress('esc')
    time.sleep(.1)
    KeyPress('up')
    time.sleep(.1)
    KeyPress('\n')
    time.sleep(3)


def say(line):
    stop()
    time.sleep(2)
    KeyPress('\n')
    for c in line:
        KeyPress(c)
    KeyPress('\n')
    KeyPress('\n')
    time.sleep(.5)


def boost():
    time.sleep(.05)
    SlowKeyPress('`')
    time.sleep(.6)


def hyper():
    time.sleep(.05)
    SlowKeyPress('s')
    time.sleep(.3)


def stance():
    time.sleep(.3)
    SlowKeyPress('end')
    time.sleep(.3)


def behold():
    time.sleep(.5)
    SlowKeyPress('f')
    time.sleep(.3)


def speed_pot():
    time.sleep(.03)
    SlowKeyPress('9')
    time.sleep(.03)


def att_pot():
    time.sleep(.03)
    SlowKeyPress('8')
    time.sleep(.03)


def acc_pot():
    time.sleep(.03)
    SlowKeyPress('7')
    time.sleep(.03)


def feed():
    time.sleep(.03)
    SlowKeyPress('0')
    time.sleep(.03)


def jump():
    KeyPress('command')


def long_jump():
    KeyDown('command')
    time.sleep(.05)
    KeyUp('command')


def turn_left():
    SlowKeyPress('left')


def turn_right():
    SlowKeyPress('right')


def move_left(length=None):
    if length is None:
        KeyDown('left')
    else:
        KeyDown('left')
        time.sleep(length)
        KeyUp('left')


def move_right(length=None):
    if length is None:
        KeyDown('right')
    else:
        KeyDown('right')
        time.sleep(length)
        KeyUp('right')


def climb():
    KeyDown('up')


def stop_climb():
    KeyUp('up')


def stop():
    KeyUp('left')
    KeyUp('right')
    KeyUp('up')
    KeyUp('down')


def att():
    KeyPress('a')
    time.sleep(.68)


def att2():
    KeyPress('shift')
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
