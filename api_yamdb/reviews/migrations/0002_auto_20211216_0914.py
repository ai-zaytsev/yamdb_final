# Generated by Django 2.2.16 on 2021-12-16 09:14

from django.db import migrations, models
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['pub_date']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['year']},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[reviews.models.year_validator]),
        ),
    ]
