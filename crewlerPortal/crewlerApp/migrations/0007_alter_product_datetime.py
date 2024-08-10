# Generated by Django 4.2.5 on 2024-03-10 09:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crewlerApp', '0006_product_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dateTime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
