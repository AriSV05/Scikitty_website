import os
from flask import Flask, jsonify, request, send_file
import scikitty_funtions as sk

app = Flask(__name__)

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
    ruta_carpeta = './demos' 
    
    nombres_archivos = os.listdir(ruta_carpeta)

    return jsonify(nombres_archivos)

@app.route('/image_tree', methods=['POST'])
def image_tree():
    data = request.form['model_name']

    df = sk.read_csv(data)
    X,y = sk.getX_Y(df)
    X_train, X_test, y_train, y_test = sk.splitX_Y(X,y)

    model = sk.decide_and_train_tree(X_train,y_train)

    #accuracy, recall, precision, f_score = sk.cal_metrics(X_test,y_test, model)

    sk.image_tree_model(X,y,model)

    return send_file("./image_tree_model/tree.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=8001)

