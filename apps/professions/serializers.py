from rest_framework import serializers

from .models import Profession, ProfessionGalleryImage, AdmissionCondition, \
    AdmissionConditionForCitizen


class ProfessionListSrz(serializers.ModelSerializer):

    class Meta:
        model = Profession
        fields = ('id', 'name',)


class ProfessionGalleryImageSrz(serializers.ModelSerializer):

    class Meta:
        model = ProfessionGalleryImage
        fields = ('id', 'image',)


class ProfessionRetrieveSrz(serializers.ModelSerializer):
    images = ProfessionGalleryImageSrz(many=True)

    class Meta:
        model = Profession
        fields = ('id', 'name', 'description', 'images')


class AdmissionConditionForCitizenSrz(serializers.ModelSerializer):
    class Meta:
        model = AdmissionConditionForCitizen
        fields = ('id', 'citizenship', 'condition',)


class ProfessionAdmissionSrz(serializers.ModelSerializer):
    for_citizens = AdmissionConditionForCitizenSrz(many=True)

    class Meta:
        model = AdmissionCondition
        fields = ('id', 'description', 'for_citizens',)
