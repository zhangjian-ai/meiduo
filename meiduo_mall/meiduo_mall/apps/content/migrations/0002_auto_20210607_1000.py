# Generated by Django 3.1.7 on 2021-06-07 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['category_id', 'sequence'], 'verbose_name': '广告内容', 'verbose_name_plural': '广告内容'},
        ),
        migrations.AlterModelOptions(
            name='contentcategory',
            options={'verbose_name': '广告类别', 'verbose_name_plural': '广告类别'},
        ),
    ]
