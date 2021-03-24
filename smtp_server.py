import re
import sys
from socket import *

# Arquivo deve ser passado como argumento de linha de comando como especificado
if len(sys.argv) < 2:
    print("Para executar, digite no terminal: python script.py usuarios.txt")
    quit()


# Le o arquivo e gera as caixas de entrada
usrs = open(sys.argv[1], "r")

#Armazena o nome das caixas de entrada
caixas = []

#Cria as caixas de entrada
for line in usrs:
    
    if line[-1] == "\n":
        nome_cx = line[:-1] + ".txt"
    else:
        nome_cx = line + ".txt"
    
    caixas.append(nome_cx[:-4])
    f = open(nome_cx, "w")
    # Quando posteriormente for acessar as caixas de entrada reabrir arquivo no modo "a"
    f.close()

usrs.close()

# Criar o socket do servidor
# 25, 465, 587 sao portas padrões para SMTPs, também pode usar uma porta arbitrada
portaServidor = 587
nomeServidor = ''
socketServidor = socket(AF_INET, SOCK_STREAM)   # Declaracao default do socket
socketServidor.bind((nomeServidor, portaServidor)) # faz o bind com a porta escolhida
socketServidor.listen(5)


while True:
    # Espera conexao com o cliente
    try:
        socketConexao, addr = socketServidor.accept()
        print("Conexão do cliente aceita!")
    except:
        print("Conexao Falhou")
        sys.exit()
    
    # receber o comando SMTP HELO enviado pelo cliente
    try:
        helo = socketConexao.recv(1024)
        
        if helo.decode() == 'HELO':
            mensagem_servidor = 'OK - HELO recebido'
            socketConexao.send(mensagem_servidor.encode())
    except:
        print('Erro no recebimento do HELO')
        sys.exit()
    

