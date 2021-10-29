import sys
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

from aux import Signal

#importe as bibliotecas

dtmf = {
    '1': [1209, 697],
    '2': [1336, 697],
    '3': [1477, 697],
    'A': [1633, 697],
    '4': [1209, 770],
    '5': [1336, 770],
    '6': [1477, 770],
    'B': [1633, 770],
    '7': [1209, 852],
    '8': [1336, 852],
    '9': [1477, 852],
    'C': [1633, 852],
    'X': [1209, 941],
    '0': [1336, 941],
    '#': [1477, 941],
    'D': [1633, 941],
}


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
     #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    sample_freq = 44100

    user_input = input("Digite uma tecla do seu telefone: ")
    try:
        freqs = dtmf[user_input]
    except:
        print("Comando inválido, modafoca")
    
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    duration = 7 #tempo em segundos que ira emitir o sinal acustico 
      
    #relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    signal1 = Signal(freq=freqs[0], amplitude=gainX, time=duration, sample_freq=sample_freq)
    signal2 = Signal(freq=freqs[1], amplitude=gainY, time=duration, sample_freq=sample_freq)

    x1, y1 = signal1.generateSin()
    x2, y2 = signal2.generateSin()

    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    tone = y1 + y2
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som
    sd.play(tone, sample_freq)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()