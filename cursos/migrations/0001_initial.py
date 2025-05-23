# Generated by Django 5.1.6 on 2025-03-25 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('publicado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Leccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('contenido', models.TextField()),
                ('orden', models.PositiveIntegerField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='lecciones/imagenes/')),
                ('video', models.FileField(blank=True, null=True, upload_to='lecciones/videos/')),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
    ]
