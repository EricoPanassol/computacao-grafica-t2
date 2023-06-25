from TPoint import TPoint
from TTriangle import TTriangle
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Objeto3D:
    def __init__(self):
        self.faces = []
        self.nFaces = 0
    
    def getNFaces(self):
        return self.nFaces
    
    def LeObjeto(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as file:
                self.nFaces = int(file.readline())

                for _ in range(self.nFaces):
                    vertices = file.readline().split()
                    if len(vertices) >= 9:
                        # Primeiro vértice
                        x1, y1, z1 = map(float, vertices[:3])
                        p1 = TPoint(x1, y1, z1)

                        # Segundo vértice
                        x2, y2, z2 = map(float, vertices[3:6])
                        p2 = TPoint(x2, y2, z2)

                        # Terceiro vértice
                        x3, y3, z3 = map(float, vertices[6:9])
                        p3 = TPoint(x3, y3, z3)

                        # Criar o triângulo e atribuir os pontos
                        triangle = TTriangle(p1, p2, p3)

                        # Adicionar o triângulo ao vetor de faces
                        self.faces.append(triangle)
                    else:
                        # Lidar com a situação em que há menos de nove valores na linha
                        print("Erro: Linha inválida no arquivo.")

        except FileNotFoundError:
            print(f"Erro na abertura do arquivo {nome_arquivo}.")

    def ExibeObjeto(self):
        for face in self.faces:
            normal = face.CalculaNormal()
            
            glColor3f(1,1,1) # desenha QUAD preenchido
            glBegin ( GL_QUADS )
            glNormal3f(normal.x,normal.y,normal.z)
            glVertex3f(face.P1.x, face.P1.y, face.P1.z)
            glVertex3f(face.P2.x, face.P2.y, face.P2.z)
            glVertex3f(face.P3.x, face.P3.y, face.P3.z)
            glEnd()
          