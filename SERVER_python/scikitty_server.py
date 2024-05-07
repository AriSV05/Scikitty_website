import os
import pandas as pd
from flask import Flask, jsonify, request, send_file
import numpy as np
import scikitty_funtions as sk
from classes import DecisionTreeClassifier, Metrics

app = Flask(__name__)

y_test_saved = None
x_test_saved = None
classifier_saved = None
uniques_targets_saved = None

@app.route('/')
def inicio():
    return "Scikitty server funcionando!"

@app.route('/guardar_csv', methods=['POST'])
def guardar_csv():
    archivo_csv = request.files['archivo']
    nombre_archivo = archivo_csv.filename

    archivo_csv.save(f'./demos/{nombre_archivo}')

    return "Archivo CSV recibido y procesado correctamente"

@app.route('/cargar_previos', methods=['GET'])
def cargar_previos():
    ruta_carpeta = './models'#TODO 
    
    nombres_archivos = os.listdir(ruta_carpeta)

    return jsonify(nombres_archivos)

@app.route('/create_tree', methods=['POST'])
def create_tree():
    global y_test_saved, classifier_saved, x_test_saved, uniques_targets_saved

    csv_name = request.form['model_name']

    csv_generator = sk.read_csv_with_column_names(csv_name)
    col_names = next(csv_generator)  # Obtener los nombres de las columnas
    data = pd.DataFrame(csv_generator, columns=col_names)
    X = data.iloc[:, :-1].values
    Y = data.iloc[:, -1].values.reshape(-1,1)

    X_train, X_test, Y_train, Y_test = sk.train_test_split(X, Y)

    classifier = DecisionTreeClassifier(min_samples_split=3, max_depth=3)
    classifier.fit(X_train,Y_train)
    
    classifier_saved = classifier

    y_test_saved = Y_test
    x_test_saved =  X_test

    classifier.print_tree(data=data) #impresion en consola

    targets = np.array(Y).flatten()
    uniques_targets = np.unique(targets)
    uniques_targets_saved = uniques_targets


@app.route('/load_tree', methods=['POST'])
def create_tree():
    global y_test_saved, classifier_saved, x_test_saved, uniques_targets_saved

    csv_name = request.form['model_name']
    model_name = csv_name
    model_name.split(".")[0]
    model_name += ".pkl"

    csv_generator = sk.read_csv_with_column_names(csv_name)
    col_names = next(csv_generator)  # Obtener los nombres de las columnas
    data = pd.DataFrame(csv_generator, columns=col_names)
    X = data.iloc[:, :-1].values
    Y = data.iloc[:, -1].values.reshape(-1,1)

    _, X_test, _, Y_test = sk.train_test_split(X, Y)

    
    classifier_saved = sk.import_model(model_name)

    y_test_saved = Y_test
    x_test_saved =  X_test

    classifier_saved.print_tree(data=data) #impresion en consola

    targets = np.array(Y).flatten()
    uniques_targets = np.unique(targets)
    uniques_targets_saved = uniques_targets

@app.route('/select_positives', methods=['GET'])
def select_positives():
    global uniques_targets_saved
    return jsonify(uniques_targets_saved)
    

@app.route('/metrics', methods=['POST'])
def metrics():
    global y_test_saved, x_test_saved, classifier_saved

    y_test = classifier_saved.predict(x_test_saved)

    positive = request.form['positive']

    accuracy = Metrics.accuracy_score(y_test_saved, y_test)
    precision = Metrics.precision_score(y_test_saved, y_test, positive)
    recall = Metrics.recall_score(y_test_saved, y_test, positive)
    f1 = Metrics.f1_score(precision, recall)
    #matriz png

    return accuracy,precision,recall,f1

if __name__ == '__main__':
    app.run(debug=True, port=8001)

