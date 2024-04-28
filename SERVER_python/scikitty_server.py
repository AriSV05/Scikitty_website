from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Scikitty server funcionando!"

@app.route('/analizar_csv', methods=['POST'])
def analizar_csv():
    archivo_csv = request.files['archivo']
    nombre_archivo = archivo_csv.filename

    print(type(archivo_csv))
    print(archivo_csv.name)

    archivo_csv.save(f'./demos/{nombre_archivo}')

    return "Archivo CSV recibido y procesado correctamente"

if __name__ == '__main__':
    app.run(debug=True, port=8001)

