# Generated by Django 2.0.5 on 2018-06-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submits',
            name='pass_field',
            field=models.CharField(db_column='pass', max_length=20),
        ),
    ]
