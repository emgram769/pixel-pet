import png
import curses
import time

def getTerminalSize():
  import os
  env = os.environ
  def ioctl_GWINSZ(fd):
    try:
      import fcntl, termios, struct, os
      cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
    '1234'))
    except:
      return
    return cr
  cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
  if not cr:
    try:
      fd = os.open(os.ctermid(), os.O_RDONLY)
      cr = ioctl_GWINSZ(fd)
      os.close(fd)
    except:
      pass
  if not cr:
    cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
  return int(cr[1]), int(cr[0])

class Image(object):
  def __init__(self, filename):
    self.filename = filename
    with open(self.filename) as f:
      im = png.Reader(file=f).read()
      self.data = list(im[2])
      self.width = im[0]
      self.height = im[1]

class Screen(object):
  def __init__(self):
    self.stdscr = curses.initscr()

  def show(self, image):
    w, h = getTerminalSize()
    wpadding = (w - image.width * 2)/2
    hpadding = (h - image.height)/2
    for i in range(image.height):
      k = 0
      for j in image.data[i]:
        k += 1
        if j > 0:
          try:
            self.stdscr.addch(hpadding + i, wpadding + k/2, '\xe2')
            self.stdscr.addch(hpadding + i, wpadding + k/2 + 1, '\xe2')
          except:
            pass
    self.stdscr.refresh()

  def end(self):
    curses.endwin()

  def sleep(self, sec):
    time.sleep(sec)

  def __delete__(self):
    curses.endwin()

#############################
## How to use this library ##
#############################
# import ascii
#
# screen = ascii.Screen()
# image = ascii.Image(filename)
# screen.show(image)
# screen.sleep(1)
# screen.end()
#
#############################
if __name__ == "__main__":
  im = Image('pixel.png')
  scr = Screen()
  scr.show(im)
  scr.sleep(1)
  scr.end()

