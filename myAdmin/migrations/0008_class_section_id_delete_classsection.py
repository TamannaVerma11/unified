# Generated by Django 4.1.5 on 2023-04-13 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAdmin', '0007_remove_class_section_id_classsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='section_id',
            field=models.ManyToManyField(related_name='sections', to='myAdmin.section'),
        ),
        migrations.DeleteModel(
            name='ClassSection',
        ),
    ]
