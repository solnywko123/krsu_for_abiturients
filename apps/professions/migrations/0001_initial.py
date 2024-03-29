# Generated by Django 3.2 on 2022-06-19 21:06

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Условие поступления',
                'verbose_name_plural': 'Условия поступления',
            },
        ),
        migrations.CreateModel(
            name='AdmissionConditionForCitizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship', models.CharField(help_text='например: "Для граждан Кыргызстана"', max_length=255, verbose_name='Гражданство')),
                ('condition', models.TextField(verbose_name='Условия')),
            ],
            options={
                'verbose_name': 'Условие поступления для граждан',
                'verbose_name_plural': 'Условия поступления для граждан',
            },
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Описание')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Позиция')),
                ('admission_condition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professions', to='professions.admissioncondition', verbose_name='Условия поступления')),
            ],
            options={
                'verbose_name': 'Направление',
                'verbose_name_plural': 'Направления',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ProfessionGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='professions/%Y/', verbose_name='Изображение')),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='professions.profession', verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Изображение галлереи специальности',
                'verbose_name_plural': 'Галлерея специальностей',
            },
        ),
        migrations.AddField(
            model_name='admissioncondition',
            name='for_citizens',
            field=models.ManyToManyField(blank=True, related_name='admission_conditions', to='professions.AdmissionConditionForCitizen', verbose_name='Для граждан'),
        ),
    ]
