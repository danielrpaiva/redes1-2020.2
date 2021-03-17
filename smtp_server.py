import re
import sys
from socket import *

# Arquivo deve ser passado como argumento de linha de comando como especificado
if len(sys.argv) < 2:
    print("Para executar, digite no terminal: python script.py usuarios.txt")
    quit()


# Le o arquivo e gera as caixas de entrada
usrs = open(sys.argv[1], "r")

for line in usrs:
    nome_cx = line[:-1] + ".txt"
    f = open(nome_cx, "w")
    # Quando posteriormente for acessar as caixas de entrada reabrir arquivo no modo "a"
    f.close()

usrs.close()