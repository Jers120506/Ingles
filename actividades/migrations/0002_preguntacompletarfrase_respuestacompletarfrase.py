# Generated by Django 5.1.6 on 2025-03-29 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreguntaCompletarFrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(help_text="Usa '[...]' para indicar los espacios a completar.")),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preguntas_completar_frase', to='actividades.evaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaCompletarFrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicion', models.PositiveIntegerField(help_text='Posición del espacio en la oración (orden).')),
                ('respuesta_correcta', models.CharField(max_length=255)),
                ('alternativas', models.TextField(blank=True, help_text='Sinónimos separados por comas (opcional).')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='actividades.preguntacompletarfrase')),
            ],
        ),
    ]
