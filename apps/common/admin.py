from django.contrib import admin
from solo.admin import SingletonModelAdmin

from apps.common.models import OnboardPage


@admin.register(OnboardPage)
class OnboardPageAdmin(SingletonModelAdmin):
    pass
