from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import joblib
import numpy as np
import pandas as pd
import os
import random
from dsplot.tree import BinaryTree
from classes import DecisionTreeClassifier as tree

def read_csv_with_column_names(filename):
    with open('./demos/'+ filename, 'r') as file:
        # Leer la primera línea para obtener los nombres de las columnas
        col_names = file.readline().strip().split(',')
        yield col_names
        # Leer el resto del archivo línea por línea
        for line in file:
            yield line.strip().split(',')

def import_model(filename): #cargar modelo
    modelo = joblib.load(f'./models/{filename}')
    return modelo

def save_model(model, name, directory="./models"):
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


def image_tree_model(Y, data):
    plotNodes = tree.BFS_list(data)
    
    places = [i for i, n in enumerate(plotNodes) if n in np.unique(Y)]
    for i,v in enumerate(places):
        index = 2*v+1
        if index < i:
            v[i]+=2
        if plotNodes[index-1]==None:
            break
        plotNodes.insert(index,None)
        plotNodes.insert(index,None)

    tree = BinaryTree(plotNodes)
    tree.plot("./image_model/TreeDecision.png", fill_color='#aec6cf')  
 
