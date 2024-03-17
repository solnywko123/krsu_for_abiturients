from typing import Optional

from rest_framework import serializers

from apps.chat.models import Message, FAQ


class MessageSrz(serializers.ModelSerializer):
    status = serializers.IntegerField(
        required=False, help_text=str({Message.SENT: 'msg was sent', Message.SEEN: 'msg was seen'}),
    )
    type = serializers.IntegerField(
        required=False, help_text=str({Message.FROM_USER: 'msg from user',
                                       Message.FROM_STAFF_USER: 'msg from staff user'})
    )

    class Meta:
        model = Message
        fields = ('id', 'text', 'status', 'type', 'sent_at',)


class FAQSrz(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer',)
