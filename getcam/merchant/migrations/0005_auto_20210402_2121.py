# Generated by Django 3.1.7 on 2021-04-02 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0004_mechant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthly_revunue',
            name='month',
            field=models.CharField(choices=[('JANUARY', 'January'), ('FEBRUARY', 'February'), ('MARCH', 'March'), ('DECEMBER', 'December')], max_length=9),
        ),
    ]