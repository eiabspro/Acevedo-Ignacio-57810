# Proyecto Final - Gestión de una biblioteca

## Descripción del proyecto

En este proyecto se realiza través de una App web con Django, un gestor de una biblioteca con el registro de autores, libros, usuarios y realizar prestamos de los libros por parte de los usuarios/clientes. 

## Objetivo funcional

El objetivo de esta app es el de poder gestionar con facilidad y comodidad la disponibilidad de los libros disponibles en una biblioteca y el manejo de los prestamos realizados en la misma. De esta manera, un empleado con su usuario podra gestionar los recursos de la biblioteca de manera eficiente, incluyendo la adición, edición y eliminación de libros, autores y usuarios. También permite registrar y gestionar préstamos de libros, así como la carga y edición de avatares para los perfiles de usuario.

## Modelos

### Autor
- **nombre**
- **apellido**
- **dni**
- **nacionalidad**

### Libro
- **titulo**
- **fecha_publicacion**
- **genero**
- **isbn** - identificador único para libros
- **autor**
- **disponible** - Cambia en función de si esta siendo o no prestado

### Usuario
- **nombre**
- **apellido**
- **email**
- **fecha_registro** - Se toma desde el momento en que se registra

### Prestamo
- **libro** - libro a prestar
- **usuario** - cliente al que se le presta
- **fecha_prestamo** - Se toma desde el moemento en el que se registra
- **devuelto** - Cambia en función de si se marca o no como completado y modifica el valor **disponible** de libro

## Usuario Administrador
- ruta --> /admin
- usuario: administrador
- contraseña: 1234

# Video de navegación: 

[Video](https://drive.google.com/file/d/1vz4rvlP6sJjYskgkKa3z2VMcF4wYnPH5/view?usp=drive_link)

