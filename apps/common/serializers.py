from rest_framework import serializers

from apps.common.models import OnboardPage


class OnboardPageSrz(serializers.ModelSerializer):

    class Meta:
        model = OnboardPage
        fields = ('title', 'subtitle', 'description', 'image',)
