from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseRedirect

from entidades.models import *
from entidades.forms import *

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash

# Create your views here.

#-- Home/Inicio
def home(request):
    return render(request, "entidades/index.html")

#-- Acerca y contacto
def acerca(request):
    return render(request, "entidades/acerca.html")

def contacto(request):
    return render(request, "entidades/contacto.html")

#-- Autor

class AutorList(LoginRequiredMixin, ListView):
    model = Autor
    template_name = 'entidades/autor_list.html'
    context_object_name = 'autores'

class AutorCreate(LoginRequiredMixin, CreateView):
    model = Autor
    form_class = AutorForm
    success_url = reverse_lazy("autores")

class AutorUpdate(LoginRequiredMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    success_url = reverse_lazy("autores")
    
class AutorDelete(LoginRequiredMixin, DeleteView):
    model = Autor
    success_url = reverse_lazy("autores")

#-- Libro

class LibroList(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'entidades/libro_list.html'
    context_object_name = 'libros'

class LibroCreate(LoginRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    success_url = reverse_lazy("libros")

    def form_valid(self, form):
        form.instance.disponible = True
        return super().form_valid(form)
    
class LibroUpdate(LoginRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    success_url = reverse_lazy("libros")

    def form_valid(self, form):
        form.instance.disponible = True
        return super().form_valid(form)
    
class LibroDelete(LoginRequiredMixin, DeleteView):
    model = Libro
    success_url = reverse_lazy("libros")

#-- Usuario

class UsuarioList(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'entidades/usuario_list.html'
    context_object_name = 'usuarios'

class UsuarioCreate(LoginRequiredMixin, CreateView):
    model = Usuario
    fields = ["nombre", "apellido", "email"]
    success_url = reverse_lazy("usuarios")

    def form_valid(self, form):
        form.instance.fecha_registro = timezone.now()
        return super().form_valid(form)

class UsuarioUpdate(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ["nombre", "apellido", "email"]
    success_url = reverse_lazy("usuarios")

    def form_valid(self, form):
        form.instance.fecha_registro = timezone.now()
        return super().form_valid(form)
    
class UsuarioDelete(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy("usuarios")

#-- Prestamo

class PrestamoList(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'entidades/prestamo_list.html'
    context_object_name = 'prestamos'

class PrestamoCreate(LoginRequiredMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm
    success_url = reverse_lazy("prestamos")

    def form_valid(self, form):
        form.instance.fecha_prestamo = timezone.now()
        form.instance.devuelto = False
        return super().form_valid(form)

class PrestamoUpdate(LoginRequiredMixin, UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    success_url = reverse_lazy("prestamos")

    def form_valid(self, form):
        form.instance.fecha_prestamo = timezone.now()
        form.instance.devuelto = False
        return super().form_valid(form)
    
class PrestamoDelete(LoginRequiredMixin, DeleteView):
    model = Prestamo
    success_url = reverse_lazy("prestamos")

@login_required
def completar_prestamo(request, pk):
    if request.method == "POST":
        prestamo = get_object_or_404(Prestamo, pk=pk)
        if not prestamo.devuelto:  # Verifica si el préstamo no ha sido marcado como devuelto aún
            prestamo.devuelto = True
            prestamo.save()
            prestamo.libro.disponible = True
            prestamo.libro.save()

        referer_url = request.META.get("HTTP_REFERER", "prestamos")
        return redirect(referer_url)

    return redirect('prestamos')

# Buscar y encontrar
@login_required
def buscarLibro(request):
    return render(request, "entidades/buscarLibro.html")
@login_required
def encontrarLibro(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        libros = Libro.objects.filter(titulo__icontains=patron)
        contexto = {'libros': libros}
    else:
        contexto = {'libros': Libro.objects.all()}
    return render(request, "entidades/libro_list.html", contexto)

#-- Login / Logout / Registration

def loginRequest(request):
    if request.method == "POST":
        usuario = request.POST["username"]
        clave = request.POST["password"]
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)

            #-- buscar/Recuperar avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).img.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar
            #--
            return render(request, "entidades/index.html")
        else:
            return redirect(reverse_lazy('login'))
    else:
        miForm = AuthenticationForm()

    return render(request, "entidades/login.html", {"form": miForm})

def registro(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)
        if miForm.is_valid():
            
            miForm.save()
            return redirect(reverse_lazy('inicio'))
        else:
            return redirect(reverse_lazy('login'))
    else:
        miForm = RegistroForm()

    return render(request, "entidades/registro.html", {"form": miForm})

#-- Edicion de Perfil / Avatar

@login_required
def editProfile(request):
    usuario = request.user
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("first_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy("inicio"))
    else:
        miForm = UserEditForm(instance=usuario)
    return render(request, "entidades/editar_perfil.html", {"form": miForm})
    
@login_required
def cambiar_clave(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse_lazy('inicio'))
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'entidades/cambiar_clave.html', {'form': form})
    
@login_required
def agregarAvatar(request):
   if request.method == "POST":
       miForm = AvatarForm(request.POST, request.FILES)
       if miForm.is_valid():
           usuario = User.objects.get(username=request.user)
           imagen = miForm.cleaned_data["imagen"]
           #_________ Borrar avatares viejos
           avatarViejo = Avatar.objects.filter(user=usuario)
           if len(avatarViejo) > 0:
               for i in range(len(avatarViejo)):
                   avatarViejo[i].delete()
           #__________________________________________
           avatar = Avatar(user=usuario, imagen=imagen)
           avatar.save()#
           #_________ Enviar la imagen al inicio
           imagen = Avatar.objects.get(user=usuario).imagen.url
           request.session["avatar"] = imagen
           #____________________________________________________
           return redirect(reverse_lazy("inicio"))
   else:
       miForm = AvatarForm()
   return render(request, "entidades/agregar_avatar.html", {"form": miForm})    
