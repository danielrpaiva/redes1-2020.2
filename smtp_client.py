import sys
from socket import *


portaServidor = 587
host = 'localhost'

try:
    socketCliente = socket(AF_INET, SOCK_STREAM)
    socketCliente.connect((host, portaServidor))
    print("Conexão com o servidor estabelecida!")
except:
    print("Conexao com o servidor falhou")
    sys.exit()


# Envia o comando SMTP HELO para o servidor antes de realizar qualquer operação nele
comando = 'HELO'
socketCliente.send(comando.encode())

respostaHELO = socketCliente.recv(1024)

if respostaHELO.decode() != 'OK - HELO recebido':
    print('Não houve resposta ao HELO')
    socketCliente.close()
    sys.exit()
else:
    print('Resposta ao HELO Recebida')