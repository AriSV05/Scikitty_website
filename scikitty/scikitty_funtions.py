import joblib
import pandas as pd
import os
import random

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
    #Hacer split al dataset en train y test
    random.seed(random_state)
    indices = list(range(len(X)))
    random.shuffle(indices)
    split_index = int((1 - test_size) * len(X))
    train_indices = indices[:split_index]
    test_indices = indices[split_index:]
    
    X_train, X_test = X[train_indices], X[test_indices]
    Y_train, Y_test = Y[train_indices], Y[test_indices]
    
    return X_train, X_test, Y_train, Y_test
