# Generated by Django 5.0.6 on 2024-07-17 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_remove_autor_fecha_nacimiento_autor_dni'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'ordering': ['dni'], 'verbose_name': 'Autor', 'verbose_name_plural': 'Autores'},
        ),
    ]
