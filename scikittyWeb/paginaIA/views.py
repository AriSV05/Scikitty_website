from django.http import HttpResponseRedirect
import requests

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def binario_binario(request):
    return render(request, 'binario_binario.html')

def model_details(request, model_name):
    return render(request, 'model_details.html',{'model_name': model_name})

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
            return HttpResponseRedirect(f'/model_details/{nombre_archivo}')
        else:
            mensaje = "Hubo un error al enviar el archivo al servidor remoto."

        return render(request, 'binario_binario.html', {'mensaje': mensaje})

def get_image_tree(request):
    if request.method == 'POST':

        form_model_name = request.POST['model_name']

        archivo_csv = {'model_name':form_model_name}

        url = 'http://127.0.0.1:8001/image_tree'

        # Hacer la solicitud POST al servidor remoto con el archivo adjunto
        response = requests.post(url, data=archivo_csv)

        path = './paginaIA/static/images/tree_image.png'
        with open(path, 'wb') as f:
            f.write(response.content)
        read_path = "/static/images/tree_image.png"

    return render(request, 'model_details.html',{'detail': read_path,'model_name': form_model_name})
