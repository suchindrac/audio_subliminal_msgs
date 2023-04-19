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
import threading

file_path = False

def cycle():
    for i in itertools.cycle([1, 2, 3]):
        yield i

gen = cycle()

class Box:
    def __init__(self, obj):
        self.cur_idx = 0
        self.obj = obj
        self.debug = 0
        
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
        for row in range(0, 400, 40):
#             for col in range(10, 100, 20):
            box = QLineEdit(self)
            box.move(row, 20)
            box.resize(40, 40)
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

    def get_wait_time(self, idx):
         mod = self.mod(idx)

         if mod:
             return mod
         else:
             return 0
         
    def set_box_char(self, box, char):
        box.setText(char)
        box.update()

    def set_box_char_next(self, box):
        while True:
            if box.cur_idx + 1 >= len(self.orig_msg):
                box.cur_idx = 0
   
            if box.cur_idx == 0:
                self.set_box_char(box.obj, self.orig_msg[box.cur_idx])
            else:
                self.set_box_char(box.obj, self.orig_msg[box.cur_idx+1])

            QtTest.QTest.qWait(self.get_wait_time(box.cur_idx) * 100)
            box.cur_idx += 1
            
    def start_boxes(self):
        self.threads = []
        print("Starting box update threads")
        bn = 0
        for box in self.boxes:
            if bn == 0:
                box.debug = 1
                bn += 1
            t = threading.Thread(target=self.set_box_char_next, args=(box,))
            t.start()
            print("Starting thread: {}".format(len(self.threads)))
            self.threads.append(t)
            
    def keyReleaseEvent(self, event):
         if event.key() == QtCore.Qt.Key_Enter-1:
             for i in range(len(self.boxes)):
                 rand_num = random.randint(0, len(self.orig_msg)-1)
                 self.boxes[i].cur_idx = rand_num
                 self.set_box_char(self.boxes[i].obj, self.orig_msg[self.boxes[i].cur_idx])

             self.start_boxes()
             # for thread in self.threads:
             #     thread.join()
         print("Out of event handler")                      
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
