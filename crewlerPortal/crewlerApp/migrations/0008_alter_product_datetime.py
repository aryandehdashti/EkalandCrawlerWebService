# Generated by Django 4.2.5 on 2024-03-10 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crewlerApp', '0007_alter_product_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dateTime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
