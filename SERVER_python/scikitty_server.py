import os
import pandas as pd
from flask import Flask, jsonify, request, send_file
import scikitty_funtions as sk
from classes import DecisionTreeClassifier, Metrics

app = Flask(__name__)

y_test_saved = None
y_pred_saved = None

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
    ruta_carpeta = './demos'#TODO 
    
    nombres_archivos = os.listdir(ruta_carpeta)

    return jsonify(nombres_archivos)

@app.route('/image_tree', methods=['POST'])
def image_tree():
    global y_test_saved, y_pred_saved

    csv_name = request.form['model_name']

    csv_generator = sk.read_csv_with_column_names(csv_name)
    col_names = next(csv_generator)  # Obtener los nombres de las columnas
    data = pd.DataFrame(csv_generator, columns=col_names)
    X = data.iloc[:, :-1].values
    Y = data.iloc[:, -1].values.reshape(-1,1)

    X_train, X_test, Y_train, Y_test = sk.train_test_split(X, Y)
    
    y_test_saved = Y_test

    classifier = DecisionTreeClassifier(min_samples_split=3, max_depth=3)
    classifier.fit(X_train,Y_train)
    classifier.print_tree(data=data)

    y_pred_saved = classifier.predict(X_test)

    #sk.image_tree_model(X,y,model)

    #return send_file("./image_tree_model/tree.png", mimetype='image/png')

@app.route('/image_tree', methods=['POST'])
def metrics():
    global y_test_saved, y_pred_saved

    positive = request.form['positive']

    accuracy = Metrics.accuracy_score(y_test_saved, y_pred_saved)
    precision = Metrics.precision_score(y_test_saved, y_pred_saved, positive)
    recall = Metrics.recall_score(y_test_saved, y_pred_saved, positive)
    f1 = Metrics.f1_score(precision, recall)
    #matriz png

    return accuracy,precision,recall,f1

if __name__ == '__main__':
    app.run(debug=True, port=8001)

