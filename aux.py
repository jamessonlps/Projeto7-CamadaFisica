
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy import signal as window


class Signal:
    def __init__(self, freq, amplitude, time, sample_freq):
        self.init = 0
        self.freq = freq
        self.amplitude = amplitude
        self.time = time
        self.sample_freq = sample_freq

    def generateSin(self):
        n = self.time * self.sample_freq
        time_array = np.linspace(0.0, self.time, n)                                    # eixo x
        signal_amplitude = self.amplitude * np.sin(self.freq * time_array * 2 * np.pi) # eixo y
        return (time_array, signal_amplitude)

    def calcFFT(self, signal):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1 / self.sample_freq
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal):
        x,y = self.calcFFT(signal, self.sample_freq)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')
