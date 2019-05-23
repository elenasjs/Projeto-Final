import pygame
import pygame.locals
from random import randrange
import sys, pygame
import numpy as np
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

jogando = 1
pygame.init()
definicao = width, height = 1000, 800
tela = pygame.display.set_mode(definicao)
relogio =pygame.time.Clock()
FPS = 40
arial = pygame.font.match_font('arial')
vermelho = (230,0,0)

branco = [255,255,255]

movsLinear1 = [80]+[int(175+x*82) for x in np.arange(-1,10,1)]
movsLinear2 = movsLinear1[::-1]
movsVert1 = [int(70+65*y) for y in np.arange(-1,11,1)]
movsVert2 = movsVert1[::-1]
movsVert2.remove(5)

print(movsVert2)

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
		self.image = pygame.transform.scale(self.image,(50,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.position = 1

	def move(self,dado):
		for e in range(dado):
			self.position += 1
			if self.position < 11:
				self.rect.centerx = movsLinear1[self.position]
				self.rect.centery = 115/2
			elif self.position < 22:
				self.rect.centerx = 920
				self.rect.centery = movsVert1[self.position-10]
			elif self.position < 31:
				self.rect.centerx = movsLinear2[self.position-21]
				self.rect.centery = height-115/2
			elif self.position < 42:
				self.rect.centerx = 80
				self.rect.centery = movsVert2[self.position-31]
			else:
				self.position = 2
				self.rect.centerx = movsLinear1[self.position]
				self.rect.centery = 115/2


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
dado2 = "-1"

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
				dado2 = np.random.randint(1,7)
				player_1.move(dado+dado2)



	Escreve("Dado Sorteado: {}".format(dado),28,arial,vermelho,500,400)
	Escreve("Dado Sorteado: {}".format(dado2),28,arial,vermelho,500,450)
	player_group.draw(tela)

	pygame.display.update()
	pygame.display.flip()
