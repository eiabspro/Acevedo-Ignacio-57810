from django.urls import path, include
from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from entidades.views import *


urlpatterns = [
    #-- Inicio - Acerca - Contacto
    path('', home, name="inicio"),
    path('acerca/', acerca, name="acerca"),
    path('contacto/', contacto, name="contacto"),

    #-- Autores
    path('autores/', AutorList.as_view(), name="autores"),
    path('autoresCreate/', AutorCreate.as_view(), name="autoresCreate"),
    path('autoresUpdate/<int:pk>/', AutorUpdate.as_view(), name="autoresUpdate"),
    path('autoresDelete/<int:pk>/', AutorDelete.as_view(), name="autoresDelete"),

    #-- Libros

    path('libros/', LibroList.as_view(), name="libros"),
    path('librosCreate/', LibroCreate.as_view(), name="librosCreate"),
    path('librosUpdate/<int:pk>/', LibroUpdate.as_view(), name="librosUpdate"),
    path('librosDelete/<int:pk>/', LibroDelete.as_view(), name="librosDelete"),   
        # Buscar
    path('buscarLibro/', buscarLibro, name="buscarLibro"),
    path('encontrarLibro/', encontrarLibro, name="encontrarLibro"),

    #-- Usuarios 
    path('usuarios/', UsuarioList.as_view(), name="usuarios"),
    path('usuariosCreate/', UsuarioCreate.as_view(), name="usuariosCreate"),
    path('usuariosUpdate/<int:pk>/', UsuarioUpdate.as_view(), name="usuariosUpdate"),
    path('usuariosDelete/<int:pk>/', UsuarioDelete.as_view(), name="usuariosDelete"),



    #-- Prestamos
    path('prestamos/', PrestamoList.as_view(), name="prestamos"),
    path('prestamosCreate/', PrestamoCreate.as_view(), name="prestamosCreate"),
    path('prestamosUpdate/<int:pk>/', PrestamoUpdate.as_view(), name="prestamosUpdate"),
    path('prestamosDelete/<int:pk>/', PrestamoDelete.as_view(), name="prestamosDelete"),
    path('prestamos/completar/<int:pk>/', completar_prestamo, name="completar_prestamo"),

    #-- Login / Logout / Regitro
    path('login/', loginRequest, name="login"),
    path('logout/', LogoutView.as_view(template_name="entidades/logout.html"), name="logout"),
    path('registro/', registro, name="registro"),

    #-- Edición de Perfil / Avatar
    path('perfil/', editProfile, name="perfil"),
    path('cambiar_clave/', cambiar_clave, name='cambiarClave'),
    path('agregar_avatar/', agregarAvatar, name='agregar_avatar'),
]
