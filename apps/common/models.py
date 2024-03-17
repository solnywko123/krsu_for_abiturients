from django.db import models
from solo.models import SingletonModel


class OnboardPage(SingletonModel):
    """Onboard page for new users"""

    title = models.CharField('Заголовок', max_length=255)
    image = models.ImageField('Изображение', upload_to='common/', blank=False)
    subtitle = models.CharField('Подзаголовок', max_length=255)
    description = models.TextField('Описание', max_length=1000)

    class Meta:
        verbose_name_plural = 'Приветственная страница для новых пользователей'
        verbose_name = 'Приветственная страница для новых пользователей'
