# Generated by Django 3.2.6 on 2021-09-10 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops_site', '0004_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('division', models.CharField(choices=[('1,', 'DCFD'), ('2', 'DDI'), ('3', 'DEI'), ('4', 'DFS'), ('5', 'OD')], max_length=5)),
                ('roles', models.ManyToManyField(to='ops_site.Role')),
            ],
            options={
                'verbose_name_plural': 'People',
            },
        ),
    ]
