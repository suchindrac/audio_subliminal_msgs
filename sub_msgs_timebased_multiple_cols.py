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
    def __init__(self, width, height, fpath):
        super(Window, self).__init__()
        self.fpath = fpath
        self.setGeometry(0, 0, width, height)
        self.show()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True) 
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True) 
        self.gap = 0

        with open(self.fpath, "r") as fd:
            self.msg = fd.read()
            self.orig_msg = self.msg.strip()
        self.orig_msg_lst = []

        ext_chars = [x for x in range(2300, 2308)]
        ext_chars.extend([x for x in range(2362, 2392)])
        ext_chars.remove(2384)

        i = 0
        while i < len(self.orig_msg):
            if (i <= len(self.orig_msg)-3) and (ord(self.orig_msg[i+1]) in ext_chars) and (ord(self.orig_msg[i+2]) in ext_chars):
                self.orig_msg_lst.append("".join((self.orig_msg[i], self.orig_msg[i+1], self.orig_msg[i+2])))
                i += 3
            if (i <= len(self.orig_msg)-2) and (ord(self.orig_msg[i+1]) in ext_chars):
                self.orig_msg_lst.append("".join((self.orig_msg[i], self.orig_msg[i+1])))
                i += 2
            else:
                self.orig_msg_lst.append(self.orig_msg[i])
                i += 1

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
            if new_idx >= len(self.orig_msg_lst):
                new_idx = 0
           
            new_char = self.orig_msg_lst[new_idx]

            
            self.set_box_char(box.obj, new_char)
            box.cur_idx = new_idx
            
    def keyReleaseEvent(self, event):
         if event.key() == QtCore.Qt.Key_Enter-1:
             for i in range(len(self.boxes)):
                 rand_num = random.randint(0, len(self.orig_msg)-1)
                 self.boxes[i].cur_idx = rand_num
                 self.set_box_char(self.boxes[i].obj, self.orig_msg[self.boxes[i].cur_idx])
             
             index = 0
             seq = 1
             while True:
                 
                 if index >= len(self.orig_msg)-1:
                     index = 0
                     seq += 1
                 if seq == 4:
                     seq = 1
                     index = 0
                 self.set_boxes_chars()
                 QtTest.QTest.qWait(seq * 100)
                 index += 1
                 
         event.accept()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="File name to read messages from")
    
    args = parser.parse_args()
    if getattr(args, "file"):
        file_path = args.file
        
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    width = 800
    height = 600

    w = Window(width, height, fpath=file_path)
    w.resize(width, height)
    w.setWindowTitle("Subliminal Messages Editor")

    w.show()
    sys.exit(app.exec_())
