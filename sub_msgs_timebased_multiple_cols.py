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
import random

file_path = False

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

    def get_num_spaces(self, num_chars):
         mod = self.mod(num_chars)

         if mod:
             self.gap = mod
         else:
             self.gap = 0

    def get_msg(self):
        init_str_lst = list(self.init_str)
        for i in range(len(self.indices)):
             cur_str_idx = self.indices[i]


             if cur_str_idx >= len(self.orig_msg) - 1:
                 cur_str_idx = 0
             else:
                 cur_str_idx += 1

             init_str_lst[i] = self.orig_msg[cur_str_idx]
             if self.indices[i] >= len(self.orig_msg)-1:
                 self.indices[i] = 0
             else:
                 self.indices[i] += 1
        self.init_str = "".join(init_str_lst)

    def keyReleaseEvent(self, event):
         if event.key() == QtCore.Qt.Key_Enter-1:
             if not file_path:
                 self.msg = self.obox.toPlainText()
             else:
                 with open(file_path, "r") as fd:
                     self.msg = fd.read()

             self.orig_msg = self.msg.strip()

             self.indices = []
             self.init_str = ""
             for i in range(1000):
                 rand_num = random.randint(0, len(self.orig_msg)-1)
                 self.init_str += self.orig_msg[rand_num]
                 self.indices.append(rand_num)

             while True:
                 rand_num = random.randint(0, len(self.indices)-1)
                 self.get_msg()
                 self.get_num_spaces(self.indices[rand_num])
                 self.obox.setText(self.init_str)
                 if self.gap == 0:
                     QtTest.QTest.qWait(50)
                 else:
                     QtTest.QTest.qWait(self.gap * 100)
                     
         event.accept()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=False, help="File name to read messages from")
    
    args = parser.parse_args()
    if getattr(args, "file"):
        file_path = args.file
        
    app = QApplication(sys.argv)
    w = Window()
    w.resize(800, 600)
    w.setWindowTitle("Subliminal Messages Editor")

    w.show()
    sys.exit(app.exec_())
