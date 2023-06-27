from Ponto import Ponto
import numpy as np


class Triangulo:   
    def __init__(self, P1:Ponto,P2:Ponto,P3:Ponto):
        self.p1 = P1
        self.p2 = P2
        self.p3 = P3
        self.normal:Ponto = self.CalculaNormal()

    def imprime(self):
        print(f"Triangulo:")
        self.p1.imprime()
        self.p2.imprime()
        self.p3.imprime()
        print(f"Normal:")
        self.normal.imprime()

    def CalculaNormal(self):
        v1 = self.p2.__sub__(self.p1)
        v2 = self.p3.__sub__(self.p1)

        normal = np.cross([v1.x, v1.y, v1.z],[v2.x,v2.y,v2.z])
        vetNormal= Ponto(normal[0],normal[1],normal[2])

        return vetNormal