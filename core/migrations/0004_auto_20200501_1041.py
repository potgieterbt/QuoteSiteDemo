# Generated by Django 3.0.5 on 2020-05-01 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_quote_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]