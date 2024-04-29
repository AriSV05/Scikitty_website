import requests

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def binario_binario(request):
    return render(request, 'binario_binario.html')

def cargar_csv(request):
    if request.method == 'POST':
        # Obtener el archivo CSV cargado por el usuario
        archivo_csv = request.FILES['archivo_csv']
        nombre_archivo = archivo_csv.name

        # URL del servidor remoto
        url = 'http://127.0.0.1:8001/analizar_csv'

        # Crear un diccionario con el archivo adjunto
        archivos = {'archivo': archivo_csv}
        archivos['nombre_archivo'] = nombre_archivo

        # Hacer la solicitud POST al servidor remoto con el archivo adjunto
        respuesta = requests.post(url, files=archivos)

        # Verificar el estado de la respuesta
        if respuesta.status_code == 200:
            mensaje = "El archivo se ha enviado correctamente al servidor remoto."
        else:
            mensaje = "Hubo un error al enviar el archivo al servidor remoto."

        return render(request, 'binario_binario.html', {'mensaje': mensaje})

    return render(request, 'binario_binario.html')#TODO render a new page

def get_image_tree(request):
    if request.method == 'GET':

        # URL del servidor remoto
        url = 'http://127.0.0.1:8001/image_tree'

        # Hacer la solicitud POST al servidor remoto con el archivo adjunto
        response = requests.get(url)

        # Verificar el estado de la respuesta
        with open('./paginaIA/static/images/tree_image.png', 'wb') as f:
            f.write(response.content)

    return render(request, 'binario_binario.html')#TODO render a new page
