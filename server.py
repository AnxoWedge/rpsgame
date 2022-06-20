# Luis Fernandes   nº20202586

import socket         #Importar a bibliotecas
from _thread import *
import pickle
from game import Game #Importar ficheiro Game.py

server = "188.166.123.78"  #IP do servidor
port = 5555           #Numero de porta na qual o servidor estara esperando conexoes

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criar o socket do TCP

try:
    s.bind((server, port)) # Aceita a conexao
except socket.error as e:  # Erro de conexao
    str(e)

s.listen(2) #Espera pela conexao
print("Servidor foi iniciado com sucesso! Á espera dos jogadores...")

connected = set() #Defenir variaveis
games = {}        #Defenir variaveis
idCount = 0       #Defenir variaveis


def threaded_client(conn, p, gameId): #Funcao para criar uma thread de 3 parametros
    global idCount                    #Variavel global
    conn.send(str.encode(str(p)))     #Enviar uma variavel codificada para iniciar o jogo

    reply = ""
    while True:                        #Enquanto for true tenta descodificar a conexção que recebe
        try:
            data = conn.recv(4096).decode() #Descodifica a variavel conn de buffer 4096

            if gameId in games:        #Se o gameId no dicionario games igualamos game a gameId
                game = games[gameId]

                if not data:           #Se não houver conexao pára
                    break
                else:                  #caso contrario se data for igual a reset o jogo reenicia
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":#Se data for diferente de get o jogo inicia
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game)) #envia dados para o client
            else:
                break
        except:
            break

    # Caso perca a conexao o jogo acaba
    print("Conexão foi perdida")
    try:
        del games[gameId]
        print("A fechar jogo...", gameId)
    except:         #caso nao feche o jogo desaparece com a conexao
        pass
    idCount -= 1
    conn.close()



while True:         #aceitação do tcp conexao cliente ao servidor
    conn, addr = s.accept()
    print("Conectado a:", addr)

#Cria o jogo quando existir 2 clienter conectados ao servidor
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("A criar um novo jogo...")
    else: #Se o game tiver criado ele inicia o jogo
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId)) #Inicia novo thread com cada cliente
