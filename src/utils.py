
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

from scipy.fftpack import fft, fftshift

def calcFFT(signal, fs):
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
    yf = fft(signal)
    return(xf, fftshift(yf))

def plotFFT(signal, sample_freq):
    x,y = calcFFT(signal, sample_freq)
    plt.figure()
    plt.stem(x, np.abs(y))
    plt.title('Fourier')

def get_fft_params(signal, sample_freq):
    x, y = calcFFT(signal, sample_freq)
    return (x, np.abs(y))

def get_dimension(m):
    # Verifica se todas as linhas da matriz
    # possuem o mesmo tamnho
    if len({len(i) for i in m}) > 1:
        raise TypeError('Matriz 2D invalida.')

    # Calcula quantidade de linhas na matriz
    linhas = len(m)

    # Se nao houverem linhas na matriz
    # assume zero colunas
    colunas = len(m[0]) if linhas else 0

    return (linhas, colunas)