# Generated by Django 2.2.14 on 2022-09-20 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoteriaApp', '0006_auto_20220920_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='monto_divisa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_en_dolares', models.CharField(max_length=250)),
            ],
        ),
    ]
