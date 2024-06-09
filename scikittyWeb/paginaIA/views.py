import requests
from django.urls import reverse
from django.shortcuts import redirect, render
from django.template import Template, Context
from django.middleware.csrf import get_token

# Create your views here.
def home(request):
    return render(request, 'home.html')

def error(request, mensaje):
    mensaje = request.GET.get('mensaje')
    return render(request, 'error.html',{'mensaje':mensaje})

def binario_binario(request):
    response = requests.get('http://127.0.0.1:8001/cargar_previos')

    if response.status_code == 200:
        csv_list = response.json()

    return render(request, 'binario_binario.html',{'csv_list':csv_list})

def model_details(request, model_name):
    model_name = request.GET.get('modelo')
    return render(request, 'model_details.html',{'model_name': model_name})

def select_y_column(request):
    return render(request, 'select_y_column.html')

def seleccionar_Y(request):
    if request.method == 'POST':
        tree_action = request.POST.get('tree_action')
        url = 'http://127.0.0.1:8001/y_column'
        altura = ''

        if tree_action == 'load_tree':
            form_model_name = request.POST.get('modelo')
            data = {'name': form_model_name}

            respuesta = requests.post(url, data = data)
            model_name = form_model_name

        elif tree_action == 'create_tree':
            archivo_csv = request.FILES['archivo_csv']
            nombre_archivo = archivo_csv.name

            altura = request.POST.get('altura')
            archivos = {'archivo': archivo_csv}
            archivos['name'] = nombre_archivo

            data = {'altura':altura}

            respuesta = requests.post(url, files=archivos, data=data)
            model_name = nombre_archivo

        if respuesta.status_code == 200:
            return render(request,'select_y_column.html',
            {'name':model_name, 'altura':altura, 'tree_action':tree_action, 'column_list':respuesta.json()})
        
        else:
            mensaje = "Hubo un error al enviar el archivo al servidor remoto."

        return render(request, 'error.html', {'mensaje': mensaje})

def tree(request):
    if request.method == 'POST':
        form_model_name = request.POST.get('modelo')
        y_column = request.POST.get('y_column')
        altura = request.POST.get('altura')
        tree_action = request.POST.get('tree_action')

        if tree_action == 'load_tree':
            url = 'http://127.0.0.1:8001/load_tree'
            data = {'name': form_model_name, 'y_column': y_column}

        else:
            url = 'http://127.0.0.1:8001/create_tree'
            data = {'name': form_model_name, 'y_column': y_column, 'altura':altura}

        respuesta = requests.post(url, data = data)

        if respuesta.status_code == 200:
                return render(request, 'model_details.html',{'model_name':form_model_name})
        else:
            mensaje = "Hubo un error al enviar los datos al servidor remoto."
    return render(request, 'error.html',{'mensaje': mensaje})

def get_image_tree(request):
    if request.method == 'POST':

        form_model_name = request.POST['model_name']

        archivo_csv = {'model_name':form_model_name}

        url = 'http://127.0.0.1:8001/image_tree'

        response = requests.post(url, data=archivo_csv)

        if response.status_code == 200:

            path = './paginaIA/static/images/tree_image.png'
            with open(path, 'wb') as f:
                f.write(response.content)
            
            details = """<br><img src="/static/images/tree_image.png" class="image_tree"></img> """

            return render(request, 'model_details.html',{'details':details,'model_name':form_model_name})

        mensaje = "Hubo un error al cargar la imagen."

    return render(request, 'error.html',{'mensaje': mensaje})

def get_image_matrix(request):
    if request.method == 'POST':
        positive = request.POST.get('option')
        form_model_name = request.POST['model_name']

        url = 'http://127.0.0.1:8001/metrics'

        data = {"positive":positive}

        respuesta = requests.post(url, data=data)
        metricas = respuesta.json()

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
           mensaje = "Hubo un error al cargar la imagen."

    return render(request, 'error.html',{'mensaje': mensaje})

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
        
    mensaje = "Hubo un error al cargar los datos."

    return render(request, 'error.html',{'mensaje': mensaje})

def get_image_ROC(request):
    if request.method == 'POST':
        form_model_name = request.POST['model_name']

    details = """ <div> Esto es para la siguiente entrega profe ╰(*°▽°*)╯ </div> """
    return render(request, 'model_details.html',{'details': details,'model_name': form_model_name})