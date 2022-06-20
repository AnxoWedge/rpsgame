# Ângelo Cunha nº20202537
# Importadção da biblioteca pygame e do Network
import pygame 
from network import Network
import pickle


# Chamar o pygame e iniciar as fontes
pygame.font.init()

# Esta secção determina a resolução da janela o modo e o titulo da janela
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pedra, Papel ou Tesoura")


#
# Definição dos buttões do jogo para o gameplay. 
# Criamos um Objecto com algumas propriedades:  o texto, posição, cor, tamanho, imagem.
# Defini-se tambem as funções dos clicks para o botão  
#

class Button:
    def __init__(self, text, x, y, color, img): #Inciar o objecto
        self.text = text                        # Texto
        self.x = x                              # Posição em x
        self.y = y                              # Posição em y 
        self.color = color                      # Cor do botão
        self.width = 230                        # largura
        self.height = 230                       # Altura
        self.image = pygame.image.load(img)     # Imagem

    # Desenho do botão
    def draw(self, win):  
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height)) # Desenhar o Rectângulo
        font = pygame.font.SysFont("arial", 12) # Estilos da fonte
        text = font.render(self.text, 1, (255,255,255)) # Render da fonte 
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2))) # Posição do Texto, e centralização
        win.blit(self.image, (self.x + round(self.width/2) - round(self.image.get_width()/2), self.y + round(self.height/2) - round(self.image.get_height()/2))) # Posição do Imagem, e centralização

    # Defnição do click 
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height: # Tamanho da tela do click e aprovação
            return True
        else:
            return False

#
# Redesenho da janela depois da página principal 
#

def windowUpdate(win, game, p):
    win.fill((190, 233, 232)) # Background da Janela 

    # Senão o jogo não tiver conectado / Waiting for player
    if not(game.connected()): 
        font = pygame.font.SysFont("arial", 60)
        text = font.render("À espera do oponente...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2)) # Centramento do texto
    else: # Textos após a conexão do Oponente 
        font = pygame.font.SysFont("arial", 50)
        text = font.render("A tua escolha", 1, (212, 180, 131))
        win.blit(text, (80, 200))

        text = font.render("Oponente", 1, (212, 180, 131))
        win.blit(text, (380, 200))
        # Movimentos dos jogadores / escolha do pedra papel ou tesoura
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent(): # caso os dois moverem. 
            text1 = font.render(move1, 1, (0,0,0)) #Fazer os dois locks 
            text2 = font.render(move2, 1, (0, 0, 0))
        else: # Caos um deles jogar 
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0)) #movimento 
            elif game.p1Went:
                text1 = font.render("Pronto!", 1, (0, 0, 0))# Lock do turno 
            else:
                text1 = font.render("À Espera...", 1, (0, 0, 0))# à espera do outro jogador

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))# movimento do 2º jogador
            elif game.p2Went:
                text2 = font.render("Pronto!", 1, (0, 0, 0)) # lock do turno
            else:
                text2 = font.render("À Espera...", 1, (0, 0, 0))# à esperda do outro jogador

        #Desenho dos Textos descritos acima 
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update() # update da tela 

#Criação dos objectos "button" Com os botões tamanhos, posições cores e imagens necessárias 
btns = [Button("Rocha", 50, 500, (27, 73, 101), "./assets/rock.png" ), Button("Tesoura", 250, 500, (98, 182, 203), "./assets/scissors.png" ), Button("Papel", 450, 500, (202, 233, 255), "./assets/paper.png" )]

#Este é o programa principal, o que irá executar o jogo 

def main():
    run = True # Para efeitos de desligar ou ligar 
    clock = pygame.time.Clock() # iniciar o tempo do jogo 
    n = Network() # Chamar a parte de Network 
    player = int(n.getP()) # Conversão e chamada dos jogadores 
    print("És o jogador", player)
    #Enquanto  O jogo estive em Run, ele irácontinuar até ao jogador quiser parar 
    while run:
        clock.tick(60)
        try:
            game = n.send("get") # Enviar get para a Rede
        except:
            run = False
            print("Não há jogo") # Falha ao perguntar por um jogo 
            break

        if game.bothWent():
            windowUpdate(win, game, player) # Desenho e redesenho da janela para continuar o jogo 
            pygame.time.delay(500) # Delay para permitir a fluidez 
            try:
                game = n.send("reset") # Reset depois de jogarem 
            except:
                run = False 
                print("Não há jogo") # Falalha do Jogo 
                break

            #fim do jogo
            font = pygame.font.SysFont("arial", 90) # Fonte 
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0): # Caso o player ganhar 
                text = font.render("Ganhaste!", 1, (255,0,0)) 
            elif game.winner() == -1: # Caso for um empate 
                text = font.render("Empate", 1, (255,0,0))
            else: # Caso o player perder 
                text = font.render("Perdeu...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
         # Para sair do jogo 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        windowUpdate(win, game, player) #Redesenho da Janela

#
# Menu do jogo / página principal
#
def menuPrincipal():
    run = True #Run true
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((190, 233, 232)) # cor do Background 
        font = pygame.font.SysFont("arial", 60) # Fonte do " Carrega para jogar! "
        text = font.render("Carrega para jogar!", 1, (255,0,0)) # Render
        win.blit(text, (100,200))
        pygame.display.update()

        #Sair do jogo 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    # incio do jogo 
    main()

# Screen peincipal
while True:
    menuPrincipal()
