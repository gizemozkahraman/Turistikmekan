# Generated by Django 3.0.3 on 2020-05-14 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200514_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='aboutus',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='contact',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='referances',
            field=models.TextField(blank=True),
        ),
    ]
