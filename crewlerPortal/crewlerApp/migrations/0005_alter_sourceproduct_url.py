# Generated by Django 4.2.5 on 2023-11-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crewlerApp', '0004_alter_sourceproduct_identifier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourceproduct',
            name='URL',
            field=models.URLField(blank=True, null=True),
        ),
    ]
