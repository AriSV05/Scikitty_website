from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import joblib
import numpy as np
import pandas as pd
import os
import random

def read_csv_with_column_names(filename):
    with open('./demos/'+ filename, 'r') as file:
        # Leer la primera línea para obtener los nombres de las columnas
        col_names = file.readline().strip().split(',')
        yield col_names
        # Leer el resto del archivo línea por línea
        for line in file:
            yield line.strip().split(',')

def train_test_split(X, Y, test_size=0.3, random_state=42):
    random.seed(random_state)
    indices = list(range(len(X)))
    random.shuffle(indices)
    split_index = int((1 - test_size) * len(X))
    train_indices = indices[:split_index]
    test_indices = indices[split_index:]
    
    X_train, X_test = X[train_indices], X[test_indices]
    Y_train, Y_test = Y[train_indices], Y[test_indices]
    
    return X_train, X_test, Y_train, Y_test

def confusion_matrix(y_true, y_pred):
    ''' Function to calculate confusion matrix '''
    
    # Convertir a arrays NumPy unidimensionales
    y_true2 = np.array(y_true).flatten()
    
    # Encontrar las clases únicas presentes en las etiquetas verdaderas y las predicciones
    classes = np.unique(np.concatenate((y_true2, y_pred)))

    # Inicializar la matriz de confusión como una matriz numpy
    matrix = np.zeros((len(classes), len(classes)), dtype=int)
    
    # Llenar la matriz de confusión
    for true, pred in zip(y_true, y_pred):
        true_idx = np.where(classes == true)[0][0]
        pred_idx = np.where(classes == pred)[0][0]
        matrix[true_idx, pred_idx] += 1
    
    # Crear un DataFrame de Pandas para la matriz de confusión
    conf_df = pd.DataFrame(matrix, index=classes, columns=classes)
    
    label_1 = classes[1] if 1 in classes else classes[0]
    label_2 = classes[0] if label_1 == classes[1] else classes[1]
    
    # Agregar etiquetas a la matriz
    conf_df.rename({label_1: label_1, label_2: label_2}, axis=0, inplace=True)
    conf_df.rename({label_1: label_1, label_2: label_2}, axis=1, inplace=True)
    
    return conf_df

def save_model(model, name, directory="."):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    file_path = os.path.join(directory, name + '.pkl')
    joblib.dump(model, file_path)

def image_tree_model(X, y, model):
    feature_cols = X.columns  # Nombres de las características usadas en el modelo
    class_names = [str(label) for label in pd.Series(y).unique()]  # Etiquetas únicas de la variable objetivo

    plt.figure(figsize=(20,10))
    plot_tree(model, feature_names=feature_cols, class_names=class_names, filled=True)
    plt.savefig('./image_tree_model/tree.png')


def import_model(name):
    return joblib.load(name +'.pkl')
