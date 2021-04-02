import re
import sys
from socket import *

def escreverMsg(dest, msg):
    nomeCx = dest + ".txt"
    cxDest = open(nomeCx, "a")
    full = msg
    cxDest.write(full)
    cxDest.close()
    return

def lerMsg(dest):
    nomeCx = dest + ".txt"
    cxDest = open(nomeCx, "r")
    fullFile = cxDest.read()
    cxDest.close()
    return fullFile

def checkFormatFile(file):
    lines = file.readlines()
    lastLine = lines[-1]
    isValid = False
    for line in lines:
        if bool(re.match("^<[a-zA-Z0-9-_.@]*>(\n|)$", line)):
            isValid = True
        else:
            isValid = False
            break
        #print("isValid: "+str(isValid))
        #print("linha: "+line)
    return isValid

# Arquivo deve ser passado como argumento de linha de comando como especificado
if len(sys.argv) < 2:
    print("Arquivo com os usuários não encontrado. DICA: Para executar digite no terminal: python script.py nome_arq_usuarios.txt")
    sys.exit()


# Le o arquivo e gera as caixas de entrada
usrs = open(sys.argv[1], "r")

#Armazena o nome das caixas de entrada
caixas = []

valido = checkFormatFile(usrs)

usrs.seek(0)

#print(valido)

if valido == False:
    print("Formato do arquivo passado não é valido, abortando..")
    usrs.close()
    sys.exit()

#Cria as caixas de entrada
for line in usrs:
    
    if line[-1] == "\n":
        nome_cx = line[1:-2] + ".txt"
    else:
        nome_cx = line[1:-1] + ".txt"
    
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

isConnected = False

while True:
    # Checa se o cliente ja esta conectado
    if isConnected == False:
        # Espera conexao com o cliente
        try:
            socketConexao, addr = socketServidor.accept()
            socketConexao.send('220 OK - Conexao estabelecida'.encode())
            print("220 OK - Conexão do cliente aceita!")
            isConnected = True
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

    #Recebe comando do cliente para decidir o que fazer
    comandoEMAIL = socketConexao.recv(1024)
    comandoEMAILdecoded = comandoEMAIL.decode()
    #print("COMANDO:", comandoEMAILdecoded)
    #Se receber um MAIL FROM o servidor sabe que é um envio de email
    if len(comandoEMAILdecoded) >= 9 and comandoEMAILdecoded[:9] == 'MAIL FROM':
        remetente = comandoEMAILdecoded[11:-1]
        #checa se o remetente existe
        if remetente in caixas:
            socketConexao.send('250 - MAIL FROM OK'.encode())
        else:
            socketConexao.send('550 Sender Address Unknown'.encode())
            continue
        
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
                socketConexao.send('550 Receiver Address Unknown'.encode())
        else:
            print("500 Syntax error, command unrecognized")
    
    # Comando READ foi arbitrado para o servidor reconhecer uma leitura
    elif len(comandoEMAILdecoded) >= 4 and comandoEMAILdecoded[:4] == 'READ':
        #print("Entrou no ELIF READ")
        cxLeitura = comandoEMAILdecoded[5:]

        dadosCx = lerMsg(cxLeitura)
        if dadosCx == '':
            dadosCx = 'THIS INBOX IS EMPTY'
        
        socketConexao.send(dadosCx.encode())

    
    elif comandoEMAILdecoded == 'QUIT':
        socketConexao.send('221 - Disconnecting..'.encode())
        isConnected = False

    else:
        print("500 Syntax error, command unrecognized")
    
    if prontoParaRecebimento:
        comandoDATA = socketConexao.recv(1024)
        comandoDATAdecoded = comandoDATA.decode()
        if comandoDATAdecoded == 'DATA':
            socketConexao.send('354 - Envie conteudo da mensagem'.encode())
            dado = socketConexao.recv(1024)
            dadoDecoded = dado.decode()
            escreverMsg(destinatario, dadoDecoded)

        else:
            print("500 Syntax error, command unrecognized")


        

    

