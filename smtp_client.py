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

# Tenta fazer o handshake do protocolo TCP para checar se conectou
dados = socketCliente.recv(1024)

print(dados.decode())