# Generated by Django 3.1.5 on 2021-04-16 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0025_auto_20210410_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
