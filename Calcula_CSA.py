"""
Created on Thu Oct  5 10:28:48 2023

@author: Victor F. S.
"""

import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
from stl import mesh
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib import ticker
plt.close('all')

def center_line(linha_central):
    """
    Recebe uma matriz contendo os pontos da linha central e retorna um conjunto
    de vetores tangentes à linha com uma identificação.
    
    - Recebe:
        linha_central[coluna][linha]: matriz contendo em cada coluna as coord.
        dos pontos e em cada linha um ponto
    - Devolve:
        Vt: array de arrays contendo uma coluna de id do vetor e três colunas
        com as componentes do vetor (vx,vy,vz)
    """
    Vt = []
    for i in range(len(linha_central)-1):
        vt = [i,
              ((linha_central[0][i+1]-linha_central[0][i])), 
              ((linha_central[1][i+1]-linha_central[1][i])), 
              ((linha_central[2][i+1]-linha_central[2][i]))]
        Vt.append(vt)    
    return(Vt)

def load_stl_file():
    """
    Abre o arquivo .stl e extrai os pontos de cada triângulo, calculando seus 
    centroides. Por fim, os centroides são ordenados de acordo com a coordenada 
    z devolvendo uma array de centroides ordenada.
    
    - Devolve:
        sorted_centroides: array de arrays contendo, em cada array, as
        coordenadas dos centroides (x,y,z) ordenados pela coordenada z
    """
    file_path = filedialog.askopenfilename()
    file_folder = os.path.dirname(file_path)
    fileJustname = file_path.split('/')
    fileJustname = fileJustname[-1]
    fileJustname = fileJustname.split('.')
    fileJustname = fileJustname[0]
    fileextension = file_path.split('/')
    fileextension = fileextension[-1]
    fileextension = fileextension.split('.')
    fileextension = fileextension[1]
    mesh_data = mesh.Mesh.from_file(file_path)
    
    # Extrai os pontos dos vértices dos triângulos e os separa em linhas
    # vertices = mesh_data.points
    # all_vertices = all_vertices.reshape(-1, 3)
    triangulos = mesh_data.vectors
    centroide = []
    for i in range(len(triangulos)):
        vertice1 = triangulos[i][0]
        vertice2 = triangulos[i][1]
        vertice3 = triangulos[i][2]
        centro = (vertice1 + vertice2 + vertice3) / 3.0
        centroide.append(centro)
    # Ordena os pontos de acordo com a sua coordenada z
    centroide = np.array(centroide)
    sorted_centroides = centroide[np.lexsort((centroide[:, 2],))]    
    return(sorted_centroides)

def perimeter(linha_central, vetor_tan, malha):
    """
    Busca os pontos que definem o perímetro da área da seção transversal do 
    .stl a partir do produto escalar entre o vetor_tan e vetores contidos no 
    plano
    
    - Recebe:
        linha_central[coluna][linha]
        malha[linha][coluna]
        vetor_tan[linha][coluna]
    - Devolve:
        
    """
    # Aplicar eq. do plano
    # identificar pontos contidos no plano
    epsilon = 5     # Define o intervalo de busca de pontos
    delta = 5e-4    # Prod. escalar (vetor_tan,B) <= delta (ideal == 0)
    Planos = []
    # Busca um par de vetores contidos no plano da área de seção transversal
    print('Gerando planos...')
    for i in range(len(vetor_tan)):       
        plano = []  # Guarda os pontos contidos em um plano
        print('def perimeter: Vetor tangente %d...' %(i))        
        z_coord = linha_central[2][i]
        pontos_no_intervalo = [malha[j] for j in range(len(malha)) if z_coord - epsilon <= malha[j][2] <= z_coord + epsilon]
        # Gera um vetor e testa se ele é normal ao vetor tangente (dentro de um erro delta)
        for ponto in pontos_no_intervalo:
            B = [(ponto[0]-linha_central[0][i]), 
                 (ponto[1]-linha_central[1][i]), 
                 (ponto[2]-linha_central[2][i])]
            if abs(np.matmul(vetor_tan[i][1:], np.transpose(B))) < delta:                        
                plano.append(ponto)
                print('+ um ponto')
        # Salva os pontos contidoa no plano juntamente com o id do vetor tan.
        if plano !=[]:
            np.array(plano.insert(0,vetor_tan[i][0]))
            Planos.append(plano)  
# -----------------------------------------------------------------------------------------------------    
        # for j in range(len(malha)):
        #     z_coord = malha[j][2]
        #     if z_coord >= linha_central[2][i] - epsilon and z_coord <= linha_central[2][i] + epsilon:
        #         if cont!=2:
        #             B = [(malha[j][0]-linha_central[0][i]), 
        #                   (malha[j][1]-linha_central[1][i]), 
        #                   (malha[j][2]-linha_central[2][i])]
        #             if abs(np.matmul(vetor_tan[i][1:], np.transpose(B))) < delta:                        
        #                 vetor_normal.append(B)
        #                 vetor_normal.insert(0,vetor_tan[i][0])
        #                 cont+=1
        #                 print('%d' %(cont))
        #         else:
        #             dupla_normal.append(vetor_normal)
        #             break
# -----------------------------------------------------------------------------------------------------
    # dupla_normal = []
    # # Busca um par de vetores contidos no plano da área de seção transversal
    # for i in range(len(vetor_tan)):
    #     cont = 0    # Contador do par de vetores contidos no plano        
    #     vetor_normal = []
    #     print('def perimeter: Vetor tangente %d...' %(i))        
    #     z_coord = linha_central[2][i]
    #     pontos_no_intervalo = [malha[j] for j in range(len(malha)) if z_coord - epsilon <= malha[j][2] <= z_coord + epsilon]
    #     # Gera um vetor e testa se ele é normal ao vetor tangente (dentro de um erro delta)
    #     for ponto in pontos_no_intervalo:
    #         if cont!=2:
    #             B = [(ponto[0]-linha_central[0][i]), 
    #                  (ponto[1]-linha_central[1][i]), 
    #                  (ponto[2]-linha_central[2][i])]
    #             if abs(np.matmul(vetor_tan[i][1:], np.transpose(B))) < delta:                        
    #                 vetor_normal.append(B)                    
    #                 cont+=1
    #                 print('%d' %(cont))
    #         else:
    #             # Salva os vetores que descrevem o plano juntamente com o id do vetor tan. 
    #             vetor_normal.insert(0,vetor_tan[i][0])
    #             dupla_normal.append(vetor_normal)
    #             break
# -----------------------------------------------------------------------------------------------------
    print('def perimeter: Concluído!')
    return(Planos)

def CSA():
    
    return()

###---------- Main ----------###

print('Selecione o arquivo da linha de centro (.txt - unidade: m):')
file_path = filedialog.askopenfilename()
file_folder = os.path.dirname(file_path)
fileJustname = file_path.split('/')
fileJustname = fileJustname[-1]
fileJustname = fileJustname.split('.')
fileJustname = fileJustname[0]
fileextension = file_path.split('/')
fileextension = fileextension[-1]
fileextension = fileextension.split('.')
fileextension = fileextension[1]    
M = pd.read_csv(file_path, sep="\t", header=None)
# Passando de m (un. do arquivo da linha central) -> mm (un. do stl)
M = M*1000
vetor_tan = center_line(M)

print('Selecione o arquivo stl:')
NZ = load_stl_file()
P = np.array(perimeter(M, vetor_tan, NZ))