from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.mail import send_mass_mail, send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from solo.admin import SingletonModelAdmin

from apps.users.models import StaffUser, Abiturient, LetterMailing, \
    LetterMailingHistory

User = get_user_model()


class StaffUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user


@admin.register(StaffUser)
class StaffUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = StaffUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_queryset(self, request):
        return StaffUser.objects.filter(is_staff=True)

    class Media:
        css = {
            'all': ('css/admin/m2m_select_input.css',)
        }


@admin.action(description='Отправить письмо')
def send_letter(modeladmin, request, queryset):
    letter = LetterMailing.objects.first()
    if not letter:
        messages.info(request, f'У вас нет писем для отправки.'
                               f'Создайте письмо в разделе "Письма для рассылки"')
        return
    sent_count = send_mail(letter.title, letter.description, settings.EMAIL_HOST_USER, list(queryset.exclude(email__isnull=True).values_list('email', flat=True)),
                           html_message=letter.description, fail_silently=True)
    letter_history = LetterMailingHistory(title=letter.title,
                                          description=letter.description,
                                          sent_at=timezone.now())
    letter_history.save()
    h = list()
    for abiturient_id in list(
            queryset.exclude(email__isnull=True).values_list('id', flat=True)):
        h.append(letter_history.abiturients.through(abiturient_id=abiturient_id,
                                                    lettermailinghistory_id=letter_history.id))
    letter_history.abiturients.through.objects.bulk_create(h)
    if sent_count > 0:
        # letter.delete()
        messages.success(request, f'Отправлено {sent_count} абитуриентам. Название письма: "{letter.title}"')
    else:
        messages.error(request, 'Из-за технических неполадок не удалось отправить письма. \n'
                                'Возможные причины: лимит рассылки был превышен или технические неполадки.\n'
                                'Обратитесь в службу поддержки.')


@admin.register(Abiturient)
class AbiturientAdmin(BaseUserAdmin):
    actions = [send_letter]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'citizenship',)
    search_fields = ('email', 'first_name', 'last_name', 'phone_number',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_queryset(self, request):
        return StaffUser.objects.filter(is_staff=False)


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    class Media:
        css = {
            'all': ('css/admin/m2m_select_input.css',)
        }


@admin.register(LetterMailing)
class LetterMailingAdmin(SingletonModelAdmin):
    list_display = ('title',)


@admin.register(LetterMailingHistory)
class LetterMailingHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    readonly_fields = ('title', 'description', 'sent_at', 'abiturients',)

    def has_add_permission(self, request):
        return False
