import re
import sys
from socket import *

def escreverMsg(dest, msg):
    nomeCx = dest + ".txt"
    cxDest = open(nomeCx, "a")
    full = msg + '\n\n'
    cxDest.write(full)
    cxDest.close()
    return

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
portaServidor = 25
nomeServidor = ''
socketServidor = socket(AF_INET, SOCK_STREAM)   # Declaracao default do socket
socketServidor.bind((nomeServidor, portaServidor)) # faz o bind com a porta escolhida
socketServidor.listen(5)


while True:
    # Espera conexao com o cliente
    try:
        socketConexao, addr = socketServidor.accept()
        print("220 OK - Conexão do cliente aceita!")
    except:
        print("Conexao Falhou")
        sys.exit()
    
    # receber o comando SMTP HELO enviado pelo cliente
    try:
        helo = socketConexao.recv(1024)
        
        if helo.decode() == 'HELO':
            mensagem_servidor = '250 OK - HELO recebido'
            print(mensagem_servidor)
            socketConexao.send(mensagem_servidor.encode())
    except:
        print('Erro no recebimento do HELO')
        sys.exit()
    
    prontoParaRecebimento = False
# TESTADO ATE AQUI==========================================
    #Recebe comando do cliente para decidir o que fazer
    comandoEMAIL = socketConexao.recv(1024)
    comandoEMAILdecoded = comandoEMAIL.decode()

    #Se receber um MAIL FROM o servidor sabe que é um envio de email
    if comandoEMAILdecoded[:9] == 'MAIL FROM':
        remetente = comandoEMAILdecoded[11:-1]
        #checa se o remetente existe
        if remetente in caixas:
            socketConexao.send('250 - MAIL FROM OK'.encode())
        else:
            socketConexao.send('Remetente Invalido'.encode())
        
        #Recebe o RCPT TO do cliente
        comandoEMAIL = socketConexao.recv(1024)
        comandoEMAILdecoded = comandoEMAIL.decode()
        
        if comandoEMAILdecoded[:7] == 'RCPT TO':
            destinatario = comandoEMAILdecoded[9:-1]
            #checa se o destinatario existe
            if destinatario in caixas:
                socketConexao.send('250 - RCPT TO OK'.encode())
                prontoParaRecebimento = True
            else:
                socketConexao.send('Destinatario Invalido'.encode())
        else:
            print("Aqui command unrecognized???1")
    #Talvez um elif aqui para leitura de email
    else:
        ###TODO - PARA LEITURA DE EMAILS
        print("Aqui command unrecognized???2")
    
    if prontoParaRecebimento:
        comandoDATA = socketConexao.recv(1024)
        comandoDATAdecoded = comandoDATA.decode()
        if comandoDATAdecoded == 'DATA':
            socketConexao.send('354 - Envie conteudo da mensagem'.encode())
            corpo = socketConexao.recv(1024)
            corpoDecoded = corpo.decode()
            escreverMsg(destinatario, corpoDecoded) # TODO servidor deve esperar um "." para parar de escrever

        else:
            print("Aqui command unrecognized???3")


        

    

