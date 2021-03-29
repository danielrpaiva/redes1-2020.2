import sys
from socket import *

#inputs do usuario
print("Digite o número da operação que se deseja fazer?")
print("1 - Enviar Email")
print("2 - Ler Emails")
usrOp = int(input("Digite aqui o número da opção escolhida: "))

if usrOp == 1:
    remetente = input("Digite o email do remetente(mesmo nome do arquivo txt da caixa de entrada):")
    destinatario = input("Digite o email do destinatario(mesmo nome do arquivo txt da caixa de entrada):")
    corpoMsg = input("Digite a mensagem que deseja enviar:")


portaServidor = 25
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

if respostaHELO.decode() == '250 OK - HELO recebido':
    print(respostaHELO.decode())
else:
    print('Não houve resposta ao HELO')
    socketCliente.close()
    sys.exit()


if usrOp == 1: # Enviar email
    prontoParaEnvio = False
    # Enviar o comando SMTP: MAIL FROM para o servidor
    mailFromMsg = 'MAIL FROM:<' + remetente + '>'
    socketCliente.send(mailFromMsg.encode())
    respostaMF = socketCliente.recv(1024)

    if respostaMF.decode() == '250 - MAIL FROM OK':
        # Enviar o comando SMTP: RCPT TO para o servidor
        rpctToMsg = 'RCPT TO:<' + destinatario + '>'
        socketCliente.send(rpctToMsg.encode())
        respostaRT = socketCliente.recv(1024)
        if respostaRT.decode() == '250 - RCPT TO OK':
            prontoParaEnvio = True
        else:
            print("Destinatario Invalido")
            sys.exit()

    else:
        print("Remetente Invalido")
        sys.exit()
    
    #Se o remetente e destinatarios forem validos, iniciar DATA
    if prontoParaEnvio:
        socketCliente.send('DATA'.encode())
        respostaDATA = socketCliente.recv(1024)
        respostaDATAdecoded = respostaDATA.decode()
        if respostaDATAdecoded == '354 - Envie conteudo da mensagem':
            socketCliente.send(corpoMsg.encode()) # TODO mensagem devera ser enviada aos poucos ate enviar "." para finalizar

elif usrOp == 2: # Ler email
    #codigo de leitura de email
    print("op2")
else:
    print("Operação inválida, digite apenas o número da operação")
    sys.exit()