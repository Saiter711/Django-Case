# Generated by Django 2.2.7 on 2019-12-06 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0003_auto_20191203_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sklep.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sklep.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_products',
            field=models.ManyToManyField(through='sklep.OrderedProduct', to='sklep.Product'),
        ),
    ]
