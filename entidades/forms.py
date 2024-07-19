from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm

from django.db.models import Q
from entidades.models import Autor, Libro, Usuario, Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Si estamos actualizando un préstamo, incluimos el libro actual en el queryset
            self.fields['libro'].queryset = Libro.objects.filter(Q(disponible=True) | Q(pk=self.instance.libro.pk))
        else:
            self.fields['libro'].queryset = Libro.objects.filter(disponible=True)

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ["nombre", "apellido", "dni", "nacionalidad"]

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit():
            raise forms.ValidationError('El DNI debe contener solo números.')
        if len(dni) not in [8]:
            raise forms.ValidationError('El DNI debe tener 8 dígitos.')
        if Autor.objects.filter(dni=dni).exists():
            raise forms.ValidationError('El DNI ya existe.')
        return dni

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "fecha_publicacion", "genero", "isbn", "autor"]

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn.isdigit():
            raise forms.ValidationError('El ISBN debe contener solo números.')
        if len(isbn) not in [10, 13]: # el identificador unico para libros debe ser de 10 o 13 digitos
            raise forms.ValidationError('El ISBN debe tener 10 o 13 dígitos.')
        if Libro.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError('El ISBN ya existe.')
        return isbn
    
class RegistroForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")    
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Contraseña a confirmar", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

class UserEditForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nombre", max_length=50, required=True)
    last_name = forms.CharField(label="Apellido", max_length=50, required=True)
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Contraseña actual", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmar nueva contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)