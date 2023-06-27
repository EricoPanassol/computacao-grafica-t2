# ***********************************************************************************
#   OpenGLBasico3D-V5.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe dois Cubos em OpenGL
#   Para maiores informações, consulte
# 
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Outro exemplo de código em Python, usando OpenGL3D pode ser obtido em
#   http://openglsamples.sourceforge.net/cube_py.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# 
# ***********************************************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
from Objeto3D import Objeto3D
from copy import copy
import numpy as np 
from PIL import Image
import random
import os.path
import time
import playsound
from ListaDeCores import *

Angulo = 0.0
Angulo_Carro = 0.0
Pos_Carro = Ponto(160,0,50)
alvo = Ponto(Pos_Carro.x,0,Pos_Carro.z+5)
alvo_camera = Ponto(0,0,0)
observador = Ponto(0, 4, 13)
moving = False
camera_view = 0
Texturas = []
gasolinas_no_mapa = 0
gasolinas = []
max_tanque = 100
tanque = 100
matriz = []
texture_sizes = []

mapLargura = 30
mapComprimento = 30
tamLadrilho = 9
buildingsHeightList = []
buildingsWallTextureList = []

# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
#/ **********************************************************************
def init():
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(76/256, 169/256, 250/256, 1.0)

    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable (GL_CULL_FACE )
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #image = Image.open("Tex.jpg")
    #print ("X:", image.size[0])
    #print ("Y:", image.size[1])
    #image.show()
   
# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
	# Evita divisÃ£o por zero, no caso de uam janela com largura 0.
    if h == 0:
        h = 1
    # Ajusta a relaÃ§Ã£o entre largura e altura para evitar distorÃ§Ã£o na imagem.
    # Veja funÃ§Ã£o "PosicUser".
    AspectRatio = w / h
	# Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)
    
    PosicUser()
# **********************************************************************
def DefineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente = [0.4, 0.4, 0.4] 
    LuzDifusa   = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9]
    PosicaoLuz0  = [2.0, 3.0, 0.0 ]  # PosiÃ§Ã£o da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable ( GL_COLOR_MATERIAL )

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)

# **********************************************************************
# DesenhaCubos()
# Desenha o cenario
#
# **********************************************************************

def enche_tanque():
    global tanque, max_tanque

    if tanque + 10 > max_tanque:
        tanque = max_tanque
        return
    
    tanque += 10

def DesenhaCubo():
    glutSolidCube(1)
    
def PosicUser():
    global camera_view, observador, alvo, Pos_Carro, alvo_camera, mapComprimento, mapLargura, tamLadrilho

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    # glViewport(0, 0, 500, 500)
    #print ("AspectRatio", AspectRatio)
    
    gluPerspective(60,AspectRatio,0.01,1000) # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #gluLookAt(observador.x, observador.y+2, observador.z, alvo.x,alvo.y,alvo.z, 0,1.0,0) 

    if camera_view == 0:
        vetor_alvo = alvo.__sub__(Pos_Carro)
        vetor_alvo = vetor_alvo.__mul__(1.5)

        obs_pos = Pos_Carro.__sub__(vetor_alvo)
        alvo_camera.x = alvo.x
        alvo_camera.z = alvo.z
        observador = Ponto(obs_pos.x, obs_pos.y+5, obs_pos.z)
    
    elif camera_view == 1:
        alvo_camera.x = alvo.x
        alvo_camera.z = alvo.z
        observador = Ponto(Pos_Carro.x,Pos_Carro.y+50,Pos_Carro.z)

    elif camera_view == 2:
        alvo_camera.x = alvo.x
        alvo_camera.y = alvo.y + 1
        alvo_camera.z = alvo.z
        observador = Ponto(Pos_Carro.x,Pos_Carro.y+1.8,Pos_Carro.z)

    elif camera_view == 3:
        alvo_camera.x = (tamLadrilho*mapComprimento)/2
        alvo_camera.y = 1
        alvo_camera.z = (tamLadrilho*mapLargura)/2
        observador = Ponto((tamLadrilho*mapLargura)/2,300,(tamLadrilho*mapComprimento)/2 - 1)

    gluLookAt(observador.x, observador.y, observador.z, alvo_camera.x,alvo_camera.y,alvo_camera.z, 0,1.0,0)

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho():
    global tamLadrilho
    
    glColor3f(0.5,0.5,0.5) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glTexCoord(0,0)
    glVertex3f(0,  0.0, 0)
    glTexCoord(0,1)
    glVertex3f(0,  0.0,  tamLadrilho)
    glTexCoord(1,1)
    glVertex3f( tamLadrilho,  0.0,  tamLadrilho)
    glTexCoord(1,0)
    glVertex3f( tamLadrilho,  0.0, 0)
    glEnd()
    
    # glColor3f(1,1,1) # desenha a borda da QUAD 
    # glBegin ( GL_LINE_STRIP )
    # glNormal3f(0,1,0)
    # glVertex3f(-7.5,  0.0, -7.5)
    # glVertex3f(-7.5,  0.0,  7.5)
    # glVertex3f( 7.5,  0.0,  7.5)
    # glVertex3f( 7.5,  0.0, -7.5)
    # glEnd()
    
# **********************************************************************
# DesenhaPiso()
# Função que desenha o piso da cidade
# **********************************************************************
def DesenhaPiso():
    global mapLargura, mapComprimento, tamLadrilho, matriz
    
    glPushMatrix()
    glTranslated(0,0,0)
    for x in range(0, mapLargura):
        glPushMatrix()
        for z in range(0, mapComprimento):
            UseTexture((matriz[z][x]))
            DesenhaLadrilho()
            glTranslated(0, 0, tamLadrilho)
        glPopMatrix()
        glTranslated(tamLadrilho, 0, 0)
    glPopMatrix()

    glPushMatrix()
    glTranslated(0,0,0)
    UseTexture(23)
    DesenhaAgua()
    glPopMatrix() 

def DesenhaAgua():
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glTexCoord(0,0)
    glVertex3f(-1000,  -4, -1000)
    glTexCoord(0,200)
    glVertex3f(-1000,  -4,  1000)
    glTexCoord(200,200)
    glVertex3f( 1000,  -4,  1000)
    glTexCoord(200,0)
    glVertex3f( 1000,  -4, -1000)
    glEnd()

def lerMatriz(arquivo):
    global mapLargura, mapComprimento, matriz
    
    with open(os.path.dirname(__file__) + arquivo, 'r') as file:
        linhas = file.readlines()
        mapLargura = len(linhas[1:])
        mapComprimento = len(linhas[1].strip().split()) 

        for linha in linhas[1:]:
            elementos = linha.strip().split()
            matriz.append([int(elemento) for elemento in elementos])

        setBuildings()

# **********************************************************************
# setBuildings()
# Sorteia as texturas dos prédios e suas alturas
# **********************************************************************
def setBuildings():
    global matriz, buildingsHeightList, buildingsWallTextureList
    qtdBuildings = 0
    while(qtdBuildings <= 50):
        for x in range(0, mapComprimento):
            for z in range(0, mapLargura):
                # print(f"x:{x} z:{z}")
                if matriz[z][x] == 0:
                    matriz[z][x] = random.choice([0,0,0,13,13])
                    buildingsHeightList.append(random.choice([10,20,30,40,50]))
                    buildingsWallTextureList.append(random.choice([14,15,16,17,18,19]))
                    qtdBuildings += 1

# **********************************************************************
# spawnBuilding()
# Desenha um prédio
# **********************************************************************
def spawnBuilding(altura, pontoInicial, tamanho, texture):
    
    rep_larg, rep_alt = calcular_repeticoes_tamanho(texture,altura,tamanho)
    
    UseTexture(texture)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(-1,0,0)
    glTexCoord(0,0)
    glVertex3f(pontoInicial.x,  0.0, pontoInicial.z)
    glTexCoord(0,rep_alt)
    glVertex3f( pontoInicial.x,  altura, pontoInicial.z)
    glTexCoord(rep_larg,rep_alt)
    glVertex3f( pontoInicial.x + tamanho,  altura,pontoInicial.z )
    glTexCoord(rep_larg,0)
    glVertex3f(pontoInicial.x + tamanho, 0.0 , pontoInicial.z)
    glEnd()

    UseTexture(texture)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,0,-1)
    glTexCoord(0,0)
    glVertex3f(pontoInicial.x + tamanho,  0.0, pontoInicial.z)
    glTexCoord(0,rep_alt)
    glVertex3f( pontoInicial.x + tamanho,  altura, pontoInicial.z)
    glTexCoord(rep_larg,rep_alt)
    glVertex3f( pontoInicial.x + tamanho,  altura, pontoInicial.z + tamanho )
    glTexCoord(rep_larg,0)
    glVertex3f(pontoInicial.x + tamanho, 0.0 , pontoInicial.z + tamanho )
    glEnd()

    UseTexture(texture)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(1,0,0)
    glTexCoord(0,0)
    glVertex3f(pontoInicial.x + tamanho,  0.0, pontoInicial.z + tamanho )
    glTexCoord(0,rep_alt)
    glVertex3f( pontoInicial.x + tamanho,  altura, pontoInicial.z + tamanho )
    glTexCoord(rep_larg,rep_alt)
    glVertex3f( pontoInicial.x,  altura, pontoInicial.z + tamanho  )
    glTexCoord(rep_larg,0)
    glVertex3f(pontoInicial.x, 0.0 , pontoInicial.z + tamanho )
    glEnd()

    UseTexture(texture)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,0,-1)
    glTexCoord(0,0)
    glVertex3f(pontoInicial.x,  0.0, pontoInicial.z + tamanho )
    glTexCoord(0,rep_alt)
    glVertex3f( pontoInicial.x,  altura, pontoInicial.z + tamanho )
    glTexCoord(rep_larg,rep_alt)
    glVertex3f(  pontoInicial.x,  altura, pontoInicial.z )
    glTexCoord(rep_larg,0)
    glVertex3f(pontoInicial.x, 0.0 , pontoInicial.z)
    glEnd()

    UseTexture(20)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glTexCoord(0,0)
    glVertex3f(pontoInicial.x,  altura, pontoInicial.z )
    glTexCoord(0,1)
    glVertex3f(pontoInicial.x, altura, pontoInicial.z + tamanho)
    glTexCoord(1,1)
    glVertex3f(  pontoInicial.x + tamanho,  altura, pontoInicial.z + tamanho)
    glTexCoord(1,0)
    glVertex3f( pontoInicial.x + tamanho,  altura, pontoInicial.z )
    glEnd()

# **********************************************************************
# spawnBuildings()
# Função que define os locais dos prédios lendo os 0 da matriz
# **********************************************************************
def spawnBuildings():
    global matriz, tamLadrilho, buildingsHeightList, buildingsWallTextureList
    aux = 0
    for x in range(0, mapLargura):
        for z in range(0, mapComprimento):
            if matriz[z][x] == 13:
                altura = buildingsHeightList[aux]
                wallTexture = buildingsWallTextureList[aux]
                pontoInicial = Ponto(x*tamLadrilho+0.5,0,z*tamLadrilho+0.5)
                tamanho = tamLadrilho - 1                
                spawnBuilding(altura,pontoInicial,tamanho, wallTexture)
                aux += 1
                
# **********************************************************************
# calcular_repeticoes_tamanho()
# Função que calcula as reps de uma textura em um determinado objeto
# **********************************************************************                       
def calcular_repeticoes_tamanho(textura, altura_obj, largura_obj):
    global texture_sizes

    largura_textura = texture_sizes[textura][0]  # Largura da textura
    altura_textura =  texture_sizes[textura][1]  # Altura da textura

    repeticoes_largura = int(largura_obj / (largura_textura/30)) + 1
    repeticoes_altura = int(altura_obj / (altura_textura/30)) + 1

    return repeticoes_largura, repeticoes_altura

# **********************************************************************
# LoadTexture()
# Função que carrega uma textura
# **********************************************************************
def LoadTexture(nome) -> int:
    # carrega a imagem
    image = Image.open(nome)

    # print(f"Texture Format: {GL_RGB}")
    # print ("X:", image.size[0])
    # print ("Y:", image.size[1])
    # converte para o formato de OpenGL 
    img_data = np.array(list(image.getdata()), np.uint8)

    # Habilita o uso de textura
    glEnable ( GL_TEXTURE_2D )

    #Cria um ID para texura
    texture = glGenTextures(1)
    errorCode =  glGetError()
    if errorCode == GL_INVALID_OPERATION: 
        print ("Erro: glGenTextures chamada entre glBegin/glEnd.")
        return -1

    # Define a forma de armazenamento dos pixels na textura (1= alihamento por byte)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Define que tipo de textura ser usada
    # GL_TEXTURE_2D ==> define que ser· usada uma textura 2D (bitmaps)
    # e o nro dela
    glBindTexture(GL_TEXTURE_2D, texture)

    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    errorCode = glGetError()
    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    # neste ponto, "texture" tem o nro da textura que foi carregada
    errorCode = glGetError()
    if errorCode == GL_INVALID_OPERATION:
        print ("Erro: glTexImage2D chamada entre glBegin/glEnd.")
        return -1

    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1
    #image.show()

    texture_sizes.append([image.size[0], image.size[1]])
    #print(texture_sizes)
    return texture

# **********************************************************************
# useTexture()
# Função que habilita o uso de textura
# **********************************************************************
def UseTexture (NroDaTextura: int):
    global Texturas
    if (NroDaTextura>len(Texturas)):
        print (f"Numero {NroDaTextura} invalido da textura.")
        glDisable (GL_TEXTURE_2D)
        return
    if (NroDaTextura < 0):
        glDisable (GL_TEXTURE_2D)
    else:
        glEnable (GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, Texturas[NroDaTextura])

# **********************************************************************
# testa_colisao()
# Função que testa a colisão do carro com o mapa
# **********************************************************************
def testaColisao(proxima_pos):
    global tamLadrilho, mapLargura, mapComprimento
    
    pos_x_matriz = proxima_pos.x/tamLadrilho
    pos_z_matriz = proxima_pos.z/tamLadrilho

    if pos_x_matriz >= mapLargura or pos_x_matriz <= 0:
        #print("colidiu por sair do x")
        return True

    if pos_z_matriz >= mapComprimento or pos_z_matriz <= 0:
        #print("colidiu por sair do z")
        return True

    if matriz[int(pos_z_matriz)][int(pos_x_matriz)] == 0 or matriz[int(pos_z_matriz)][int(pos_x_matriz)] > 12:
        #print(f"em cima de {matriz[int(pos_z_matriz)][int(pos_x_matriz)]}")
        #print("colidiu por piso errado")
        return True
    
    #print("sem colisão")

    return False

# **********************************************************************
# spawn_gasolinas()
# Função que gera as gasolinas no mapa  
# **********************************************************************
def spawn_gasolina():
    global matriz, gasolinas_no_mapa, gasolinas, tamLadrilho, mapComprimento, mapLargura

    while gasolinas_no_mapa < 8:
        x_gasolina = random.randint(0,(tamLadrilho*mapLargura)-1)
        z_gasolina = random.randint(0,(tamLadrilho*mapComprimento)-1)

        x_gas_abs = int(x_gasolina/tamLadrilho)
        z_gas_abs = int(z_gasolina/tamLadrilho)

        #print("---------------", x_gas_abs, z_gas_abs)

        if matriz[z_gas_abs][x_gas_abs] > 0 and matriz[z_gas_abs][x_gas_abs] < 13:
            nova_gasolina = Ponto(x_gasolina,0,z_gasolina)
            gasolinas.append(nova_gasolina)
            gasolinas_no_mapa += 1
            # print(f"Galão de gasolina spawnado em x:{nova_gasolina.x} z:{nova_gasolina.z}")

# **********************************************************************
# get_gasolina()
# Função que remove o galão de gasolina do mapa e adiciona ao tanque
# **********************************************************************
def get_gasolina():
    global gasolinas_no_mapa, tanque, tamLadrilho

    for gas in gasolinas:
        if int(gas.x/tamLadrilho) == int(Pos_Carro.x/tamLadrilho) and int(gas.z/tamLadrilho) == int(Pos_Carro.z/tamLadrilho):
            gasolinas.remove(gas)
            gasolinas_no_mapa -= 1
            
            if tanque + 10 <= max_tanque:
                tanque += 10
            else:
                tanque = max_tanque

            # playsound.playsound('./Sounds/GASOLINA.mp3', False)
            return
        
# **********************************************************************
# desenha_gasolinas()
# Funcao que desenha os galões de gasolina
# **********************************************************************
def desenha_gasolinas():
    global Angulo
    for gas in gasolinas:
        glColor3f(1,0,0)
        glPushMatrix()
        glTranslatef(gas.x,gas.y+0.5,gas.z)
        # glScaled(1,1,0.5)
        glRotatef(Angulo,0,1,0)
        DesenhaCubo()
        glPopMatrix()
        Angulo = Angulo + 0.3
        
def printMatriz(matriz):
    for linha in matriz:
        print(linha)
        
# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
# **********************************************************************
def display():
    global Angulo
    global Angulo_Carro
    global moving
    global matriz
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    DefineLuz()
    PosicUser()
    spawn_gasolina()
    desenhaCarro()

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    
    Angulo = Angulo + 1

    spawnBuildings()
    desenha_gasolinas()
    DesenhaBackground()

    if(moving):
        moveForward(0.9)
    
    DesenhaEm2D()

    glutSwapBuffers()

# **********************************************************************
#  Função que desenha o background do cenário
# **********************************************************************
def DesenhaBackground():
    DesenhaCeu()
    DesenhaBase()

# **********************************************************************
#  Função que desenha o céu
# **********************************************************************
def DesenhaCeu():
    global tamLadrilho, mapComprimento, mapLargura
    dist = 500
    maxHeight = 500
    minHeight = -50
    UseTexture(21)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(1,0,0)
    glTexCoord(0,1)
    glVertex3f(-dist,  minHeight, -dist)
    glTexCoord(1,1)
    glVertex3f(mapComprimento*tamLadrilho + dist, minHeight , -dist)
    glTexCoord(1,0)
    glVertex3f( mapComprimento*tamLadrilho + dist,maxHeight, -dist )
    glTexCoord(0,0)
    glVertex3f( -dist,  maxHeight, -dist)
    glEnd()

    UseTexture(21)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,0,1)
    glTexCoord(0,1)
    glVertex3f( -dist, minHeight , -dist)
    glTexCoord(0,0)
    glVertex3f( -dist,  maxHeight, -dist)
    glTexCoord(1,0)
    glVertex3f( -dist, maxHeight , mapLargura*tamLadrilho + dist)
    glTexCoord(1,1)
    glVertex3f( -dist, minHeight , mapLargura*tamLadrilho + dist)
    glEnd()

    UseTexture(21)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,0,1)
    glTexCoord(0,1)
    glVertex3f( mapLargura*tamLadrilho + dist, minHeight , -dist)
    glTexCoord(1,1)
    glVertex3f( mapLargura*tamLadrilho + dist, minHeight , mapComprimento*tamLadrilho + dist)
    glTexCoord(1,0)
    glVertex3f( mapLargura*tamLadrilho + dist, maxHeight , mapComprimento*tamLadrilho + dist)
    glTexCoord(0,0)
    glVertex3f( mapLargura*tamLadrilho + dist, maxHeight , -dist)
    glEnd()

    UseTexture(21)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(1,0,0)
    glTexCoord(1,1)
    glVertex3f(-dist,  minHeight, mapComprimento*tamLadrilho+dist)
    glTexCoord(1,0)
    glVertex3f( -dist,  maxHeight, mapComprimento*tamLadrilho+dist)
    glTexCoord(0,0)
    glVertex3f( mapLargura*tamLadrilho + dist,maxHeight, mapComprimento*tamLadrilho+dist )
    glTexCoord(0,1)
    glVertex3f(mapLargura*tamLadrilho + dist, minHeight , mapComprimento*tamLadrilho+dist)
    glEnd()

# **********************************************************************
#  Função que desenha o ambiente
# **********************************************************************
def DesenhaBase():
    global tamLadrilho, mapComprimento, mapLargura
    dist = 0
    maxHeight = 0
    minHeight = -5
    UseTexture(22)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(1,0,0)
    glTexCoord(0,10)
    glVertex3f(-dist,  minHeight, -dist)
    glTexCoord(1,10)
    glVertex3f( -dist,  maxHeight, -dist)
    glTexCoord(1,0)
    glVertex3f( mapComprimento*tamLadrilho + dist,maxHeight, -dist )
    glTexCoord(0,0)
    glVertex3f(mapComprimento*tamLadrilho + dist, minHeight , -dist)
    glEnd()

    UseTexture(22)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,0,1)
    glTexCoord(0,10)
    glVertex3f( -dist, minHeight , -dist)
    glTexCoord(0,0)
    glVertex3f( -dist, minHeight , mapLargura*tamLadrilho + dist)
    glTexCoord(1,0)
    glVertex3f( -dist, maxHeight , mapLargura*tamLadrilho + dist)
    glTexCoord(1,10)
    glVertex3f( -dist,  maxHeight, -dist)
    glEnd()

    UseTexture(22)
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,0,1)
    glTexCoord(0,10)
    glVertex3f( mapLargura*tamLadrilho + dist, minHeight , -dist)
    glTexCoord(1,10)
    glVertex3f( mapLargura*tamLadrilho + dist, maxHeight , -dist)
    glTexCoord(1,0)
    glVertex3f( mapLargura*tamLadrilho + dist, maxHeight , mapComprimento*tamLadrilho + dist)
    glTexCoord(0,0)
    glVertex3f( mapLargura*tamLadrilho + dist, minHeight , mapComprimento*tamLadrilho + dist)
    glEnd()

    UseTexture(22)
    glColor3f(1,1,1,) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(1,0,0)
    glTexCoord(1,10)
    glVertex3f(-dist,  minHeight, mapComprimento*tamLadrilho+dist)
    glTexCoord(1,0)
    glVertex3f(mapLargura*tamLadrilho + dist, minHeight , mapComprimento*tamLadrilho+dist)
    glTexCoord(0,0)
    glVertex3f( mapLargura*tamLadrilho + dist,maxHeight, mapComprimento*tamLadrilho+dist )
    glTexCoord(0,10)
    glVertex3f( -dist,  maxHeight, mapComprimento*tamLadrilho+dist)
    glEnd()


# **********************************************************************
#  Função que desenha e modela o carro
# **********************************************************************
def desenhaCarro():
    global Pos_Carro, Vaca
    compCarro = 3
    largCarro = 1.5
    altCarro = 0.6
    altCapo = 0.4
    distChao = 0.05

    Carro.ExibeObjeto(Pos_Carro,Angulo_Carro)
    #car
    # glColor3f(1,0,1)
    # glPushMatrix()
    # glTranslatef(Pos_Carro.x,Pos_Carro.y+0.5,Pos_Carro.z)
    # glRotatef(Angulo_Carro,0,1,0)
    # DesenhaCubo()
    # glPopMatrix()
    
    # glColor4f(1,0,0,1)

    # glPushMatrix()
    # glTranslatef(Pos_Carro.x,Pos_Carro.y+0.5,Pos_Carro.z)
    # glRotatef(Angulo_Carro,0,1,0)
    #  # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(0,1,0)
    # glVertex3f(largCarro/2,  distChao, compCarro/2 )
    # glVertex3f(largCarro/2, distChao , - compCarro/2)
    # glVertex3f(- largCarro/2, distChao, - compCarro/2 )
    # glVertex3f(- largCarro/2,  distChao, compCarro/2 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(0,1,0)
    # glVertex3f(largCarro/2,  distChao + altCarro, compCarro/2 )
    # glVertex3f(largCarro/2, distChao + altCarro , - compCarro/2)
    # glVertex3f(- largCarro/2, distChao + altCarro, - compCarro/2 )
    # glVertex3f(- largCarro/2,  distChao + altCarro, compCarro/2 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f(- largCarro/2,  distChao, compCarro/2 )
    # glVertex3f(- largCarro/2,  distChao + altCarro, compCarro/2 )
    # glVertex3f(- largCarro/2, distChao + altCarro, - compCarro/2 )
    # glVertex3f(- largCarro/2, distChao, - compCarro/2 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f(largCarro/2,  distChao, compCarro/2 )
    # glVertex3f(largCarro/2, distChao, - compCarro/2 )
    # glVertex3f(largCarro/2, distChao + altCarro, - compCarro/2 )
    # glVertex3f(largCarro/2,  distChao + altCarro, compCarro/2 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f( largCarro/2,  distChao, - compCarro/2 )
    # glVertex3f( - largCarro/2, distChao, - compCarro/2 )
    # glVertex3f( - largCarro/2, distChao + altCarro, - compCarro/2 )
    # glVertex3f( largCarro/2,  distChao + altCarro, - compCarro/2 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f( largCarro/2,  distChao, compCarro/2 )
    # glVertex3f( largCarro/2, distChao + altCarro, compCarro/2 )
    # glVertex3f( - largCarro/2, distChao + altCarro, compCarro/2 )
    # glVertex3f( - largCarro/2,  distChao, compCarro/2 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f( largCarro/2,  distChao + altCarro, compCarro/4 )
    # glVertex3f( largCarro/2, distChao + altCarro + altCapo, compCarro/4 )
    # glVertex3f( - largCarro/2, distChao + altCarro + altCapo, compCarro/4 )
    # glVertex3f( - largCarro/2,  distChao + altCarro, compCarro/4 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f( largCarro/2,  distChao + altCarro, - compCarro/4 )
    # glVertex3f(  - largCarro/2, distChao + altCarro, - compCarro/4 )
    # glVertex3f(  - largCarro/2, distChao + altCarro + altCapo, - compCarro/4 )
    # glVertex3f( largCarro/2,  distChao + altCarro + altCapo, - compCarro/4 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(0,1,0)
    # glVertex3f( largCarro/2,  distChao + altCarro + altCapo,  compCarro/4 )
    # glVertex3f( largCarro/2, distChao + altCarro + altCapo , - compCarro/4)
    # glVertex3f( - largCarro/2, distChao + altCarro + altCapo, - compCarro/4 )
    # glVertex3f( - largCarro/2,  distChao + altCarro + altCapo,  compCarro/4 )
    # glEnd()
    
    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f( - largCarro/2,  distChao + altCarro,  compCarro/4 )
    # glVertex3f( - largCarro/2,  distChao + altCarro + altCapo,  compCarro/4 )
    # glVertex3f( - largCarro/2, distChao + altCarro + altCapo, - compCarro/4 )
    # glVertex3f( - largCarro/2, distChao + altCarro, - compCarro/4 )
    # glEnd()

    # # glColor4f(1,0,1,1) # desenha QUAD preenchido
    # glBegin ( GL_QUADS )
    # glNormal3f(1,0,0)
    # glVertex3f(  largCarro/2,  distChao + altCarro,  compCarro/4 )
    # glVertex3f(  largCarro/2, distChao + altCarro, - compCarro/4 )
    # glVertex3f(  largCarro/2, distChao + altCarro + altCapo, - compCarro/4 )
    # glVertex3f(  largCarro/2,  distChao + altCarro + altCapo,  compCarro/4 )
    # glEnd()

    # glPopMatrix()

# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/60:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()

    

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    global image
    global moving
    global Angulo_Carro
    global alvo_camera

    var_angulo = 5
    #print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b' ':
        init()

    if args[0] == b'i':
        image.show()

    if args[0] == b'w':
        moveForward(1)
    
    if args[0] == b'd':
        rotaciona_alvo(-var_angulo)
        rotaciona_observador(-var_angulo)
        Angulo_Carro = Angulo_Carro + var_angulo*-1

    if args[0] == b'a':
        rotaciona_alvo(var_angulo)
        rotaciona_observador(var_angulo)
        Angulo_Carro = Angulo_Carro + var_angulo*1

    if args[0] == b's':
        moveBackward(1)

    if args[0] == b' ':
        moving = not moving

    if args[0] == b'u':
        alvo_camera.y += 1

    if args[0] == b'j':
        alvo_camera.y -= 1

        
    #print(args)
    # ForÃ§a o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global alvo, matriz

    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        change_camera_view()
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        #printMatriz(matriz)
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
    if a_keys == GLUT_KEY_RIGHT:       # Se pressionar RIGHT
        pass
    glutPostRedisplay()

def moveForward(fator):
    global alvo
    global observador
    global Pos_Carro
    global moving
    global tanque

    if tanque > 0:
        vetor_alvo = alvo.__sub__(Pos_Carro)
        nova_pos_alvo = alvo.__add__(vetor_alvo.versor().__mul__(fator))
        nova_pos_car = Pos_Carro.__add__(vetor_alvo.versor().__mul__(fator))
        nova_pos_obs = observador.__add__(vetor_alvo.versor().__mul__(fator))

        colided = testaColisao(nova_pos_car)
        get_gasolina()
            
        if colided:
            moving = False   
            return

        alvo = nova_pos_alvo
        Pos_Carro = nova_pos_car
        observador = nova_pos_obs

        tanque -= 0.1

        # Pos_Carro.imprime()
    
def moveBackward(fator):
    global alvo
    global observador
    global Pos_Carro
    global tanque
    
    vetor_alvo = alvo.__sub__(Pos_Carro)
    alvo = alvo.__sub__(vetor_alvo.versor().__mul__(fator))
    Pos_Carro = Pos_Carro.__sub__(vetor_alvo.versor().__mul__(fator))
    observador = observador.__sub__(vetor_alvo.versor().__mul__(fator))

    if tanque + 5 > max_tanque:
        tanque = max_tanque
    else:
        tanque += 5
    
def change_camera_view():
    global camera_view

    camera_view += 1 

    if camera_view == 4:
        camera_view = 0

    #print(f"Camera View: {camera_view}")
        
def rotaciona_alvo(angulo_cam):
    global alvo
    global observador
    global atual_vetor_alvo
    global Pos_Carro

    vetor_alvo = alvo.__sub__(Pos_Carro)
    vetor_alvo.rotacionaY(angulo_cam)

    alvo = Pos_Carro.__add__(vetor_alvo)

def rotaciona_observador(angulo_cam):
    global alvo
    global observador
    global Pos_Carro

    vetor_alvo = observador.__sub__(Pos_Carro)
    vetor_alvo.rotacionaY(angulo_cam)

    observador = Pos_Carro.__add__(vetor_alvo)

def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()

def testaColisaoCarro():
    global Pos_Carro

def printString(s, posX, posY, cor):
    defineCor(cor)
    
    glRasterPos3i(posX, posY, 0)
    for i in range(len(s)):
        glutBitmapCharacter(globals()['GLUT_BITMAP_HELVETICA_18'], c_int(ord(s[i])))   

def DesenhaEm2D():
    global tanque, max_tanque

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    glViewport(0, 0, w, int(h*0.1)) 

    glOrtho(0,10, 0,10, 0,1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    defineCor(Black)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(0,3.5)
    glVertex2f(10,3.5)
    glEnd()

    s = "Gasolina: " + str(round(tanque,2)) + f"L /  {max_tanque}L"
    printString(s, 0, 1, Black)

    defineCor(Red)
    glLineWidth(35)
    glBegin(GL_LINES)
    glVertex2f(0,1.7)
    glVertex2f(10*(tanque/max_tanque),1.7)
    glEnd()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, int(h*0.035), w, h-(int(h*0.035)))
    
# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

#print("LEU MATRIZ HEIN")
lerMatriz("/Textures/Mapa1.txt")

#Texturas.append(LoadTexture("/Textures/NADA.jpg"))

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH | GLUT_RGB)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de tÃ­tulo da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Car Game")

# executa algumas inicializaÃ§Ãµes
init ()

Carro = Objeto3D()
Carro.LeObjeto("Objetos/AE86.tri")
#Vaca.ImprimeObjeto()

try: 
    Texturas.append(LoadTexture("./Textures/GRASS2.jpg"))
    Texturas.append(LoadTexture("./Textures/CROSS2.jpg"))
    Texturas.append(LoadTexture("./Textures/DL2.jpg"))
    Texturas.append(LoadTexture("./Textures/DLR2.jpg"))
    Texturas.append(LoadTexture("./Textures/DR2.jpg"))
    Texturas.append(LoadTexture("./Textures/LR2.jpg"))
    Texturas.append(LoadTexture("./Textures/None2.jpg"))
    Texturas.append(LoadTexture("./Textures/UD2.jpg"))
    Texturas.append(LoadTexture("./Textures/UDL2.jpg"))
    Texturas.append(LoadTexture("./Textures/UDR2.jpg"))
    Texturas.append(LoadTexture("./Textures/UL2.jpg"))
    Texturas.append(LoadTexture("./Textures/ULR2.jpg"))
    Texturas.append(LoadTexture("./Textures/UR2.jpg"))
    Texturas.append(LoadTexture("./Textures/PREDIO1.jpg"))
    Texturas.append(LoadTexture("./Textures/PAREDE.jpg"))
    Texturas.append(LoadTexture("./Textures/predio2.jpg"))
    Texturas.append(LoadTexture("./Textures/predio3.jpg"))
    Texturas.append(LoadTexture("./Textures/predio4.jpg"))
    Texturas.append(LoadTexture("./Textures/predio5.jpg"))
    Texturas.append(LoadTexture("./Textures/predio6.jpg"))
    Texturas.append(LoadTexture("./Textures/TETO.jpg"))
    Texturas.append(LoadTexture("./Textures/ceu.jpg"))
    Texturas.append(LoadTexture("./Textures/TIJOLOS.jpg"))
    Texturas.append(LoadTexture("./Textures/agua.jpg"))
except:
    print(f"Texturas não encontradas")

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# serÃ¡ chamada automaticamente quando
# for necessÃ¡rio redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# pip install playsound==1.2.2 
# precisa ser essa versão
# playsound.playsound('./Sounds/DINGA.mp3', False)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# serÃ¡ chamada automaticamente quando
# o usuÃ¡rio alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# serÃ¡ chamada automaticamente sempre
# o usuÃ¡rio pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" serÃ¡ chamada
# automaticamente sempre o usuÃ¡rio
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)

try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
