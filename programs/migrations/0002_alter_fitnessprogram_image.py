# Generated by Django 5.0.2 on 2024-10-26 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessprogram',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='program_images/'),
        ),
    ]
