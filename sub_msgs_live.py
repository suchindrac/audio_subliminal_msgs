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

single_char = False

class Window(QMainWindow):
    def __init__(self, amplitude=True):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 800, 600)
        self.show()
        self.amplitude = amplitude
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True) 
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True) 
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
         if event.key() == QtCore.Qt.Key_Enter-1:
            self.live_dance()
         event.accept()

    def live_dance(self):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 600
            
        frames = []  # Initialize array to store frames
    
        self.obox.setProperty("urgent", True)
        self.obox.style().unpolish(self.obox)
        self.obox.style().polish(self.obox)
    
        msg = self.tbox.text()
        msg_put = ""
        if single_char:
            msg_put = msg

            font = QtGui.QFont()
            font.setPointSize(256)
            self.obox.setFont(font)

            p = pyaudio.PyAudio()  # Create an interface to PortAudio                                                              
            print('Recording')

            stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
            char_num = 0
            # Store data in chunks for 3 seconds
            for i in range(0, int(fs / chunk * seconds)):
                if char_num >= len(msg):
                    char_num = 0
                char = msg[char_num]
                data = stream.read(chunk, exception_on_overflow=False)
                numpydata = np.frombuffer(data, dtype=np.int16)
    
                if not self.amplitude:
                    content = np.fft.fft(numpydata)
                    freqs = np.fft.fftfreq(len(content))
                    max_idx = np.argmax(np.abs(content))
                    freq = freqs[max_idx]
                    set_val = freq * 10000
                else:
                    max_amp = max(numpydata)
                    set_val = int(max_amp / 20)
                
                if set_val > 25:
                    set_val = 10
    
                set_val = "{}%".format(set_val)
                
                # self.obox.setStyleSheet("color: rgba(0, 0, 255, {})".format(set_val))
              
                self.obox.setText(char)
                self.obox.update()
                char_num += 1
                QtTest.QTest.qWait(100)
                
            # Stop and close the stream 
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            p.terminate()
    
            print('Finished recording')

        else:
            p = pyaudio.PyAudio()  # Create an interface to PortAudio                                                              
            print('Recording')

            stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
            
            e_num = 0
            for i in range(100):
                msg_put = msg_put + "{}\t".format(msg)
                if e_num % 5 == 0:
                    msg_put += "\n"
                    e_num += 1

            self.obox.setText(msg_put)
    
            # Store data in chunks for 3 seconds
            for i in range(0, int(fs / chunk * seconds)):

                data = stream.read(chunk, exception_on_overflow=False)
                numpydata = np.frombuffer(data, dtype=np.int16)
    
                if not self.amplitude:
                    content = np.fft.fft(numpydata)
                    freqs = np.fft.fftfreq(len(content))
                    max_idx = np.argmax(np.abs(content))
                    freq = freqs[max_idx]
                    set_val = freq * 10000
                else:
                    max_amp = max(numpydata)
                    set_val = int(max_amp / 20)
                
                if set_val > 25:
                    set_val = 10
    
                set_val = "{}%".format(set_val)
                
                self.obox.setStyleSheet("color: rgba(0, 0, 255, {})".format(set_val))
                self.obox.update()
                QtTest.QTest.qWait(100)
                
            # Stop and close the stream 
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            p.terminate()
    
            print('Finished recording')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", required=False, type=str, help="The subliminal message")
    parser.add_argument("-f", "--frequency", required=False, action="store_true", help="Frequency based?")
    parser.add_argument("-l", "--file", required=False, type=str, help="File to read")
    parser.add_argument("-s", "--single_char", required=False, action="store_true", help="Display single char")
    args = parser.parse_args()

    message = ""
    if getattr(args, "message"):
        message = args.message
    amp = not args.frequency
    if getattr(args, 'file'):
        with open(args.file, 'r') as fd:
            message = fd.read()
    print(args.single_char)
    if getattr(args, "single_char"):
        single_char = True
    print(single_char)
    app = QApplication(sys.argv)
    w = Window(amplitude=amp)
    w.resize(800, 600)
    w.setWindowTitle("Subliminal Messages")

    w.tbox.setText(message)
    
    w.show()
    sys.exit(app.exec_())
