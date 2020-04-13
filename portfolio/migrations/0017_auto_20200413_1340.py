# Generated by Django 3.0.3 on 2020-04-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0016_holding_value_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='holding',
            options={'ordering': ['stock']},
        ),
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['-date', 'stock']},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
    ]
