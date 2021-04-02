# Implementação de um protótipo simplificado de servidor de e-mail (SMTP) utilizando sockets. 

Trabalho de implementação para Redes I 2020.2 
Professor: Diego Gimenez Passos
Grupo:
- Breno Reis Dos Santos
- Daniel Ribeiro Paiva
- Eriky Nunes Marciano
- Kayalla Pontes Lino
- Roberto Silva Lourenço

Linguagem usada: Python 3.9.0

Processos de compilação e execução

1) Entre na pasta do projeto
2) Abra 2 terminais.
3) Em um dos terminais, execute o cógido abaixo na linha de comando. Este será o nosso servidor.
```
python smtp_server.py usuarios.txt
```
4) No outro terminal, execute o código abaixo na linha de comando. Este será nosso cliente.
```
python smtp_client.py
```

Pronto, agora com o cliente e servidor prontos. Provavelmente você verá no terminal do cliente o seguinte menu:
```
1 - Enviar e-mail
2 - Ler E-mail
3 - Desconectar
```
