import pygame

class CasaPropriedade():
    def __init__(self, position, houseMultiplier, buildingMultiplier, cost, color, name, houseCost, buildingCost, aluguel):
        self.position = position
        self.quantHouse = 0
        self.houseMultiplier = houseMultiplier
        self.houseCost = houseCost
        self.quantBuildings = 0
        self.buildingMultiplier = buildingMultiplier
        self.buildingCost = buildingCost
        self.cost = cost
        self.monopoly = False
        self.owner = None
        self.color = color
        self.name = name
        self.aluguel = aluguel

    def addHouse(self, xy):
        self.quantHouse += 1
        return House("casa.png",xy)

    def addBuilding(self):
        if self.quantHouse > 4:
            self.quantBuildings += 1
            self.quantHouse -= 4

    def getAluguel(self):
        houseCost = self.aluguel * self.quantHouse * self.houseMultiplier
        buildingCost = self.aluguel * self.quantBuildings * self.buildingMultiplier
        return self.aluguel + buildingCost + houseCost

    def buyProperty(self, owner):
        self.owner = owner

    def sellHouses(self, quant):
        self.quantHouse -= quant
        return self.houseCost*quant*0.7

    def sellBuildings(self, quant):
        self.quantBuildings -= quant
        return self.buildingCost*quant*0.7

class CasaGoToDP():
    def __init__(self, position, name):
        self.position = position
        self.name = name

    def dpzou(self, player):
        player.position = self.position
        player.inDP = True

class CasaDP():
    def __init__(self, position):
        self.position = position

class CasaVoid():
    def __init__(self, position, name):
        self.position = position
        self.name = name

class CasaParking():
    def __init__(self, position, name, cost, aluguel):
        self.position = position
        self.owner = None
        self.name = name
        self.cost = cost
        self.aluguel = aluguel
        self.monopoly = False
        self.color = "parking"

    def getAluguel(self):
        if self.monopoly:
            return self.aluguel*2
        return self.aluguel


class casaEvento():
    def __init__(self, position, name, cost):
        self.position = position
        self.name = name
        self.cost = cost

class CasaYellow():
    def __init__(self, position, name, cost, aluguel):
        self.position = position
        self.owner = None
        self.name = name
        self.cost = cost
        self.aluguel = aluguel
        self.monopoly = False
        self.color = "yellow"

    def getAluguel(self):
        if monopoly:
            return self.aluguel*2
        return self.aluguel

class CasaAPS():
    def __init__(self, position):
        self.position = position
        self.name = "APS"

class CasaProvas():
    def __init__(self, position):
        self.position = position
        self.name = "PROVAS FINAIS"

class CasaPicPay():
    def __init__(self, position):
        self.position = position
        self.name = "CASH BACK PICPAY R$350"
        self.money = 350

class House(pygame.sprite.Sprite):
    def __init__(self, imagem, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagem).convert_alpha()
        self.image = pygame.transform.scale(self.image,(25,25))
        self.rect = self.image.get_rect()
        self.rect.center = xy + (20,20)
