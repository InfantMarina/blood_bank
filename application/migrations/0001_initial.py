# Generated by Django 3.0.5 on 2020-05-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_name', models.CharField(max_length=40)),
                ('location', models.CharField(max_length=40)),
                ('mobile', models.IntegerField()),
                ('blood_group', models.CharField(max_length=7)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
