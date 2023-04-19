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

class Box:
    def __init__(self, obj):
        self.cur_idx = 0
        self.obj = obj
        
class Window(QMainWindow):
    def __init__(self, fpath):
        super(Window, self).__init__()
        self.fpath = fpath
        self.setGeometry(0, 0, 800, 600)
        self.show()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True) 
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True) 
        self.gap = 0

        with open(self.fpath, "r") as fd:
            self.msg = fd.read()
            self.orig_msg = self.msg.strip()
            
        self.boxes = []
        for row in range(10, 1000, 20):
            for col in range(10, 1000, 20):
                box = QLineEdit(self)
                box.move(row, col)
                box.resize(20, 20)
                box.show()
                a_box = Box(box)
                self.boxes.append(a_box)

    def mod(self, num):
        res = list(map(lambda x, y: x % y, (num, num, num), (3, 6, 9)))
        res = res[::-1]

        if 0 in res:
            return next(gen)
        else:
            return False

    def get_time_gap(self, num_chars):
         mod = self.mod(num_chars)

         if mod:
             self.gap = mod
         else:
             self.gap = 0

    def set_box_char(self, box, char):
        box.setText(char)
        box.update()

    def set_boxes_chars(self):
        for box in self.boxes:
            cur_idx = box.cur_idx
            new_idx = cur_idx + 1
            if new_idx >= len(self.orig_msg):
                new_idx = 0
            new_char = self.orig_msg[new_idx]

            self.set_box_char(box.obj, new_char)
            box.cur_idx = new_idx
            
    def keyReleaseEvent(self, event):
         if event.key() == QtCore.Qt.Key_Enter-1:
             for i in range(len(self.boxes)):
                 rand_num = random.randint(0, len(self.orig_msg)-1)
                 self.boxes[i].cur_idx = rand_num
                 self.set_box_char(self.boxes[i].obj, self.orig_msg[self.boxes[i].cur_idx])
             
             index = 0
             while True:
                 if index >= len(self.orig_msg)-1:
                     index = 0
                
                 self.get_time_gap(index)
                 print(self.gap)
                 self.set_boxes_chars()
                 if self.gap == 0:
                     QtTest.QTest.qWait(500)
                 else:
                     QtTest.QTest.qWait(self.gap * 1000)
                 index += 1
                 
         event.accept()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="File name to read messages from")
    
    args = parser.parse_args()
    if getattr(args, "file"):
        file_path = args.file
        
    app = QApplication(sys.argv)
    w = Window(fpath=file_path)
    w.resize(800, 600)
    w.setWindowTitle("Subliminal Messages Editor")

    w.show()
    sys.exit(app.exec_())
