# Generated by Django 3.0.3 on 2020-04-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0021_auto_20200418_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dividend',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='stock',
            name='yahoo_code',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
