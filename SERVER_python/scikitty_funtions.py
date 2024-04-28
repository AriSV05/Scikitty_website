from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import matplotlib.pyplot as plt
import joblib
import numpy as np
import pandas as pd
import os


def read_csv(csv_name):
    return pd.read_csv('./demos/' + csv_name)

def is_classifier(y):
    unique_values = np.unique(y)
    if len(unique_values) == 2 or y.dtype == np.object:
        return True
    return False


def decide_and_train_tree(X, y, max_depth=None):
    if is_classifier(y):
        print("Using DecisionTreeClassifier")
        model = DecisionTreeClassifier(max_depth=max_depth)
    else:
        print("Using DecisionTreeRegressor")
        model = DecisionTreeRegressor(max_depth=max_depth)

    model.fit(X, y)

    return model

def getX_Y(df):
    X = df.drop(columns=[df.columns[-1]]) # Excluye la variable objetivo
    y = df[df.columns[-1]]
    # Codifica si es categórica usando one-hot encoding
    if any(X.dtypes == 'object'):
        #revisar
        X_one_hot = pd.get_dummies(X)
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
            return X_one_hot, y
        return X_one_hot, y
    return X, y
        
def splitX_Y(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)  # 30% para prueba

    return X_train, X_test, y_train, y_test


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

def cal_metrics(x_test, y_test, model):
    accuracy, recall, precision, f_score = [], [], [], []
    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    f_score = f1_score(y_test, predictions)

    return accuracy, recall, precision, f_score

