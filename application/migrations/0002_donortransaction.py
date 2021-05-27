# Generated by Django 3.0.5 on 2020-05-10 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonorTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField()),
                ('donated_to', models.CharField(max_length=50)),
                ('receiver_mobile', models.IntegerField()),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Donor')),
            ],
        ),
    ]
