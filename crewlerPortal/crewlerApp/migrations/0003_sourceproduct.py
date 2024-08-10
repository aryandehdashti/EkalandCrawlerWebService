# Generated by Django 4.2.5 on 2023-11-10 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crewlerApp', '0002_alter_product_color_alter_product_insurance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('URL', models.URLField(blank=True, null=True, unique=True)),
                ('provider', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]