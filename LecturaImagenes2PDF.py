#!/usr/bin/env python
# coding: utf-8

# # Trabajo en Casa

# ### Realizado por: Juan Barrera y Katherine Barrera

#NOTA: ----------------------------------
# Si se trabaja en Linux dejar como esta 
# Si se trabaja en Windows descomentar en donde diga windows y comentar las lineas de linux
# ---------------------------------------
# In[2]:


## Importacion de librerias necesarias
from matplotlib.backends.backend_pdf import PdfPages, PdfFile
import numpy as np
from matplotlib import pyplot as plt
#from PyPDF2 import PdfFileMerger, PdfFileReader
import matplotlib.image as mpimg
import subprocess
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from os import remove
from tqdm import tqdm
import time
import numpy as np
import cv2

def calculoHistogramaGRAY(path, valor):
    ##Histograma en Escala de grises
    img = leerImagen(path)
    his2GRay = cv2.calcHist([img],[0],None,[256],[0,256]) 
    plt.plot(his2GRay) #calculating histogram
    #plt.hist(img.ravel(), 256, [0,256])
    plt.savefig('histograma2Gray/'+str(valor)+"histograma2Gray.jpg")
    plt.show()
    return 'histograma2Gray/'+str(valor)+"histograma2Gray.jpg"


def calculoHistogramaColor(img, valor):
    
    for i, col in enumerate(['b', 'g', 'r']):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color = col)
        plt.xlim([0, 256])

    plt.savefig('histograma2Color/'+str(valor)+"histograma2COlor.jpg")  
    plt.show()
    return 'histograma2Color/'+str(valor)+"histograma2COlor.jpg"


def obtenerImagenGRAY(image, valor):
    ##Imagen en escala de grsies
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('Gray/'+str(valor)+'ToGray.jpg', gray_image)
    return 'Gray/'+str(valor)+'ToGray.jpg'


def leerImagen(path):
    img = cv2.imread(path)
    return img;

def medirTIempoEjecuion(directorio, listImagenes, identificador):
    vectorTiempo = []
    for i in tqdm(range(len(listImagenes))):
        inicio = time.time()
        path = dirpath+directorio+'/'+listImagenes[i]
        if 'jpg' in path:
            ##Lectura de la Imagen
            img = leerImagen(path)
            ##Imagen en escala de grsies
            pathGray = obtenerImagenGRAY(img, i)
            ##Histograma a color
            pathHistoColor = calculoHistogramaColor(img, i)
            ##Histograma a Gray
            pathHistoGray = calculoHistogramaGRAY(pathGray, i)    
        fin = time.time()
        vectorTiempo.append(fin-inicio)
        inicio = 0
        fin = 0
    return vectorTiempo

def graficaTiempo(tiempo):
    plt.figure(figsize=(15, 5))
    plt.plot(tiempo)
    plt.xlabel('Imagenes')
    plt.ylabel('Segundos')
    plt.title('Tiempo de ejecucion del Programa')
    plt.savefig("TiempoEjecucion.jpg")  
    plt.show()
    
    
def generacionPDF(directorio, listImagenes, identificador, tiempo, tiempoTotalEjecucion):
    w, h = A4
    cont = 0
    graficaTiempo(tiempo)
    #c = canvas.Canvas("informe-LecturaImagenes-Windows.pdf", pagesize=A4)
    c = canvas.Canvas("informe-LecturaImagenes.pdf", pagesize=A4)
    c.drawString(200, h - 50, "¡Universidad Politecnica Salesiana!")
    c.drawString(50, h - 70, "Realizado por: Juan Barrera y Katherine Barrera")
    c.drawString(50, h - 90, "Fecha: 26/04/20201")
    #c.drawString(150, h - 115, "Grafica del tiempo de ejecucion en Windows")
    c.drawString(150, h - 115, "Grafica del tiempo de ejecucion en Linux")
    c.drawImage("TiempoEjecucion.jpg", 50, h- 375, 500, 250)            
    #c.drawString(50, h - 450, "El tiempo total de la ejecucion del programa en Windows es: "+str(tiempoTotalEjecucion))
    c.drawString(50, h - 450, "El tiempo total de la ejecucion del programa en linux es: "+str(tiempoTotalEjecucion))
    c.showPage()
    
    for i in tqdm(range(len(listImagenes))):
        
        path = dirpath+directorio+'/'+listImagenes[i]
        pathGray = 'Gray/'+str(i)+'ToGray.jpg'
        pathHistoColor = 'histograma2Color/'+str(i)+"histograma2COlor.jpg"
        pathHistoGray = 'histograma2Gray/'+str(i)+"histograma2Gray.jpg"
        
        if 'jpg' in path:
            
            ##Grafica de Imagen Original
            c.drawString(150, h - 115, "Imagen Original")
            c.drawImage(path, 50, h- 380, 250, 250)
            
            ##Grafica de Imagen en Escala de Grises
            c.drawString(400, h - 115, "Imagen Escala de Grises")
            c.drawImage(pathGray, 325, h- 380, 250, 250)
            
            ##Grafica de Histograma de Imagen a color
            c.drawString(100, h - 400, "HIstograma de imagen a color")
            c.drawImage(pathHistoColor, 50, h- 660, 250, 250)
            
            ##Grafica de Histograma en Escala de Grises
            c.drawString(340, h - 400, "Histograma de imagen Escala de Grises")
            c.drawImage(pathHistoGray, 325, h- 660, 250, 250)
              
            c.showPage()
            cont+=1
        if cont == 10: 
            break;
            
    c.save()

if  __name__ ==  '__main__':
    
    plt.figure(figsize=(9, 3))
    dirpath = 'imagenes/'
    pixel = 100
    BSDS300 = os.listdir(dirpath+'BSDS300')
    print("Cantidad de imagenes en directorio: ", len(BSDS300))
    #Vector de tiempos. 
    timearr = []
    inicioPro = time.time()
    timearr = medirTIempoEjecuion("BSDS300", BSDS300,0)
    finPro = time.time()
    tiempoFinal = finPro-inicioPro
    generacionPDF("BSDS300", BSDS300,0, timearr, tiempoFinal)


# In[ ]:





# In[ ]:




