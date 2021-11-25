from django.conf import settings
from rest_framework import serializers, reverse
from . import models


class MetaModelSerializer(serializers.ModelSerializer):
    rdf = serializers.SerializerMethodField(read_only=True)

    def get_rdf(self, obj):
        return obj.get_rdf_representation()


class PersonSerializer(MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Person
        fields = [
            "id",
            "uri",
            "label",
            "firstName",
            "lastName",
            "description",
            "organizations",
            "employedAt",
        ]

    def get_uri(self, obj):
        return f"{settings.GLOBAL_HOST_URL}{reverse.reverse('person-detail', kwargs={'pk': obj.id})}"


class PersonRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Person
        fields = ["rdf", ]


class OrganizationSerializer(MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Organization
        fields = [
            "id",
            "uri",
            "label",
            "website",
            "description",
        ]

    def get_uri(self, obj):

        return reverse.reverse('organization-detail', kwargs={"pk": obj.id})


class OrganizationRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Organization
        fields = ["rdf", ]
