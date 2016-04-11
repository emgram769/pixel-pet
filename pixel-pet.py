#!/usr/bin/python2.7
import ascii

screen = ascii.Screen()
image = ascii.Image('pixel.png')
screen.show(image)
screen.sleep(1)
screen.end()

# TODO: make it actually interactive :^)
