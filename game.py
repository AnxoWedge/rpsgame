# Classe Jogo
class Game:
    # Função de começo com os parametros self e identificador
    def __init__(self, id):
        # player 1 foi como Falso
        self.p1Went = False
        # player 2 foi como Falso
        self.p2Went = False
        # Pronto como falso
        self.ready = False
        # id com o parametro de identificador
        self.id = id
        # movimentos com nada
        self.moves = [None, None]
        # vitórias a começar com 0
        self.wins = [0,0]
        # empates a começar com 0
        self.ties = 0

# Função que obtém os movimentos do jogador e passa o parametro p
    def get_player_move(self, p):
        # Parametros podem ser 0 ou 1 e retorna o movimento
        """
        :param p: [0,1]
        :return: Move
        """
        # retorna o movimento com o parametro p
        return self.moves[p]

# função jogada onde obtém o parametro player e move
    def play(self, player, move):
        # moves relacionados a cada player
        self.moves[player] = move
        # se o player for 0 será o player 1
        if player == 0:
            # o player 1 joga ficando a True
            self.p1Went = True
        # Se não for 0 será o player 2
        else:
            # o player 2 joga ficando a True
            self.p2Went = True

# Função que faz a ligação
    def connected(self):
        # Retorna se está pronto ou não
        return self.ready

# Funlão que faz os dois player irem
    def bothWent(self):
        # Retorna que os 2 players jogaram
        return self.p1Went and self.p2Went

# Função de vencedor
    def winner(self):
        
        # Movimento do player 1
        p1 = self.moves[0].upper()[0]
        # Movimento do player 2
        p2 = self.moves[1].upper()[0]
        winner = -1
        #Se player 1 jogar rocha contra tesoura do player 2
        if p1 == "R" and p2 == "T":
            # Ganha o player 1
            winner = 0
        #Se player 1 jogar tesoura contra rocha do player 2
        elif p1 == "T" and p2 == "R":
            # Ganha o player 2
            winner = 1
        #Se player 1 jogar papel contra rocha do player 2
        elif p1 == "P" and p2 == "R":
            # Ganha o player 1
            winner = 0
        #Se player 1 jogar rocha contra papel do player 2
        elif p1 == "R" and p2 == "P":
            # Ganha o player 2
            winner = 1
        #Se player 1 jogar tesoura contra papel do player 2
        elif p1 == "T" and p2 == "P":
            # Ganha o player 1
            winner = 0
        #Se player 1 jogar papel contra tesoura do player 2
        elif p1 == "P" and p2 == "T":
            # Ganha o player 2
            winner = 1
        # Retorna o vencedor como player 1 ou 2
        print(winner)
        return winner

# Resetar do jogar
    def resetWent(self):
        # Deixar novamente a jogada do player 1 como False
        self.p1Went = False
        # Deixar novamente a jogada do player 2 como False
        self.p2Went = False
