# Generated by Django 5.1.1 on 2024-10-02 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_alter_categorys_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorys',
            name='name',
            field=models.CharField(choices=[('action', 'Action'), ('comedy', 'Comedy'), ('drama', 'Drama'), ('horror', 'Horror'), ('science_fiction', 'Science Fiction'), ('romance', 'Romance'), ('thriller', 'Thriller'), ('animation', 'Animation'), ('documentary', 'Documentary'), ('fantasy', 'Fantasy')], max_length=30),
        ),
    ]
