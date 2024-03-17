from ckeditor.fields import RichTextField
from django.db import models


class Profession(models.Model):
    """Profession of ETF"""

    name = models.CharField(
        'Название', max_length=255, unique=True, null=False,
    )
    description = RichTextField('Описание')
    position = models.PositiveSmallIntegerField('Позиция', default=0)
    admission_condition = models.ForeignKey(
        'AdmissionCondition', verbose_name='Условия поступления', related_name='professions',
        null=True, on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        ordering = ['position']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        new_profession = super(Profession, self).save(force_insert, force_update, using, update_fields)
        return new_profession


class ProfessionGalleryImage(models.Model):
    """Gallery for profession"""

    profession = models.ForeignKey(
        Profession, verbose_name='Специальность', on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        'Изображение', upload_to='professions/%Y/', blank=False,
    )

    class Meta:
        verbose_name = 'Изображение галлереи специальности'
        verbose_name_plural = 'Галлерея специальностей'

    def __str__(self):
        return f'Изображение id:{self.id} для специальности {self.profession_id}'


class AdmissionCondition(models.Model):
    """Admission condition to the professions"""

    description = RichTextField('Описание')
    for_citizens = models.ManyToManyField('AdmissionConditionForCitizen', related_name='admission_conditions',
                                          verbose_name='Для граждан', blank=True)

    class Meta:
        verbose_name = 'Условие поступления'
        verbose_name_plural = 'Условия поступления'

    def __str__(self):
        return f'№{self.id} Условие поступление'


class AdmissionConditionForCitizen(models.Model):
    """Admission condition to the different citizens"""

    citizenship = models.CharField('Гражданство', help_text='например: "Для граждан Кыргызстана"',
                                   max_length=255)
    condition = models.TextField('Условие')

    class Meta:
        verbose_name_plural = 'Условия поступления для граждан'
        verbose_name = 'Условие поступления для граждан'

    def __str__(self):
        return f'№{self.id} {self.citizenship}: {self.short_condition}'

    @property
    def short_condition(self) -> str:
        return f'{self.condition[:50]} {"..." if self.condition and len(self.condition) > 50 else ""}'
