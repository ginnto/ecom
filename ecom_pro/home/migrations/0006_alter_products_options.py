# Generated by Django 4.2 on 2023-05-08 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_categ_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['-date']},
        ),
    ]
