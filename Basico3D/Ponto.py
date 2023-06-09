# ************************************************
#   Ponto.py
#   Define a classe Ponto
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************
from math import cos, sin

""" Classe Ponto """
class Ponto:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    """ Imprime os valores de cada eixo do ponto """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            print (msg, self.x, self.y, self.z)
        else:
            print (self.x, self.y, self.z)

    """ Define os valores dos eixos do ponto """
    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
# Definicao de operadores
# https://www.programiz.com/python-programming/operator-overloading

    def __add__(self, other):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
            return Ponto(x, y, z)

    def __mul__(self, other: int):
            x = self.x * other
            y = self.y * other
            z = self.z * other
            return Ponto(x, y, z)

    def RotateY(self, angulo):
        print('oiii')
        anguloRad = angulo * 3.14159265359/180.0;
        xr =  self.x*cos(anguloRad) + self.z*sin(anguloRad);
        zr = -self.x*sin(anguloRad) + self.z*cos(anguloRad);
        return Ponto(xr, self.y, zr)



# ********************************************************************** */
#                                                                        */
#  Calcula a interseccao entre 2 retas (no plano "XY" Z = 0)             */
#                                                                        */
# k : ponto inicial da reta 1                                            */
# l : ponto final da reta 1                                              */
# m : ponto inicial da reta 2                                            */
# n : ponto final da reta 2                                              */
# 
# Retorna:
# 0, se não houver interseccao ou 1, caso haja                           */
# int, valor do parâmetro no ponto de interseção (sobre a reta KL)       */
# int, valor do parâmetro no ponto de interseção (sobre a reta MN)       */
#                                                                        */
# ********************************************************************** */
def intersec2d(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> (int, float, float):
    det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

    if (det == 0.0):
        return 0, None, None # não há intersecção

    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

    return 1, s, t # há intersecção

# **********************************************************************
# HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto)
# Detecta interseccao entre os pontos
#
# **********************************************************************
def HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> bool:
    ret, s, t = intersec2d( k,  l,  m,  n)

    if not ret: return False

    return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0

