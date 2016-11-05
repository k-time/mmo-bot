from PIL import Image
from PIL import ImageGrab
from motions import *

im = None
pixels = None
width, height = 0, 0
x2 = 0
direction = 'right'


# Locate monsters around you
def monsters_around(x_min_range, x_max_range, y_min, y_max):
    global x2, direction

    if direction == 'left':
        left_bound = x2-x_max_range
        right_bound = x2-x_min_range
        if left_bound > 0 and right_bound < width:
            for i in range(left_bound, right_bound):
                for j in range(y_min, y_max):
                    rgba=pixels[i,j]
                    # Find monster1 or monster2 or monster3
                    if rgba[0] == 153 and rgba[1] == 136 and rgba[2] == 119 \
                    or rgba[0] == 221 and rgba[1] == 102 and rgba[2] == 0 \
                    or rgba[0] == 153 and rgba[1] == 102 and rgba[2] == 51:
                        return True

    elif direction == 'right':
        left_bound = x2+x_min_range
        right_bound = x2+x_max_range
        if left_bound > 0 and right_bound < width:
            for i in range(left_bound, right_bound):
                for j in range(y_min, y_max):
                    rgba=pixels[i,j]
                    # Find monster1 or monster2 or monster3
                    #if rgba[0] == 153 and rgba[1] == 136 and rgba[2] == 119 \
                    #or rgba[0] == 221 and rgba[1] == 102 and rgba[2] == 0 \
                    if rgba[0] == 51 and rgba[1] == 51 and rgba[2] == 34:
                        print i,j
                        return True

    return False


def say(line):
    stop()
    time.sleep(2)
    KeyPress('\n')
    for c in line:
        KeyPress(c)
    KeyPress('\n')
    KeyPress('\n')
    time.sleep(.5)


def check_chat():
    for i in range(13,27):
        for j in range(1047,1150):
            rgba = pixels[i,j]
            # There is white text
            if rgba[0] == 255 and rgba[1] == 255 and rgba[2] == 255:
                # Check if there is another player
                if others_around(36,385,100,300):
                    stop()
                    say('hello')

# Check if another player is in the map
def others_around(x_min, x_max, y_min, y_max):
    global pixels
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            rgba = pixels[i,j]
            # Found yourself
            if rgba[0] == 238 and rgba[1] == 0 and rgba[2] == 0:
               return True
    return False

    
def main():

    global im, pixels, width, height, x2, direction

    """
    im = Image.open("/Users/ktime/Desktop/test3.png")
    pixels = im.load()
    width, height = im.size
    x2 = 861
    direction = 'right'
    """

    #print monsters_around(-230,300,658,688)
    #print monsters_around(-860,735,366,height-200)

    if False:
        for x in range(width):
            for y in range(height):
                print pixels[x,y]

    for i in range(50): att()


    """
    im=ImageGrab.grab(bbox=(0,0,1606,1150))
    
    pixels = im.load()
    width, height = im.size

    check_chat()
    """

main()