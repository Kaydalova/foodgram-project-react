# Generated by Django 2.2.16 on 2023-02-03 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230203_2030'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together=set(),
        ),
    ]
