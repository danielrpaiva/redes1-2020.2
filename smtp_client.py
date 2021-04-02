import sys
from socket import *

# Mensagem vazia buga
portaServidor = 25
host = 'localhost'

try:
    socketCliente = socket(AF_INET, SOCK_STREAM)
    socketCliente.connect((host, portaServidor))
    respostaCon = socketCliente.recv(1024)
    print(respostaCon.decode())
except:
    print("Conexao com o servidor falhou")
    sys.exit()



while True:
    
    #inputs do usuario
    print("Digite o número da operação que se deseja fazer")
    print("1 - Enviar Email")
    print("2 - Ler Emails")
    print("3 - Desconectar")
    usrOp = int(input("Digite aqui o número da opção escolhida: "))

    if usrOp == 1 or usrOp == 2 or usrOp == 3: 
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


    if usrOp == 3:
        socketCliente.send('QUIT'.encode())
        respostaBYE = socketCliente.recv(1024)
        print(respostaBYE.decode())
        socketCliente.close()
        print("Conexao Interrompida pelo usuário!")
        sys.exit()


    elif usrOp == 1: # Enviar email
        remetente = input("Digite o seu email (remetente, mesmo nome do arquivo txt da caixa de entrada):")
        destinatario = input("Digite o email do destinatario (mesmo nome do arquivo txt da caixa de entrada):")
        corpoMsg = input("Digite a mensagem que deseja enviar:")
        
        prontoParaEnvio = False
        # Enviar o comando SMTP: MAIL FROM para o servidor
        mailFromMsg = 'MAIL FROM:<' + remetente + '>'
        socketCliente.send(mailFromMsg.encode())
        respostaMF = socketCliente.recv(1024)

        if respostaMF.decode() == '250 - MAIL FROM OK':
            print(respostaMF.decode())
            # Enviar o comando SMTP: RCPT TO para o servidor
            rpctToMsg = 'RCPT TO:<' + destinatario + '>'
            socketCliente.send(rpctToMsg.encode())
            respostaRT = socketCliente.recv(1024)
            if respostaRT.decode() == '250 - RCPT TO OK':
                print(respostaRT.decode())
                prontoParaEnvio = True
            else:
                print(respostaRT.decode())

        else:
            print(respostaMF.decode())
        
        #Se o remetente e destinatarios forem validos, iniciar DATA
        if prontoParaEnvio:
            socketCliente.send('DATA'.encode())
            respostaDATA = socketCliente.recv(1024)
            respostaDATAdecoded = respostaDATA.decode()
            if respostaDATAdecoded == '354 - Envie conteudo da mensagem':
                print(respostaDATAdecoded)
                msgFull = "\rremetente: "+remetente+"\ndestinatario: "+destinatario+"\nmensagem:\n"+corpoMsg+"\r\n.\r\n"
                socketCliente.sendall(msgFull.encode())
                
        continue

    elif usrOp == 2: # Ler email
        usrLeitor = input("Digite o seu email (mesmo nome do arquivo txt):")
        #Protocolo de acesso de email onde o destinatário obtém suas mensagens do servidor não segue o protocolo SMTP
        leituraUsr = "READ:" + usrLeitor
        socketCliente.send(leituraUsr.encode())

        respostaLeitura = socketCliente.recv(4096)
        respostaLeituraDecoded = respostaLeitura.decode()

        print(respostaLeituraDecoded)

        continue

    else:
        print("Operação inválida, digite apenas o número da operação")