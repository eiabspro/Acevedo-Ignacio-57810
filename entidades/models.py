from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8, unique=True)
    nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        unique_together = ('nombre', 'apellido')
        ordering = ['dni']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13, unique=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        unique_together = ('nombre', 'apellido')
        ordering = ['apellido','nombre']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.libro.titulo} prestado a {self.usuario.nombre}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Es un nuevo préstamo
            if not self.libro.disponible:
                raise ValidationError('El libro ya está prestado y no se puede volver a prestar hasta que se devuelva.')
            self.libro.disponible = False
            self.libro.save()
        else:
            # Es una actualización de un préstamo existente
            old_prestamo = Prestamo.objects.get(pk=self.pk)
            if old_prestamo.libro != self.libro:
                if not self.libro.disponible:
                    raise ValidationError('El libro ya está prestado y no se puede volver a prestar hasta que se devuelva.')
                self.libro.disponible = False
                self.libro.save()
                # Establece el libro anterior como disponible
                old_prestamo.libro.disponible = True
                old_prestamo.libro.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.libro.disponible = True
        self.libro.save()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['fecha_prestamo']
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'


class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"