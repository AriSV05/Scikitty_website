import os
import pandas as pd
from flask import Flask, jsonify, request, send_file
import numpy as np
from scikitty import scikitty_funtions as sk
from scikitty.models.DecisionTree import DecisionTreeClassifier
from scikitty.metrics.metrics import accuracy_score, recall_score, precision_score, f1_score, img_confusion_matrix

app = Flask(__name__)

y_test_saved = None
x_test_saved = None
classifier_saved = None
uniques_targets_saved = None

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@app.route('/')
def inicio():
    return "Scikitty server funcionando!"

@app.route('/cargar_previos', methods=['GET'])
def cargar_previos():
    global project_root

    ruta_carpeta = os.path.join(project_root, 'SERVER_python/created_models')
    
    nombres_archivos = os.listdir(ruta_carpeta)

    return jsonify(nombres_archivos)

@app.route('/create_tree', methods=['POST'])
def create_tree():
    global y_test_saved, classifier_saved, x_test_saved, uniques_targets_saved, project_root

    archivo_csv = request.files['archivo']
    nombre_archivo = archivo_csv.filename.split(".")[0]

    csv = os.path.join(project_root, 'csv', nombre_archivo)
    model = os.path.join(project_root, 'SERVER_python/created_models')
    img = os.path.join(project_root, 'SERVER_python/image_model/TreeDecision')

    altura = int(request.form['altura'])

    archivo_csv.save(f'{csv}.csv')

    data = sk.read_csv_with_column_names(csv)
    X = data.iloc[:, :-1].values
    Y = data.iloc[:, -1].values.reshape(-1,1)

    X_train, X_test, Y_train, Y_test = sk.train_test_split(X, Y)

    classifier = DecisionTreeClassifier(min_samples_split= 2, max_depth=altura)
    classifier.fit(X_train,Y_train)
    
    classifier_saved = classifier

    y_test_saved = Y_test
    x_test_saved =  X_test


    classifier.print_tree(data=data) #consola
    classifier.image_tree_model(Y, data, img) #png

    sk.save_model(classifier_saved, nombre_archivo, model)

    targets = np.array(Y).flatten()
    uniques_targets = np.unique(targets)
    uniques_targets_saved = uniques_targets

    return "Modelo correctamente"


@app.route('/load_tree', methods=['POST'])
def load_tree():
    global y_test_saved, classifier_saved, x_test_saved, uniques_targets_saved, project_root

    model_name = request.form['form_model_name']
    csv_name = model_name.split(".")[0]

    csv = os.path.join(project_root, 'csv', csv_name)
    model = os.path.join(project_root, 'SERVER_python/created_models', model_name)

    data = sk.read_csv_with_column_names(csv)
    X = data.iloc[:, :-1].values
    Y = data.iloc[:, -1].values.reshape(-1,1)

    _, X_test, _, Y_test = sk.train_test_split(X, Y)
    
    classifier_saved = sk.import_model(model)

    y_test_saved = Y_test
    x_test_saved =  X_test

    classifier_saved.print_tree(data=data) #consola
    #classifier_saved.image_tree_model(Y, data) #png
    
    targets = np.array(Y).flatten()
    uniques_targets = np.unique(targets)
    uniques_targets_saved = uniques_targets

    return "Modelo correctamente"

@app.route('/select_positives', methods=['GET'])
def select_positives():
    global uniques_targets_saved

    targets = {
        "one":uniques_targets_saved[0],
        "two":uniques_targets_saved[1]
    }

    return jsonify(targets)
    

@app.route('/metrics', methods=['POST'])
def metrics():
    global y_test_saved, x_test_saved, classifier_saved

    y_pred = classifier_saved.predict(x_test_saved)
 
    positive = request.form['positive']

    accuracy = accuracy_score(y_test_saved, y_pred)
    precision = precision_score(y_test_saved, y_pred, positive)
    recall = recall_score(y_test_saved, y_pred, positive)
    f1 = f1_score(precision, recall)

    img_confusion_matrix(y_test_saved, y_pred)

    results = {
        "Accuracy":accuracy,
        "Precision":precision,
        "recall":recall,
        "f1":f1
    }

    return jsonify(results)

@app.route('/metrics_image', methods=['GET'])
def metrics_image():
    matrix_route = "./image_model/Confusion_Matrix.png"

    return send_file(matrix_route, mimetype='image/png')


@app.route('/image_tree', methods=['POST'])
def image_tree():

    tree_route = "./image_model/TreeDecision.png"

    return send_file(tree_route, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=8001)

