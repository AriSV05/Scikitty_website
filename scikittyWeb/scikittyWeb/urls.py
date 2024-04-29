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
    path('loaded_model/', views.loaded_model, name='loaded_model'),
    path('model_details/<str:model_name>/', views.model_details, name='model_details'),
    path('binario_binario/', views.binario_binario, name='binario_binario'),
    path('guardar_csv/', views.guardar_csv, name='guardar_csv'),
    path('get_image_tree/', views.get_image_tree, name='get_image_tree'),
]

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# urlpatterns += staticfiles_urlpatterns()