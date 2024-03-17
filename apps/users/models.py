from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from solo.models import SingletonModel

from apps.users.managers import UserManager


class User(AbstractUser):
    """Users"""
    KG, RU, KZ, BY, TJ, OTHERS = 1, 2, 3, 4, 5, 0
    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField('Электронная почта', unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=25, null=True)
    citizenship = models.PositiveSmallIntegerField(
        'Гражданство', choices=((KG, 'Кыргызстан'), (RU, 'Россия'), (KZ, 'Казахстан'),
                                (BY, 'Белоруссия'), (TJ, 'Таджикистан'), (OTHERS, 'Другое')),
        null=True,
    )
    school_fullname = models.CharField(
        'Школа', default='', max_length=255,
    )

    REQUIRED_FIELDS = []

    objects = UserManager()

    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email


class Abiturient(User):
    class Meta:
        proxy = True
        verbose_name = "Абитуриент"
        verbose_name_plural = "Абитуриенты"


class StaffUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class UserRegistrationApplication(models.Model):
    email = models.EmailField('Электронная почта', null=False)
    password = models.CharField('Пароль', max_length=128)
    verification_code = models.PositiveSmallIntegerField('Код подтверждения', unique=True)

    class Meta:
        verbose_name_plural = 'Заявки на регистрацию'
        verbose_name = 'Заявка на регистрацию'
        unique_together = ['email', 'verification_code']


class LetterMailing(SingletonModel):
    """Mailing letter to abiturients"""

    title = models.CharField('Заголовок', max_length=255)
    description = RichTextField('Описание')
    created_at = models.DateTimeField('Создано в', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Письма для рассылки'
        verbose_name = 'Письмо для рассылки'

    def __str__(self):
        return self.title


class LetterMailingHistory(models.Model):
    """History mailing letter to abiturients"""

    title = models.CharField('Заголовок', max_length=255)
    description = RichTextField('Описание')
    sent_at = models.DateTimeField('Создано в', auto_now_add=True)
    abiturients = models.ManyToManyField(
        Abiturient, related_name='mailed_letters', verbose_name='Абитуриенты',
        help_text='данным абитуриентам были отправлены письма',
    )

    class Meta:
        verbose_name_plural = 'История Письма для рассылки'
        verbose_name = 'История Письмо для рассылки'
