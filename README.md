# Encoder & Decoder

## Sobre o projeto

O projeto consiste em duas partes: o `encoder`, no qual o usuário digita uma tecla numérica e então o som correspondente é reproduzido, gerando as respectivas ondas senoidais e transformadas de Fourier, e o `decoder`, o qual grava um sinal sonoro, filtra as frequências de pico e identifica a tecla correspondente ao sinal sonoro.

## Dependências

Algumas dependências são necessárias para executar os arquivos. Para instalá-las, recomenda-se a criação de um ambiente virtual:

```
python3 -m venv env
```

E então a instalação das dependências:

```
pip install -r requirements.txt
```

## Execução

Para rodar o encoder, basta executar o arquivo `encoder.py` na raiz do projeto. Analogamente, execute o arquivo `decoder.py` na raiz para rodar o decodificador.

Cada um dos coders geram gráficos correspondentes. Exemplo dos resultados podem ser encontrados na pasta `img`.