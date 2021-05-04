# Generated by Django 3.1.7 on 2021-04-02 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_faq_of_product_complted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchant', '0003_monthly_revunue'),
    ]

    operations = [
        migrations.CreateModel(
            name='mechant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revunue', models.IntegerField(default=0)),
                ('total_order', models.IntegerField(default=0)),
                ('completed_orders', models.IntegerField(default=0)),
                ('mechant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('monthly_revunue', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='merchant.monthly_revunue')),
                ('product', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.products')),
            ],
        ),
    ]