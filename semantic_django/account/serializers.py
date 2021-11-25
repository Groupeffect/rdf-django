from django.conf import settings
from rest_framework import serializers, reverse
from . import models


def uri_builder(name, obj):
    return f"{settings.GLOBAL_HOST_URL}{reverse.reverse(str(name)+'-detail', kwargs={'pk': obj.id})}"


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
            "projects",
        ]

    def get_uri(self, obj):
        return uri_builder('person', obj)


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
        return uri_builder('organization', obj)


class OrganizationRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Organization
        fields = ["rdf", ]


class ProjectSerializer(MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Project
        fields = [
            "id",
            "uri",
            "label",
            "website",
            "description",
            "repository",
            "organizations",
        ]

    def get_uri(self, obj):
        return uri_builder('project', obj)


class ProjectRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Project
        fields = ["rdf", ]
