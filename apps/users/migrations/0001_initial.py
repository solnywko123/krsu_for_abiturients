# Generated by Django 3.2 on 2022-06-19 21:06

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetterMailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в')),
            ],
            options={
                'verbose_name': 'Письмо для рассылки',
                'verbose_name_plural': 'Письма для рассылки',
            },
        ),
        migrations.CreateModel(
            name='UserRegistrationApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('password', models.CharField(max_length=128, verbose_name='Пароль')),
                ('verification_code', models.PositiveSmallIntegerField(unique=True, verbose_name='Код подтверждения')),
            ],
            options={
                'verbose_name': 'Заявка на регистрацию',
                'verbose_name_plural': 'Заявки на регистрацию',
                'unique_together': {('email', 'verification_code')},
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=25, null=True)),
                ('citizenship', models.PositiveSmallIntegerField(choices=[(1, 'Кыргызстан'), (2, 'Россия'), (3, 'Казахстан'), (4, 'Белоруссия'), (5, 'Таджикистан'), (0, 'Другое')], null=True, verbose_name='Гражданство')),
                ('school_fullname', models.CharField(default='', max_length=255, verbose_name='Школа')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Abiturient',
            fields=[
            ],
            options={
                'verbose_name': 'Абитуриент',
                'verbose_name_plural': 'Абитуриенты',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='StaffUser',
            fields=[
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='LetterMailingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Описание')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в')),
                ('abiturients', models.ManyToManyField(help_text='данным абитуриентам были отправлены письма', related_name='mailed_letters', to='users.Abiturient', verbose_name='Абитуриенты')),
            ],
            options={
                'verbose_name': 'История Письмо для рассылки',
                'verbose_name_plural': 'История Письма для рассылки',
            },
        ),
    ]