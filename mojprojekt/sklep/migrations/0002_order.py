# Generated by Django 2.2.7 on 2019-11-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('send', models.CharField(max_length=100)),
            ],
        ),
    ]