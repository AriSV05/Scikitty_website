"""
URL configuration for scikittyWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from paginaIA import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('model_details/<str:model_name>/', views.model_details, name='model_details'),
    path('binario_binario/', views.binario_binario, name='binario_binario'),
    path('get_image_tree/', views.get_image_tree, name='get_image_tree'),
    path('get_positives/', views.get_positives, name='get_positives'),
    path('get_image_matrix/', views.get_image_matrix, name='get_image_matrix'),
    path('create_tree/', views.create_tree, name='create_tree'),
    path('load_tree/', views.load_tree, name='load_tree'),
    path('get_image_ROC/', views.get_image_ROC, name='get_image_ROC'),
]

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# urlpatterns += staticfiles_urlpatterns()