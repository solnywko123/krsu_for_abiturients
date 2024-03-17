from typing import Optional

from django.contrib import admin
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    """Беседа"""
    ACTIVE, BANNED = 1, 2

    sender = models.OneToOneField(
        to=User, related_name='conversation', on_delete=models.CASCADE, verbose_name='Отправитель',
    )
    status = models.PositiveSmallIntegerField(
        'Статус', choices=((ACTIVE, 'Активно'), (BANNED, 'Заблокировано'),)
    )

    class Meta:
        verbose_name_plural = 'Беседы'
        verbose_name = 'Беседа'

    def __str__(self):
        return f'Беседа id:{self.id}'


class Message(models.Model):
    """Сообщение"""
    SENT, SEEN = 1, 2
    FROM_USER, FROM_STAFF_USER = 1, 2

    text = models.TextField(
        'Текст', max_length=1000, null=False,
    )
    status = models.PositiveSmallIntegerField(
        'Статус', choices=((SENT, 'Отправлено'), (SEEN, 'Просмотрено')),
        default=SENT,
    )
    is_deleted = models.BooleanField('Удалено?', default=False)
    type = models.PositiveSmallIntegerField(
        'Тип', choices=((FROM_USER, 'От абитуриента'), (FROM_STAFF_USER, 'От администратора',)),
        default=FROM_STAFF_USER,
    )
    conversation = models.ForeignKey(to=Conversation, related_name='messages', on_delete=models.CASCADE)
    sent_at = models.DateTimeField('Отправлено в', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = 'Сообщение'

    def status_repr(self) -> Optional[str]:
        if self.status == self.SENT:
            return 'sent'
        elif self.status == self.SEEN:
            return 'seen'


class FAQ(models.Model):
    """Frequently asked questions"""

    question = models.TextField('Вопрос', max_length=500, unique=True)
    answer = models.TextField('Ответ')
    position = models.PositiveSmallIntegerField('Позиция', default=0)

    class Meta:
        verbose_name_plural = 'Вопросы и Ответы'
        verbose_name = 'Вопросы и Ответы'
        ordering = ['position']

    def __str__(self):
        return self.question
