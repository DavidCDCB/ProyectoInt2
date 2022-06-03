import cv2
import numpy as np
import pandas as pd
import seaborn as sb
import tensorflow as tf
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import InputLayer,Input,Conv2D, MaxPool2D,Reshape,Dense,Flatten
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import KFold

from tensorflow.keras.preprocessing.image import ImageDataGenerator




def cargarDatos(rutaOrigen,numeroCategorias,limite,ancho,alto):
    imagenesCargadas=[]
    valorEsperado=[]
    #plt.style.use('dark_background')
    plt.figure(figsize=(20,20))

    for categoria in range(0,numeroCategorias):
        print(f"Cargando: {categoria}")
        for idImagen in range(0,limite[categoria]):
            ruta=rutaOrigen+str(categoria)+"/"+str(categoria)+"_"+str(idImagen)+".jpg"
            imagen = cv2.imread(ruta)
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            imagen = cv2.resize(imagen, (ancho, alto))

            if(idImagen == 0):
                plt.subplot(5,5,categoria+1)
                plt.yticks([])
                plt.xlabel(str(categoria))
                plt.imshow(imagen,cmap='gray_r')

            imagen = imagen.flatten()
            imagen = imagen / 255
            imagenesCargadas.append(imagen)
            probabilidades = np.zeros(numeroCategorias)
            probabilidades[categoria] = 1
            valorEsperado.append(probabilidades)

    
    plt.show()
    imagenesEntrenamiento = np.array(imagenesCargadas)
    valoresEsperados = np.array(valorEsperado)
    print(f"{len(imagenesEntrenamiento)} imagenes cargadas")
    return imagenesEntrenamiento, valoresEsperados


def view_results(loss_values,val_loss_values,acc_values,val_acc_values):
    plt.style.use('dark_background')
    epochs = range(1, len(loss_values) + 1)
    plt.figure(figsize=(12,12))

    plt.subplot(2,1,1)
    plt.title('Analisis de costo y exactitud desde el entrenamiento y la validación')
    plt.plot(epochs, loss_values, 'y', label='Training loss')
    plt.plot(epochs, val_loss_values, 'g', label='Validation loss')
    plt.xlabel('Epocas')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(2,1,2)
    plt.plot(epochs, acc_values, 'y', label='Training Accuracy')
    plt.plot(epochs, val_acc_values, 'g', label='Validation accuracy')
    plt.xlabel('Epocas')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()


ancho = 256
alto = 256
pixeles = ancho*alto
numeroCanales = 1
formaImagen = (ancho,alto,numeroCanales)
numeroCategorias = 5

cantidaDatosEntrenamiento = [490 for x in range(5)]
cantidaDatosPruebas = [160 for x in range(5)] 
imagenes, probabilidades = cargarDatos("dataset/Train/",numeroCategorias,cantidaDatosEntrenamiento,ancho,alto)
imagenesPrueba, probabilidadesPrueba = cargarDatos("dataset/Test/",numeroCategorias,cantidaDatosPruebas,ancho,alto)
'''
model=Sequential()
#Capa entrada
model.add(InputLayer(input_shape=(pixeles,)))
model.add(Reshape(formaImagen)) # Rearma la imagen en forma de matriz

#Capas Ocultas
#Capas convolucionales
model.add(Conv2D(kernel_size=5,strides=2,filters=16,padding="same",activation="relu",name="capa_1"))
model.add(MaxPool2D(pool_size=2,strides=2))

model.add(Conv2D(kernel_size=3,strides=1,filters=36,padding="same",activation="relu",name="capa_2"))
model.add(MaxPool2D(pool_size=2,strides=2))


#Aplanamiento
model.add(Flatten())
model.add(Dense(128,activation="relu"))

#Capa de salida
model.add(Dense(numeroCategorias,activation="softmax"))


#Traducir de keras a tensorflow
model.compile(optimizer="adam",loss="categorical_crossentropy", metrics=["accuracy"])
#Entrenamiento
model.fit(x=imagenes,y=probabilidades,epochs=30,batch_size=60)

#Prueba del modelo
imagenesPrueba,probabilidadesPrueba=cargarDatos("dataset/test/",numeroCategorias,cantidaDatosPruebas,ancho,alto)
resultados=model.evaluate(x=imagenesPrueba,y=probabilidadesPrueba)
print("Accuracy=",resultados[1])

# Guardar modelo
ruta="models/modeloA.h5"
model.save(ruta)
# Informe de estructura de la red
model.summary()
'''