# Generated by Django 2.2.7 on 2019-12-22 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0006_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sklep.Discount'),
        ),
    ]
