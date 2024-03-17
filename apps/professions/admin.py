from django.contrib import admin
from .models import Profession, ProfessionGalleryImage, AdmissionCondition, \
    AdmissionConditionForCitizen


class ProfessionGalleryImageAdminInline(admin.TabularInline):
    model = ProfessionGalleryImage
    extra = 1


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (ProfessionGalleryImageAdminInline,)


@admin.register(AdmissionCondition)
class AdmissionConditionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    class Media:
        css = {
            'all': ('css/admin/m2m_select_input.css',)
        }


@admin.register(AdmissionConditionForCitizen)
class AdmissionConditionForCitizenAdmin(admin.ModelAdmin):
    list_display = ('id', 'citizenship', 'get_short_description',)
    list_display_links = ('id', 'citizenship',)

    def get_short_description(self, instance: AdmissionConditionForCitizen):
        return instance.short_condition

    get_short_description.short_description = 'Краткое описание условия'
