import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTextEdit, QMainWindow
from PyQt5 import QtGui, QtCore, QtTest
from scipy.io import wavfile as wav
import numpy as np
import time
import argparse
import pyaudio
import wave
import struct
import itertools

sep = " "
change_type = "spaces"

def cycle():
    for i in itertools.cycle([1, 2, 3]):
        yield i

gen = cycle()

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 800, 600)
        self.show()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True) 
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True) 
        self.gap = 0

        self.obox = QTextEdit(self)
        self.obox.move(0, 100)
        self.obox.resize(800, 400)
        self.obox.show()

    def mod(self, num):
        res = list(map(lambda x, y: x % y, (num, num, num), (3, 6, 9)))
        res = res[::-1]

        if 0 in res:
            return next(gen)
        else:
            return False

    def get_num_spaces(self):
         self.num_chars = len(self.msg_enl)
         mod = self.mod(self.num_chars)

         if mod:
             self.gap = mod
         else:
             self.gap = 0

    def keyReleaseEvent(self, event):
         if event.key() == QtCore.Qt.Key_Enter-1:
             msg = self.obox.toPlainText()
             msg = msg.strip()
             msg = "{}{}".format(msg, " ")
             msg = 100 * msg

             self.msg_enl = ""
             for c in msg:
                 self.get_num_spaces()
                 self.msg_enl = "{}{}{}".format(self.msg_enl, c, sep * self.gap)

             self.obox.setText(self.msg_enl)
         event.accept()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--separator", type=str, required=False, help="Separator to use for text")
    parser.add_argument("-c", "--change_type", type=str, required=False, help="Change type wanted [letter/spaces]")
    
    args = parser.parse_args()
    if getattr(args, "separator"):
        sep = args.separator
    if getattr(args, "change_type"):
        change_type = args.change_type
    
    app = QApplication(sys.argv)
    w = Window()
    w.resize(800, 600)
    w.setWindowTitle("Subliminal Messages Editor")

    w.show()
    sys.exit(app.exec_())
