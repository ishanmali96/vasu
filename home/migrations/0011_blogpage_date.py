# Generated by Django 3.2.5 on 2021-07-28 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_blogpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
