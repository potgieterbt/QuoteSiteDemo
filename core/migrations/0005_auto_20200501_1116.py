# Generated by Django 3.0.5 on 2020-05-01 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200501_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
