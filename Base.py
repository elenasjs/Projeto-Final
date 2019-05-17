import pygame
import pygame.locals
from random import randrange
import sys, pygame
import numpy as np

jogando = 1
pygame.init()
definicao = width, height = 1000, 800
tela = pygame.display.set_mode(definicao)
relogio =pygame.time.Clock()
FPS = 40
arial = pygame.font.match_font('arial')
vermelho = (230,0,0)

def Escreve(texto,size,fonte,cor,x,y):
    font = pygame.font.Font(fonte,size)
    ts = font.render(texto,True,cor)
    texto_rect = ts.get_rect()
    texto_rect.midtop = (x,y)
    tela.blit(ts,texto_rect)

class Jogador(pygame.sprite.Sprite):

    def __init__(self,foto_peao,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(foto_peao)
        self.image = pygame.transform.scale(self.image,(170,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self,dado):
    	if self.rect.y <=20:
    		self.rect.x += dado*20
    	if self.rect.x >= 790:
    		self.rect.y += dado*20
    	if self.rect.x > 20 and self.rect.y >= 700:
    		self.rect.x -= dado*20
    	if self.rect.x <= 20 and self.rect.y > 10:
    		self.rect.y -= dado*20


class Fundo(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("tabuleiro.png").convert()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


player_group = pygame.sprite.Group()
fundo_group = pygame.sprite.Group()

player_1 = Jogador("imagem_peao.png",5,5)
fundo = Fundo(0,0)

player_group.add(player_1)
fundo_group.add(fundo)


dado = "-1"

jogando = True
while jogando:
	relogio.tick(FPS)
	fundo_group.draw(tela)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
			if event.key == pygame.K_SPACE:
				dado = np.random.randint(1,7)
				player_1.move(dado)


	
	Escreve("Dado Sorteado: {}".format(dado),28,arial,vermelho,200,160)
	player_group.draw(tela)

	pygame.display.update()
	pygame.display.flip()




