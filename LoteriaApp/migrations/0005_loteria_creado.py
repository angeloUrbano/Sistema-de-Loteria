# Generated by Django 2.2.14 on 2022-09-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoteriaApp', '0004_auto_20220916_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='loteria',
            name='creado',
            field=models.DateField(auto_now=True),
        ),
    ]
