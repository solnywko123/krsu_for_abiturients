from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import Conversation, Message, FAQ


class MessageBaseInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = [
            {'type': Message.FROM_STAFF_USER},
        ]
        super(MessageBaseInlineFormSet, self).__init__(*args, **kwargs)


class MessageAdminInline(admin.TabularInline):
    template = 'admin/chat_tabular_inline.html'

    model = Message
    fields = ('text', 'type', 'sent_at')
    readonly_fields = ('type', 'sent_at',)
    extra = 1
    formset = MessageBaseInlineFormSet

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    class Media:
        css = {
            'all': ('css/admin/conversation.css',)
        }


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('sender',)
    readonly_fields = ('sender',)
    inlines = (MessageAdminInline,)

    # class Media:
    #     html = {
    #         'all': (
    #             'admin/chat_tabular_inline.html',
    #         )
    #     }


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass
