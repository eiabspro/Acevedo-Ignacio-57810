# Generated by Django 5.0.6 on 2024-07-15 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0004_alter_libro_isbn_alter_usuario_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestamo',
            name='fecha_devolucion',
        ),
        migrations.AddField(
            model_name='libro',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='devuelto',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha_prestamo',
            field=models.DateField(auto_now_add=True),
        ),
    ]
