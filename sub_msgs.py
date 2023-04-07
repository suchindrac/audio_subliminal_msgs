import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTextEdit
from PyQt5 import QtGui, QtCore, QtTest
from scipy.io import wavfile as wav
import numpy as np
import time
import argparse

#
# Making it easier
#
decoded_freqs = []

def read_wav(filename):
    rate, data = wav.read(filename)
    
    # 15ms chunk includes delimiting 5ms 1600hz tone
    duration = 0.015
    
    # calculate the length of our chunk in the np.array using sample rate
    chunk = int(rate * duration)
    
    # length of delimiting 1600hz tone
    offset = int(rate * 0.005)
    
    # number of bits in the audio data to decode
    bits = int(len(data) / chunk)

    return chunk, offset, data, rate, bits

def get_freq(chunk, bit, offset, data, rate):
    # start position of the current bit
    strt = (chunk * bit) 
        
    # remove the delimiting 1600hz tone
    end = (strt + chunk) - offset
    
    # slice the array for each bit
    sliced = data[strt:end]

    w = np.fft.fft(sliced)
    freqs = np.fft.fftfreq(len(w))

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    if idx >= len(freqs):
        idx = len(freqs) - 1
    freq = freqs[idx]
    freq_in_hertz = abs(freq * rate)
    return freq_in_hertz

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 800, 600)
        self.show()

        self.tbox = QLineEdit(self)
        self.tbox.move(0, 0)
        self.tbox.resize(800, 40)
        self.tbox.setCursorPosition(0)
        self.tbox.show()

        self.obox = QTextEdit(self)
        self.obox.move(0, 100)
        self.obox.resize(800, 400)
        self.obox.show()

    def keyPressEvent(self, event):
        msg = self.tbox.text()

        if event.key() == QtCore.Qt.Key_Enter-1:
            self.tbox.hide()
            self.obox.resize(800, 600)
            self.obox.move(0, 0)
            do_the_dance(self.obox, msg)
        event.accept()

def do_the_dance(obox, msg):
    obox.setProperty("urgent", True)
    obox.style().unpolish(obox)
    obox.style().polish(obox)

    msg_put = ""
    enum = 0
    for i in range(100):
        msg_put = msg_put + "{}\t".format(msg)
        if enum % 5 == 0:
            msg_put += "\n"
        enum += 1
        
    obox.setText(msg_put)
    
    for freq in decoded_freqs:
        set_freq = int(freq / 20)
        if set_freq < 10:
            set_freq = 15
        if set_freq >= 50:
            set_freq = 50
            
        set_freq = "{}%".format(set_freq)
        obox.setStyleSheet("color: rgba(0, 0, 255, {})".format(set_freq))
        obox.update()
        QtTest.QTest.qWait(100)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", required=True, type=str, help="The subliminal message")
    parser.add_argument("-a", "--audio_file", required=True, type=str, help="The audio file path")
    args = parser.parse_args()

    message = args.message
    audio_file = args.audio_file
    msg = message    
    app = QApplication(sys.argv)
    w = Window()
    w.resize(800, 600)
    w.setWindowTitle("Subliminal Messages")

    w.tbox.setText(message)
    chunk, offset, data, rate, bits = read_wav(audio_file)
    
    decoded_freqs = [get_freq(chunk, bit, offset, data, rate) for bit in range(bits)]
    
    w.show()
    sys.exit(app.exec_())
