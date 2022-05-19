#sudo pip3 install virtualenv
#virtualenv venv
#source venv/bin/activate
#pip3 freeze > requirements.txt
#deactivate
# pip3 install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.5.0-cp38-cp38-manylinux2010_x86_64.whl
# pip install https://storage.googleapis.com/tensorflow/windows/cpu/tensorflow_cpu-2.5.0-cp38-cp38-win_amd64.whl
# pip3 install pandas scikit-learn seaborn opencv-python

import io
import keras
import pandas as pd
import seaborn as sb
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import KFold

from keras.layers import Dense
from keras.models import Sequential

accuracy_fold = []
loss_fold = []
confusion_matrices = []
resultados = []

dataframe=pd.read_csv("./cbw.csv",delimiter=",") # https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data
dataframe["diagnosis"].replace({'M':1,'B':0},inplace=True)
dataframe = dataframe.drop(["id","Unnamed: 32"],axis=1)
print(dataframe.head(100))

X = dataframe.drop(["diagnosis"],axis=1)
X = MinMaxScaler().fit_transform(X)
y = dataframe["diagnosis"]
print(X.shape)
print(y.shape)

n_input = 30
n_output = 1

model = Sequential([
    Dense(int(n_output*((n_input/n_output)**(1/3))**2),input_dim = n_input,activation = "relu"),
    Dense(int(n_output*((n_input/n_output)**(1/3))),activation = "relu"),
    Dense(n_output,activation = "sigmoid")
])

model.compile(
    loss = "binary_crossentropy",
    optimizer = "adam", 
    metrics = ["accuracy"]
)

model.summary()

input("...")

i=1
myFolds = KFold(n_splits=5, shuffle=True, random_state=3)
for train,test in myFolds.split(X,y):
    print("\n############ Training fold ",i," ########################")
    resultados.append(model.fit(
        X[train],
        y[train],
        epochs = 200,
        batch_size = 100,
        validation_data=(X[test], y[test]),
        verbose = 2
    ))
    
    y_test = y[test]
    y_pred = model.predict(X[test])
    y_pred = list( map(lambda x: round(x[0]), y_pred) )
    matrix = confusion_matrix(y_test, y_pred)
    metricas = model.evaluate(X[test],y_test)
    
    confusion_matrices.append(matrix)
    accuracy_fold.append(metricas[1])
    loss_fold.append(metricas[0])
    i+=1
    
for i in range(len(confusion_matrices)):
    print(f"\nPartición #{i+1}")
    print(confusion_matrices[i])
    print(accuracy_fold[i])
    print(loss_fold[i])

print(f"\nExactitud promedio: {sum(accuracy_fold)/len(accuracy_fold)}")

plt.rcParams['figure.figsize'] = (16, 16)
plt.style.use('dark_background')

plt.subplot(4,1,1)
plt.ylabel("Exactitud - Entrenamiento")
for i in range(1,len(resultados)):
    plt.plot(resultados[i].history["accuracy"],label = str(i+1))
plt.legend()

plt.subplot(4,1,2)
plt.ylabel("Exactitud - Validación")
for i in range(1,len(resultados)):
    plt.plot(resultados[i].history["val_accuracy"],label = str(i+1))
plt.legend()

plt.subplot(4,1,3)
plt.ylabel("Perdida - Entrenamiento")
for i in range(1,len(resultados)):
    plt.plot(resultados[i].history["loss"],label = str(i+1))
plt.legend()

plt.subplot(4,1,4)
plt.ylabel("Perdida - Validación")
for i in range(1,len(resultados)):
    plt.plot(resultados[i].history["val_loss"],label = str(i+1))
plt.legend()
    
plt.xlabel("# Epoca")
#plt.savefig('resultado.png', dpi=100)
plt.show()
