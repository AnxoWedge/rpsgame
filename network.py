import socket                                                                   #Importação que define que sepode utilizar sockets no programa
import pickle                                                                   #Utiliza a representação binária para o formato de fluxo de dados


class Network:                                                                  #Define a classe
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #Define a família do endereço e o tipo Sock_strem, definido como protocolo TCP
        self.server = "localhost"                                               #Aribuição do ip/localhost
        self.port = 5555                                                        #Define explicitamente a porta aberta
        self.addr = (self.server, self.port)                                    #Atribuição do ip e porta ao endereço
        self.p = self.connect()                                                 #Conexão com servidor

    def getP(self):                                                             #Inicio de jogo do cliente
        return self.p                                                           #Feedback do servidor

    def connect(self):                                                         #Função de conexão
        try:
            self.client.connect(self.addr)                                     #Realiza tentativa de conexão
            return self.client.recv(2048).decode()                             #Recepção da mensagem do cliente, 2048 representa o tamanho do buffer
        except:
            pass

    def send(self, data):                                                       #Função de envio de dados
        try:
            self.client.send(str.encode(data))                                  #Envio de dados codificados em binário
            return pickle.loads(self.client.recv(2048*2))                       #utiliza a função para leitura do objeto em binário, 4096 representa o tamanho do buffer
        except socket.error as e:                                               #Em caso de erro, imprime o erro
            print(e)

