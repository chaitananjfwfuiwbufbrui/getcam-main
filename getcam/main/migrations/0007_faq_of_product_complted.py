# Generated by Django 3.1.2 on 2021-03-27 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_faq_of_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq_of_product',
            name='complted',
            field=models.BooleanField(default=False),
        ),
    ]
