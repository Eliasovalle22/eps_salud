# Generated by Django 5.2.1 on 2025-05-27 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_medico_especialidad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='direccion',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AddField(
            model_name='medico',
            name='telefono',
            field=models.CharField(default='-', max_length=15),
        ),
    ]
