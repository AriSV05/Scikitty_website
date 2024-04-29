import requests

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def binario_binario(request):
    response = requests.get('http://127.0.0.1:8001/cargar_previos')

    if response.status_code == 200:
        csv_list = response.json()

    return render(request, 'binario_binario.html',{'csv_list':csv_list})

def model_details(request, model_name):
    model_name = request.GET.get('modelo')
    return render(request, 'model_details.html',{'model_name': model_name})

def loaded_model(request):
    form_model_name = request.POST.get('modelo')

    return render(request, 'model_details.html',{'model_name':form_model_name})

def guardar_csv(request):
    if request.method == 'POST':

        archivo_csv = request.FILES['archivo_csv']
        nombre_archivo = archivo_csv.name

        url = 'http://127.0.0.1:8001/guardar_csv'

        archivos = {'archivo': archivo_csv}
        archivos['nombre_archivo'] = nombre_archivo


        respuesta = requests.post(url, files=archivos)

        if respuesta.status_code == 200:
            return render(request, 'model_details.html',{'model_name':nombre_archivo})
        else:
            mensaje = "Hubo un error al enviar el archivo al servidor remoto."

        return render(request, 'binario_binario.html', {'mensaje': mensaje})

def get_image_tree(request):
    if request.method == 'POST':

        form_model_name = request.POST['model_name']

        archivo_csv = {'model_name':form_model_name}

        url = 'http://127.0.0.1:8001/image_tree'

        response = requests.post(url, data=archivo_csv)

        path = './paginaIA/static/images/tree_image.png'
        with open(path, 'wb') as f:
            f.write(response.content)
        read_path = "/static/images/tree_image.png"

    return render(request, 'model_details.html',{'detail': read_path,'model_name': form_model_name})
