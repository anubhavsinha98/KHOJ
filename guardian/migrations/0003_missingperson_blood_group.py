# Generated by Django 2.1 on 2020-02-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guardian', '0002_auto_20200207_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='missingperson',
            name='blood_group',
            field=models.TextField(blank=True, null=True),
        ),
    ]