# Generated by Django 3.0.5 on 2020-05-15 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200515_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='notes',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
