# Scripted by SuTerminal
#
# Color Name
#
# pip install webcolors
# pip install Pillow
# pip install pynput

import tkinter as tk

from pynput import keyboard
from pynput.keyboard import Key, Listener
from pynput.keyboard import Key, Controller


from ctypes import windll, Structure, c_long, byref
import webcolors
import PIL.ImageGrab


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePositionX():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x


def queryMousePositionY():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.y


# get screen color
def get_pixel_colour(xcord, ycord):
    return PIL.ImageGrab.grab().load()[xcord, ycord]


def PosAndColor():
    X = queryMousePositionX()
    Y = queryMousePositionY()
    color = get_pixel_colour(X, Y)
    return color


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return closest_name


def getColor():
    mouseX = queryMousePositionX()
    mouseY = queryMousePositionY()
    requested_colour = PosAndColor()
    closest_name = get_colour_name(requested_colour)
    return f"Mouse Cord: X:{mouseX} Y:{mouseY} Color Name: {closest_name}"


def on_release(key):
    if key == keyboard.Key.esc:
        quit()+
    if key == keyboard.KeyCode(char='+'):
        root = tk.Tk()
        root.title("Color Info")
        btn_text = tk.StringVar()
        btn = tk.Label(root, textvariable=btn_text)
        btn_text.set(getColor())
        btn.pack()
        root.mainloop()


with keyboard.Listener(on_release=on_release) as listener:
    listener.join()

