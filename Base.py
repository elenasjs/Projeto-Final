import pygame.locals
from random import randrange
import sys, pygame, os, time
import numpy as np
from Casa import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.mixer.init()
definicao = width, height = 1300, 800
tela = pygame.display.set_mode(definicao)
relogio =pygame.time.Clock()
FPS = 40
arial = pygame.font.match_font('arial')
vermelho = [230,0,0]
branco = [255,255,255]
preto = [0,0,0]
laranja = [255,100,0]
azul = [0,0,255]
roxo = [127,0,255]
amarelo = [255,255,0]
verde = [0,255,0]
rosa = [255,0,255]
azulClaro = [0,250,255]

colors = {}
colors["vermelho"] = vermelho
colors["laranja"] = laranja
colors["azul"] = azul
colors["roxo"] = roxo
colors["amarelo"] = amarelo
colors["verde"] = verde
colors["rosa"] = rosa
colors["azul claro"] = azulClaro

quants = {}
quants["yellow"] = 4
quants["parking"] = 2
quants["vermelho"] = 3
quants["laranja"] = 3
quants["azul"] = 2
quants["roxo"] = 2
quants["amarelo"] = 3
quants["verde"] = 3
quants["rosa"] = 3
quants["azul claro"] = 3


def Escreve(texto,size,fonte,cor,x,y):
    font = pygame.font.Font(fonte,size)
    ts = font.render(texto,True,cor)
    texto_rect = ts.get_rect()
    texto_rect.midtop = (x,y)
    tela.blit(ts,texto_rect)

def Carta(player, casa):
    start_time = time.time()
    elapsed_time = 0
    if str(type(casa)) == "<class 'Casa.CasaAPS'>":
        carta = APSdict[np.random.randint(0,len(APSdict))]
    else:
        carta = provaDict[np.random.randint(0,len(provaDict))]
    if carta["tipo"] == "dp":
        player.dpzou()
    elif carta["tipo"] == "freePass":
        player.freePass += 1
    elif carta["tipo"] == "money":
        if player.money < carta["money"] and carta["money"] < 0:
            player.money = 0
            player.faliu = True
        else:
            player.money += carta["money"]
    while elapsed_time < 4:
        Escreve("{0}".format(carta["texto"]),28,arial,vermelho,400,400)
        player_group.draw(tela)
        sideMenu()
        pygame.display.update()
        pygame.display.flip()
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

def Compra(player, casa):
    if casa.owner == None:
        if player.money > casa.cost:
            transaction = True
            while transaction:
                Escreve("Deseja comprar {0} por {1}R$ (y/n)".format(casa.name, casa.cost),28,arial,vermelho,400,400)
                player_group.draw(tela)
                sideMenu()
                pygame.display.update()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                        if event.key == pygame.K_y:
                            casa.owner = player.name
                            player.money -= casa.cost
                            player.propriedades.append(casa)
                            transaction = False
                        if event.key == pygame.K_n:
                            transaction = False
        elif casa.owner != player.name:
            aluguel = casa.getAluguel()
            if player.money > aluguel:
                player.money -= aluguel
            else:
                player.faliu = True
                aluguel = player.money
                player.money = 0
            for owner in player_group:
                if owner.name == casa.owner:
                    owner.money += aluguel
    elif casa.owner == player.name and casa.quantHouse < 1:
        transaction = True
        while transaction:
            Escreve("Deseja colocar uma casa em {0} por {1}R$ (y/n)".format(casa.name, casa.houseCost),28,arial,vermelho,400,400)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_y:
                        player.money -= casa.houseCost
                        house = casa.addHouse(player.rect.center)
                        constructions_group.add(house)
                        transaction = False
                    if event.key == pygame.K_n:
                        transaction = False
            player_group.draw(tela)
            sideMenu()
            pygame.display.update()
            pygame.display.flip()

def pobre(player):
    global jogando, n, lineY
    for prop in player.propriedades:
        prop.owner = None
    jogando -= 1
    n -= 1
    lineY = height/jogando
    actualPlayer.remove(player.number)
    player_group.remove(player)
    player.kill()

def sideMenu():
        for y in range(jogando):
            pygame.draw.line(tela, preto, (1000,y*lineY), (width, y*lineY), 5)
        pygame.draw.line(tela, preto, (1000,height), (width, height), 5)
        Y = 0
        for player in player_group:
            Escreve(str(player.name), 20, arial, preto, 1040, Y*lineY+10)
            Escreve("{0}R$".format(player.money), 20, arial, preto, 1040, Y*lineY+35)
            Escreve(("Tchau DP: {0}").format(player.freePass), 20, arial, preto, 1150, Y*lineY+10)
            for p, n in zip(player.propriedades, range(len(player.propriedades))):
                try:
                    Escreve("{0}".format(p.name), 20, arial, colors[p.color], 1150, Y*lineY+50+n*25)
                except:
                    Escreve("{0}".format(p.name), 20, arial, preto, 1150, Y*lineY+50+n*25)
            Y += 1
        pygame.draw.line(tela, preto, (width,0), (width, height), 5)
        pygame.draw.line(tela, preto, (1000,height), (1000, 0), 2)

def dplandia(player, dado1, dado2):
    dados = False
    if player.freePass > 0:
        transaction = True
        while transaction:
            Escreve("Deseja colocar gastar uma de duas cartas pra sair da dp(y/n)",28,arial,vermelho,400,400)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_y:
                        player.freePass -= 1
                        player.inDP = False
                        transaction = False
                    if event.key == pygame.K_n:
                        transaction = False
                        dados = True
            player_group.draw(tela)
            sideMenu()
            pygame.display.update()
            pygame.display.flip()
    if player.freePass <= 0 or dados:
        if dado1 == dado2:
            player.inDP = False


class Jogador(pygame.sprite.Sprite):
    def __init__(self, foto_peao, x, y, name, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(foto_peao).convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.rect.centerx = x/2
        self.rect.centery = y
        self.position = 0
        self.money = 1500
        self.inDP = False
        self.name = name
        self.freePass = 0
        self.faliu = False
        self.number = number
        self.propriedades = []

        movsLinear1 = [(int(2000-x+X*82),y-675) for X in np.arange(0,10,1)]
        movsVert1 = [(y+200,int(70+65*Y)) for Y in np.arange(1,11,1)]
        movsLinear2 = [(int(175+X*82),height-115/2) for X in np.arange(8,-2,-1)]
        movsVert2 = [(820-y,int(70+65*Y)) for Y in np.arange(9,-1,-1)]

        self.movs = movsLinear2 + movsVert2 + movsLinear1 + movsVert1

    def dpzou(self):
        self.inDP = True
        self.position = 9
        self.rect.center = self.movs[self.position]

    def useCasa(self):
        tela.fill(branco)
        fundo_group.draw(tela)
        player_group.draw(tela)
        sideMenu()
        pygame.display.update()
        pygame.display.flip()
        casa = lista_Casas[self.position]
        if str(type(casa)) == "<class 'Casa.CasaGoToDP'>":
            self.dpzou()

        elif str(type(casa)) == "<class 'Casa.casaEvento'>":
            if self.money > casa.cost:
                self.money -= casa.cost
            else:
                self.faliu = True

        elif str(type(casa)) != "<class 'Casa.CasaDP'>" and str(type(casa)) != "<class 'Casa.CasaVoid'>" and str(type(casa)) != "<class 'Casa.CasaGoToDP'>":
            return casa

    def move(self,dado1, dado2):
        if not self.inDP:
            for e in range(dado1+dado2):
                sound = pygame.mixer.Sound('audio_movimento.ogg')
                pygame.mixer.Sound.set_volume(sound,0.3)
                pygame.mixer.Sound.play(sound)
                try:
                    self.position += 1
                    self.rect.center = self.movs[self.position]
                except:
                    self.position = 0
                    self.rect.center = self.movs[self.position]
                start_time = time.time()
                elapsed_time = 0
                while elapsed_time < 0.5:
                    elapsed_time = time.time() - start_time
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                    relogio.tick(FPS)
                    tela.fill(branco)
                    fundo_group.draw(tela)
                    if dado1 != None:
                        Escreve("Dado Sorteado: {}".format(dado1),28,arial,vermelho,500,400)
                    if dado2 != None:
                        Escreve("Dado Sorteado: {}".format(dado2),28,arial,vermelho,500,450)
                    player_group.draw(tela)
                    sideMenu()
                    pygame.display.update()
                    pygame.display.flip()

                casa = lista_Casas[self.position]
                if str(type(casa)) == "<class 'Casa.CasaPicPay'>":
                    self.money += casa.money



class Fundo(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Imagem_Tabuleiro.png").convert()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

player_group = pygame.sprite.Group()
fundo_group = pygame.sprite.Group()
constructions_group = pygame.sprite.Group()

fundo = Fundo(0,0)
fundo_group.add(fundo)

lista_Casas = []
lista_Casas.append(CasaPropriedade(position=0, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=100, color="roxo", name="CEMP", aluguel=200))
lista_Casas.append(CasaProvas(position=1))
lista_Casas.append(CasaPropriedade(position=2, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=150, color="roxo", name="MAQUINA DE LANCHES", aluguel=200))
lista_Casas.append(casaEvento(position=3, name="PROVA SUBSTITURIVA PAGUE R$200", cost=200))
lista_Casas.append(CasaYellow(position=4, name="YELLOW BIKE", cost=200, aluguel=100))
lista_Casas.append(CasaPropriedade(position=5, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=150, color="azul claro", name="SALA DAS ENTIDADES", aluguel=200))
lista_Casas.append(CasaAPS(position=6))
lista_Casas.append(CasaPropriedade(position=7, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=200, color="azul claro", name="REFEITORIO", aluguel=200))
lista_Casas.append(CasaPropriedade(position=8, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=300, color="azul claro", name="SALA DOS PROFESSORES", aluguel=200))
lista_Casas.append(CasaDP(position=9))
lista_Casas.append(CasaPropriedade(position=10, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=400, color="rosa", name="LAB DE CEMP. (4 ANDAR)", aluguel=200))
lista_Casas.append(CasaParking(position=11, name="PARKING PREDIO 1", cost=150, aluguel=100))
lista_Casas.append(CasaPropriedade(position=22, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=350, color="rosa", name="LAB. 2 (4 ANDAR)", aluguel=200))
lista_Casas.append(CasaPropriedade(position=13, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=350, color="rosa", name="LAB. 2 (4 ANDAR)", aluguel=200))
lista_Casas.append(CasaYellow(position=14, name="GRIN PATINETE", cost=400, aluguel=100))
lista_Casas.append(CasaPropriedade(position=15, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=700, color="laranja", name="SALAS DE AULAS PREDIO 2", aluguel=200))
lista_Casas.append(CasaProvas(position=16))
lista_Casas.append(CasaPropriedade(position=17, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=450, color="laranja", name="SALAS DE AULAS PREDIO 1", aluguel=200))
lista_Casas.append(CasaPropriedade(position=18, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=300, color="laranja", name="AFFARI CAFE", aluguel=200))
lista_Casas.append(CasaVoid(position=19, name="KZA CAFE FREE COFFE"))
lista_Casas.append(CasaPropriedade(position=20, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=400, color="red", name="LAB.TERMO", aluguel=200))
lista_Casas.append(CasaAPS(position=21))
lista_Casas.append(CasaPropriedade(position=22, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=450, color="red", name="AUDITORIO", aluguel=200))
lista_Casas.append(CasaPropriedade(position=23, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=350, color="red", name="LAB DE CONTROLE E AUTOMAÇÃO (SUB. 1)", aluguel=200))
lista_Casas.append(CasaYellow(position=24, name="YELLOW E-BIKE", cost=550, aluguel=100))
lista_Casas.append(CasaPropriedade(position=25, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=180, color="yellow", name="HELP DESK", aluguel=200))
lista_Casas.append(CasaPropriedade(position=26, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=400, color="yellow", name="BIBLIOTECA", aluguel=200))
lista_Casas.append(CasaParking(position=27, name="PARKING PREDIO 2", cost=150, aluguel=100))
lista_Casas.append(CasaPropriedade(position=28, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=230, color="yellow", name="CASA DO PAO DE QUEIJO", aluguel=200))
lista_Casas.append(CasaGoToDP(position=29, name="VOCÊ FICOU DE DP"))
lista_Casas.append(CasaPropriedade(position=30, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=400, color="green", name="PROFESSORES", aluguel=200))
lista_Casas.append(CasaPropriedade(position=31, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=250, color="green", name="QUADRA PREDIO 1", aluguel=200))
lista_Casas.append(CasaProvas(position=32))
lista_Casas.append(CasaPropriedade(position=33, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=500, color="green", name="LAB DE R.V.", aluguel=200))
lista_Casas.append(CasaYellow(position=34, name="YELLOW PATINETE", cost=400, aluguel=100))
lista_Casas.append(CasaAPS(position=35))
lista_Casas.append(CasaPropriedade(position=36, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=800, color="blue", name="FABLAB", aluguel=200))
lista_Casas.append(casaEvento(position=37, name="MENSALIDADE PAGUE", cost=200))
lista_Casas.append(CasaPropriedade(position=38, houseMultiplier=0.2, buildingMultiplier=0.4, houseCost=500, buildingCost=2000, cost=1000, color="blue", name="TECHLAB", aluguel=200))
lista_Casas.append(CasaPicPay(position=39))

dado1 = None
dado2 = None

APSdict = {}
provaDict = {}
for e in range(6):
    APSdict[e] = {}
    provaDict[e] = {}
    provaDict[e]["texto"] = "texto generico"
    provaDict[e]["tipo"] = "nenhum"

APSdict[0]["texto"] = "Parabens, a sua APS foi tao boa que você ganhou 300R$"
APSdict[0]["money"] = 300
APSdict[0]["tipo"] = "money"

APSdict[1]["texto"] = "Ops, a sua APS foi tao ruim que você perdeu 200R$"
APSdict[1]["money"] = -200
APSdict[1]["tipo"] = "money"

APSdict[2]["texto"] = "Sem querer olhou o git do amigo e copiou tudo, DP..."
APSdict[2]["tipo"] = "dp"

APSdict[3]["texto"] = "Ops, a sua APS foi tao ruim que você perdeu 200R$"
APSdict[3]["money"] = -400
APSdict[3]["tipo"] = "money"

APSdict[4]["texto"] = "Mano, sua APS foi tão boa agora você né o novo professor"
APSdict[4]["money"] = 300
APSdict[4]["tipo"] = "money"

APSdict[5]["texto"] = "O nerdao da sala ta no seu grupo da APS, com isso tu sai da dp facilmente"
APSdict[5]["tipo"] = "freePass"

provaDict[0]["texto"] = "Pra estudar pras pf tu gastou 500 conto em redbull"
provaDict[0]["tipo"] = "money"
provaDict[0]["money"] = -500

provaDict[1]["texto"] = "As pf tao ai e tu n sabe nada, pague R$200 um veterano pra te ajudar"
provaDict[1]["tipo"] = "money"
provaDict[1]["money"] = -200

provaDict[2]["texto"] = "As pf tao ai e tu n sabe nada, pague R$200 um veterano pra te ajudar"
provaDict[2]["tipo"] = "money"
provaDict[2]["money"] = -200

provaDict[3]["texto"] = "Não te pegaram colando na prova de instrumed"
provaDict[3]["tipo"] = "money"
provaDict[3]["money"] = 300

provaDict[4]["texto"] = "Te pegaram colando na prova de instrumed, DP..."
provaDict[4]["tipo"] = "dp"

provaDict[5]["texto"] = "Tu tirou 4.95, mas fez amizade com o prof arredondou sua nota te tirando da DP"
provaDict[5]["tipo"] = "freePass"

casaPropriedades = ["<class 'Casa.CasaPropriedade'>", "<class 'Casa.CasaYellow'>", "<class 'Casa.CasaParking'>"]


menuPlayersQuant = True
while menuPlayersQuant:
    relogio.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_2:
                full = True
                menuPlayersQuant = False
                jogando = 2

            if event.key == pygame.K_3:
                full = True
                menuPlayersQuant = False
                jogando = 3

            if event.key == pygame.K_4:
                full = True
                menuPlayersQuant = False
                jogando = 4


    tela.fill(branco)
    Escreve("MonoInsper",80,arial,preto,width/2,50)
    Escreve("Quantidade de players: 2 - 4",40 ,arial, preto, width/2, 200)
    pygame.display.update()
    pygame.display.flip()

actualPlayer = [x+1 for x in range(jogando)]
n = 0

lineY = height/jogando

if jogando >= 1:
    name1 = "Player 1"
    player_1 = Jogador("Imagem_Peao_1.png",2000-170,800-25, name=name1, number=1)
    player_group.add(player_1)
if jogando >= 2:
    name2 = "Player 2"
    player_2 = Jogador("Imagem_Peao_2.png",2000-170,800-50, name=name2, number=2)
    player_group.add(player_2)
if jogando >= 3:
    name3 = "Player 3"
    player_3 = Jogador("Imagem_Peao_3.png",2000-170,800-75, name=name3, number=3)
    player_group.add(player_3)
if jogando >= 4:
    name4 = "Player 4"
    player_4 = Jogador("Imagem_Peao_4.png",2000-170,800-100, name=name4, number=4)
    player_group.add(player_4)


menu = True
while full:
    while menu:
        relogio.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    inGame = True
                    menu = False

        tela.fill(branco)
        Escreve("MonoInsper",80,arial,preto,width/2,50)

        Escreve("Regras: ",40,arial,preto,width/2-300,200)
        Escreve("- Espaço: lança os dados",40,arial,preto,width/2-100,250)
        Escreve("- Toda vez que passar pelo PicPay, você ganha 350R$",40,arial,preto,width/2+130,300)

        Escreve("Espaço para continuar",40,arial,preto,width/2,height/2+300)

        pygame.display.update()
        pygame.display.flip()

    while inGame:
        relogio.tick(FPS)
        tela.fill(branco)
        fundo_group.draw(tela)
        Escreve("P --> pause",20,arial,preto,200,660)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    player_1.faliu = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_p:
                    inGame = False
                    menu = True
                if event.key == pygame.K_SPACE:
                    sound = pygame.mixer.Sound('Audio_Dados.ogg')
                    pygame.mixer.Sound.set_volume(sound,0.3)
                    pygame.mixer.Sound.play(sound)
                    start_time = time.time()
                    elapsed_time = 0
                    while elapsed_time < 2:
                        elapsed_time = time.time() - start_time
                    dado1 = np.random.randint(1,7)
                    dado2 = np.random.randint(1,7)
                    for player in player_group:
                        if player.faliu:
                            pobre(player)
                        if actualPlayer[n] == player.number:
                            if not player.inDP:
                                player.move(dado1, dado2)
                            else:
                                dplandia(player, dado1, dado2)
                            casa = player.useCasa()
                            if casa != None:
                                if str(type(casa)) not in casaPropriedades and str(type(casa)) != "<class 'Casa.CasaDP'>":
                                    Carta(player, casa)
                                if str(type(casa)) in casaPropriedades:
                                    Compra(player, casa)
                    if actualPlayer[n] < jogando:
                        n += 1
                    else:
                        n = 0
        casa =  None
        if len(player_group) <= 1:
            print("end game")
            inGame = False
            endGame = True
            full = False
            for player in player_group:
                vencedor = player
            break
        sideMenu()

        if dado1 != None:
            Escreve("Dado Sorteado: {}".format(dado1),28,arial,vermelho,500,400)
        if dado2 != None:
            Escreve("Dado Sorteado: {}".format(dado2),28,arial,vermelho,500,450)

        player_group.draw(tela)
        constructions_group.draw(tela)
        pygame.display.update()
        pygame.display.flip()

while endGame:
    relogio.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                endGame = False

    tela.fill(branco)
    Escreve("MonoInsper",80,arial,preto,width/2,50)
    Escreve("O vencedor foi {0}".format(vencedor.name),40,arial,preto,width/2,height/2)
    Escreve("Espaço para terminar",40,arial,preto,width/2,height/2+300)

    pygame.display.update()
    pygame.display.flip()
