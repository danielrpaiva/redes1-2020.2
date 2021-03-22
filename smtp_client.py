import sys
from socket import *


portaServidor = 587
nomeServidor = 'redes1uff'

socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((nomeServidor, portaServidor))

# Tenta fazer o handshake do protocolo TCP para checar se conectou
dados = socketCliente.recv(1024)

print(dados)