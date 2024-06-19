import joblib
import pandas as pd
import numpy as np
import os
import random
from ..scikitty.models.DecisionTree import DecisionTreeClassifier

def read_csv_with_column_names(filename):
    name_csv = f'{filename}.csv'
    # Leer solo la primera fila para obtener los nombres de las columnas
    with open(name_csv, 'r') as file:
        col_names = next(file).strip().split(',')

    # Leer el resto del archivo omitiendo la primera fila
    data = pd.read_csv(name_csv, skiprows=1, header=None, names = col_names)

    return data

def import_model(filename): 
    #Cargar modelo
    modelo = joblib.load(filename)
    return modelo

def save_model(model, name, directory):
    #Guardar el modelo
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    file_path = os.path.join(directory, name + '.pkl')
    joblib.dump(model, file_path)


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

def residual(y, h):
    return y - h

def decay(alpha, alpha_decay=0.9):
    return alpha * alpha_decay

def tree_gradient_boosting(X, y, T=100, alpha=0.1, alpha_min=0.01, loss='mse', data_columns=None):
    r = y
    h = np.zeros_like(y, dtype=np.float64)

    for i in range(T):
        tree = DecisionTreeClassifier(min_samples_split=2, max_depth=1)
        tree.fit(X, r.reshape(-1,1))
        ht = np.array(tree.predict(X)).reshape(-1,1)
        h += alpha * ht
        r = residual(y, h)
        alpha = decay(alpha)
        print(f"\n\t***Iteration {i+1}***\n")
        tree.print_tree(data=data_columns)
        if alpha < alpha_min:
            break
    
    return h