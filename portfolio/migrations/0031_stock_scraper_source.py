# Generated by Django 5.0.1 on 2024-11-04 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0030_alter_account_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='scraper_source',
            field=models.CharField(choices=[('ft', 'ft'), ('yahoo', 'yahoo')], default='ft', max_length=5),
        ),
    ]
