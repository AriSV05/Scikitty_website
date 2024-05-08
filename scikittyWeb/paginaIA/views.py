import requests
from django.urls import reverse
from django.shortcuts import render
from django.template import Template, Context
from django.middleware.csrf import get_token

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

def load_tree(request):

    if request.method == 'POST':

            form_model_name = request.POST.get('modelo')

            url = 'http://127.0.0.1:8001/load_tree'
            data = {'form_model_name': form_model_name}

            respuesta = requests.post(url, data = data)

            if respuesta.status_code == 200:
                return render(request, 'model_details.html',{'model_name':form_model_name})
            else:
                mensaje = "Hubo un error al enviar el archivo al servidor remoto."

    return render(request, 'binario_binario.html', {'mensaje': mensaje})

def create_tree(request):
    if request.method == 'POST':

        archivo_csv = request.FILES['archivo_csv']
        nombre_archivo = archivo_csv.name

        altura = request.POST.get('altura')

        url = 'http://127.0.0.1:8001/create_tree'

        archivos = {'archivo': archivo_csv}
        archivos['nombre_archivo'] = nombre_archivo

        data = {'altura':altura}

        respuesta = requests.post(url, files=archivos, data=data)

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

    details = """<br><img src="/static/images/tree_image.png" class="image_tree"></img> """

    return render(request, 'model_details.html',{'details': details,'model_name': form_model_name})

def get_image_matrix(request):
    if request.method == 'POST':
        positive = request.POST.get('option')
        form_model_name = request.POST['model_name']

        url = 'http://127.0.0.1:8001/metrics'

        data = {"positive":positive}

        respuesta = requests.post(url, data=data)
        metricas = respuesta.json()
        print(metricas)

        details = f""" 
                    <br><br><br>
                    <div> Accuracy: {metricas['Accuracy']} </div>
                    <div> Precision: {metricas['Precision']} </div>
                    <div> f1: {metricas['f1']} </div>
                    <div> recall: {metricas['recall']} </div>
                    <br><br>
           """
        url = 'http://127.0.0.1:8001/metrics_image'

        respuesta = requests.get(url)
        path = './paginaIA/static/images/matrix_image.png'

        with open(path, 'wb') as f:
            f.write(respuesta.content)

        details += """ <img src="/static/images/matrix_image.png" class="image_matrix"></img> """
        
        if respuesta.status_code == 200:
            return render(request, 'model_details.html',{'details':details,'model_name':form_model_name})
        else:
            mensaje = "Hubo un error al enviar el archivo al servidor remoto."
        return mensaje

def get_positives(request):
    if request.method == 'POST':
        url_get_image_matrix = reverse('get_image_matrix')

        form_model_name = request.POST['model_name']
        response = requests.get('http://127.0.0.1:8001/select_positives')
        csrf_token = get_token(request)

        if response.status_code == 200:
            positive = response.json()

        template_string =   """
                            <br><br><br>
                            <h4>Selecciona el target positivo del modelo</h4>
                            <form method="post" action="{{ url_get_image_matrix }}" class="message">
                                <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                                <input type="hidden" name='model_name' value="{{model_name}}">
                                <br>
                                <div class="inp_cont">
                                    <input type="radio" id="option1" name="option" value="{{ positive.one }}">
                                    <label for="option1">{{ positive.one }}</label>
                                </div>
                                <div class="inp_cont">
                                    <input type="radio" id="option2" name="option" value="{{ positive.two }}">
                                    <label for="option2">{{ positive.two }}</label>
                                </div>
                                <br><br>
                                <button id="ok-button">OK</button>
                            </form>
                            """

        template = Template(template_string)
        context = Context({
            'url_get_image_matrix': url_get_image_matrix,
            'positive': positive,
            'csrf_token': csrf_token,
            'model_name': form_model_name
        })
        rendered_template = template.render(context)

    return render(request, 'model_details.html',{'details': rendered_template,'model_name': form_model_name})

def get_image_ROC(request):
    if request.method == 'POST':
        form_model_name = request.POST['model_name']

    details = """ <div> Esto es para la siguiente entrega profe ╰(*°▽°*)╯ </div> """
    return render(request, 'model_details.html',{'details': details,'model_name': form_model_name})