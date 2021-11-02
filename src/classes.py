import time
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import peakutils

from .constants import *
from src.utils import calcFFT, get_fft_params, get_dimension


class Signal:
    def __init__(self):
        self.init = 0

    def generate_sinusoidal(self, freq, amplitude, time, sample_freq):
        n = time * sample_freq
        time_array = np.linspace(0.0, time, n)                               # eixo x
        signal_amplitude = amplitude * np.sin(freq * time_array * 2 * np.pi) # eixo y
        return (time_array, signal_amplitude)


class Encoder:
    def __init__(self, sample_freq=SAMPLE_FREQ, gain_x=0.3, gain_y=0.3, duration=6):
        self.sample_freq = sample_freq
        self.gain_x = gain_x
        self.gain_y = gain_y
        self.duration = duration
        self.freqs = []
        self.x1, self.x2, self.y1, self.y2 = (None, None, None, None)
        self.tone = None
        self.user_input = None

    def freqs_from_input(self):
        correct_input = False
        while not correct_input:
            self.user_input = input("Digite uma tecla: ")
            if self.user_input not in DTMF.keys():
                print("Comando inválido. Tente novamente")
            else:
                self.freqs = DTMF[self.user_input]
                correct_input = True
        print(f"Gerando som da tecla {self.user_input}...")

    def play_signal(self):
        signal1 = Signal()
        signal2 = Signal()
        self.x1, self.y1 = signal1.generate_sinusoidal(self.freqs[0], self.gain_x, self.duration, self.sample_freq)
        self.x2, self.y2 = signal2.generate_sinusoidal(self.freqs[1], self.gain_y, self.duration, self.sample_freq)
        # Resultante
        self.tone = self.y1 + self.y2
        # Toca o som e aguarda reprodução completa
        sd.play(self.tone, self.sample_freq)
        sd.wait()

    def plot_signals(self):
        # Plota senoidais
        fig, axis = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
        axis[0].plot(self.x1, self.y1, label=f'$f_1 = {self.freqs[0]} Hz$')
        axis[0].plot(self.x2, self.y2, label=f'$f_2 = {self.freqs[1]} Hz$')
        axis[0].plot(self.x1, self.tone, '.-', label='Resultante')
        axis[0].set_xlim((0, 3e-3))
        axis[0].set_title(f'Tecla digitada: {self.user_input}')
        axis[0].set_xlabel('Tempo [s]')
        axis[0].set_ylabel('Amplitude')
        axis[0].legend()
        axis[0].grid()
        # Plota gráfico de Fourier
        X, Y = get_fft_params(self.tone, self.sample_freq)
        axis[1].stem(X, Y)
        axis[1].set_title("Fourier")
        # Mostra resultados
        plt.show()

    def execute(self):
        self.freqs_from_input()
        self.play_signal()
        self.plot_signals()


class Decoder:
    def __init__(self, sample_freq=SAMPLE_FREQ, channels=2, duration=3):
        self.sample_freq = sample_freq
        self.channels = channels
        self.duration = duration
        self.len_sample = self.sample_freq * self.duration
        self.y_audio  = []
        self.time_rec = []
        self.peaks    = []

    def record_audio(self):
        # Grava áudio
        print("A gravação iniciará em 1 segundo...")
        time.sleep(1)
        print("Gravando...")
        audio = sd.rec(int(self.len_sample), self.sample_freq, self.channels)
        sd.wait()
        print("... Fim da gravação")
        # Guarda gravação em array
        num_cols = get_dimension(audio)[1]
        if num_cols == 2:
            self.y_audio = audio[:,1]
        else:
            self.y_audio = audio
        # Espaço de tempo da gravação
        self.time_rec = np.linspace(0, self.duration, self.len_sample)

    def get_peaks(self, X, Y):
        # Pega índices dos picos
        index = peakutils.indexes(np.abs(Y), thres=0.3, min_dist=20)
        # Grava os 2 maiores picos detectados
        self.peaks = [freq for freq in X[index] if freq > 0]
        self.peaks.sort()
        self.peaks = sorted(self.peaks[-2:], reverse=False)
        # self.peaks = self.peaks[-2:]
        for p in self.peaks:
            print(f"Frequência de pico: {p}")
        for key, freqs in DTMF.items():
            if ((abs(np.min(self.peaks) - freqs[1]) < 5) and (abs(np.max(self.peaks) - freqs[0]) < 5)):
                print(f"Tecla pressionada pelo usuário: {key}")
        
    def plot_signals(self):
        figure, axis = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
        axis[0, 0].plot(self.time_rec, self.y_audio)
        axis[0, 0].set_title("Sinal do áudio gravado")
        axis[0, 0].set_xlabel("Tempo [s]")
        axis[0, 0].set_ylabel("Amplitude")
        axis[0, 0].grid()
        # Gráfico da Transformada de Fourier
        X, Y = calcFFT(self.y_audio, self.sample_freq)
        self.get_peaks(X, Y)
        axis[0, 1].stem(X, np.abs(Y))
        axis[0, 1].set_title("Transformada de Fourier para áudio gravado")
        axis[0, 1].grid()
        # Gráfico com picos
        axis[1, 0].stem(X, np.imag(Y))
        axis[1, 0].set_title("Análise espectral do sinal de áudio")
        # axis[1, 1].get_xaxis().set_visible(False)
        # axis[1, 1].get_yaxis().set_visible(False)
        axis[1, 1].set_axis_off()
        # Plota resultados
        plt.show()

    def execute(self):
        self.record_audio()
        self.plot_signals()
