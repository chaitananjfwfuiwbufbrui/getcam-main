# Generated by Django 3.1.7 on 2021-04-02 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchant', '0002_delete_mechant'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthly_revunue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=9)),
                ('revunue', models.IntegerField(default=0)),
            ],
        ),
    ]
