from Xlib import display, X, XK
from Xlib.protocol import event
from Xlib.ext import xtest
import os
import time

from Xlib.ext.xtest import fake_input

# Mouse sensitivy
MOUSE_SENSIVITY = 1.0

# How to figure out media keys: xmodmap -pke | grep audio -i
# or xev
# or showkey -k (outside X)

# Key codes for special chars
VK_LEFT = 113 
VK_RIGHT = 114 
VK_SPACE = 65
VK_ENTER = 36
VK_BACKSPACE = 22
VK_POINT = 60
VK_EXCLAM = 10
VK_QUESTION = 97

# Arrow keys (For presentation mode)
VK_LEFT = 113
VK_RIGHT = 114

# Media keys
VK_PLAY_PAUSE = 172
VK_PREV_TRACK = 173
VK_NEXT_TRACK = 171
VK_MUTE = 121
VK_VOL_DOWN = 122
VK_VOL_UP = 123

class Controller:

  def __init__(self):
    self.disp = display.Display()
    self.scr = self.disp.screen()
    self.root = self.disp.screen().root

  def type_button(self, keycode):
    self.press_button(keycode)
    self.release_button(keycode)

  def type_char(self, char):
    self.press_button(self.disp.keysym_to_keycode(XK.string_to_keysym(char)))
    self.release_button(self.disp.keysym_to_keycode(XK.string_to_keysym(char)))

  def press_button(self, keycode):
    fake_input(self.disp, X.KeyPress, keycode)
    self.disp.sync()

  def release_button(self, keycode):
    fake_input(self.disp, X.KeyRelease, keycode)
    self.disp.sync()

  def move_mouse(self, deltaX, deltaY):
    self.disp.warp_pointer(deltaX*MOUSE_SENSIVITY, deltaY*MOUSE_SENSIVITY)
    self.disp.flush()

  def click(self, button):
    xtest.fake_input(self.disp, X.ButtonPress, button)
    xtest.fake_input(self.disp, X.ButtonRelease, button)
    self.disp.flush()

  def handle_message(self, message):

    try:

      protocol = ord(message[0]);

      # Mouse movement
      if(protocol == 0x01):

        print 'Mouse movement!'
        #print 'Bytes (dx): '+hex(ord(message[1]))+'  '+hex(ord(message[2]))+' '+hex(ord(message[3]))+' '+hex(ord(message[4]))
        #print 'Bytes (dy): '+hex(ord(message[5]))+'  '+hex(ord(message[6]))+' '+hex(ord(message[7]))+' '+hex(ord(message[8]))

        # Java signed byte trick
        if(ord(message[1]) >= 127):
          dx = (ord(message[1])<<24)+(ord(message[2])<<16)+(ord(message[3])<<8)+(ord(message[4])) - (1<<32)
        else:
          dx = (ord(message[1])<<24)+(ord(message[2])<<16)+(ord(message[3])<<8)+(ord(message[4]))
            
        if(ord(message[5]) >= 127):
          dy = (ord(message[5])<<24)+(ord(message[6])<<16)+(ord(message[7])<<8)+(ord(message[8])) - (1<<32)
        else:
          dy = (ord(message[5])<<24)+(ord(message[6])<<16)+(ord(message[7])<<8)+(ord(message[8]))

        print 'dx: '+str(dx)+' dy: '+str(dy)

        self.move_mouse(dx/80, dy/80)

      # Mouse left button click 
      elif(protocol == 0x02):
        print 'Mouse left button click!'
        self.click(1)

      # Mouse right button click 
      elif(protocol == 0x03):
        print 'Mouse right button click!'
        self.click(3)

      # Keypress
      elif(protocol == 0x04):
        #keycode = ord(message[1])
        print 'Char: '+hex(ord(message[4]))

        # Enter, space and backspace are special cases...
        if ord(message[4]) == 0x0a:
          self.type_button(VK_ENTER)
        elif ord(message[4]) == 0x20:
          self.type_button(VK_SPACE)
        elif ord(message[4]) == 0x08:
          self.type_button(VK_BACKSPACE)
        elif ord(message[4]) == 0x2e:
          self.type_button(VK_POINT)
        elif ord(message[4]) == 0x21:
          self.type_button(VK_EXCLAM)
        elif ord(message[4]) == 0x3f:
          self.type_button(VK_QUESTION)
        else:
          self.type_char(message[4])

      # Presentation mode
      elif(protocol == 0x05):
        if(ord(message[1]) == 0x01):
          print 'Presentation mode. Going left.'
          self.type_button(VK_LEFT)

        elif(ord(message[1]) == 0x02):
          print 'Presentation mode. Going right.'
          self.type_button(VK_RIGHT)
          
      # Media mode
      elif(protocol == 0x06):
        if(ord(message[1]) == 0x01):
          print 'Media mode. Previous track!'
          self.type_button(VK_PREV_TRACK)
        elif(ord(message[1]) == 0x02):
          print 'Media mode. Next track!'
          self.type_button(VK_NEXT_TRACK)
        elif(ord(message[1]) == 0x03):
          print 'Media mode. Volume up!'
          self.type_button(VK_VOL_UP)
        elif(ord(message[1]) == 0x04):
          print 'Media mode. Vol down!'
          self.type_button(VK_VOL_DOWN)
        elif(ord(message[1]) == 0x05):
          print 'Media mode. Mute!'
          self.type_button(VK_MUTE)
        elif(ord(message[1]) == 0x06):
          print 'Media mode. Play/pause!'
          self.type_button(VK_PLAY_PAUSE)

      else:
        print 'Unrecognized message. First byte: '+str(ord(message[0]))

    except Exception, e:
      print 'Error while decoding message ('+str(e)+'). Ignoring and moving on.'
